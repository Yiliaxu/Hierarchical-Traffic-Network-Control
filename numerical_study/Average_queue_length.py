# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt
from collections import defaultdict


MethodsNum = 3


Tc = 60.0

############################################################################################
#################################### Queue length #########################################
traffic_demand = ['400','600','800','900','1000','1100','1200','1300']
method_name = ['Fix','BPR','GameFullConnected'] #,'Mixed','Game''Fix','Fix',

doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()


AvgLinkQ = np.zeros((len(method_name),len(traffic_demand)))
for k in xrange(len(traffic_demand)):

	doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fix0_queue'+traffic_demand[k]+'.xml')
	FixQueueRoot = doc21.getroot()
	doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BPR_queue'+traffic_demand[k]+'.xml')
	BPRQueueRoot = doc22.getroot()
	doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_queue'+traffic_demand[k]+'.xml')
	GameQueueRoot = doc23.getroot()


	counter = 0
	MethodsName = ['FTC','BPAR','GSCR']

	LanesID = []
	# for root in [FixQueueRoot,BPRQueueRoot,GameQueueRoot]:
	# 	for lane in root.iter('lane'):
	# 		if lane.get('id') in LanesID:
	# 			continue
	# 		else:
	# 			LanesID = LanesID + lane.get('id').split()

	for junction in JunctionRoot.findall('Intersection'):
		for movement in junction.findall('movement'):
			connection = movement.find('connection')
			InputLanes = connection.get('from').split()
			OutputLanes = connection.get('to').split()
			LanesID = LanesID+InputLanes+OutputLanes
				



	for root in [FixQueueRoot,BPRQueueRoot,GameQueueRoot]:
		Datas  = root.findall('data')
		Datalen = len(Datas)

		LanesQueue = {}
		AvgLanesQueue={}
		for lane in LanesID:
			LanesQueue[lane]=np.zeros(int(Tc))
			AvgLanesQueue[lane]=np.zeros(int(Datalen/Tc)+1)

		num = 0
		for i in xrange(Datalen):
			Lanes = Datas[i].find('lanes')
			num = num+1
			for lane in Lanes.findall('lane'):
				laneID = lane.get('id')
				if laneID in LanesID:
					LanesQueue[laneID][num-1] = lane.get('queueing_length')
					if i%Tc==0.0:
						n = int(i/Tc)			
						AvgLanesQueue[laneID][n] = np.mean(LanesQueue[laneID])
			if i%Tc==0.0:
				num=0

		# pdb.set_trace()
		#print IntersectionLaneQueue
		LanesNumber = len(AvgLanesQueue)
		LanesID = AvgLanesQueue.keys()
		LinksQueue = {}
		for i in xrange(LanesNumber):
			linkId = LanesID[i].split('_')[0]
			if linkId not in LinksQueue.keys():
				LinksQueue[linkId] = AvgLanesQueue[LanesID[i]]
			else:
				LinksQueue[linkId]+= AvgLanesQueue[LanesID[i]]



		LinksNumber = len(LinksQueue)
		print LinksNumber
		TotalQlen = 0
		LinksID = LinksQueue.keys()
		print len(LinksQueue[LinksID[0]])
		
		for i in xrange(LinksNumber):
			TotalQlen += np.sum(LinksQueue[LinksID[i]])
		AvgLinkQ[counter][k] = TotalQlen/(LinksNumber*len(LinksQueue[LinksID[0]]))

		
		counter = counter +1


print AvgLinkQ
print AvgLinkQ*2.5

FTC 4.4 6.9 35.9 163.4 204.0 226.1 241.1 249.8
BPAR 4.8 7.3 15.9 20.6 30.9 98.6 171.3 206.6
GSCR 4.7 7.1 20.3 26.4 34.5 49.3 67.2 83.3
