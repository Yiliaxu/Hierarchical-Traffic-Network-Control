# -*- coding: UTF-8 -*-
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import random
from tqdm import tqdm
from time import time
from scipy.optimize import linprog
from cvxopt import matrix,solvers
from scipy.sparse import identity
import pdb


if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:
	sys.exit("please declare environment variable 'SUMO_HOME'")
sumoBinary = "E:/software/sumo-win64-0.32.0/sumo-0.32.0/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "chj.sumocfg","--seed", str(42)]

PORT = 8813
import traci

doc1 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSAction.xml')
ActionRoot = doc1.getroot()
doc2 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
RouteRoot = doc2.getroot()
doc3 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.net.xml')
NetRoot = doc4.getroot()

saturateflow = 2 ##veh/s



##############################################################################################################
if __name__ == '__main__':	

	traci.start(sumoCmd)

	Tsim = 3600
	Tc = 60

	ActionInfo={}
	PhaseTime={}
	for intersection in ActionRoot.findall('Intersection'):
		intersection_id = intersection.get('id')
		PhaseNum = int(intersection.get('PhaseNum'))
		PhaseTime[intersection_id]=np.ones(PhaseNum)*int(Tc/PhaseNum)
		PhaseAction = []
		for i in xrange(PhaseNum):
			PhaseAction.append(intersection.get('phase'+str(i+1)))
		ActionInfo[intersection_id]=PhaseAction

	# print ActionInfo
	# print PhaseTime


	# for loop in LoopsRoot:
	# 	LaneID = loop.get('id')
	# 	ArrivalRate[LaneID]=0


	Counter = 0
	for i in range(Tsim):
		traci.simulationStep()
		Counter = Counter + 1

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

	traci.close() 

