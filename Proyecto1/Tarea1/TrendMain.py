import time
import rrdtool
from getSNMP import *
from TrendGraph import *

carga_CPU = consultaSNMP('DanielBenitez4cv5','localhost','1.3.6.1.2.1.25.3.3.1.2')
nucleos = len(carga_CPU)
print(nucleos)

datasources = []
rraverages = []

for i in range(nucleos):
    data_string = "DS:CPU" + str(i+1) + "load:GAUGE:600:U:U"
    datasources.append(data_string)
    rraverages.append("RRA:AVERAGE:0.5:1:24")

ret = rrdtool.create("trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     datasources,
                     rraverages)

while 1:
    carga_CPU = consultaSNMP('DanielBenitez4cv5','localhost','1.3.6.1.2.1.25.3.3.1.2')

    valor = "N" 
    for val_CPU in carga_CPU:
        valor = valor + ":" + str(val_CPU)

    print(valor)
    rrdtool.update('trend.rrd', valor)
    rrdtool.dump('trend.rrd','trend.xml')
    for n in range(nucleos):
        graficar("CPU"+str(n+1)+"load", "cpu"+str(n+1)+".png")
    time.sleep(1)
