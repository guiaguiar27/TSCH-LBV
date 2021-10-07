# TSCH-LB
VWider bandwidth channel allocation protocol in TSCH networks.

To run the algorithm it is necessary to follow this steps:

1) Install the contiki-ng environment, via docker, on your machine: https://github.com/contiki-ng/contiki-ng/wiki/Docker
2) Get the whole system up and running, replace all the files in the Contiki-NG (Original) by the all the files available in this repository.
3) After replacing the only available example, will be the TSCH-LBV.
4) So far the TSCH-LBV supports only 18 nodes and only supports the COOJA mote
5) For each execution it is necessary to clean the files os/arvore.txt (topology file) and os/TCH.txt (slotframe file)
6) In order to measure the metrics of packet delivery and throughput it is necessary to copy the COOJA logs and pass them to a python analyzer inside the Analyzer folder
7) Before copying, make sure that the times are in ms (click on the time parameter in COOJA)
8) The results obtained will be checked after that.

In the Contiki-NG architecture, the main implementations are as follows: os/net/tsch/

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

>Makefile  

This repository is an extension of the original Contiki-NG implementation: https://github.com/contiki-ng/contiki-ng
