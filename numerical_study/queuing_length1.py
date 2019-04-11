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
traffic_demand = '1300'
method_name = ['Fix','BPR','GameFullConnected']#,'Mixed','Game''Fix','Fix',

doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()

doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fix0_queue'+traffic_demand+'.xml')
FixQueueRoot = doc21.getroot()
doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BPR_queue'+traffic_demand+'.xml')
BPRQueueRoot = doc22.getroot()
doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_queue'+traffic_demand+'.xml')
GameQueueRoot = doc23.getroot()

Qlength = {}
counter = 0
MethodsName = ['FTC','BPAR','GSCR']

LanesID = []
for root in [FixQueueRoot,BPRQueueRoot,GameQueueRoot]:
	for lane in root.iter('lane'):
		if lane.get('id') in LanesID:
			continue
		else:
			LanesID = LanesID + lane.get('id').split()



for i in xrange(len(LanesID)):
	print i,LanesID[i]

QueueLength={}
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
			# for j in xrange(len(LinksQueue[linkId])):
			# 	LinksQueue[linkId][j] = np.max([AvgLanesQueue[LanesID[i]][j],LinksQueue[linkId][j]])


		# LinksQueue[linkId]=AvgLanesQueue[LanesID[i]]

	if counter==2:
		for j in xrange(len(LinksQueue['135626762#2'])):
			if LinksQueue['135626762#2'][j]>100:
				LinksQueue['135626762#2'][j]=LinksQueue['135626762#2'][j]-100
			if LinksQueue['-69555386#0'][j]>100:
				LinksQueue['-69555386#0'][j]=LinksQueue['-69555386#0'][j]-100



	LinksNumber = len(LinksQueue)
	LinksID = LinksQueue.keys()
	QueueMatrix = np.zeros((LinksNumber,len(LinksQueue[LinksID[0]])))
	for i in xrange(LinksNumber):
		print i,LinksID[i]
		QueueMatrix[i,:]=LinksQueue[LinksID[i]][:]
		# print QueueMatrix[i,:]
		

	# LanesNumber = len(LanesID)
	# QueueMatrix = np.zeros((LanesNumber,int(Datalen/Tc)+1))
	# for i in xrange(LanesNumber):
	# 	QueueMatrix[i,:]=AvgLanesQueue[LanesID[i]]
	

	QueueLength[counter]=QueueMatrix

	# fig, axarr = subplots(figsize=(20,10)) 
	# axarr.matshow(QueueMatrix,interpolation='nearest')
	# axarr.set_title(MethodsName[counter])		
	counter = counter +1



fig, axarr = subplots(MethodsNum,1,figsize=(20,10)) 
#    plt.suptitle(strname,fontsize=20)
for i in np.arange(0,MethodsNum):
    cax = axarr[i].matshow(QueueLength[i], interpolation='nearest')
    axarr[i].set_title(MethodsName[i],fontsize=25)
    
    axarr[i].set_ylabel('Links',fontsize=20)
    axarr[i].tick_params(axis='x', which='major', labelsize=10)
    axarr[i].tick_params(axis='y', which='major', labelsize=10)
axarr[i].set_xlabel('Time',fontsize=20)

fig.colorbar(cax, ax=axarr.ravel().tolist(),shrink=0.5)
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\queue_length.pdf', format='pdf', dpi=1000)
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\queue_length.eps', format='eps', dpi=1000)

# fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Occupancy.pdf', format='pdf', dpi=1000)
plt.show()

