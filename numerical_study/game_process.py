# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt


traffic_demand = ['400','600','800','900','1000','11001','1200','13001']#,'700','1400','1500']#,'1600','1700','1800','1900','2000']
doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()

Tc = 60.0

GameRecord = np.zeros((len(traffic_demand),4))
for k in xrange(len(traffic_demand)):
	print k

	doc11 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameRecord'+traffic_demand[k]+'.xml')
	GameRoot = doc11.getroot()



	GameTimes = 0
	GameEndNoViolates = 0
	GameEndGreenTime = 0
	GameEndFullUtilization = 0
	for ctrlstep in GameRoot.findall('CtrlTimeStep'):
		Intersections = ctrlstep.findall('Intersection')
		GameTimes += len(Intersections)
		for intersection in Intersections:
			intersection_id = intersection.get('ID')
			iterationsteps = intersection.findall('IterationStep')
			violate = iterationsteps[-1].get('Violates')
			Utilization = iterationsteps[-1].get('Utilization')
			PhaseTime0 = iterationsteps[-1].get('PhaseTime').split('.')
			PhaseTime=np.zeros(3)
			PhaseTime[0]=float(PhaseTime0[0][1:])
			PhaseTime[1]=float(PhaseTime0[1])
			PhaseTime[2]=float(PhaseTime0[2])
			vehnum = np.zeros(3)
			if intersection_id=="cluster_479970073_832425883":
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_31_1'))
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_32_1'))
				vehnum[1]+=float(iterationsteps[-1].get('VehNum_33_2'))
				vehnum[2]+=float(iterationsteps[-1].get('VehNum_34_3'))
			elif intersection_id=="cluster_1091232602_1091232686_479970097_832425852":
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_41_1'))
				vehnum[1]+=float(iterationsteps[-1].get('VehNum_42_2'))
				vehnum[2]+=float(iterationsteps[-1].get('VehNum_43_3'))
			elif intersection_id=="2387375101":
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_10_1'))
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_11_1'))
				vehnum[1]+=float(iterationsteps[-1].get('VehNum_12_2'))
				vehnum[2]+=float(iterationsteps[-1].get('VehNum_13_3'))
			elif intersection_id=="cluster_400709716_5240921810":
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_21_1'))
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_22_2'))
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_23_3'))
				vehnum[0]+=float(iterationsteps[-1].get('VehNum_24_3'))
			
			Utilization=1

			for i in xrange(3):
				if PhaseTime[i]*0.2-vehnum[i]>0:
					Utilization=0

			if violate=='0' and Utilization!=1:
				GameEndNoViolates+=1
			elif Utilization==1:
				GameEndFullUtilization+=1
			else:
				GameEndGreenTime+=1


	GameRecord[k,0]=GameEndNoViolates
	GameRecord[k,1]=GameEndFullUtilization
	GameRecord[k,2]=GameEndGreenTime
	GameRecord[k,3]=GameTimes

GameRecord = np.transpose(GameRecord)



