import sys
import rrdtool
import time

nombreRRD = "trend"
proyeccion = 3000
tope = 90
tope2 = 100

def graficar(cpu,nombre):
    tiempo_final=int(rrdtool.last(str(nombreRRD)+".rrd"))
    tiempo_inicial=1592365786
    ret=rrdtool.graph(nombre,"--start",str(tiempo_inicial),
                      "--end",str(tiempo_final+proyeccion),
                      "--vertical-label=Carga CPU",
                      "--title= Minimos Cuadrados CPU - Daniel Benitez Lopez ",
                      "--color","ARROW#009900",
                      '--vertical-label',"Uso de CPU ( %)",
                      '--lower-limit','0',
                      '--upper-limit','100',
                      "DEF:carga="+str(nombreRRD)+".rrd:"+str(cpu)+":AVERAGE",
                      "AREA:carga#00FF00:Carga del CPU actual",
                      "LINE1:"+str(tope)+"#FF0000",
                      "LINE1:" + str(tope2) + "#FF0000",
                      "VDEF:a=carga,LSLSLOPE",
                      "VDEF:b=carga,LSLINT",
                      'CDEF:avg2=carga,POP,a,COUNT,*,b,+',
                      'VDEF:maxColect=avg2,MAXIMUM',
                      'CDEF:result=avg2,'+str(tope)+',GE,avg2,maxColect,IF',
                      'CDEF:result2=avg2,'+ str(tope2)+',GE,avg2,maxColect,IF',
                      'VDEF:respuesta=result,MINIMUM',
                      'PRINT:respuesta:"%c":strftime',
                      'VDEF:respuesta2=result2,MINIMUM',
                      'PRINT:respuesta2:"%c":strftime',
                      "LINE2:avg2#FFBB00:Prediccion de Minimos Cuadrados",
                      "COMMENT:Llega al 90 el dia ",
                      'GPRINT:respuesta:"%c":strftime',
                      "COMMENT:Llega al 100 el dia ",
                      'GPRINT:respuesta2:"%c":strftime')

