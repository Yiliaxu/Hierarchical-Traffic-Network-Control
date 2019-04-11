# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt

doc1 = etree.parse('D:\conference_paper\ITSC2018\Simulation\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()


Tc = 60.0

############################################################################################
#################################### Queue length #########################################

doc21 = etree.parse('D:\conference_paper\ITSC2018\Simulation\Fix_queue'+traffic_demand+'.xml')
FixQueueRoot = doc21.getroot()
doc22 = etree.parse('D:\conference_paper\ITSC2018\Simulation\BP_queue'+traffic_demand+'.xml')
BPQueueRoot = doc22.getroot()
doc23 = etree.parse('D:\conference_paper\ITSC2018\Simulation\Game_queue'+traffic_demand+'.xml')
GameQueueRoot = doc23.getroot()

Qlength = {}
counter = 0
MethodsName = ['FTC','CBP','GSC']

LanesID = []
for root in [FixQueueRoot,BPQueueRoot,GameQueueRoot]:
	for lane in root.iter('lane'):
		if lane.get('id') in LanesID:
			continue
		else:
			LanesID = LanesID + lane.get('id').split()



for i in xrange(len(LanesID)):
	print i,LanesID[i]

QueueLength={}
for root in [FixQueueRoot,BPQueueRoot,GameQueueRoot]:
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
	LanesNumber = len(LanesID)
	QueueMatrix = np.zeros((LanesNumber,int(Datalen/Tc)+1))
	for i in xrange(LanesNumber):
		QueueMatrix[i,:]=AvgLanesQueue[LanesID[i]]
	

	QueueLength[counter]=QueueMatrix

	# fig, axarr = subplots(figsize=(20,10)) 
	# axarr.matshow(QueueMatrix,interpolation='nearest')
	# axarr.set_title(MethodsName[counter])		
	counter = counter +1



fig, axarr = subplots(1,MethodsNum,figsize=(20,10)) 
#    plt.suptitle(strname,fontsize=20)
for i in np.arange(0,MethodsNum):
    cax = axarr[i].matshow(QueueLength[i], interpolation='nearest')
    axarr[i].set_title(MethodsName[i],fontsize=25)
    axarr[i].set_xlabel('Time',fontsize=20)
    axarr[i].set_ylabel('Link number',fontsize=20)
    axarr[i].tick_params(axis='x', which='major', labelsize=10)
    axarr[i].tick_params(axis='y', which='major', labelsize=10)

fig.colorbar(cax, ax=axarr.ravel().tolist(),shrink=0.5)
fig.savefig('D:\\conference_paper\\ITSC2018\\IEEEtran\\IEEEtran\\Fig\\Occupancy'+traffic_demand+'.pdf', format='pdf', dpi=1000)
# fig.savefig("occupancy"+traffic_demand+".pdf", bbox_inches='tight')
show()
######################## route

