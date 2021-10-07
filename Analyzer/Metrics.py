# code to collect throughput from cooja simulations  
import re
import scipy.stats
import numpy as np
from functools import reduce  
import sys 

# to calculate confidence interval  
def confident_interval_data(X, confidence = 0.95, sigma = -1):
    def S(X): #funcao para calcular o desvio padrao amostral
        s = 0
        for i in range(0,len(X)):
            s = s + (X[i] - np.mean(X))**2
        s = np.sqrt(s/(len(X)-1))
        return s
    n = len(X) # numero de elementos na amostra
    Xs = np.mean(X) # media amostral
    s = S(X) # desvio padrao amostral
    zalpha = abs(scipy.stats.norm.ppf((1 - confidence)/2))
    if(sigma != -1): # se a variancia eh conhecida
        IC1 = Xs - zalpha*sigma/np.sqrt(n)
        IC2 = Xs + zalpha*sigma/np.sqrt(n)
    else: # se a variancia eh desconhecida
        if(n >= 50): # se o tamanho da amostra eh maior do que 50
            # Usa a distribuicao normal
            IC1 = Xs - zalpha*s/np.sqrt(n)
            IC2 = Xs + zalpha*s/np.sqrt(n)
        else: # se o tamanho da amostra eh menor do que 50
            # Usa a distribuicao t de Student
            talpha = scipy.stats.t.ppf((1 + confidence) / 2., n-1)
            IC1 = Xs - talpha*s/np.sqrt(n)
            IC2 = Xs + talpha*s/np.sqrt(n)
    return  talpha*s/np.sqrt(n) 

#avarage 
def average(list): 
    return sum(list)/len(list)
# just add two numbers 
def add(a,b): 
    return a + b  
# get the next word by a word reference     
def next(a,source): 
    for i,w in enumerate(source): 
        if w == a: 
            return source[i+1]  
# this functions is specific to the file format adopted in the data collection 
def extract_node(source): 
    for i,w in enumerate(words):
            if w == "Pckt": 
                return words[i+1]  
            if w == "Tx_try":   
                return words[i+1] 
            if w == "increased_Bandwidth": 
                return words[i+1] 
# get the number of packets sent by a specif node 
def extract_tx_success(source):   
    for i,w in enumerate(words):
            if w == "Pckt": 
                return words[i+2]  
# get the packets received in a specific node 
def extract_rx(source): 
    for i,w in enumerate(words):
            if w == "Pckt": 
                return words[i+3] 
# get the number of attempts to send packets on this node 
def extract_tx_try(source):  
    for i,w in enumerate(words):
            if w == "Tx_try": 
                return words[i+2] 
# get the amount of channels used in the transmission 
def extract_tx_widerband(source):   
    for i,w in enumerate(words):
            if w == "increased_Bandwidth": 
                return words[i+2] 


#converte tempo (string) para inteiro
def justTime(string): 
    return int(string)
    
PDR_TASA = [] 
PDR_LBV = []
PRR_TASA = []  
Throughput_TASA = [] 
Throughput_LBV = []
PRR_LBV = []  
init_time = 0  
final_time = 0
numNodes = 0 
if numNodes == 0: 
    print("Mude o tamanho da rede em numNodes") 
    sys.exit()
pckt_len = 43
flag = 0   
    
path = "" 
if path == "": 
    print("Insira o caminho do arquivo") 
    sys.exit()
#network parameters   
# define slotframe size here  
slotframe_size = numNodes + 2 
aux_numNode = numNodes + 1

nodes = [0 for i in range(numNodes)]
# metrics per node  
Tx_per_node = [0 for i in range(0,aux_numNode)] 
Rx_per_node = [0 for i in range(0,aux_numNode)] 
Tx_try_per_node = [0 for i in range(0,aux_numNode)] 
throughput_per_node = [0 for i in range(0,aux_numNode)]  
Wider_band = [1 for i in range(0,aux_numNode)] 
#fill nodes  
for i in range(0,numNodes): 
    nodes.append(i) 
# total metrics 
Tx_total = 0
Tx_try_sent = 0 
Rx_total = 0  

#bandwidth   

with open(path,'r') as f:
    for line in f:  
        words = line.split() 
        if "Tx_try" in words:  
            node = int(extract_node(words))
            aux_tx_try = int(extract_tx_try(words))  
            for i in range(1,aux_numNode): 
                if i == node:
                    Tx_try_per_node[i] = aux_tx_try    
        if "Pckt" in words:  
            if flag == 0 : 
                itime = words[0]  
                #quando  é dado em milisegundos
                init_time = justTime(itime)
                flag = 1  
            else: 
                fTime = words[0] 
                #quando é dado em milisegundos
                final_time = justTime(fTime)

            node = int(extract_node(words))
        
            aux_tx = int(extract_tx_success(words)) 
            aux_rx = int(extract_rx(words)) 
        
            Lrx = int(extract_rx(words))  
            for i in range(1,aux_numNode): 
                if i == node:   
                    if Rx_per_node[i] < Lrx:
                        Rx_per_node[i] = Lrx
            Ltx = int(extract_tx_success(words))  
            for i in range(1,aux_numNode): 
                if i == node:  
                    if Tx_per_node[i] < Ltx:
                        Tx_per_node[i] = Ltx 
        if "increased_Bandwidth" in words:   

            node = int(extract_node(words)) 
            Bw = int(extract_tx_widerband(words))  
            #garante que não haja canais usados sem no minimo 1 canal computado
            if Bw == 0: 
                Bw = 1 
            for i in range(1,aux_numNode): 
                if i == node:     
                    if Wider_band[i] <= Bw: 
                        Wider_band[i] = Bw

            
                

    print("metrics simulation {} nodes".format(numNodes))
    print("nodes:", nodes[:]) 

    #print("Metrics for TASA") 

    Tx_total =  reduce(lambda x, y:x+y, Tx_try_per_node) 
    Rx_total =  reduce(lambda x, y:x+y, Rx_per_node) 

    
    prr = Tx_total - Rx_total 
    prr = prr/Tx_total 
    aux_tasa =  (Rx_total/Tx_total)*100  
    PRR_TASA.append(prr)
    
    PDR_TASA.append(aux_tasa) 
    #* 10 por conta de que cada slot tem 10 ms 
    #por 100 para dar em percentual 
    time = final_time - init_time 
    time = time * 0.001
    Throughput = ((Rx_total*pckt_len)/time) 

    print("Througput(%)",Throughput) 
    Throughput_TASA.append(Throughput)
    print("PDR(%):",aux_tasa) 
    print("PRR(%)",prr) 


    print("Metrics for TSCH-LBV:")   

    Tx_total =  reduce(lambda x, y:x+y, Tx_try_per_node) 
    #multiplica os pacotes apenas daqueles que conseguiram mandar pacotes  

    for i in range(0, aux_numNode): 
        Tx_per_node[i] = Tx_per_node[i] * Wider_band[i]   
    Rx_total =  reduce(lambda x, y:x+y, Tx_per_node)  

    for i in range(0, aux_numNode): 
        Tx_try_per_node[i] = Tx_try_per_node[i] * Wider_band[i]   

    Tx_total =  reduce(lambda x, y:x+y, Tx_try_per_node) 
    
    prr = Tx_total - Rx_total 
    prr = prr/Tx_total 
    
    aux_lbv = (Rx_total/Tx_total)*100 
    time = final_time - init_time 
    time = time * 0.001
    Throughput = ((Rx_total*pckt_len)/time) 

    print("Througput(%)",Throughput) 
    Throughput_LBV.append(Throughput)
    
    
    print("PDR(%):",aux_lbv)  
    print("PRR(%):",prr)
    PRR_LBV.append(prr)
    PDR_LBV.append(aux_lbv)
    print("---------------------------------------------------------------------------") 



arq=open("saida4.txt","a")
arq.write("{}nodes\n".format(numNodes))   

arq.write("PDRTASA = {}\n".format(average(PDR_TASA)))   
arq.write("Interval_conf_TASA_PDR: {} \n".format(confident_interval_data(PDR_TASA,0.95)))
arq.write("PDRLBV = {}\n".format(average(PDR_LBV)))  
arq.write("Interval_conf_LBV_PDR: {} \n".format(confident_interval_data(PDR_LBV,0.95)))

arq.write("RELTASA = {}\n".format(average(PRR_TASA)))  
arq.write("Interval_conf_TASA_confiabilidade: {} \n".format(confident_interval_data(PRR_TASA,0.95)))

arq.write("RELLBV = {}\n".format(average(PRR_LBV)))   
arq.write("Interval_conf_LBV_confiabilidade: {} \n".format(confident_interval_data(PRR_LBV,0.95)))

arq.write("THTASA = {}\n".format(average(Throughput_TASA)))  
arq.write("Interval_conf_THTASA: {} \n".format(confident_interval_data(Throughput_TASA,0.95)))

arq.write("THLBV = {}\n".format(average(Throughput_LBV)))   
arq.write("Interval_conf_THLBV: {} \n".format(confident_interval_data(Throughput_LBV,0.95)))

arq.close()      