from getSNMP import *
from TrendUpdate import *
from TrendCreate import *
import threading

#oid : 1.3.6.1.2.1.2.2.1.10.1 - Octetos de entrada


def main():
	ip = input("Inserte la IP del Agente: ")
	puerto = int(input("Inserte el puerto: "))
	comunidad = input("Inserte el nombre de la comunidad del agente: ")
	oid = input("Inserte el OID de la variable que desea leer: ")
	consulta = consultaSNMP(comunidad, ip, puerto, oid)

	if (consulta == "None" or consulta == ""):
		return "No se puede obtener su OID"
	else:
		nombre_rrd = input("Inserte el nombre del archivo RRD: ")

		if create(nombre_rrd) == True:
			updateThread = threading.Thread(target=haceUpdate,
											name="Update - Worker",
											args=(nombre_rrd, comunidad, ip, puerto, oid))
			updateThread.start()

			return "Datos correctos, iniciando Holt Winters"

		else:
			return "Falla en archivo RRD"


if __name__ == "__main__":
	main()