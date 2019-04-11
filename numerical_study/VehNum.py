# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt



SimLen = 3600
Tc = 60
Times = SimLen/Tc

traffic_demand = ['8']#'5','6','7','8','9',
MethodsNum = 3
method_name = ['FTC','HTSC','ASC'] 
colorstr = ['k','b','g','r']


for k in xrange(len(traffic_demand)): 	

	# pdb.set_trace()
	############################### Total number of vehicles along time ######################
	doc11 = etree.parse('../FTCsummary'+traffic_demand[k]+'.xml')
	FixStepsRoot = doc11.getroot()
	doc12 = etree.parse('../HTSCsummary'+traffic_demand[k]+'.xml')
	HTSCStepsRoot = doc12.getroot()	
	doc13 = etree.parse('../ACTsummary'+traffic_demand[k]+'.xml')
	TestStepsRoot = doc13.getroot()
	
	StepNum = len(FixStepsRoot.findall('step')) 
	VehNumAlongTime = np.zeros((MethodsNum,StepNum))
	InsertedAlongTime = np.zeros((MethodsNum,StepNum))
	WaitToInsert = np.zeros((MethodsNum,StepNum))
	ArrivalsAlongTime = np.zeros((MethodsNum,StepNum))
	MeanSpeedAlongTime = np.zeros((MethodsNum,StepNum))
	counter = 0
	for root in [FixStepsRoot,HTSCStepsRoot,TestStepsRoot]:
		Steps = root.findall('step')
		for i in xrange(StepNum):
			VehNumAlongTime[counter][i] = float(Steps[i].get('running'))
			InsertedAlongTime[counter][i] = float(Steps[i].get('inserted'))
			ArrivalsAlongTime[counter][i] = float(Steps[i].get('ended'))
			MeanSpeedAlongTime[counter][i] = float(Steps[i].get('meanSpeed'))
			WaitToInsert[counter][i] = float(Steps[i].get('waiting'))
		counter = counter + 1


	fig,ax = subplots(figsize=(15,10))
	for i in xrange(MethodsNum):
		ax.plot(VehNumAlongTime[i][:],colorstr[i],linewidth=5)
	ax.legend(method_name,prop={'size':25})
	ax.set_xlabel('Time(s)',fontsize=25)
	ax.set_ylabel('Vehicle Number',fontsize=25)
	plt.tick_params(labelsize = 20)
	title('The total number of vehicles in the network along time with demand '+traffic_demand[k],fontsize=30)
	grid()
	fig.savefig('../Figures/Total_vehicle_Number'+traffic_demand[k]+'.eps', format='eps', dpi=1000)



	fig,ax = subplots(figsize=(15,10))
	for i in xrange(MethodsNum):
		ax.plot(InsertedAlongTime[i][:],colorstr[i],linewidth=5)
	ax.legend(method_name,prop={'size':25})
	ax.set_xlabel('Time(s)',fontsize=25)
	ax.set_ylabel('Vehicle Number',fontsize=25)
	plt.tick_params(labelsize = 20)
	title('The number of vehicles inserted into the network with demand '+traffic_demand[k],fontsize=30)
	grid()
	fig.savefig('../Figures/Inserted_VehNum'+traffic_demand[k]+'.eps', format='eps', dpi=1000)


	fig,ax = subplots(figsize=(15,10))
	for i in xrange(MethodsNum):
		ax.plot(ArrivalsAlongTime[i][:],colorstr[i],linewidth=5)
	ax.legend(method_name,prop={'size':25})
	ax.set_xlabel('Time(s)',fontsize=25)
	ax.set_ylabel('Vehicle Number',fontsize=25)
	plt.tick_params(labelsize = 20)
	title('The number of vehicles reaching their destination with demand '+traffic_demand[k],fontsize=30)
	grid()
	fig.savefig('../Figures//Arrival_vehicle_Number'+traffic_demand[k]+'.eps', format='eps', dpi=1000)


	fig,ax = subplots(figsize=(15,10))
	for i in xrange(MethodsNum):
		ax.plot(WaitToInsert[i][:],colorstr[i],linewidth=5)
	ax.legend(method_name,prop={'size':25})
	ax.set_xlabel('Time(s)',fontsize=25)
	ax.set_ylabel('Vehicle Number',fontsize=25)
	plt.tick_params(labelsize = 20)
	title('The number of vehicles waiting to insert the network with demand '+traffic_demand[k],fontsize=30)
	grid()
	fig.savefig('../Figures/Wait_to_Insert'+traffic_demand[k]+'.eps', format='eps', dpi=1000)


	# fig,axarr = subplots(figsize=(15,10))
	# for i in xrange(MethodsNum):
	# 	cycleSpeed = np.zeros(int(StepNum/Tc))
	# 	for j in xrange(int(StepNum/Tc)):
	# 		cycleSpeed[j] = np.mean(MeanSpeedAlongTime[i][int(Tc*j):int(Tc*(j+1)+1)])
	# 	axarr.plot(cycleSpeed,colorstr[i],linewidth=5)
	# axarr.legend(['Fixed-time','BackPressure','Game control'])
	# title('The mean speed for vehicles along time')


	fig,axarr = subplots(figsize=(15,10))
	for i in xrange(MethodsNum):
		Speed = np.zeros(StepNum)
		for j in xrange(StepNum):
			Speed[j] = MeanSpeedAlongTime[i][j]
		axarr.plot(Speed,colorstr[i],linewidth=5)
	axarr.legend(method_name,prop={'size':25})
	ax.set_xlabel('Time(s)',fontsize=25)
	ax.set_ylabel('Speed (m/s)',fontsize=25)
	plt.tick_params(labelsize = 20)
	title('The mean speed for vehicles along time with demand '+traffic_demand[k],fontsize=30)
	grid()
	fig.savefig('../Figures/Mean_Speed'+traffic_demand[k]+'.eps', format='eps', dpi=1000)



# ############################################################################################
# #################################### Queue length #########################################
# doc1 = etree.parse('../IntersectionCtrl_info.xml')
# JunctionRoot = doc1.getroot()

# doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fix_queue'+traffic_demand+'.xml')
# FixQueueRoot = doc21.getroot()
# doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BP_queue'+traffic_demand+'.xml')
# BPQueueRoot = doc22.getroot()
# doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Game_queue'+traffic_demand+'.xml')
# GameQueueRoot = doc23.getroot()
# doc24 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameBargaining_queue'+traffic_demand+'.xml')
# GameBargainingQueueRoot = doc24.getroot()

# Qlength = {}
# counter = 0
# for root in [FixQueueRoot,BPQueueRoot,GameQueueRoot,GameBargainingQueueRoot]:
# 	Datas  = root.findall('data')
# 	Datalen = len(Datas)

# 	LanesQueue = {}
# 	for junction in JunctionRoot.findall('Intersection'):
# 		for movement in junction.findall('movement'):
# 			connection = movement.find('connection')
# 			InputLanes = connection.get('from').split()
# 			for lane in InputLanes:
# 				LanesQueue[lane]=np.zeros(int(Datalen/Tc)+1)

# 	for i in xrange(Datalen):
# 		if i%Tc==0.0:
# 			n = int(i/Tc)
# 			Lanes = Datas[i].find('lanes')
# 			for lane in Lanes.findall('lane'):
# 				laneID = lane.get('id')
# 				if laneID in LanesQueue.keys():
# 					LanesQueue[laneID][n] = float(lane.get('queueing_length'))

# 	IntersectionLaneQueue = {}
# 	for junction in JunctionRoot:
# 		for movement in junction.findall('movement'):
# 			connection = movement.find('connection')
# 			inputlanes = connection.get('from').split()
# 			if len(inputlanes)==1:
# 				inputlaneID = inputlanes[0]
# 				IntersectionLaneQueue[inputlaneID]=LanesQueue[inputlanes[0]]
# 			else:
# 				inputlaneID = inputlanes[-1]
# 				IntersectionLaneQueue[inputlaneID] = LanesQueue[inputlanes[0]]
# 				for i in np.arange(1,len(inputlanes)):
# 					IntersectionLaneQueue[inputlaneID]=IntersectionLaneQueue[inputlaneID]+LanesQueue[inputlanes[i]]

# 	# pdb.set_trace()
# 	#print IntersectionLaneQueue

# 	IntersectionLanes = IntersectionLaneQueue.keys()
# 	LanesNumber = len(IntersectionLanes)
# 	QueueMatrix = np.zeros((LanesNumber,int(Datalen/Tc)+1))
# 	for i in xrange(LanesNumber):
# 		QueueMatrix[i,:]=IntersectionLaneQueue[IntersectionLanes[i]]
# 	Qlength[counter]=QueueMatrix
# 	counter = counter +1

# fig, axarr = subplots(MethodsNum,1,figsize=(20,10)) 
# MethodsName = ['Fixed-time','BackPressure','Gamecontrol','GameBargaining']
# for i in xrange(MethodsNum):
# 	cax = axarr[i].matshow(Qlength[i],interpolation='nearest')
# 	axarr[i].set_title(MethodsName[i],fontsize=20)
# fig.colorbar(cax, ax=axarr.ravel().tolist(), shrink=0.5)
# fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Occupancy.pdf', format='pdf', dpi=1000)

show()


