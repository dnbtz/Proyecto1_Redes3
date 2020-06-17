import time
import rrdtool
import sys
from getSNMP import *
from envia_correo import *


def haceUpdate(nombreRRD, comunidad, agente, puerto, oid):
    init_time = rrdtool.last("RRD/" + nombreRRD + str(".rrd"))
    while 1:
        try:
            valor_leido = int(consultaSNMP(comunidad, agente, puerto, oid))
            value = "N:" + str(valor_leido)
            print(value)
            rrdtool.update("RRD/" + nombreRRD + str(".rrd"), value)
            rrdtool.dump("RRD/" + nombreRRD + str(".rrd"), "XML/" + nombreRRD + str(".xml"))
            graph(nombreRRD, 1, init_time)
            time.sleep(1)
        except Exception as e:
            sys.exit("Error! Favor de verificar el sistema.")
            #sendEmail("Error, favor de llamar a un especialista!.", nombreRRD + ".png")


def graph(nombreRRD, num_graphs, init_time):
    for i in range(num_graphs):
        ret = rrdtool.graph("IMG/" + nombreRRD + ".png",
                                "--title=Holt-Winters de Daniel Benitez Lopez",
                                "--start", str(init_time),
                                "--end", str(rrdtool.last("RRD/" + nombreRRD + '.rrd')),
                                "--vertical-label=Datos de entrada",
                                "--width=1000",
                                "--height=500",
                                "DEF:obs=" + "RRD/" + nombreRRD + ".rrd:VALUES" + str(i+1) + ":AVERAGE",
                                "DEF:pred=" + "RRD/" + nombreRRD + ".rrd:VALUES" + str(i+1) + ":HWPREDICT",
                                "DEF:dev=" + "RRD/" + nombreRRD + ".rrd:VALUES" + str(i+1) + ":DEVPREDICT",
                                "DEF:fail=" + "RRD/" + nombreRRD + ".rrd:VALUES" + str(i+1) + ":FAILURES",
                                "CDEF:pfail=fail,1,*",
                                "CDEF:scaledobs=obs,8,*",
                                "CDEF:upper=pred,dev,2,*,+",
                                "CDEF:lower=pred,dev,2,*,-",
                                "CDEF:scaledupper=upper,8,*",
                                "CDEF:scaledlower=lower,8,*",
                                "TICK:fail#FDD017:1.0:FFallas",
                                "CDEF:scaledpred=pred,8,*",
                                "LINE1:scaledobs#00FF00:Datos de entrada",
                                "LINE2:scaledpred#ee0099:Prediccion",
                                "LINE1:scaledupper#FF000E:Limite superior",
                                "LINE1:scaledlower#0012FF:Limite inferior",
                                "PRINT:pfail:LAST:%0.0lf")
        print(ret[2][0])

        if (ret[2][0] == '1'):
            print("Error")
            sendEmail("Error, favor de llamar a un especialista.", nombreRRD + ".png")