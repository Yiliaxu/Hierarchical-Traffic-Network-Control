# -*- coding: UTF-8 -*-
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import random
#from tqdm import tqdm
#from time import time
#from scipy.optimize import linprog
#from cvxopt import matrix,solvers
from scipy.sparse import identity
from collections import defaultdict


import pdb

demand_level = 10

SUMO_HOME = "/usr/local/bin/sumo"
tools = "/home/Arain/sumo-git/tools/"
sys.path.append(tools)

sumoBinary = "/usr/local/bin/sumo"

sumoCmd = [sumoBinary, "-c", "fixchj"+str(demand_level)+".sumocfg","--seed", str(random.randint(1,100))]


# if 'SUMO_HOME' in os.environ:
# 	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
# 	sys.path.append(tools)
# else:
# 	sys.exit("please declare environment variable 'SUMO_HOME'")
# sumoBinary = "E:/software/sumo-win64-0.32.0/sumo-0.32.0/bin/sumo-gui"

# sumoCmd = [sumoBinary, "-c", "chj.sumocfg","--seed", str(random.randint(1,100))]

PORT = 8813
import traci

# doc1 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSAction.xml')
# ActionRoot = doc1.getroot()
# doc2 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
# RouteRoot = doc2.getroot()
# doc3 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops_ctrl.xml')
# LoopsRoot = doc3.getroot()
# doc4 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.net.xml')
# NetRoot = doc4.getroot()


doc1 = etree.parse('./TLSAction.xml')
ActionRoot = doc1.getroot()
doc2 = etree.parse('./Chj_final.rou.xml')
RouteRoot = doc2.getroot()
doc3 = etree.parse('./loops_ctrl.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('./Chj_final.net.xml')
NetRoot = doc4.getroot()

EdgesList = []
for edge in NetRoot.findall('edge'):
	new_EdgeID = edge.get('Region')+edge.get('id')
	EdgesList.append(new_EdgeID)

# print len(EdgesList)

VehNum_files = doc.Document()
VehNum = VehNum_files.createElement('VehicleNumber')
VehNum_files.appendChild(VehNum)


def get_random_phasetime(PhaseNum,Tc):
	PhaseTime = np.zeros(PhaseNum)
	for i in xrange(PhaseNum):
		PhaseTime[i]=random.randint(0,Tc-np.sum(PhaseTime[0:i]))
	PhaseTime[-1]=Tc-np.sum(PhaseTime[0:-1])
	
	for i in xrange(PhaseNum):
		List_PhaseTime = PhaseTime.tolist()
		if List_PhaseTime[i]<10:
			max_index = List_PhaseTime.index(max(List_PhaseTime))
			PhaseTime[max_index]=PhaseTime[max_index]-(10-PhaseTime[i])
			PhaseTime[i]=10

	return PhaseTime


##############################################################################################################
if __name__ == '__main__':	

	traci.start(sumoCmd)

	Tsim = 3600
	Tc = 60

	ActionInfo=defaultdict(lambda:0)
	PhaseTime=defaultdict(lambda:0)
	for intersection in ActionRoot.findall('Intersection'):
		intersection_id = intersection.get('id')
		PhaseNum = int(intersection.get('PhaseNum'))
		PhaseTime[intersection_id]= get_random_phasetime(PhaseNum,Tc)  #np.ones(PhaseNum)*int(Tc/PhaseNum)
		PhaseAction = []
		for i in xrange(PhaseNum):
			PhaseAction.append(intersection.get('phase'+str(i+1)))
		ActionInfo[intersection_id]=PhaseAction
	print PhaseTime

	# print ActionInfo
	# print PhaseTime

	VehNumEdge = defaultdict(lambda:0)
	# OccupyEdge = defaultdict(lambda:0)

	Counter = 0

	for i in range(Tsim):
		traci.simulationStep()
		Counter = Counter + 1

		for edge in EdgesList:
			edge_id = edge[2:]
			VehNumEdge[edge]+= traci.edge.getLastStepVehicleNumber(edge_id)
			# OccupyEdge[edge]+= traci.edge.getLastStepOccupancy(edge_id)


		############################################################################################################################
		####################################-------------Implement the signal setting--------------###################################
		for id in PhaseTime.keys():
			PhaseLen = PhaseTime[id]
			PhaseNum = len(PhaseLen)
			if PhaseNum==2:
				if Counter<=PhaseLen[0]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][0])
				elif Counter>PhaseLen[0] and Counter<=Tc:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][1])	

			if PhaseNum==3:
				if Counter<=PhaseLen[0]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][0])
				elif Counter>PhaseLen[0] and Counter<=PhaseLen[0]+PhaseLen[1]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][1])
				elif Counter>PhaseLen[0]+PhaseLen[1] and Counter<=Tc:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][2])


			if PhaseNum==4:
				if Counter<=PhaseLen[0]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][0])
				elif Counter>PhaseLen[0] and Counter<=PhaseLen[0]+PhaseLen[1]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][1])
				elif Counter>PhaseLen[0]+PhaseLen[1] and Counter<=PhaseLen[0]+PhaseLen[1]+PhaseLen[2]:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][2])
				elif Counter>PhaseLen[0]+PhaseLen[1]+PhaseLen[2] and Counter<=Tc:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][3])
			

		if Counter==Tc:			
			Counter = 0	
			#### record the 
			period = i/Tc
			for edge in EdgesList:
				interval = VehNum_files.createElement('interval')
				interval.setAttribute('begin',str(period*Tc))
				interval.setAttribute('end',str((period+1)*Tc))
				interval.setAttribute('id',edge)
				VehNumEdge[edge]/Tc
				interval.setAttribute('vehnum',str(VehNumEdge[edge]/Tc))
				# interval.setAttribute('Occupy',str(OccupyEdge[edge]/Tc))
				VehNum.appendChild(interval)
			VehNumEdge = defaultdict(lambda:0)
			# OccupyEdge = defaultdict(lambda:0)

			###change the phase time

			# if (i+1)%1200==0:
			# 	for intersection in ActionRoot.findall('Intersection'):
			# 		intersection_id = intersection.get('id')
			# 		PhaseNum = int(intersection.get('PhaseNum'))
			# 		PhaseTime[intersection_id]=get_random_phasetime(PhaseNum,Tc)
				# print PhaseTime
				

	fp = open('./FTCVehNum'+str(demand_level)+'.xml','w')
	
	try:
		VehNum_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
	except:
		trackback.print_exc() 
	finally: 
		fp.close() 

	traci.close()
