# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import os,sys,re
import xml.etree.ElementTree as etree
import math
import numpy as np 



def plotall(content,str1,str2):
	result = np.zeros((len(content[0]),len(content)))
	for i in range(len(content[0])):
		for j in range(len(content)):
			result[i,j]=content[j][i]

	pos = list(range(len(result[0,:])))
	width = 0.2
	# 绘制
	fig, ax = plt.subplots(figsize=(20,10))
	size1 = result.shape
	colorstr = ['k','b','r','m','r','b','c']

	# colorstr = ['k','y','g','m','r','b','lime','orange','maroon']'c',
	for i in np.arange(0,size1[0]):
		plt.bar([p + i*width for p in pos],result[i,:], width,color=colorstr[i])
    
	 
	# 设置标签和距离
	ax.set_xlabel('Traffic demand',fontsize=20)
	ax.set_ylabel(str2,fontsize=20)
	ax.set_title(str1,fontsize=20)
	ax.set_xticks([p + 1.5 * width for p in pos])
	     
	# 设置x，y轴限制
	#    xlim(min(pos)-width, max(pos)+width*4)
	# xlim(0-width,18)
	#    ylim([0, 700])
	# plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
		# [r'$1$',r'$2$',r'$3$',r'$4$',r'$5$',r'$6$',r'$7$',r'$8$',r'$9$',r'$10$',r'$11$',r'$12$',r'$13$',r'$14$',r'$15$',r'$16$',r'$17$',r'$18$'])

	# 绘制
	#legend(['Cyclic control by MPC with revised MP', 'One step control with revised MP', 'Fixed route MP'], loc='upper right', prop={'size':16})
	plt.legend(['FT','BPR','GR'], bbox_to_anchor=(1.0, 1), loc='upper left', prop={'size':16})
	plt.grid()
	# plt.show()
	fig.savefig(str1,format='eps',dpi=1000)



#################################

traffic_demand = ['400','600','800','900','1000','1100','1200','1300']#,'900','400','600','700',
method_name = ['Fix','BPR','GameFullConnected']#,'Mixed','Game''Fix',



AvgTravelTime = {}
LossTime = {}
WaitSteps ={}
ReroutingNum = {}

for k in xrange(len(traffic_demand)):

	doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\Fix0_tripinfo'+traffic_demand[k]+'.xml')
	FixTripRoot = doc21.getroot()
	doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\BPR_tripinfo'+traffic_demand[k]+'.xml')
	BPRTripRoot = doc22.getroot()
	# if traffic_demand[k] in ['600','800','900','1000']:
	# 	doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected1_tripinfo'+traffic_demand[k]+'.xml')
	# else:
	doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_tripinfo'+traffic_demand[k]+'.xml')


	GameTripRoot = doc23.getroot()

	RootTotal = [FixTripRoot,BPRTripRoot,GameTripRoot]
	MethodsNum = len(RootTotal)
	AvgTravelTime[k] = []
	LossTime[k] = []
	WaitSteps[k] = []
	ReroutingNum[k] = []

	for j in xrange(MethodsNum):
		tripinfos  = RootTotal[j].findall('tripinfo')		
		TravelTime=[]
		lossT = []
		waitT =[]
		rerouting = []

		for tripinfo in tripinfos:

		
			TravelTime.append(float(tripinfo.get('duration')))

			lossT.append(float(tripinfo.get('timeLoss')))

			waitT.append(float(tripinfo.get('waitSteps')))
			RouteNum = float(tripinfo.get('rerouteNo'))
			if RouteNum>8:
				RouteNum=0
			rerouting.append(RouteNum)

		AvgTravelTime[k].append(np.mean(TravelTime))
		LossTime[k].append(np.mean(lossT)) 
		WaitSteps[k].append(np.mean(waitT))
		ReroutingNum[k].append(np.mean(rerouting))

plotall(AvgTravelTime,'Average travel time of arrivals','Travel time')
plotall(LossTime,'Loss Time of arrivals','Travel time')
plotall(WaitSteps,'Waiting time of arrivals','Travel time')
plotall(ReroutingNum,'Rerouting number of arrivals','Travel time')
plt.show()



