# -*- coding: UTF-8 -*-
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import random
from tqdm import tqdm
# from time import time
# from scipy.optimize import linprog
# from cvxopt import matrix,solvers
from scipy.sparse import identity
from collections import defaultdict


import pdb

demand_level = 8

SUMO_HOME = "/usr/local/bin/sumo"
tools = "/home/Arain/sumo-git/tools/"
sys.path.append(tools)

sumoBinary = "/usr/local/bin/sumo"

sumoCmd = [sumoBinary, "-c", "actchj"+str(demand_level)+".sumocfg","--seed", str(random.randint(1,100))]

# if 'SUMO_HOME' in os.environ:
# 	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
# 	sys.path.append(tools)
# else:
# 	sys.exit("please declare environment variable 'SUMO_HOME'")
# sumoBinary = "E:/software/sumo-win64-0.32.0/sumo-0.32.0/bin/sumo-gui"

# sumoCmd = [sumoBinary, "-c", 'actchj'+str(demand_level)+'.sumocfg',"--seed", str(random.randint(1,100))]

PORT = 8813
import traci

doc3 = etree.parse('./loops_actuated.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('./Chj_final.net.xml')
NetRoot = doc4.getroot()
doc5 = etree.parse('./PhaseLanesCont.xml')
PhaseLanesRoot = doc5.getroot()

EdgesList = []
for edge in NetRoot.findall('edge'):
	new_EdgeID = edge.get('Region')+edge.get('id')
	EdgesList.append(new_EdgeID)

VehNum_files = doc.Document()
VehNum = VehNum_files.createElement('VehicleNumber')
VehNum_files.appendChild(VehNum)

##############################################################################################################
if __name__ == '__main__':	

	traci.start(sumoCmd)

	Tsim = 3600
	deltT = 10
	Tc = 60

	Occupy = defaultdict(lambda:0)
	Actions = defaultdict(lambda:0)
	CurrentPhase = defaultdict(lambda:0)
	NextAction = defaultdict(lambda:0)
	for junction in PhaseLanesRoot.findall('Intersection'):
		CurrentPhase[junction.get('id')]=['1',0]

		Occupy[junction.get('id')]=defaultdict(lambda:0)
		Actions[junction.get('id')]=defaultdict(lambda:0)
		for phase in junction.findall('Phase'):
			lanesNum = len(phase.get('fromLanes').split())
			Occupy[junction.get('id')][phase.get('No')]=0
			Actions[junction.get('id')][phase.get('No')]=phase.get('action')
		
		NextAction[junction.get('id')]=Actions[junction.get('id')][CurrentPhase[junction.get('id')][0]]
	

	PhaseSequence = {2:np.array([[2],[1]]),3:np.array([[2,3],[3,1],[1,2]]),4:np.array([[2,3,4],[3,4,1],[4,1,2],[1,2,3]])}

	Counter = 0
	Counter_T = 0

	VehNumEdge = defaultdict(lambda:0)

	for i in range(Tsim):
		traci.simulationStep()
		
		if Counter%deltT==0:
			Counter = 0

			for junction in PhaseLanesRoot.findall('Intersection'):
				Occupy[junction.get('id')]=defaultdict(lambda:0)
				for phase in junction.findall('Phase'):
					Occupy[junction.get('id')][phase.get('No')]=0
			 


			#### get the detected value for each phase
			for loop in LoopsRoot.findall('inductionLoop'):
				loop_id = loop.get('id')
				lane_id = loop.get('lane')
				detectvalue = traci.inductionloop.getLastStepOccupancy(loop_id)
				 
				for junction in PhaseLanesRoot.findall('Intersection'):
					if lane_id in junction.get('LoopLanes').split():
						for phase in junction.findall('Phase'):
							if lane_id in phase.get('fromLanes'):
								Occupy[junction.get('id')][phase.get('No')]+=detectvalue

			for junction in Occupy.keys():
				flag = 0
				PhaseNum = len(Occupy[junction].keys())
				if Occupy[junction][CurrentPhase[junction][0]]!=0 and CurrentPhase[junction][1]<4:
					NextAction[junction]=Actions[junction][CurrentPhase[junction][0]]
					CurrentPhase[junction][1]+=1
					flag = 1
				else:
					CurrentPhase[junction][1]=0
					## next phase
					for PhaseNo in PhaseSequence[PhaseNum][int(CurrentPhase[junction][0])-1]:

						if Occupy[junction][str(PhaseNo)]>0:
							NextAction[junction]=Actions[junction][str(PhaseNo)]
							CurrentPhase[junction][0]=str(PhaseNo)
							CurrentPhase[junction][1]+=1
							flag = 1
							break
				if flag==0:
					NextAction[junction]=Actions[junction][CurrentPhase[junction][0]]
					CurrentPhase[junction][1]+=1
					flag = 0

		############################################################################################################################
		####################################-------------Implement the signal setting--------------###################################
		for junction in Occupy.keys():
			traci.trafficlights.setRedYellowGreenState(junction,NextAction[junction])			
			
		Counter = Counter + 1

		Counter_T = Counter_T + 1

		for edge in EdgesList:
			edge_id = edge[2:]
			VehNumEdge[edge]+= traci.edge.getLastStepVehicleNumber(edge_id)
			# OccupyEdge[edge]+= traci.edge.getLastStepOccupancy(edge_id)
		

		if Counter_T==Tc:			
			Counter_T = 0	
			#### record the 
			period = i/Tc
			for edge in EdgesList:
				interval = VehNum_files.createElement('interval')
				interval.setAttribute('begin',str(period*Tc))
				interval.setAttribute('end',str((period+1)*Tc))
				interval.setAttribute('id',edge)				
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
				

	# fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\ACTVehNum.xml','w')

	fp = open('./ACTVehNum'+str(demand_level)+'.xml','w')	
	try:
		VehNum_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
	except:
		trackback.print_exc() 
	finally: 
		fp.close() 

	traci.close()