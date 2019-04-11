# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt

traffic_demand = '700'
MethodsNum = 3

doc11 = etree.parse('D:\Journal_paper\conference paper\ITSC\Simulation\Fix_tripinfo'+traffic_demand+'.xml')
FixTripsRoot = doc11.getroot()
doc12 = etree.parse('D:\Journal_paper\conference paper\ITSC\Simulation\BP_tripinfo'+traffic_demand+'.xml')
BPTripsRoot = doc12.getroot()
doc13 = etree.parse('D:\Journal_paper\conference paper\ITSC\Simulation\Game_tripinfo'+traffic_demand+'.xml')
GameTripsRoot = doc13.getroot()


doc3 = etree.parse('D:\Journal_paper\conference paper\ITSC\Simulation\IntersectionCtrl_info.xml')
JunctionRoot = doc3.getroot()

Tc = 60.0  

TravelTime = {}
TimeLoss = {}
WaitTime= {}
Reroute = {}

############################### Total number of vehicles along time ######################
OD = [['-69555386#3','230351342'],['135626778#0','230491011'],['240833369#0','492979895#2'],['95775639#1','-448953275#0']]
MeanTravelTime = np.zeros((MethodsNum,len(OD)))
MeanWaitTime = np.zeros((MethodsNum,len(OD)))
counter = 0
for root in [FixTripsRoot,BPTripsRoot,GameTripsRoot]:
	for od in xrange(len(OD)):
		TravelTime[od] = {}
		TimeLoss[od] = {}
		WaitTime[od] = {}
		Reroute[od] = {}

	for tripinfo in root.findall('tripinfo'):
		vehid = tripinfo.get('id')
		departlink = tripinfo.get('departLane').split('_')[0]
		arrivallink = tripinfo.get('arrivalLane').split('_')[0]
		for i in xrange(len(OD)):
			if departlink==OD[i][0] and arrivallink==OD[i][1]:
				TravelTime[i][vehid] = float(tripinfo.get('duration'))
				WaitTime[i][vehid]=float(tripinfo.get('waitSteps'))
				TimeLoss[i][vehid]=float(tripinfo.get('timeLoss'))
				Reroute[i][vehid]= int(tripinfo.get('rerouteNo'))

	for od in xrange(len(OD)):
		MeanTravelTime[counter,od] = np.mean(TravelTime[od].values())
		MeanWaitTime[counter,od] = np.mean(WaitTime[od].values())

	counter = counter +1


# pdb.set_trace()

pos = list(range(len(MeanWaitTime[0,:])))
width = 0.2
fig, ax = plt.subplots(figsize=(16,10)) 
bar(pos, MeanWaitTime[0,:], width, alpha=0.5, color='b')
bar([p + width for p in pos], MeanWaitTime[1,:], width, alpha=0.5, color='g')
bar([p + width*2 for p in pos], MeanWaitTime[2,:], width, alpha=0.5, color='r')
 
ax.set_xlabel('OD pairs',fontsize=20)
ax.set_ylabel('Mean travel time for arrived vehicles',fontsize=20)
ax.set_title('The mean travel time for each OD pair',fontsize=20)
ax.set_xticks([p + 1.5 * width for p in pos])
xticks([0,1,2,3],
       [r'$OD1$',r'$OD2$',r'$OD3$',r'$OD4$'])
     
# xlim(min(pos)-width, max(pos)+width*4)
# ylim([0, max(max(data1), max(data2), max(data3)) * 1.2])

legend(['Fix_ctrl','BP_ctrl','Game_ctrl'], loc='upper left', prop={'size':16})
grid()
show()





