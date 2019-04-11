import matplotlib.pyplot as plt
import os,sys,re
import xml.etree.ElementTree as etree
import math
import numpy as np 
from collections import defaultdict


############################################################################################
#################################### Queue length #########################################
traffic_demand = '1200'
method_name = ['Fix','BPR','GameFullConnected']#,'Mixed','Game''Fix','Fix',

doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()

doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fix0_queue'+traffic_demand+'.xml')
FixQueueRoot = doc21.getroot()
doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BPR_queue'+traffic_demand+'.xml')
BPRQueueRoot = doc22.getroot()
doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_queue'+traffic_demand+'.xml')
GameQueueRoot = doc23.getroot()


Tc = 60
MethodsNum = len(method_name)
Qlength = {}
counter = 0
for root in [FixQueueRoot,BPRQueueRoot,GameQueueRoot]:#
	Datas  = root.findall('data')
	Datalen = len(Datas)

	LanesQueue = {}
	for junction in JunctionRoot.findall('Intersection'):
		for movement in junction.findall('movement'):
			connection = movement.find('connection')
			InputLanes = connection.get('from').split()
			OutputLanes = connection.get('to').split()
			TotalLanes = InputLanes+OutputLanes
			for lane in TotalLanes:
				LanesQueue[lane]=np.zeros(int(Datalen/Tc)+1)

	for i in xrange(Datalen):
		if i%Tc==0.0:
			n = int(i/Tc)
			Lanes = Datas[i].find('lanes')
			for lane in Lanes.findall('lane'):
				laneID = lane.get('id')
				if laneID in LanesQueue.keys():
					LanesQueue[laneID][n] = float(lane.get('queueing_length'))

	# IntersectionLaneQueue = {}
	# for junction in JunctionRoot:
	# 	for movement in junction.findall('movement'):
	# 		connection = movement.find('connection')
	# 		inputlanes = connection.get('from').split()
	# 		if len(inputlanes)==1:
	# 			inputlaneID = inputlanes[0]
	# 			IntersectionLaneQueue[inputlaneID]=LanesQueue[inputlanes[0]]
	# 		else:
	# 			inputlaneID = inputlanes[-1]
	# 			IntersectionLaneQueue[inputlaneID] = LanesQueue[inputlanes[0]]
	# 			for i in np.arange(1,len(inputlanes)):
	# 				IntersectionLaneQueue[inputlaneID]=IntersectionLaneQueue[inputlaneID]+LanesQueue[inputlanes[i]]

	# pdb.set_trace()
	#print IntersectionLaneQueue

	# IntersectionLanes = IntersectionLaneQueue.keys()
	LanesNumber = len(LanesQueue)
	LanesID = LanesQueue.keys()
	LinksQueue = defaultdict(lambda :0)
	for i in xrange(LanesNumber):
		linkId = LanesID[i].split('_')[0]
		LinksQueue[linkId]+=LanesQueue[LanesID[i]]



	LinksNumber = len(LinksQueue)
	LinksID = LinksQueue.keys()
	QueueMatrix = np.zeros((LinksNumber,int(Datalen/Tc)+1))
	for i in xrange(LinksNumber):
		print LinksID[i]
		QueueMatrix[i,:]=LinksQueue[LinksID[i]][:]
		# print QueueMatrix[i,:]
		

	Qlength[counter]=QueueMatrix
	counter = counter +1

fig, axarr = plt.subplots(MethodsNum,1,figsize=(10,20)) 
MethodsName = ['Fixed-time','BackPressureRouting','Gamecontrol']#,
for i in xrange(MethodsNum):
	# print Qlength[i].shape
	cax = axarr[i].matshow(Qlength[i],interpolation='nearest')
	axarr[i].set_title(MethodsName[i],fontsize=20)
fig.colorbar(cax, ax=axarr.ravel().tolist(), shrink=0.5)
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Occupancy.pdf', format='pdf', dpi=1000)
plt.show()