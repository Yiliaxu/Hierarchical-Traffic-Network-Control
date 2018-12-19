from Upper_ctrl import Update_policy
import numpy as np
from scipy.stats import norm 
from scipy.stats import poisson
import matplotlib.pyplot as plt
from collections import defaultdict
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc


# T = 60
# Tu = 3

# Action= np.zeros((6,2))
# Action[0,:]=np.array([0,20]) ##R1-R2
# Action[1,:]=np.array([0,18]) ##R1-R3
# Action[2,:]=np.array([0,30]) #R2-R1
# Action[3,:]=np.array([0,29]) #R2-R3
# Action[4,:]=np.array([0,30]) #R3-R1
# Action[5,:]=np.array([0,27]) #R3-R2

# N_current=[723,945,501]
# D_current=np.array([10,15,12])
# State=np.zeros((3,2))
# State[0,:]=np.array([603,884])
# State[1,:]=np.array([835,1109])
# State[2,:]=np.array([367,692])
# upper_controller = Update_policy(T,Tu,State, Action, N_current, D_current)
# upper_controller.STPM_network()


# fig, ax = plt.subplots(1, 1)
# x = np.arange(poisson.ppf(0.001,100,loc=0),poisson.ppf(0.999, 100,loc=0))
# ax.plot(x, poisson.pmf(x, 100), 'bo', ms=8, label='poisson pmf')


# fig, ax = plt.subplots(1, 1)
# print norm.ppf(0.001,20,10),norm.ppf(0.999,20,10)
# x = np.linspace(norm.ppf(0.001,20,10),norm.ppf(0.999,20,10), 100)
# ax.plot(x, norm.pdf(x,20,10),'r-', lw=5, alpha=0.6, label='norm pdf')
# plt.show()


# QGaussian_mean=20
# QGaussian_std = 10
# Min_G = int(norm.ppf(0.001,QGaussian_mean,QGaussian_std))
# Max_G = int(norm.ppf(0.999,QGaussian_mean,QGaussian_std))
# print Min_G,Max_G
# Qout=defaultdict(lambda:0)
# x= range(Min_G,Max_G)
# y = np.zeros(len(x))
# for k in xrange(len(x)):
# 	i = x[k]
# 	# print norm.pdf(i+1,QGaussian_mean,QGaussian_std),norm.pdf(i,QGaussian_mean,QGaussian_std)
# 	Qout[x[k]]=norm.cdf(i+1,QGaussian_mean,QGaussian_std)-norm.cdf(i,QGaussian_mean,QGaussian_std)
# 	y[k] = Qout[x[k]]

# maxkey = max(Qout,key=Qout.get)
# print Qout[maxkey]
# Qout[maxkey] = Qout[maxkey]+1.0-np.sum(Qout.values())
# print Qout[maxkey]
# print np.sum(Qout.values())
# # print len(Qout.values())
# # fig,ax = plt.subplots()
# # ax.plot(range(Min_G,Max_G),Qout.values())
# fig,ax = plt.subplots()
# ax.plot(x,y)
# plt.show

# Min_P = int(poisson.ppf(0.0001, 20))
# Max_P = int(poisson.ppf(0.9999, 20))

# Qin=defaultdict(lambda:0)		
# for i in range(Min_P,Max_P):		
# 	Qin[i]=poisson.pmf(i,20)
# maxkey = max(Qin,key=Qin.get)		
# Qin[maxkey] = Qin[maxkey]+1.0-np.sum(Qin.values())
# print np.sum(Qin.values())
# fig,ax = plt.subplots()
# ax.plot(range(Min_P,Max_P),Qin.values())
# plt.show()

doc1 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSAction.xml')
ActionRoot = doc1.getroot()
doc2 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
RouteRoot = doc2.getroot()
doc3 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops_ctrl.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_ctrl.net.xml')
NetRoot = doc4.getroot()

#### get the interregional links and the boundary links of each region
Interaction = ['R1_IN','R1_OUT','R1-R2','R1-R3','R2_IN','R2_OUT','R2-R1','R2-R3','R3_IN','R3_OUT','R3-R1','R3-R2']
Interaction_edges = defaultdict(list)
for edge in NetRoot.findall('edge'):
	edge_id = edge.get('id')
	region_id = edge.get('Region')
	between= edge.get('between')
	lanes = edge.findall('lane')
	edgeinfo = str(len(lanes))+edge_id ### the number of lanes + the edge id

	for region in ['R1','R2','R3']:
		if edge_id[0:7]=='Origion' and region_id==region:
			Interaction_edges[region+'_IN'].append(edgeinfo)
		if edge_id[0:11]=="Destination" and region_id==region:
			Interaction_edges[region+'_OUT'].append(edgeinfo)
		if between!=None and region_id==region:
			Interaction_edges[between].append(edgeinfo)

print Interaction_edges