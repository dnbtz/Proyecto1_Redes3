import sys

from pysnmp.hlapi import *



def consultaSNMP(comunidad, host, oid):
    resultado = []
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(), 
    CommunityData(comunidad), 
    UdpTransportTarget((host, 161)), 
    ContextData(), 
    ObjectType(ObjectIdentity(oid)),
    lexicographicMode=False):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break
        else:
            for varBind in varBinds:
                if (varBind != 'None'  or varBind != ""):           
                    varB =(' = '.join([x.prettyPrint() for x in varBind]))
                    zipvarB = varB.split()
                    resultado.append(' '.join(zipvarB[2::]))
    return resultado
