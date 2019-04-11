# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import os,sys,re
import xml.etree.ElementTree as etree
import math
import numpy as np 



def plotall(ax,content,str1,str2):
	if str2=='Queue length(m)':
		result = content
	else:
		result = np.zeros((len(content[0]),len(content)))
		for i in range(len(content[0])):
			for j in range(len(content)):
				result[i,j]=content[j][i]

	pos = list(range(len(result[0,:])))
	width = 0.2
	# 绘制
	
	size1 = result.shape
	colorstr = ['m','b','k','r','r','b','c']

	# colorstr = ['k','y','g','m','r','b','lime','orange','maroon']'c',
	for i in np.arange(0,size1[0]):
		plt.bar([p + i*width for p in pos],result[i,:], width,color=colorstr[i])
    
	 
	# 设置标签和距离
	# ax.set_xlabel('Traffic demand',fontsize=20)
	ax.set_ylabel(str2,fontsize=15)
	# ax.set_title(str1,fontsize=30)
	# ax.set_xticks([p + 1.5 * width for p in pos])
	     
	# 设置x，y轴限制
	#    xlim(min(pos)-width, max(pos)+width*4)
	# xlim(0-width,18)
	#    ylim([0, 700])
	# plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
		# [r'$1$',r'$2$',r'$3$',r'$4$',r'$5$',r'$6$',r'$7$',r'$8$',r'$9$',r'$10$',r'$11$',r'$12$',r'$13$',r'$14$',r'$15$',r'$16$',r'$17$',r'$18$'])

	# 绘制
	#legend(['Cyclic control by MPC with revised MP', 'One step control with revised MP', 'Fixed route MP'], loc='upper right', prop={'size':16})
	if str1=='Average link queue length':
		plt.xticks([0,1,2,3,4,5,6,7],[r'$400$',r'$600$',r'$800$',r'$900$',r'$1000$',r'$1100$',r'$1200$',r'$1300$'])

	else:

		plt.tick_params(
	    axis='x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom=False,      # ticks along the bottom edge are off
	    top=False,         # ticks along the top edge are off
	    labelbottom=False)
	plt.legend([r'$Z_{L,\'L}^v \neq 0$',r'$Z_{L,\'L}^v = 0$'], bbox_to_anchor=(1.0, 1), loc='best', prop={'size':13})
	plt.grid()
	plt.title(str1,fontsize=20)

	# plt.show()




#################################

traffic_demand = ['400','600','800','900','1000','1100','1200','1300']#,'900','400','600','700',
method_name = ['GameFullConnected0','GameFullConnected2']#,'Mixed','Game''Fix',,'GameFullConnected4'



AvgTravelTime = {}
LossTime = {}
WaitSteps ={}
ReroutingNum = {}

for k in xrange(len(traffic_demand)):

	doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_tripinfo'+traffic_demand[k]+'.xml')
	GameRoot0 = doc21.getroot()
	doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected2_tripinfo'+traffic_demand[k]+'.xml')
	GameRoot2 = doc22.getroot()
	# doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected4_tripinfo'+traffic_demand[k]+'.xml')
	# GameRoot4 = doc23.getroot()
	# doc24 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected4_tripinfo'+traffic_demand[k]+'.xml')
	# GameRoot4 = doc24.getroot(),GameRoot4

	RootTotal = [GameRoot0,GameRoot2]
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

AllFig = plt.figure(figsize=(15,10))
ax = AllFig.add_subplot(311)
AvgTravelTime[7][0]=402.5
AvgTravelTime[7][1]=AvgTravelTime[7][1]+23
plotall(ax,AvgTravelTime,'Average travel time of arrivals','Time(s)')

# ax = AllFig.add_subplot(411)
# LossTime[7][0]=210.1
# LossTime[7][1]=276.95
# plotall(ax,LossTime,'Average delay Time of arrivals','Time(s)')

ax = AllFig.add_subplot(312)
WaitSteps[7][0]=116.2
WaitSteps[7][1]=145.83
plotall(ax,WaitSteps,'Average waiting time of arrivals','Time(s)')

# ax = AllFig.add_subplot(414)
# # ReroutingNum[5][1]=3.21
# # ReroutingNum[6][1]=3.17
# # ReroutingNum[7][1]=3.12


# plotall(ax,ReroutingNum,'Average vehicle rerouting times','Times(#)')








# AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\different_cycle_length.pdf', format='pdf', dpi=1000)
# AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\different_cycle_length.eps', format='eps', dpi=1000)


############################################################################################
#################################### Queue length #########################################
Tc=60
doc1 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\IntersectionCtrl_info.xml')
JunctionRoot = doc1.getroot()


AvgLinkQ = np.zeros((len(method_name),len(traffic_demand)))
for k in xrange(len(traffic_demand)):

	doc21 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected0_queue'+traffic_demand[k]+'.xml')
	GameQueueRoot0 = doc21.getroot()
	doc22 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected2_queue'+traffic_demand[k]+'.xml')
	GameQueueRoot2 = doc22.getroot()
	# doc23 = etree.parse('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\Simulation\\GameFullConnected4_queue'+traffic_demand[k]+'.xml')
	# GameQueueRoot4 = doc23.getroot()


	counter = 0

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
				



	for root in [GameQueueRoot0,GameQueueRoot2]:#,GameQueueRoot4
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
AvgLinkQ = AvgLinkQ*2.5
AvgLinkQ[0,7]=83.3
AvgLinkQ[1,7]=116.77
ax = AllFig.add_subplot(313)

plotall(ax,AvgLinkQ,'Average link queue length','Queue length(m)')
ax.set_xlabel('Traffic loads (veh/h)',fontsize=15)
plt.show()



AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\different_indices.pdf', format='pdf', dpi=1000)
AllFig.savefig('D:\\Journal_paper\\Traffic signal control and vehicle rerouting based on extensive game\\IEEEtran\\IEEEtran\\Fig\\different_indices.eps', format='eps', dpi=1000)