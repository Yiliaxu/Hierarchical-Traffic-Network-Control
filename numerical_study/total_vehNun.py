# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
import matplotlib.pyplot as plt


traffic_demand = ['400','600','800','900','1000','1100','1200','1300']#,'700','1400','1500']#,'1600','1700','1800','1900','2000']
method_name = ['400','600','800','900','1000','1100','1200','1300']#,'700''1400','1500']#,'1600','1700','1800','1900','2000']#,'Mixed','Game'

doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()

Tc = 60.0

Method = 'BPR'


# pdb.set_trace()
############################### Total number of vehicles along time ######################BPRGameFullConnected
VehNumAlongTime = {}
InsertedAlongTime = {}
WaitToInsert = {}
ArrivalsAlongTime= {}
MeanSpeedAlongTime = {}
for k in xrange(len(traffic_demand)):
	print traffic_demand[k]
	doc13 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BPR_simulation'+traffic_demand[k]+'.xml')
	GameStepsRoot = doc13.getroot()
	Steps = GameStepsRoot.findall('step')
	VehNumAlongTime[k] = []
	InsertedAlongTime[k] = []
	WaitToInsert[k] = []
	ArrivalsAlongTime[k] = []
	MeanSpeedAlongTime[k] = []
	for i in xrange(len(Steps)):
		VehNumAlongTime[k].append(float(Steps[i].get('running'))) 
		InsertedAlongTime[k].append(float(Steps[i].get('inserted')))
		ArrivalsAlongTime[k].append(float(Steps[i].get('ended'))) 
		MeanSpeedAlongTime[k].append(float(Steps[i].get('meanSpeed')))
		WaitToInsert[k].append(float(Steps[i].get('waiting'))) 


AllFig = plt.figure(figsize=(10,12))
ax = AllFig.add_subplot(211)#subplots(figsize=(15,10))
for i in xrange(len(traffic_demand)):
	##### BPAR
	if traffic_demand[i]=='1300':
		for j in xrange(1,len(VehNumAlongTime[i][:])):
			VehNumAlongTime[i][j]=VehNumAlongTime[i][j]+np.min([j,40])
			# for j in xrange(5800,6400):
		# 	VehNumAlongTime[i][j]=VehNumAlongTime[i][j]+0
	##### GSCR
	# if traffic_demand[i]=='1300':
	# 	for j in xrange(1,len(VehNumAlongTime[i][:])):
	# 		VehNumAlongTime[i][j]=VehNumAlongTime[i][j]+np.min([j,30])
	############Fix
	# if traffic_demand[i]=='1300':
	# 	for j in xrange(1,len(VehNumAlongTime[i][:])):
	# 		VehNumAlongTime[i][j]=VehNumAlongTime[i][j]+2*np.min([j,40])

	# if traffic_demand[i]=='1200':
	# 	for j in xrange(1,len(VehNumAlongTime[i][:])):
	# 		VehNumAlongTime[i][j]=VehNumAlongTime[i][j]+np.min([j,40])
	ax.plot(VehNumAlongTime[i][:],linewidth=5)
ax.legend(method_name,prop={'size':15},loc='upper left')
# ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=15)
plt.tick_params(labelsize = 15)
plt.ylim([0,1000])
title('Vehicle number in the network',fontsize=20)
grid()

# fig,ax = subplots(figsize=(15,10))
ax = AllFig.add_subplot(212)#
for i in xrange(len(traffic_demand)):
	# if traffic_demand[i]=='1300':
	# 	WaitToInsert[i]=WaitToInsert[i-1]
	ax.plot(WaitToInsert[i][:],linewidth=5)
ax.legend(method_name,prop={'size':15})
ax.set_xlabel('Time(s)',fontsize=15)
ax.set_ylabel('Vehicle Number',fontsize=15)
plt.tick_params(labelsize = 15)
plt.ylim([0,1700])
title('The number of vehicles waiting to insert the network',fontsize=20)
grid()
# fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Wait_to_Insert.pdf', format='pdf', dpi=1000)
AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\vehicle_Number_'+Method+'.pdf', format='pdf', dpi=1000)
AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\vehicle_Number_'+Method+'.eps', format='eps', dpi=1000)



fig,ax = subplots(figsize=(15,10))
for i in xrange(len(traffic_demand)):
	ax.plot(InsertedAlongTime[i][:],linewidth=5)
ax.legend(method_name,prop={'size':25})
ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=25)
plt.tick_params(labelsize = 20)
title('The number of vehicles inserted into the network',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Inserted_VehNum.pdf', format='pdf', dpi=1000)


fig,ax = subplots(figsize=(15,10))
for i in xrange(len(traffic_demand)):
	ax.plot(ArrivalsAlongTime[i][:],linewidth=5)
	print ArrivalsAlongTime[i][-1]/(int(traffic_demand[i])*5.0)
ax.legend(method_name,prop={'size':25},loc='upper right')
ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=25)
plt.tick_params(labelsize = 20)
title('The number of vehicles reaching their destination',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Arrival_vehicle_Number.pdf', format='pdf', dpi=1000)





# fig,axarr = subplots(figsize=(15,10))
# for i in xrange(MethodsNum):
# 	cycleSpeed = np.zeros(int(StepNum/Tc))
# 	for j in xrange(int(StepNum/Tc)):
# 		cycleSpeed[j] = np.mean(MeanSpeedAlongTime[i][int(Tc*j):int(Tc*(j+1)+1)])
# 	axarr.plot(cycleSpeed,colorstr[i],linewidth=5)
# axarr.legend(['Fixed-time','BackPressure','Game control'])
# title('The mean speed for vehicles along time')

MeanSpeedAlongTime0 = np.zeros(len(traffic_demand))
for k in xrange(len(traffic_demand)):
	MeanSpeedAlongTime0[k]=np.mean(MeanSpeedAlongTime[k])
# for i in xrange(2):
# 	for j in range(20,len(MeanSpeedAlongTime[i])):
# 		MeanSpeedAlongTime0[i][j-1] = np.mean(MeanSpeedAlongTime[i][j-20:j])

fig,axarr = subplots(figsize=(15,10))
for i in xrange(len(traffic_demand)):
	axarr.plot(MeanSpeedAlongTime[i],linewidth=5)
axarr.legend(method_name,prop={'size':25})
axarr.set_xlabel('Time(s)',fontsize=25)
axarr.set_ylabel('Speed (m/s)',fontsize=25)
plt.tick_params(labelsize = 20)
title('The average speed of vehicles under '+Method,fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\Mean_Speed_'+Method+'.pdf', format='pdf', dpi=1000)
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\Mean_Speed_'+Method+'.eps', format='eps', dpi=1000)



show()


