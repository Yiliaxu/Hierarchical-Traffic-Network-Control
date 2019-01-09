# -*- coding: UTF-8 -*-
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import math
import numpy as np
import random
# from tqdm import tqdm
# from time import time
from scipy.optimize import linprog
# from cvxopt import matrix,solvers
from scipy.sparse import identity
from collections import defaultdict
from Upper_ctrl import Update_policy
from Coefficients import Coefficients
import pickle
import cplex
import pdb
from NetLabels import *

demand_level = 9

SUMO_HOME = "/usr/local/bin/sumo"
tools = "/home/Arain/sumo-git/tools/"
sys.path.append(tools)

sumoBinary = "/usr/local/bin/sumo"

sumoCmd = [sumoBinary, "-c", "chj9.sumocfg","--seed", str(random.randint(1,100))]


# if 'SUMO_HOME' in os.environ:
# 	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
# 	sys.path.append(tools)
# else:
# 	sys.exit("please declare environment variable 'SUMO_HOME'")
# sumoBinary = "E:/software/sumo-win64-0.32.0/sumo-0.32.0/bin/sumo-gui"

# sumoCmd = [sumoBinary, "-c", "chj.sumocfg","--seed", str(random.randint(1,100))]

PORT = 8813
import traci

# doc1 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSAction.xml')
# ActionRoot = doc1.getroot()
# doc2 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
# RouteRoot = doc2.getroot()
# doc3 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops_ctrl.xml')
# LoopsRoot = doc3.getroot()
# doc4 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_ctrl.net.xml')
# NetRoot = doc4.getroot()
# doc5 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSconnections.xml')
# PhaseRoot = doc5.getroot()

doc1 = etree.parse('./TLSAction.xml')
ActionRoot = doc1.getroot()
doc2 = etree.parse('./Chj_final.rou.xml')
RouteRoot = doc2.getroot()
doc3 = etree.parse('./loops_ctrl.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('./Chj_ctrl.net.xml')
NetRoot = doc4.getroot()
doc5 = etree.parse('./TLSconnections.xml')
PhaseRoot = doc5.getroot()

VehNum_files = doc.Document()
VehNum = VehNum_files.createElement('VehicleNumber')
VehNum_files.appendChild(VehNum)

#### parameters
Tsim = 3600
Tc = 60
Tu = 3 ## upper level control cycle
tc = 6 ## lower level control cycle
period = 10 ##seconds
Veh_L = 7



###### all the links in the network--------------- RegionID+EdgeID
AllEdgesList = []
for edge in NetRoot.findall('edge'):
	new_EdgeID = edge.get('Region')+edge.get('id')
	AllEdgesList.append(new_EdgeID)
# print len(AllEdgesList)

######## Edges need to be record for paths
######## EdgesList = {edge_id:{path_id:[np.zeros(Tc)]}}
EdgesList = defaultdict(dict)
EdgesOccupy = defaultdict(lambda:0)
for routes in RouteRoot.findall('routes'):
	for route in routes.findall('route'):
		pathlinks = route.get('edges').split()
		# print pathlinks
		for link in pathlinks:
			EdgesList[link]=defaultdict(dict)
			if link[0:4] == 'Dest':  ### the destination links have infinite occupancy
				EdgesOccupy[link] = 10000
				break
			else:
				for edge in NetRoot.iter('edge'):
					edge_id = edge.get('id')
					if link == edge_id:
						l = 0
						for lane in edge.findall('lane'):
							lanelen = float(lane.get('length'))
							l += 1
						EdgesOccupy[link] = lanelen * l / Veh_L
						break

for routes in RouteRoot.findall('routes'):
	for route in routes.findall('route'):
		route_id = route.get('id')
		pathlinks = route.get('edges').split()
		for link in pathlinks:
			EdgesList[link][route_id]=np.zeros(Tc/period)

#### loops installed in the enterance of the network
LoopsInput = defaultdict(list)
LoopsAmongRegions = defaultdict(list)
LoopsOutput = defaultdict(list)
LoopsOutputNum = defaultdict(lambda:0)
for zone in ['R1','R2','R3']:
	for loop in LoopsRoot:
		loop_id = loop.get('id')
		region_id = loop_id[0:2]
		position = loop.get('position')
		if zone==region_id and position=='BoundaryIn':
			LoopsInput[zone].append(loop_id)
		elif zone==region_id and position=='BoundaryOut':
			LoopsOutput[zone].append(loop_id)
	LoopsOutputNum[zone] = len(LoopsOutput[zone])
for connection in ['R1-R2','R1-R3','R2-R1','R2-R3','R3-R1','R3-R2']:
	for loop in LoopsRoot:
		loop_id = loop.get('id')
		position = loop.get('position')
		if  position==connection:
			LoopsAmongRegions[connection].append(loop_id)


###### PathInput={region_id:{path_id:[input link ids]}}
PathInput = defaultdict(dict)
for zone in ['R1','R2','R3']:
	PathInput[zone]=defaultdict(list)
	y = NetInfoY[zone]
	ylen = len(y)
	for i in range(ylen):
		if i in FirstMovement[zone]:
			pathname = y['y'+str(i)][0]			
			InputLinks = y['y'+str(i)][4].split()
			for link in InputLinks:
				for key in NetLinks[zone].keys():
					if link==key:
						PathInput[zone][pathname]+=NetLinks[zone][key]

##find the number of lanes in input links--- PathInput={region_id:{path_id:[input link id_number of lanes]}}
### PathInputValue = {region_id:{path_id:[the input flow of the first input link np.zeros(Tc/period)]}}
PathInputValue = defaultdict(dict)
for zone in ['R1','R2','R3']:
	PathInputValue[zone]=defaultdict(lambda:np.zeros(Tc/period))
	for path in PathInput[zone].keys():
		links = PathInput[zone][path]
		for i,link in enumerate(links) :
			for edge in NetRoot.findall('edge'):
				edge_id = edge.get('id')
				lanenum = len(edge.findall('lane')) 
				if link == edge_id:
					PathInput[zone][path][i]=PathInput[zone][path][i]+'_'+str(lanenum)


########## calculate the link occupancy for links ##########################

LinksOccupy = defaultdict(dict)
for zone in ['R1','R2','R3']:
	x = NetInfoX[zone]
	y = NetInfoY[zone]
	xoccup = defaultdict(lambda:0)
	for i in range(len(x)):
		path = x[i][0]
		xlabel = x[i][1]
		links = x[i][2]
		lanenum = 0
		for j in range(len(y)):
			uplinks = y['y'+str(j)][4].split()
			if j+1 in FirstMovement[zone] or j==len(y)-1:
				downlinks = y['y'+str(j)][5].split()
			else:
				downlinks = []
			if y['y'+str(j)][0]==path and xlabel in uplinks: ## the last
				for link in links:
					if link[0:4]=='Dest': ### the destination links have infinite occupancy
						xoccup[i]=10000
						break
					else:
						for edge in NetRoot.iter('edge'):
							edge_id = edge.get('id')
							if link==edge_id:
								l = 0
								for lane in edge.findall('lane'):
									lanelen = float(lane.get('length'))
									l+=1
								xoccup[i]+=lanelen*l/Veh_L
								break


			elif y['y'+str(j)][0]==path and xlabel in downlinks:
				for link in links:
					if link[0:4]=='Dest':
						xoccup[i]=10000
						break
					else:
						for edge in NetRoot.iter('edge'):
							edge_id = edge.get('id')
							if link==edge_id:
								l = 0
								for lane in edge.findall('lane'):
									lanelen = float(lane.get('length'))
									l+=1
								xoccup[i]+=lanelen*l/Veh_L
								break
	LinksOccupy[zone]=xoccup




##############################################################################################################
if __name__ == '__main__':	

	traci.start(sumoCmd)	

    ### initialize the signal settings for all controlled intersections 
	ActionInfo=defaultdict(lambda:0)
	PhaseTime=defaultdict(dict)
	for intersection in ActionRoot.findall('Intersection'):
		intersection_id = intersection.get('id')
		PhaseNum = int(intersection.get('PhaseNum'))
		if PhaseNum==2:
			PhaseTime[intersection_id][1]= np.hstack((np.ones(Tc/2),np.zeros(Tc/2)))
			PhaseTime[intersection_id][2]= np.hstack((np.zeros(Tc/2),np.ones(Tc/2)))
		elif PhaseNum==3:
			PhaseTime[intersection_id][1]= np.hstack((np.ones(Tc/3),np.zeros(2*Tc/3)))
			PhaseTime[intersection_id][2]= np.hstack((np.zeros(Tc/3),np.ones(Tc/3),np.zeros(Tc/3)))
			PhaseTime[intersection_id][3]= np.hstack((np.zeros(2*Tc/3),np.ones(Tc/3)))
		elif PhaseNum==4:
			PhaseTime[intersection_id][1]= np.hstack((np.ones(Tc/4),np.zeros(3*Tc/4)))
			PhaseTime[intersection_id][2]= np.hstack((np.zeros(Tc/4),np.ones(Tc/4),np.zeros(Tc/2)))
			PhaseTime[intersection_id][3]= np.hstack((np.zeros(Tc/2),np.ones(Tc/4),np.zeros(Tc/4)))
			PhaseTime[intersection_id][4]= np.hstack((np.zeros(3*Tc/4),np.ones(Tc/4)))
		#np.ones(PhaseNum)*int(Tc/PhaseNum) #get_random_phasetime(PhaseNum,Tc) 
		PhaseAction = []
		for i in xrange(PhaseNum):
			PhaseAction.append(intersection.get('phase'+str(i+1)))
		ActionInfo[intersection_id]=PhaseAction
	# print PhaseTime

	
	VehNumEdge = defaultdict(lambda:0) ### record

	VehNumRegion = defaultdict(lambda:np.zeros(Tc))
	### policy update cycle Tu  
	VehNumLoop = defaultdict(lambda:np.zeros(Tu))
	VehNumLoopsAmongRegions = defaultdict(lambda:np.zeros(Tu))

	Counter = 0

	zone = ['R1','R2','R3']
	warm_up = Tc*Tu*3


	############################################################################################################
	############################ simulation start ###########################################
	for i in range(Tsim):

		traci.simulationStep()

		for edge in AllEdgesList:  ###record
			edge_id = edge[2:]
			VehNumEdge[edge]+= traci.edge.getLastStepVehicleNumber(edge_id)
			# OccupyEdge[edge]+= traci.edge.getLastStepOccupancy(edge_id)

		if i>warm_up: ### warm-up the network
		

			####################################################################################
			##################### collect the regional-based info. for upper level optimization
			j = i%Tc-1
			if j<0:
				j=59
			for zone in ['R1','R2','R3']:
				VehNumRegion[zone][j] = 0
			for edge in AllEdgesList:
				edge_id = edge[2:]
				region_id = edge[0:2]
				temp = traci.edge.getLastStepVehicleNumber(edge_id)
				VehNumRegion[region_id][j]+=temp
				 


			j = i%(Tu*Tc)-1
			if j<0:
				j=Tu*Tc-1

			for k in range(Tu):
				if j==k*Tc:
					VehNumLoop[loop][k] = 0
					VehNumLoopsAmongRegions[connection][k] = 0
				if j>=k*Tc and j<(k+1)*Tc:
					for zone in ['R1', 'R2', 'R3']:
						for loop in LoopsInput[zone]:
							if traci.inductionloop.getLastStepMeanSpeed(loop) < 0.1:
								vehnum = 0
							else:
								vehnum = traci.inductionloop.getLastStepVehicleNumber(loop)
							VehNumLoop[loop][k] += vehnum
						for connection in ['R1-R2', 'R1-R3', 'R2-R1', 'R2-R3', 'R3-R1', 'R3-R2']:
							for l, loop in enumerate(LoopsAmongRegions[connection]):
								if traci.inductionloop.getLastStepMeanSpeed(loop) < 0.1:
									vehnum = 0
								else:
									vehnum = traci.inductionloop.getLastStepVehicleNumber(loop)
								VehNumLoopsAmongRegions[connection][k] += vehnum



			######################################################################################
			################ get the number of vehicles on each path for lower level optimization
			
			if i%period==0 and i>0:
				j = i%Tc
				j = j/10-1
				if j<0:
					j=5
				# print i,j
				for edge in EdgesList.keys():
					for path in EdgesList[edge].keys():
						EdgesList[edge][path][j]=0

				##### EdgesList = {edge_id:{path_id:[np.zeros(Tc/period)]}}
				vehID = traci.vehicle.getIDList()
				for id in vehID:
					veh_route_id = traci.vehicle.getRouteID(id)
					veh_route_id = veh_route_id.split('_')[0]
					veh_edge_id = traci.vehicle.getRoadID(id)
					for edge in EdgesList.keys():
						for path in EdgesList[edge].keys():
							if veh_route_id==path and veh_edge_id==edge:
								EdgesList[edge][path][j]+=1
								break

			######## get the number of vehicles
			#### PathInput={region_id:{path_id:[input link id _number of lanes,  ,  ]}}
			### PathInputValue = {region_id:{path_id:[the input flow of the first input link np.zeros(Tc/period)]}}
			#### for lower control per period (10seconds)
			j = i % Tc - 1
			if j < 0:
				j = Tc-1

			for k in range(Tc/period):
				if j == k*period:
					for zone in PathInput.keys():
						for path in PathInput[zone].keys():
							PathInputValue[zone][path][k] = 0
				elif j>=k*period and j<(k+1)*period:
					for zone in PathInput.keys():
						for path in PathInput[zone].keys():
							link = PathInput[zone][path][0]
							link_id = link.split('_')[0]
							lanenum = int(link.split('_')[1])
							for l in range(lanenum):
								loop_id = zone + link_id + '_' + str(l)
								if traci.inductionloop.getLastStepMeanSpeed(loop_id)<0.1:
									vehnum = 0
								else:
									vehnum = traci.inductionloop.getLastStepVehicleNumber(loop_id)

								PathInputValue[zone][path][k] += vehnum

			#################################################################################
			################# update the upper level policy every Tu cycles #################
			if i%(Tc*Tu)==0 and i>0:
				zone = ['R1','R2','R3']

				### calculate the number of movements between regions
				### set the maximum and minimum numbre of vehicles among regions
				# SaturationFlow = 0.8 #veh/s
				ActionRange = np.zeros((6,2))
				linktype = ['R1-R2','R1-R3','R2-R1','R2-R3','R3-R1','R3-R2']
				loopsnum = defaultdict(lambda:0)
				for j in xrange(len(linktype)):
					loopsnum[j] = len(LoopsAmongRegions[linktype[j]])
					for connection in PhaseRoot.iter('connection'):
						between=connection.get('between')
						if between==linktype[j]:
							ActionRange[j,1]+=1
				ActionRange[1,1]=ActionRange[1,1]-1  ## R1-R3
				ActionRange[2,1]=ActionRange[2,1]-1  ## R2-R1
				####  using the saturation traffic flow
				#ActionRange[:,1] = ActionRange[:,1]*SaturationFlow*Tc
				
				## use the average output of previous signal cycles
				for j in xrange(len(linktype)):
					ActionRange[j,1] = ActionRange[j,1]*np.mean(VehNumLoopsAmongRegions[linktype[j]])/loopsnum[j]


				### the average number of vehicles in regions 
				N_current=np.zeros(3)
				for j in range(3):
					N_current[j] = np.mean(VehNumRegion[zone[j]])

				### the average traffic demand for regions 
				D_current=np.zeros(3)
				for j in xrange(3):
					for loop in LoopsInput[zone[j]]:
						D_current[j]+=np.mean(VehNumLoop[loop])
				
				upper_controller = Update_policy(Tc,Tu,ActionRange,N_current,D_current,LoopsOutputNum)
				State, ActionSpace, Opt_policy, action_interval = upper_controller.STPM_network()


			#################################################################################
			################# the lower level control every one cycles #################
			if i%(tc*period)==0 and i>=Tu*Tc+warm_up:

				## determine current network state and action to take
				VehNumZone = defaultdict(lambda:0)
				for zone in ['R1','R2','R3']:
					VehNumZone[zone] = np.mean(VehNumRegion[zone])
				s = -1*np.ones(3)
				zone = ['R1', 'R2', 'R3']
				for k in xrange(3): #zone
					for j in xrange(3): # judge state
						if VehNumZone[zone[k]]>=State[zone[k]][j] and VehNumZone[zone[k]]<State[zone[k]][j+1]:
							s[k]=j
							break
					if s[k]==-1:
						s[k]=2
				State_current = np.dot(s,np.array([9,3,1]))
				ActionLabel = Opt_policy[int(State_current)]
				Action_current = ActionSpace[int(ActionLabel)]

				#############################################################################################################################################
				##################################################   optimize the signal settings   #########################################################
				
				ObjWeight={'R1':100,'R2':100,'R3':100}
				PathWeights = defaultdict(dict)
				PathWeights['R1']={
				's2-n7':1,
				's4-n5':1,
				's5-e6':1,
				's6-w5':1,
				's7-n4':1,
				'n1-s6':1,
				'n3-s7':1,
				'n5-w3':1,
				'n7-s3':1,
				'n6-e5':1,
				'w7-s2':1,
				'w2-n6':1,
				'e3-n3':1,
				'e1-w5':1,
				'n4-w2':1,
				'w9-n3':1,
				'w9-n1':1,
				'w7-s7':1,
				'w5-w9':1}
				
				PathWeights['R2']={
				"w3-e3":1,
				"s5-e6":1,
				"n1-s6":1,
				"n2-s8":1,
				"w8-e4":1,
				"e4-w8":1,
				"n6-e5":1,
				"e3-n3":1,
				"e1-w5":1,
				"e5-e1":1,
				"e3-s5":1,
				"w9-n1":1
				}
				PathWeights['R3']={
				"w4-s1":1,
				"w3-e3":1,
				"s2-n7":1,
				"s4-n5":1,
				"s5-e6":1,
				"s6-w5":1,
				"s7-n4":1,
				"n1-s6":1,
				"n3-s7":1,
				"n5-w3":1,
				"n7-s3":1,
				"w8-e4":1,
				"e4-w8":1,
				"w7-s2":1,
				"w2-n6":1,
				"s1-w4":1,
				"e3-s5":1,
				"n4-w2":1,
				"w7-s7":1}


				for zone in ['R1','R2','R3']:

					### calculate the initial number of vehicles in  links on paths
					InitVehNum_x = defaultdict(lambda:0)
					x = NetInfoX[zone]
					for j in range(len(x)):
						path_id = x[j][0]
						links = x[j][2]
						##### EdgesList = {edge_id:{path_id:[np.zeros(Tc/period)]}}
						for link in links:
							# print link,path_id
							# InitVehNum_x[j]+=np.mean(EdgesList[link][path_id])
							InitVehNum_x[j] += EdgesList[link][path_id][-1]
						if InitVehNum_x[j]>LinksOccupy[zone][j]:
							print 'overflow'
							InitVehNum_x[j] = LinksOccupy[zone][j]
					
					### find the number of lanes in input links--- PathInput={region_id:{path_id:[input link id_number of lanes]}}
					### PathInputValue = {region_id:{path_id:[the input flow of the first input link np.zeros(Tc/period)]}}
					##0: the input number of vehicles through the first link (estimated demand)
					##1: the total number of vehicles in all the links (initial value)
					InputLinksValue = defaultdict(lambda:np.zeros(2))
					for path in PathInput[zone].keys():
						InputLinksValue[path][0]=np.mean(PathInputValue[zone][path])
						links = PathInput[zone][path]
						for link in links:
							link_id = link.split('_')[0]
							# InputLinksValue[path][1]+=np.mean(EdgesList[link_id][path])
							InputLinksValue[path][1] += EdgesList[link_id][path][-1]
							## judge whether overflow
							totalvehnum=0
							for temp_path in EdgesList[link_id].keys():
								totalvehnum+= EdgesList[link_id][temp_path][-1]
							if totalvehnum>EdgesOccupy[link_id]:
								print 'overflow'

					OptCoeff = Coefficients(zone,tc,period,PathWeights,InputLinksValue,ObjWeight[zone],InitVehNum_x,LinksOccupy[zone],Action_current,action_interval)
					x_Eq,y_Eq,s_Eq,e_Eq,v_Eq,b_Eq,row_Eq = OptCoeff.EqCoeff()
					x_Ineq,y_Ineq,s_Ineq,e_Ineq,v_Ineq,b_Ineq,slack_Ineq,row_Ineq = OptCoeff.IneqCoeff()
					x_obj,y_obj,s_obj,e_obj,v_obj,slack_obj = OptCoeff.ObjCoeff()
					Aeq = np.hstack((x_Eq,y_Eq,s_Eq,e_Eq,v_Eq))
					Aineq = np.hstack((x_Ineq,y_Ineq,s_Ineq,e_Ineq,v_Ineq,slack_Ineq))

					OptimizeProblem = cplex.Cplex()

					## set the decision varibales, lower band upper bounds, and the objective coefficiences
					xlen = len(NetInfoX[zone])
					upbounds = np.zeros(xlen*tc)
					for j in range(xlen):
						upbounds[j*tc:(j+1)*tc]=LinksOccupy[zone][j]*np.ones(tc)
					OptimizeProblem.variables.add(names = ["x"+str(j) for j in range(xlen*tc)], obj = x_obj,
												lb = np.zeros(xlen*tc), ub=upbounds,
						                          types = [OptimizeProblem.variables.type.continuous]*xlen*tc)
					ylen = len(NetInfoY[zone])
					OptimizeProblem.variables.add(names = ["y"+str(j) for j in range(ylen*tc)], obj = y_obj, lb = np.zeros(ylen*tc),
						                          types = [OptimizeProblem.variables.type.continuous]*ylen*tc)
					slen = len(NetInfoS[zone])
					OptimizeProblem.variables.add(names = ["s"+str(j) for j in range(slen*tc)], obj = s_obj,
					                              types = [OptimizeProblem.variables.type.binary]*slen*tc)
					OptimizeProblem.variables.add(names = ["e"+str(j) for j in range(slen*(tc-1))], obj = e_obj,
												  types = [OptimizeProblem.variables.type.continuous]*slen*(tc-1))
					OptimizeProblem.variables.add(names= ["v"+str(j) for j in range(slen*(tc-1))], obj = v_obj,
												  types = [OptimizeProblem.variables.type.continuous]*slen*(tc-1))
					OptimizeProblem.variables.add(names=["slack" + str(j) for j in range(2)], obj=slack_obj, lb = np.zeros(2),
												  types=[OptimizeProblem.variables.type.continuous]*2)

					Variables_Num = OptimizeProblem.variables.get_num()
					Variables_Name = OptimizeProblem.variables.get_names()

					############# add equition constraints
					for j in range(row_Eq):
						OptimizeProblem.linear_constraints.add(lin_expr= [cplex.SparsePair(ind= [var for var in Variables_Name[0:-2]],
							val= Aeq[j,:])],rhs= [b_Eq[j]], senses = ['E'],names = ['Eq'+str(j)])

					############# add inequition constraints
					for j in range(row_Ineq):
						OptimizeProblem.linear_constraints.add(lin_expr= [cplex.SparsePair(ind= [var for var in Variables_Name],
							val= Aineq[j,:])],rhs= [b_Ineq[j]], senses = ['L'],names = ['Ineq'+str(j)])
					
					# Solve the model and print the answer
					OptimizeProblem.objective.set_sense(OptimizeProblem.objective.sense.maximize)
					OptimizeProblem.solve()
					Results = OptimizeProblem.solution.get_values()
					Xvalues = Results[0:xlen*tc]
					Yvalues = Results[xlen*tc:(xlen+ylen)*tc]
					Svalues = Results[(xlen+ylen)*tc:(xlen+ylen+slen)*tc]
					Evalues = Results[(xlen+ylen+slen)*tc:(xlen+ylen+slen)*tc+slen*(tc-1)]
					Vvalues = Results[(xlen+ylen+slen)*tc+slen*(tc-1):(xlen+ylen+slen)*tc+2*slen*(tc-1)]
					SlackValues = Results[-2:]

					NewPhaseTime = Results[(xlen+ylen)*tc:(xlen+ylen+slen)*tc]
					## update the signal settings
					for k in range(slen):
						junction_id = NetInfoS[zone]['s'+str(k)][:-2]
						phasesequence = int(NetInfoS[zone]['s'+str(k)][-1])
						for j in range(tc):
							PhaseTime[junction_id][phasesequence][j*period:(j+1)*period]=NewPhaseTime[k*tc+j]*np.ones(period)



		############################################################################################################################
		####################################-------------Implement the signal setting--------------###################################
		if Counter==Tc:			
			Counter = 0	
			#### record the vehnum on each pahse every 60 seconds
			period0 = i/Tc
			for edge in AllEdgesList:
				interval = VehNum_files.createElement('interval')
				interval.setAttribute('begin',str(period0*Tc))
				interval.setAttribute('end',str((period0+1)*Tc))
				interval.setAttribute('id',edge) 
				interval.setAttribute('vehnum',str(VehNumEdge[edge]/Tc))
				# interval.setAttribute('Occupy',str(OccupyEdge[edge]/Tc))
				VehNum.appendChild(interval)
			VehNumEdge = defaultdict(lambda:0)
			# OccupyEdge = defaultdict(lambda:0)

		for id in PhaseTime.keys(): ##PhaseTime={intersection_id:{phasesequence:[0 0 0 1 1 0 0]}}
			PhaseNum = len(PhaseTime[id])
			for phase in PhaseTime[id].keys():
				# print Counter
				if PhaseTime[id][phase][Counter]==1:
					traci.trafficlights.setRedYellowGreenState(id,ActionInfo[id][phase-1])
					break

		Counter = Counter + 1
				

	fp = open('./VehNum'+str(demand_level)+'.xml','w')
	
	try:
		VehNum_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
	except:
		trackback.print_exc() 
	finally: 
		fp.close() 

	traci.close()