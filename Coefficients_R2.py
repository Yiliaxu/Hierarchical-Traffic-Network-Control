import numpy as np
from collections import defaultdict

period = 10 ##seconds

x_R2={
0: ['w3-e3', 'x0', ['69555386#0']], 
1: ['w3-e3', 'x1', ['69555386#1', '69555386#2']], 
2: ['w3-e3', 'x2', ['DestinationE3']], 
3: ['s5-e6', 'x3', ['135626792#6']], 
4: ['s5-e6', 'x4', ['492979895#0', '492979895#1']], 
5: ['s5-e6', 'x5', ['492979895#2', '72084621', '72084599#0']], 
6: ['s5-e6', 'x6', ['412826784#1', '412826784#2DestinationE6']], 
7: ['n1-s6', 'x7', ['OrigionN1']], 
8: ['n1-s6', 'x8', ['-72084599#0', '-72084621', '-492979895#2']], 
9: ['n1-s6', 'x9', ['-492979895#1', '-492979895#0']], 
10: ['n1-s6', 'R2_R1_1', ['-135626792#6']], 
11: ['n2-s8', 'x10', ['OrigionN2']], 
12: ['n2-s8', 'x8', ['-72084599#0', '-72084621', '-492979895#2']], 
13: ['n2-s8', 'x9', ['-492979895#1', '-492979895#0']], 
14: ['n2-s8', 'x11', ['492979892']], 
15: ['n2-s8', 'x12', ['492979887#0']], 
16: ['n2-s8', 'x13', ['492979887#1', '492979887#2', '492979887#3', '230493751', '230493750#0', '230493750#1', '93864593#0', '93864593#1', 'DestinationS8']], 
17: ['w8-e4', 'x14', ['492979896#2']], 
18: ['w8-e4', 'x15', ['-230239443#2', '-230239443#1']], 
19: ['w8-e4', 'x16', ['-230239443#0', '-230239442', '-448953275#1', 'DestinationE4']], 
20: ['e4-w8', 'x17', ['OrigionE4', '448953275#1', '230239442', '230239443#0']], 
21: ['e4-w8', 'x18', ['230239443#1', '230239443#2']], 
22: ['e4-w8', 'R2_R3_1', ['-492979896#2']], 
23: ['n6-e5', 'x19', ['38869999#3']], 
24: ['n6-e5', 'x20', ['38869999#4']], 
25: ['n6-e5', 'x21', ['38869048#0', '24626397', '230239444', '230239445#0', 'DestinationE5']], 
26: ['e3-n3', 'x22', ['OrigionE3']], 
27: ['e3-n3', 'x23', ['-38869048#2']], 
28: ['e3-n3', 'x24', ['-38869048#1', '-38869048#0']], 
29: ['e3-n3', 'x25', ['-38869999#4']], 
30: ['e3-n3', 'R2_R1_2', ['-38869999#3']], 
31: ['e1-w5', 'x26', ['OrigionE1']], 
32: ['e1-w5', 'x27', ['-230493745#2', '-230493745#1', '-230493750#0', '-230493751', '-492979887#3', '-492979887#2', '-492979887#1']], 
33: ['e1-w5', 'x28', ['-492979887#0']], 
34: ['e1-w5', 'x29', ['-492979892']], 
35: ['e1-w5', 'x30', ['-38867851']], 
36: ['e1-w5', 'R2_R1_2', ['-38869999#3']], 
37: ['e5-e1', 'x31', ['OrigionE5', '-230239445#0', '-230239444', '-24626397', '38869048#1']], 
38: ['e5-e1', 'x32', ['38869048#2']], 
39: ['e5-e1', 'x33', ['38869048#3', '38869048#4', '230493753', '230493752#0']], 
40: ['e5-e1', 'x34', ['DestinationE1']], 
41: ['e3-s5', 'x22', ['OrigionE3']], 
42: ['e3-s5', 'x35', ['-69555386#2', '-69555386#1']], 
43: ['e3-s5', 'R2_R3_2', ['-69555386#0']], 
44: ['w9-n1', 'x3', ['135626792#6']], 
45: ['w9-n1', 'x4', ['492979895#0', '492979895#1']], 
46: ['w9-n1', 'x5', ['492979895#2', '72084621', '72084599#0']], 
47: ['w9-n1', 'x36', ['DestinationN1']]}

States_R2={
'x0': ['69555386#0'], 
'x1': ['69555386#1', '69555386#2'], 
'x2': ['DestinationE3'], 
'x3': ['135626792#6'], 
'x4': ['492979895#0', '492979895#1'], 
'x5': ['492979895#2', '72084621', '72084599#0'], 
'x6': ['412826784#1', '412826784#2' 'DestinationE6'], 
'x7': ['OrigionN1'], 
'x8': ['-72084599#0', '-72084621', '-492979895#2'], 
'x9': ['-492979895#1', '-492979895#0'], 
'x10': ['OrigionN2'], 
'x11': ['492979892'], 
'x12': ['492979887#0'], 
'x13': ['492979887#1', '492979887#2', '492979887#3', '230493751', '230493750#0','230493750#1', '93864593#0', '93864593#1','DestinationS8'], 
'x14': ['492979896#2'], 
'x15': ['-230239443#2', '-230239443#1'], 
'x16': ['-230239443#0', '-230239442', '-448953275#1','DestinationE4'],
'x17': ['OrigionE4', '448953275#1', '230239442', '230239443#0'], 
'x18': ['230239443#1', '230239443#2'], 
'x19': ['38869999#3'], 
'x20': ['38869999#4'], 
'x21': ['38869048#0', '24626397', '230239444', '230239445#0','DestinationE5'], 	
'x22': ['OrigionE3'], 
'x23': ['-38869048#2'], 
'x24': ['-38869048#1', '-38869048#0'], 
'x25': ['-38869999#4'], 
'x26': ['OrigionE1'], 
'x27': ['-230493745#2', '-230493745#1','-230493750#0', '-230493751', '-492979887#3', '-492979887#2', '-492979887#1'], 
'x28': ['-492979887#0'],
'x29': ['-492979892'],
'x30': ['-38867851'],
'x31': ['OrigionE5', '-230239445#0', '-230239444', '-24626397', '38869048#1'], 
'x32': ['38869048#2'], 
'x33': ['38869048#3', '38869048#4', '230493753', '230493752#0'], 
'x34': ['DestinationE1'], 
'x35': ['-69555386#2', '-69555386#1'],
'x36': ['DestinationN1'],
'R2_R1_1':['-135626792#6'],
'R2_R3_1':['-492979896#2'],
'R2_R1_2':['-38869999#3'],
'R2_R3_2':['-69555386#0']
}


s_R2={
's0': 'R2_Junction3_1',
's1': 'R2_Junction7_1', 
's2': 'R2_Junction1_1',
's3': 'R2_Junction5_1', 
's4': 'R2_Junction10_1', 
's5': 'R2_Junction1_2',  
's6': 'R2_Junction10_2', 
's7': 'R2_Junction2_2', 
's8': 'R2_Junction3_2',
's9': 'R2_Junction2_1',
's10': 'R2_Junction6_1', 
's11': 'R2_Junction11_1', 
's12': 'R2_Junction5_2', 
's13': 'R2_Junction6_2', 
's14': 'R2_Junction8_1', 
's15': 'R2_Junction1_3', 
's16': 'R2_Junction11_2',
's17': 'R2_Junction7_2', 
's18': 'R2_Junction8_2'
}

##path/junction/phasesequence/lanenum/uplinks/downlinks/ratio
y_R2= {
#PathID="w3-e3"
'y0': ["w3-e3",'R2_Junction3', '1', 2, 'x0', 'x1',1], 
'y1': ["w3-e3",'R2_Junction7', '1', 2, 'x1', 'x2',1], 
#PathID="s5-e6"
'y2': ["s5-e6",'R2_Junction1', '1', 1, 'x3', 'x4',0.5],
'y3': ["s5-e6",'R2_Junction5', '1', 1, 'x4', 'x5',0.5], 
'y4': ["s5-e6",'R2_Junction10', '1', 2, 'x5', 'x6',1], 
#PathID="n1-s6"
'y5': ["n1-s6",'R2_Junction10', '1', 1, 'x7', 'x8',1],
'y6': ["n1-s6",'R2_Junction5', '1', 1, 'x8', 'x9',0.5],
'y7': ["n1-s6",'R2_Junction1', '2', 1, 'x9', 'R2_R1_1',1], 
#PathID="n2-s8"
'y8': ["n2-s8",'R2_Junction10', '2', 1, 'x10', 'x8'],
'y9': ["n2-s8",'R2_Junction5', '1', 1, 'x8', 'x9',0.5], 
'y10': ["n2-s8",'R2_Junction1', '2', 1, 'x9', 'x11',1],
'y11': ["n2-s8",'R2_Junction2', '2', 1, 'x11', 'x12',1],
'y12': ["n2-s8",'R2_Junction3', '2', 1, 'x12', 'x13',1],
#PathID="w8-e4"
'y13': ["w8-e4",'R2_Junction2', '1', 1, 'x14', 'x15',1], 
'y14': ["w8-e4",'R2_Junction6', '1', 1, 'x15', 'x16',1],
#PathID="e4-w8"
'y15': ["e4-w8",'R2_Junction6', '1', 1, 'x17', 'x18',1], 
'y16': ["e4-w8",'R2_Junction2', '1', 1, 'x18', 'R2_R3_1',1],
##PathID="n6-e5"
'y17': ["n6-e5",'R2_Junction11', '1', 1, 'x19', 'x20',1], 
'y18': ["n6-e5",'R2_Junction5', '2', 1, 'x20', 'x21',1],
#PathID="e3-n3"
'y19': ["e3-n3",'R2_Junction7', '1', 1, 'x22', 'x23',1], 
'y20': ["e3-n3",'R2_Junction6', '2', 1, 'x23', 'x24',1], 
'y21': ["e3-n3",'R2_Junction5', '2', 1, 'x24', 'x25',1], 
'y22': ["e3-n3",'R2_Junction11', '1', 1, 'x25', 'R2_R1_2',1], 
#PathID="e1-w5"
'y23': ["e1-w5",'R2_Junction8', '1', 1, 'x26', 'x27',1], 
'y24': ["e1-w5",'R2_Junction3', '2', 1, 'x27', 'x28',1], 
'y25': ["e1-w5",'R2_Junction2', '2', 1, 'x28', 'x29',1], 
'y26': ["e1-w5",'R2_Junction1', '3', 1, 'x29', 'x30',1], 
'y27': ["e1-w5",'R2_Junction11', '2', 1, 'x30', 'R2_R1_2',1], 
#PathID="e5-e1"
'y28': ["e5-e1",'R2_Junction6', '2', 1, 'x31', 'x32',1], 
'y29': ["e5-e1",'R2_Junction7', '2', 1, 'x32', 'x33',1],
'y30': ["e5-e1",'R2_Junction8', '2', 1, 'x33', 'x34',1], 
##PathID="e3-s5"
'y31': ["e3-s5",'R2_Junction7', '1', 2, 'x22', 'x35',1], 
'y32': ["e3-s5",'R2_Junction3', '1', 2, 'x35', 'R2_R3_2',1], 
#PathID="w9-n1"
'y33': ["w9-n1",'R2_Junction1', '1', 1, 'x3', 'x4',0.5],
'y34': ["w9-n1",'R2_Junction5', '1', 1, 'x4', 'x5',0.5], 
'y35': ["w9-n1",'R2_Junction10', '1', 1, 'x5', 'x36',1]
}

# ## generate the x_variable
# i = 0
# x_path_R2 = defaultdict(list)
# for j in xrange(len(y_R2)):	
# 	links = y_R2['y'+str(j)][4].split()
# 	for link in links:
# 		x_path_R2[i].append(y_R2['y'+str(j)][0])
# 		x_path_R2[i].append(link)
# 		x_path_R2[i].append(States_R2[link])
# 		i+=1
# 	if j<len(y_R2)-1 and y_R2['y'+str(j)][0]!=y_R2['y'+str(j+1)][0]:
# 		links = y_R2['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R2[i].append(y_R2['y'+str(j)][0])
# 			x_path_R2[i].append(link)
# 			x_path_R2[i].append(States_R2[link])
# 			i+=1
# 	elif j==len(y_R2)-1:
# 		links = y_R2['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R2[i].append(y_R2['y'+str(j)][0])
# 			x_path_R2[i].append(link)
# 			x_path_R2[i].append(States_R2[link])
# 			i+=1

# print x_path_R2

x_len = len(x_R2)
s_len = len(s_R2)
y_len = len(y_R2)
print x_len,s_len,y_len

# tc = 6

# EqCons = 1000 ## the number of equition constraints
# x_Eq = np.zeros((EqCons,x_len*tc))
# s_Eq = np.zeros((EqCons,s_len*tc))
# y_Eq = np.zeros((EqCons,y_len*tc))
# v_Eq = np.zeros((EqCons,s_len*tc))
# e_Eq = np.zeros((EqCons,s_len*tc))
# b_Eq = np.zeros(EqCons)

# IneqCons = 1000 ## the number of equition constraints
# x_Ineq = np.zeros((IneqCons,x_len*tc))
# s_Ineq = np.zeros((IneqCons,s_len*tc))
# y_Ineq = np.zeros((IneqCons,y_len*tc))
# v_Ineq = np.zeros((IneqCons,s_len*(tc-1)))
# e_Ineq = np.zeros((EqCons,s_len*(tc-1)))
# b_Ineq = np.zeros(IneqCons)

# ### Equition constraints 
# yo_Mat = np.eye(tc)
# yi_Mat = -np.eye(tc)
# x_Mat = np.zeros((tc,tc))
# x_Mat[0,0]=1
# for i in range(1,tc):
# 	x_Mat[i,i-1]=-1
# 	x_Mat[i,i]=1
# # print yi_Mat,yo_Mat,x_Mat

# #####generate PathInput and PathWeight
# # PathInput = defaultdict(list)
# # PathWeight = defaultdict(lambda:1)
# # for i in range(y_len):
# # 	if i in [0,2,4,7,8,12,13,16,18,20,25,27,29,32,33,36,43,49,52]:
# # 		name = y_R2['y'+str(i)][0]
# # 		PathWeight[name]=1
# # 		InputLink = y_R2['y'+str(i)][4].split()
# # 		for link in InputLink:
# # 			for key in States_R2.keys():
# # 				if link==key:
# # 					PathInput[name]+=States_R2[key]
# # print PathInput,PathWeight

# PathInput={
# 's4-n5': ['70438941#5'], 
# 's7-n4': ['100323308#6', '100323308#7', '100323308#8'], 
# 'n5-w3': ['OrigionN5'], 
# 'e1-w5': ['-38869999#3'], 
# 'n1-s6': ['-135626792#6'], 
# 'n7-s3': ['OrigionN7', '44578496#3'], 
# 's5-e6': ['492981118#0'], 
# 's2-n7': ['135626776#6', '135626776#7'], 
# 'w2-n6': ['240833369#1'], 
# 'n4-w2': ['OrigionN4'], 
# 'n3-s7': ['OrigionN3'], 
# 'w7-s7': ['OrigionW7', '135626788#1', '135626788#2', '135626788#3', '135626760', '38869999#0'], 
# 's6-w5': ['100323308#6', '100323308#7', '100323308#8'], 
# 'w9-n3': ['OrigionW9'], 
# 'w7-s2': ['OrigionW7', '253924913'], 
# 'e3-n3': ['-38869999#3'], 
# 'n6-e5': ['OrigionN6', '-85711505#4'], 
# 'w9-n1': ['OrigionW9'], 
# 'w5-w9': ['OrigionW5', '-100323308#10', '68313226#0']}

# PathWeight={
# 's4-n5': 1, 's7-n4': 1, 'n5-w3': 1, 'e1-w5': 1, 'n1-s6': 1, 'n7-s3': 1, 's5-e6': 1, 's2-n7': 1, 
# 'w2-n6': 1, 'n4-w2': 1, 'n3-s7': 1, 'w7-s7': 1, 's6-w5': 1, 'w9-n3': 1, 'w7-s2': 1, 'e3-n3': 1, 
# 'n6-e5': 1, 'w9-n1': 1, 'w5-w9': 1}



# ##0: the input number of vehicles through the first link (estimated demand)
# ##1: the total number of vehicles in all the links (initial value)
# PathInputValue = defaultdict(lambda:[0]*2)
# PathInputValue['s2-n7']=[0,1] 

# ########################################################### Equition constraints flow conservation ############################################
# #### Path1
# #'y0': ["s2-n7",'R2_Junction16', '2', 2, 'x0', 'x1'],
# # x0(k+1)=x0(k)+d_R3_R2(k)-y0(k)
# # xL = 0
# # yoL = 0
# # x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
# # y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
# # b_Eq[row*tc:(row+1)*tc] = PathInputValue['s2-n7'][0]*np.ones(tc)
# # b_Eq[row*tc] += PathInputValue['s2-n7'][1]
# # row += 1

# xL = 0
# yoL = 0
# yiL = 0
# row = 0
# for j in range(y_len):
# 	temp = y_R2['y'+str(j)] 
# 	links = temp[4].split()
# 	path = temp[0]
# 	if j in [0,2,4,7,8,12,13,16,18,20,25,27,29,32,33,36,43,49,52]:
# 		for i in range(x_len):
# 			if x_R2[i][0]==path and x_R2[i][1] in links:
# 				xL = i 
# 				x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat				
# 		yoL = j				
# 		y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
# 		b_Eq[row*tc:(row+1)*tc] = PathInputValue[path][0]*np.ones(tc)
# 		b_Eq[row*tc] += PathInputValue[path][1]
# 		row += 1
# 	else:
# 		for i in range(x_len):
# 			if x_R2[i][0]==path and x_R2[i][1] in links:
# 				xL = i 
# 		yoL = j
# 		yiL = j-1
# 		x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
# 		y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
# 		y_Eq[row*tc:(row+1)*tc,yiL*tc:(yiL+1)*tc] = yi_Mat
# 		b_Eq[row*tc:(row+1)*tc] = np.zeros(tc)
# 		row += 1

# ########################################################## Equition constraints for signals##########################################################
# ###get junction name
# sone_Mat = np.eye(tc)
# ssum_Mat = np.ones(tc)
# Junction_name = []
# for junction in s_R2.values():
# 	Junction_name.append(junction[:-2])
# Junction_name=set(Junction_name)
# # print Junction_name

# ###junction phase label--{junction name{pahsesequence:label}}
# JpL = defaultdict(dict) 
# for junction in Junction_name:	 
# 	for i in xrange(s_len):
# 		name = s_R2['s'+str(i)][:-2]
# 		if name==Junction:
# 			PhaseSequence = int(s_R2['s'+str(i)][-1])
# 			JpL[name][PhaseSequence]=i 
# 	################ only one phase can be activated at one time
# 	for pL in JpL[junction].values():
# 		s_Eq[row*tc:(row+1)*tc,pL*tc:(pL+1)*tc] = sone_Mat
# 	b_Eq[row*tc:(row+1)*tc] = np.ones(tc)
# 	row+=1

# ############## the sum of the signal phase equal to tc #############
# row = row*tc
# for junction in JpL.keys():
# 	for pL in junction.values():
# 		s_Eq[row,pL*tc:(pL+1)*tc] = np.ones(tc)
# 	b_Eq[row] = tc
# 	row+=1


# ########################################################### Equition constraints for auxilary variables ########################################
# saturationflow = 0.5*period
# InitVehNum_x_R2 = defaultdict(lambda:0)
# InitCoefficient= defaultdict(lambda:0)
# for i in range(s_len):
# 	junction = s_R2['s'+str(i)][:-2]
# 	pahsesequence = s_R2['s'+str(i)][-1]
	
# 	for j in range(y_len):
# 		temp = y_R2['y'+str(j)]
# 		if temp[1]==junction and temp[2]==pahsesequence:
# 			path = temp[0]
# 			lane_num = temp[3]
# 			uplinks = temp[4].split()
# 			downlinks = temp[5].split()
# 			ratio = temp[6]
# 			coeff = PathWeight[path]*ratio*saturationflow*lane_num
# 			for k in range(x_len):
# 				if path==x_R2[k][0] and x_R2[k][1] in uplinks:
# 					xL=k
# 					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = coeff*np.eye(tc-1)	
# 					InitCoefficient[i]=InitCoefficient[i]+coeff*InitVehNum_x_R2[xL]
						
# 				elif path==x_R2[k][0] and x_R2[k][1] in downlinks:
# 					xL=k
# 					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = -1*coeff*np.eye(tc-1)
# 					InitCoefficient[i]=InitCoefficient[i]-coeff*InitVehNum_x_R2[xL]
					
# 	eL = i
# 	e_Eq[row:row+tc-1,eL*(tc-1):(eL+1)*(tc-1)]=-1*np.eyes(tc-1)
# 	b_Eq[row:row+tc-1] = np.zeros(tc-1)
# 	row = row+tc-1

# print row
# #############################################################################################################################
# ################################################ Inequition constraints #################################################
# row = 0

# ################################### minimum function ###############################
# for i in range(y_len):
# 	yL = i
# 	temp = y_R2['y'+str(j)]
# 	path = temp[0]
# 	junction = temp[1]
# 	pahsesequence = temp[2]
# 	lane_num = temp[3]
# 	uplinks = temp[4].split()	
# 	ratio = temp[6]
# 	## -x+y<=0
# 	InitVehNum = 0
# 	for k in range(x_len):
# 		if path==x_R2[k][0] and x_R2[k][1] in uplinks:
# 			xL=k
# 			InitVehNum = InitVehNum + InitVehNum_x_R2[xL] ##initial time of control
# 			x_Ineq[row+1:row+tc,xL*tc:(xL+1)*tc-1] = -1*np.eye(tc-1)	
	
# 	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
# 	b_Ineq[row] = InitVehNum
# 	b_Ineq[row+1:row+tc]=np.zeros(tc)
# 	row = row+tc

# 	## -c*s*r+y<=0
# 	for j in range(s_len):
# 		if s_R2['s'+str(j)] == junction+'_'+pahsesequence:
# 			sL = j
# 			coeff = saturationflow*lane_num*ratio
# 			s_Ineq[row:row+tc,sL*tc:(sL+1)*tc]=-1*coeff*np.eye(tc)
# 	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
# 	b_Ineq[row:row+tc]=np.zeros(tc)
# 	row = row+tc


# ############################# auxilary constraints ################################
# emin = -1000
# emax = 1000
# for j in range(s_len):
# 	sL = j 
# 	## -v+emin*s<=0
# 	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=emin*np.eye(tc-1)
# 	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
# 	b_Ineq[row:row+tc-1]=np.zeros(tc-1)
# 	row=row+tc-1

# 	## v-emax*s<=0
# 	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=-1*emax*np.eye(tc-1)
# 	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
# 	b_Ineq[row:row+tc-1]=np.zeros(tc-1)
# 	row=row+tc-1

# 	## v-e+emax(1-s)>=0
# 	## -v+e+emax*s<=emax
# 	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=emax*np.eye(tc-1)
# 	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
# 	e_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
# 	b_Ineq[row:row+tc-1]=emax*np.ones(tc-1)
# 	row=row+tc-1

# 	## v-e+emin(1-s)<=0
# 	## v-e-emin*s<=-emin
# 	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=-1*emin*np.eye(tc-1)
# 	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
# 	e_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
# 	b_Ineq[row:row+tc-1]=-!*emin*np.ones(tc-1)
# 	row=row+tc-1

# ##################### -y<0 #######################################
# for i in range(y_len):
# 	yL = i 
# 	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc]=-1*np.eye(tc)
# 	b_Ineq[row:row+tc]=np.zeros(tc)
# 	row=row+tc

# ##################### 0<=x<xmax #######################################
# for i in range(x_len):
# 	xL = i 

# 	### -x<=0
# 	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=-1*np.eye(tc)
# 	b_Ineq[row:row+tc]=np.zeros(tc)
# 	row=row+tc

# 	### x<=xmax
# 	links = x_R2[i][2]
# 	occup=0
# 	for link in links:
# 		occup+=Occupy[link]
# 	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=np.eye(tc)
# 	b_Ineq[row:row+tc]=occup*np.ones(tc)
# 	row=row+tc

# print row


# #########################################################################################################################
# ####################################################### Objective function ###############################################
# f = np.zeros((x_len+y_len+s_len*3)*tc)
# fweight = 10


# ##### Combine
# ## varibale x-y-s-e-v
# Aeq = np.hstack((x_Eq,y_Eq,s_Eq,e_Eq,v_Eq))
# Aineq = np.hstack((x_Ineq,y_Ineq,s_Ineq,e_Ineq,v_Ineq))
		


			
















