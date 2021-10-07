# TSCH-LBV
Protocolo de alocação de canais de largura de banda variável em redes TSCH. 

Para executar o algoritmo é necessário seguir os seguintes passos: 
1) Instalar o ambiente do contiki-ng, via docker, em sua máquina: https://github.com/contiki-ng/contiki-ng/wiki/Docker 
2) Após obter todo o sistema em funcionamento, substitua o repositório Contiki-NG(Original) pelo Contiki-NG disponibilizada neste repositório. 
3) Após a substituição o único exemplo disponível será o do TSCH-LBV.   
4) Até o momento o TSCH-LBV suporta apenas 18 nós e possui suporte apenas para o COOJA mote  
5) Para cada execução é necessário limpar os arquivos os/arvore.txt e os/TCH.txt
6) Para aferir as métricas de entrega de pacotes e vasão é necessário copiar os logs do COOJA e passá-los em uma análisador em python dentro da pasta Analisador 
7) Os resultados poderão ser conferidos após isso.  

Na arquitetura do Contiki-NG, as principais implementação são as seguintes: 
os/net/tsch/ 
  > tsch_schedule.c  
  > tsch_schedule.h 
  > network-graph.h 
  > conf.c
  > conf.h
  > tsch-log.c 
  > tsch-log.h 
  > tsch.c
  > tsch.h 
  > tsch-conf.h 

examples/6tisch/tschLBV 
  > node.c
  > project-conf.h
  > Makefile
