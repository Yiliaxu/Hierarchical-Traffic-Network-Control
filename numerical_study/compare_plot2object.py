# -*- coding: UTF-8 -*-
import os, sys, re
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import pdb
from pylab import *
 


traffic_demand = '1400'
method_name = ['BP','GameBargaining']

doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()

Tc = 60.0

# pdb.set_trace()
############################### Total number of vehicles along time ######################

doc14 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\'+method_name[0]+'_simulation'+traffic_demand+'.xml')
GameStepsRoot = doc14.getroot()
doc15 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\'+method_name[1]+'_simulation'+traffic_demand+'.xml')
GameBargainingStepsRoot = doc15.getroot()


MethodsNum = 2
colorstr = ['k','b','g','y','r']
StepNum = len(GameStepsRoot.findall('step'))
VehNumAlongTime = np.zeros((MethodsNum,StepNum))
InsertedAlongTime = np.zeros((MethodsNum,StepNum))
WaitToInsert = np.zeros((MethodsNum,StepNum))
ArrivalsAlongTime = np.zeros((MethodsNum,StepNum))
MeanSpeedAlongTime = np.zeros((MethodsNum,StepNum))
counter = 0
for root in [GameStepsRoot,GameBargainingStepsRoot]:
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
title('The total number of vehicles in the network along time',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Total_vehicle_Number'+traffic_demand+'.pdf', format='pdf', dpi=1000)



fig,ax = subplots(figsize=(15,10))
for i in xrange(MethodsNum):
	ax.plot(InsertedAlongTime[i][:],colorstr[i],linewidth=5)
ax.legend(method_name,prop={'size':25})
ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=25)
plt.tick_params(labelsize = 20)
title('The number of vehicles inserted into the network',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Inserted_VehNum'+traffic_demand+'.pdf', format='pdf', dpi=1000)


fig,ax = subplots(figsize=(15,10))
for i in xrange(MethodsNum):
	ax.plot(ArrivalsAlongTime[i][:],colorstr[i],linewidth=5)
ax.legend(method_name,prop={'size':25})
ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=25)
plt.tick_params(labelsize = 20)
title('The number of vehicles reaching their destination',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Arrival_vehicle_Number'+traffic_demand+'.pdf', format='pdf', dpi=1000)


fig,ax = subplots(figsize=(15,10))
for i in xrange(MethodsNum):
	ax.plot(WaitToInsert[i][:],colorstr[i],linewidth=5)
ax.legend(method_name,prop={'size':25})
ax.set_xlabel('Time(s)',fontsize=25)
ax.set_ylabel('Vehicle Number',fontsize=25)
plt.tick_params(labelsize = 20)
title('The number of vehicles waiting to insert the network',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Wait_to_Insert'+traffic_demand+'.pdf', format='pdf', dpi=1000)


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
title('The mean speed for vehicles along time',fontsize=30)
grid()
fig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fig\\Mean_Speed'+traffic_demand+'.pdf', format='pdf', dpi=1000)



show()


