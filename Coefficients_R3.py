import numpy as np
from collections import defaultdict



period = 10 ##seconds

x_R3={
0: ['w4-s1', 'x0', ['OrigionW4', '-135626767#7']], 
1: ['w4-s1', 'x1', ['-135626767#6', '-135626767#5']], 
2: ['w4-s1', 'x2', ['-135626767#3', 'DestinationS1']], 
3: ['w3-e3', 'x3', ['OrigionW3']], 
4: ['w3-e3', 'x4', ['91568767#5']], 
5: ['w3-e3', 'x5', ['91568767#6']], 
6: ['w3-e3', 'x6', ['91568767#8']], 
7: ['w3-e3', 'x7', ['91568767#9']], 
8: ['w3-e3', 'x8', ['91568767#10', '135626766', '135626762#0']], 
9: ['w3-e3', 'x9', ['135626762#1']], 
10: ['w3-e3', 'x10', ['135626762#2']], 
11: ['w3-e3', 'R3_R2_1', ['135626776#6']], 
12: ['s2-n7', 'x11', ['OrigionS2']], 
13: ['s2-n7', 'x5', ['91568767#6']], 
14: ['s2-n7', 'x12', ['135626776#3', '135626776#4', '135626776#5']], 
15: ['s2-n7', 'R3_R1_1', ['162259815#2', '135626776#7']], 
16: ['s4-n5', 'x13', ['OrigionS4', '135626776#1']], 
17: ['s4-n5', 'x6', ['91568767#8']], 
18: ['s4-n5', 'x7', ['91568767#9']], 
19: ['s4-n5', 'x14', ['70438941#1', '70438941#2', '70438941#3']], 
20: ['s4-n5', 'R3_R1_2', ['70438941#4', '70438941#5']], 
21: ['s5-e6', 'x15', ['OrigionS5']], 
22: ['s5-e6', 'x7', ['91568767#9']], 
23: ['s5-e6', 'x8', ['91568767#10', '135626766', '135626762#0']], 
24: ['s5-e6', 'x16', ['253924915#0', '253924915#1']], 
25: ['s5-e6', 'R3_R1_3', ['492981118#0']], 
26: ['s6-w5', 'x17', ['OrigionS6', '-230239448#0', '-230239447', '-230491007']], 
27: ['s6-w5', 'x9', ['135626762#1']], 
28: ['s6-w5', 'x10', ['135626762#2']], 
29: ['s6-w5', 'x18', ['100323308#5']], 
30: ['s6-w5', 'R3_R1_4', ['100323308#6', '100323308#7', '100323308#8']], 
31: ['s7-n4', 'x19', ['OrigionS7', '100323308#2', '100323308#3']], 
32: ['s7-n4', 'x18', ['100323308#5']], 
33: ['s7-n4', 'R3_R1_4', ['100323308#6', '100323308#7', '100323308#8']], 
34: ['n1-s6', 'x20', ['-100323308#6']], 
35: ['n1-s6', 'x21', ['-100323308#5']], 
36: ['n1-s6', 'x22', ['69550029#1', '492979883']], 
37: ['n1-s6', 'x23', ['230491007', '230239447', '230239448#0', 'DestinationS6']], 
38: ['n3-s7', 'x20', ['-100323308#6']], 
39: ['n3-s7', 'x21', ['-100323308#5']], 
40: ['n3-s7', 'x24', ['542054843#1', '542054843#2', 'DestinationS7']], 
41: ['n5-w3', 'x25', ['253924914#3', '253924914#4']], 
42: ['n5-w3', 'x26', ['253924914#5', '253924914#6', '253924914#7']], 
43: ['n5-w3', 'x27', ['492979884#0']], 
44: ['n5-w3', 'x28', ['492979884#1']], 
45: ['n5-w3', 'x29', ['492979884#3']],
46: ['n5-w3', 'x30', ['492979884#4']], 
47: ['n5-w3', 'x31', ['DestinationW3']], 
48: ['n7-s3', 'x32', ['162259815#0', '162259815#1', '162259815#2']], 
49: ['n7-s3', 'x33', ['162259815#3', '162259815#4', '162259815#5']], 
50: ['n7-s3', 'x34', ['162259815#7', 'DestinationS3']], 
51: ['w8-e4', 'x35', ['OrigionW8']], 
52: ['w8-e4', 'x36', ['38866846#1']], 
53: ['w8-e4', 'x37', ['38866846#2']], 
54: ['w8-e4', 'x38', ['38866846#3', '135626787', '135626763#0', '135626763#1']], 
55: ['w8-e4', 'x39', ['492981119']], 
56: ['w8-e4', 'x40', ['492979896#0']], 
57: ['w8-e4', 'R3_R2_2', ['492979896#2']], 
58: ['e4-w8', 'x41', ['-492979896#2']], 
59: ['e4-w8', 'x42', ['-492979896#0']], 
60: ['e4-w8', 'x43', ['-492981119']], 
61: ['e4-w8', 'x44', ['-135626763#1', '-135626763#0', '-135626787', '-38866846#3']], 
62: ['e4-w8', 'x45', ['-38866846#2']], 
63: ['e4-w8', 'x46', ['-38866846#1']], 
64: ['e4-w8', 'x47', ['DestinationW8']], 
65: ['w7-s2', 'x48', ['95775639#1', '95775639#2']], 
66: ['w7-s2', 'x49', ['95775639#3', '95775639#4', '95775639#5']],
67: ['w7-s2', 'x28', ['492979884#1']], 
68: ['w7-s2', 'x29', ['492979884#3']], 
69: ['w7-s2', 'x50', ['DestinationS2']], 
70: ['w2-n6', 'x51', ['OrigionW2']], 
71: ['w2-n6', 'x52', ['135626767#7']], 
72: ['w2-n6', 'x53', ['240833369#0']], 
73: ['w2-n6', 'R3_R1_5', ['240833369#1']], 
74: ['s1-w4', 'x54', ['OrigionS1', '135626767#3']], 
75: ['s1-w4', 'x55', ['135626767#5', '135626767#6']], 
76: ['s1-w4', 'x52', ['135626767#7']], 
77: ['s1-w4', 'x56', ['DestinationW4']], 
78: ['e3-s5', 'x57', ['-69555386#0']], 
79: ['e3-s5', 'x22', ['69550029#1', '492979883']], 
80: ['e3-s5', 'x58', ['492981120', '135626779', '135626780#0', '135626780#1', '135626780#2']], 
81: ['e3-s5', 'x59', ['DestinationS5']], 
82: ['n4-w2', 'x32', ['162259815#0', '162259815#1', '162259815#2']], 
83: ['n4-w2', 'x60', ['69059186#0', '69059186#1', '69059186#2']], 
84: ['n4-w2', 'x61', ['DestinationW2']], 
85: ['w7-s7', 'x62', ['68313224#2']], 
86: ['w7-s7', 'x63', ['492979886']],
87: ['w7-s7', 'x10', ['135626762#2']], 
88: ['w7-s7', 'x24', ['542054843#1', '542054843#2', 'DestinationS7']]}

States_R3={
'x0': ['OrigionW4', '-135626767#7'], 
'x1': ['-135626767#6', '-135626767#5'],
'x2': ['-135626767#3','DestinationS1'], 
'x3': ['OrigionW3'], 
'x4': ['91568767#5'], 
'x5': ['91568767#6'],
'x6': ['91568767#8'],
'x7': ['91568767#9'],
'x8':['91568767#10', '135626766', '135626762#0'], 
'x9': ['135626762#1'], 
'x10':['135626762#2'], 
"R3_R2_1":['135626776#6',],
'x11': ['OrigionS2'],
'x12': ['135626776#3', '135626776#4', '135626776#5'], 
'R3_R1_1':['162259815#2','135626776#7'],
'x13': ['OrigionS4', '135626776#1'], 
'x14': ['70438941#1', '70438941#2', '70438941#3'], 
'R3_R1_2':['70438941#4','70438941#5'],
'x15': ['OrigionS5'], 
'x16': ['253924915#0', '253924915#1'],
'R3_R1_3':['492981118#0'],
'x17': ['OrigionS6', '-230239448#0', '-230239447', '-230491007'], 
'x18': ['100323308#5'], 
'R3_R1_4':['100323308#6','100323308#7','100323308#8'],
'x19': ['OrigionS7', '100323308#2', '100323308#3'], 
'x20': ['-100323308#6'],
'x21': ['-100323308#5'], 
'x22': ['69550029#1', '492979883'],
'x23': ['230491007', '230239447', '230239448#0','DestinationS6'],
'x24': ['542054843#1', '542054843#2','DestinationS7'],
'x25': ['253924914#3', '253924914#4'],
'x26': ['253924914#5', '253924914#6', '253924914#7'],
'x27': ['492979884#0'], 
'x28':['492979884#1'],
'x29': ['492979884#3'],
'x30': ['492979884#4'],
'x31': ['DestinationW3'], 
'x32': ['162259815#0', '162259815#1', '162259815#2'],
'x33':['162259815#3', '162259815#4', '162259815#5'],
'x34': ['162259815#7','DestinationS3'],
'x35': ['OrigionW8'],
'x36': ['38866846#1'], 
'x37': ['38866846#2'], 
'x38': ['38866846#3', '135626787', '135626763#0', '135626763#1'],
'x39': ['492981119'],
'x40': ['492979896#0'],
'R3_R2_2':['492979896#2'],
'x41': ['-492979896#2'], 
'x42': ['-492979896#0'],
'x43': ['-492981119'],
'x44': ['-135626763#1', '-135626763#0', '-135626787', '-38866846#3'],
'x45': ['-38866846#2'],
'x46': ['-38866846#1'],
'x47': ['DestinationW8'],
'x48': ['95775639#1', '95775639#2'],
'x49': ['95775639#3', '95775639#4', '95775639#5'],
'x50': ['DestinationS2'], 
'x51': ['OrigionW2'],
'x52': ['135626767#7'], 
'x53': ['240833369#0'],
'R3_R1_5':['240833369#1'],
'x54': ['OrigionS1', '135626767#3'],
'x55': ['135626767#5', '135626767#6'],
'x56': ['DestinationW4'], 
'x57': ['-69555386#0'], 
'x58': ['492981120', '135626779', '135626780#0', '135626780#1', '135626780#2'], 
'x59': ['DestinationS5'], 
'x60': ['69059186#0', '69059186#1','69059186#2'], 
'x61': ['DestinationW2'], 
'x62': ['68313224#2'], 
'x63': ['492979886']
}


s_R3={
's0': 'R3_Junction10_3',
's1': 'R3_Junction11_2', 
's2': 'R3_Junction11_1',
's3': 'R3_Junction12_2',
's4': 'R3_Junction14_1', 
's5': 'R3_Junction8_1',
's6': 'R3_Junction7_3',
's7': 'R3_Junction6_1',
's8': 'R3_Junction12_3', 
's9': 'R3_Junction14_3', 
's10': 'R3_Junction4_2',
's11': 'R3_Junction8_3',
's12': 'R3_Junction3_2', 
's13': 'R3_Junction7_2',
's14': 'R3_Junction6_2', 
's15': 'R3_Junction1_2',
's16': 'R3_Junction6_3',
's17': 'R3_Junction7_1',
's18': 'R3_Junction13_2',       
's19': 'R3_Junction14_2',   
's20': 'R3_Junction12_1', 
's21': 'R3_Junction5_1',
's22': 'R3_Junction13_1', 
's23': 'R3_Junction4_1', 
's24': 'R3_Junction3_1', 
's25': 'R3_Junction2_1', 
's26': 'R3_Junction1_1', 
's27': 'R3_Junction5_2',
's28': 'R3_Junction10_2', 
's29': 'R3_Junction8_2',
's30': 'R3_Junction9_',
's31': 'R3_Junction10_1',
's32': 'R3_Junction2_2'
}

 
y_R3={ 
#PathID="w4-s1"
'y0': ["w4-s1",'R3_Junction10', '3', 2, 'x0', 'x1',1], 
'y1': ["w4-s1",'R3_Junction11', '2', 2, 'x1', 'x2',1], 
#PathID="w3-e3"
'y2': ["w3-e3",'R3_Junction11', '1', 2, 'x3', 'x4',1],
'y3': ["w3-e3",'R3_Junction12', '2', 2, 'x4', 'x5',1],  
'y4': ["w3-e3",'R3_Junction14', '1', 2, 'x5', 'x6',1], 
'y5': ["w3-e3",'R3_Junction8', '1', 2, 'x6', 'x7 x8',0.5], 
'y6': ["w3-e3",'R3_Junction7', '3', 1, 'x7 x8', 'x9 x10',1], 
'y7': ["w3-e3",'R3_Junction6', '1', 2, 'x9 x10', 'R3_R2_1',1],
#PathID="s2-n7"
'y8': ["s2-n7",'R3_Junction12', '3', 1, 'x11', 'x5',1], 
'y9': ["s2-n7",'R3_Junction14', '1', 1, 'x5', 'x12 R3_R1_1',1],
#PathID="s4-n5"
'y10': ["s4-n5",'R3_Junction14', '3', 1, 'x13', 'x6',1], 
'y11': ["s4-n5",'R3_Junction8', '1', 2, 'x6', 'x7 x14',0.5], 
'y12': ["s4-n5",'R3_Junction4', '2', 1, 'x7 x14', 'R3_R1_2',1],
#PathID="s5-e6"
'y13': ["s5-e6",'R3_Junction8', '3', 1, 'x15', 'x7 x8',1], 
'y14': ["s5-e6",'R3_Junction7', '3', 1, 'x7 x8', 'x16',1], 
'y15': ["s5-e6",'R3_Junction3', '2', 2, 'x16', 'R3_R1_3',1],  
##PathID="s6-w5"
'y16': ["s6-w5",'R3_Junction7', '2', 1, 'x17', 'x9 x10',1], 
'y17': ["s6-w5",'R3_Junction6', '2', 1, 'x9 x10', 'x18',1],
'y18': ["s6-w5",'R3_Junction1', '2', 2, 'x18', 'R3_R1_4',0.5],
#PathID="s7-n4"
'y19': ["s7-n4",'R3_Junction6', '3', 2, 'x19', 'x18',1],
'y20': ["s7-n4",'R3_Junction1', '2', 2, 'x18', 'R3_R1_4',0.5],
#PathID="n1-s6"
'y21': ["n1-s6",'R3_Junction1', '2', 2, 'x20', 'x21',0.5], 
'y22': ["n1-s6",'R3_Junction6', '3', 1, 'x21', 'x22',1], 
'y23': ["n1-s6",'R3_Junction7', '1', 1, 'x22', 'x23',1], 
#PathID="n3-s7"
'y24': ["n3-s7",'R3_Junction1', '2', 2, 'x20', 'x21',0.5], 
'y25': ["n3-s7",'R3_Junction6', '3', 2, 'x21', 'x24',1], 
#PathID="n5-w3"
'y26': ["n5-w3",'R3_Junction13', '2', 1, 'x25', 'x26',1], 
'y27': ["n5-w3",'R3_Junction8', '3', 1, 'x26', 'x27 x28',1],
'y28': ["n5-w3",'R3_Junction14', '2', 2, 'x27 x28', 'x29',0.5], 
'y29': ["n5-w3",'R3_Junction12', '1', 2, 'x29', 'x30',1], 
'y30': ["n5-w3",'R3_Junction11', '1', 2, 'x30', 'x31',1], 
#PathID="n7-s3"
'y31': ["n7-s3",'R3_Junction14', '3', 2, 'x32 x33', 'x34',1],
#PathID="w8-e4"
'y32': ["w8-e4",'R3_Junction5', '1', 1, 'x35', 'x36',1], 
'y33': ["w8-e4",'R3_Junction13', '1', 1, 'x36', 'x37',1], 
'y34': ["w8-e4",'R3_Junction4', '1', 1, 'x37', 'x38',1],
'y35': ["w8-e4",'R3_Junction3', '1', 1, 'x38', 'x39',1],
'y36': ["w8-e4",'R3_Junction2', '1', 1, 'x39', 'x40',1], 
'y37': ["w8-e4",'R3_Junction1', '1', 1, 'x40', 'R3_R2_2',1],
#PathID="e4-w8"
'y38': ["e4-w8",'R3_Junction1', '1', 1, 'x41', 'x42',1], 
'y39': ["e4-w8",'R3_Junction2', '1', 1, 'x42', 'x43',1], 
'y40': ["e4-w8",'R3_Junction3', '1', 1, 'x43', 'x44',1], 
'y41': ["e4-w8",'R3_Junction4', '1', 1, 'x44', 'x45',1], 
'y42': ["e4-w8",'R3_Junction13', '1', 1, 'x45', 'x46',1], 
'y43': ["e4-w8",'R3_Junction5', '1', 1, 'x46', 'x47',1], 
#PathID="w7-s2"
'y44': ["w7-s2",'R3_Junction5', '2', 1, 'x48', 'x49 x28',1], 
'y45': ["w7-s2",'R3_Junction14', '2', 2, 'x49 x28', 'x29',0.5], 
'y46': ["w7-s2",'R3_Junction12', '1', 1, 'x29', 'x50',1], 
##PathID="w2-n6"
'y47': ["w2-n6",'R3_Junction10', '2', 1, 'x51', 'x52 x53 R3_R1_5',1], 
#PathID="s1-w4"
'y48': ["s1-w4",'R3_Junction11', '2', 2, 'x54', 'x55',1], 
'y49': ["s1-w4",'R3_Junction10', '3', 2, 'x55', 'x52 x56',1],
##PathID="e3-s5"
'y50': ["e3-s5",'R3_Junction6', '1', 2, 'x57', 'x22',1], 
'y51': ["e3-s5",'R3_Junction7', '1', 2, 'x22', 'x58',1], 
'y52': ["e3-s5",'R3_Junction8', '2', 1, 'x58', 'x59',1], 
#PathID="n4-w2"
'y53': ["n4-w2",'R3_Junction10', '1', 1, 'x32 x60', 'x61',1], 
##PathID="w7-s7"
'y54': ["w7-s7",'R3_Junction2', '2', 1, 'x62', 'x63 x10',1],  
'y55': ["w7-s7",'R3_Junction6', '1', 1, 'x63 x10', 'x24',1]
}


# ## generate the x_variable
# i = 0
# x_path_R3 = defaultdict(list)
# for j in xrange(len(y_R3)):	
# 	links = y_R3['y'+str(j)][4].split()
# 	for link in links:
# 		x_path_R3[i].append(y_R3['y'+str(j)][0])
# 		x_path_R3[i].append(link)
# 		x_path_R3[i].append(States_R3[link])
# 		i+=1
# 	if j<len(y_R3)-1 and y_R3['y'+str(j)][0]!=y_R3['y'+str(j+1)][0]:
# 		links = y_R3['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R3[i].append(y_R3['y'+str(j)][0])
# 			x_path_R3[i].append(link)
# 			x_path_R3[i].append(States_R3[link])
# 			i+=1
# 	elif j==len(y_R3)-1:
# 		links = y_R3['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R3[i].append(y_R3['y'+str(j)][0])
# 			x_path_R3[i].append(link)
# 			x_path_R3[i].append(States_R3[link])
# 			i+=1

# print x_path_R3

x_len = len(x_R3)
s_len = len(s_R3)
y_len = len(y_R3)
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
# # 		name = y_R3['y'+str(i)][0]
# # 		PathWeight[name]=1
# # 		InputLink = y_R3['y'+str(i)][4].split()
# # 		for link in InputLink:
# # 			for key in States_R3.keys():
# # 				if link==key:
# # 					PathInput[name]+=States_R3[key]
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
# #'y0': ["s2-n7",'R3_Junction16', '2', 2, 'x0', 'x1'],
# # x0(k+1)=x0(k)+d_R3_R3(k)-y0(k)
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
# 	temp = y_R3['y'+str(j)] 
# 	links = temp[4].split()
# 	path = temp[0]
# 	if j in [0,2,4,7,8,12,13,16,18,20,25,27,29,32,33,36,43,49,52]:
# 		for i in range(x_len):
# 			if x_R3[i][0]==path and x_R3[i][1] in links:
# 				xL = i 
# 				x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat				
# 		yoL = j				
# 		y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
# 		b_Eq[row*tc:(row+1)*tc] = PathInputValue[path][0]*np.ones(tc)
# 		b_Eq[row*tc] += PathInputValue[path][1]
# 		row += 1
# 	else:
# 		for i in range(x_len):
# 			if x_R3[i][0]==path and x_R3[i][1] in links:
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
# for junction in s_R3.values():
# 	Junction_name.append(junction[:-2])
# Junction_name=set(Junction_name)
# # print Junction_name

# ###junction phase label--{junction name{pahsesequence:label}}
# JpL = defaultdict(dict) 
# for junction in Junction_name:	 
# 	for i in xrange(s_len):
# 		name = s_R3['s'+str(i)][:-2]
# 		if name==Junction:
# 			PhaseSequence = int(s_R3['s'+str(i)][-1])
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
# InitVehNum_x_R3 = defaultdict(lambda:0)
# InitCoefficient= defaultdict(lambda:0)
# for i in range(s_len):
# 	junction = s_R3['s'+str(i)][:-2]
# 	pahsesequence = s_R3['s'+str(i)][-1]
	
# 	for j in range(y_len):
# 		temp = y_R3['y'+str(j)]
# 		if temp[1]==junction and temp[2]==pahsesequence:
# 			path = temp[0]
# 			lane_num = temp[3]
# 			uplinks = temp[4].split()
# 			downlinks = temp[5].split()
# 			ratio = temp[6]
# 			coeff = PathWeight[path]*ratio*saturationflow*lane_num
# 			for k in range(x_len):
# 				if path==x_R3[k][0] and x_R3[k][1] in uplinks:
# 					xL=k
# 					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = coeff*np.eye(tc-1)	
# 					InitCoefficient[i]=InitCoefficient[i]+coeff*InitVehNum_x_R3[xL]
						
# 				elif path==x_R3[k][0] and x_R3[k][1] in downlinks:
# 					xL=k
# 					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = -1*coeff*np.eye(tc-1)
# 					InitCoefficient[i]=InitCoefficient[i]-coeff*InitVehNum_x_R3[xL]
					
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
# 	temp = y_R3['y'+str(j)]
# 	path = temp[0]
# 	junction = temp[1]
# 	pahsesequence = temp[2]
# 	lane_num = temp[3]
# 	uplinks = temp[4].split()	
# 	ratio = temp[6]
# 	## -x+y<=0
# 	InitVehNum = 0
# 	for k in range(x_len):
# 		if path==x_R3[k][0] and x_R3[k][1] in uplinks:
# 			xL=k
# 			InitVehNum = InitVehNum + InitVehNum_x_R3[xL] ##initial time of control
# 			x_Ineq[row+1:row+tc,xL*tc:(xL+1)*tc-1] = -1*np.eye(tc-1)	
	
# 	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
# 	b_Ineq[row] = InitVehNum
# 	b_Ineq[row+1:row+tc]=np.zeros(tc)
# 	row = row+tc

# 	## -c*s*r+y<=0
# 	for j in range(s_len):
# 		if s_R3['s'+str(j)] == junction+'_'+pahsesequence:
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
# 	links = x_R3[i][2]
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
		


			
















