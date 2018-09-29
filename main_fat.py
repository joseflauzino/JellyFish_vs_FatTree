# encoding: utf-8
import generate_cmds_fat
import shlex
import subprocess
from subprocess import Popen, PIPE
from multiprocessing import Process
import sys
import os
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.net import Mininet
from ripl.ripl.dctopo import FatTreeTopo
import time

pods = 4;
processList = []

def poxMnFt(adjListFile, routingFile):
	print "Criando pox"
	command = shlex.split('sudo pox/pox.py DCController --topo=ft,'+ str(pods) +' --routing=ECMP')
	with open(os.devnull, "w") as fnull:
		pPox = Popen(command, stdout=fnull, stderr=fnull)
		processList.append(pPox)
	command = shlex.split('sudo lxterm -e mn --custom ripl/ripl/mn.py --topo ft,'+ str(pods) +' --controller=remote --mac --link tc,bw=10,delay=10ms')
	with open(os.devnull, "w") as fnull:
		pMininet = Popen(command, stdout=fnull, stderr=fnull)
		processList.append(pMininet)

def throughputCalculation(directory):
	arquivosDiretorio = os.listdir(directory)
	arquivos = []
	size = len(arquivosDiretorio)
	#verifica se há arquivos nulos:
	for i in range(size):
		if os.stat(directory + '/'+ arquivosDiretorio[i]).st_size != 0:
			arquivos.append(arquivosDiretorio[i])
	size = len(arquivos)
	bandwidthList = []
	
	for i in range(size):
		with open(directory + '/'+ arquivos[i], 'r') as f:
			try:
				lines = f.read().splitlines()
				last_line = lines[-1]
				bandwidth = last_line.split()

				#Cálculo para 8 flows
				if bandwidth[0] == '[SUM]':
					bandwidthList.append(bandwidth[5])
				else: # Cálculos para 1 flow
					#Alguns testes geram apenas kbytes,então:
					if bandwidth[7] == 'Kbits/sec':
						bandwidthList.append(str(float(bandwidth[6])/1024))
					else:
						bandwidthList.append(bandwidth[6])
			except:
				print('Erro na Leitura dos arquivos, conteúdo inesperado')
 				raw_input("Pressione Enter para continuar...")

 	try:
 		bandW = [float(i) for i in bandwidthList]
 		Avg = sum(bandW)/len(bandwidthList)
 		print('Largura de banda utilizada:')
 		print(str(Avg)+ ' Mbits/sec')
 		print('')
 		raw_input("Pressione Enter para continuar...")
 	except:
 		print('Erro na Leitura dos dados gerados pelo iperf')
 		raw_input("Pressione Enter para continuar...")

def start():
	adjListFile = 'graphFt'
	routeringmode = 'ecmp_8_' # ecmp_8_ or ksp_
	flowsNumber = 8
	#gambiarra pura ;)
	num_hosts = (pods ** 3)/4
	hosts = [(str(i)) for i in range (1, num_hosts + 1)]
	generate_cmds_fat.InitTestFt(pods, routeringmode, flowsNumber)
	routingFile = routeringmode + adjListFile
	#poxMnFt(adjListFile, routingFile)
	#throughputCalculation('results/ecmp_8_/')

if __name__ == "__main__":
	start()
	for i in range(len(processList)):
		processList[i].kill()
'''
def main():
	param = sys.argv
	if len(param) >= 4:
		pods = int(param[1])
		adjListFile = 'graphFt'
		routeringmode = 'ecmp_8_' # ecmp_8_ or ksp_
		flowsNumber = 8
		num_hosts = (pods ** 3)/4
		hosts = [(str(i)) for i in range (1, num_hosts + 1)]
		generate_cmds_fat.InitTestFt(pods, routeringmode, flowsNumber)
		routingFile = routeringmode + adjListFile

if __name__ == "__main__":
	main()
'''