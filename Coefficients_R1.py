import numpy as np
from collections import defaultdict

period = 10 ##seconds

x_R1={
0: ['s2-n7', 'x0', ['135626776#6', '135626776#7']], 
1: ['s2-n7', 'x1', ['162259820#0', '162259820#1', '162259820#2', '104758675', '104758670', '104758678#0']], 
2: ['s2-n7', 'x2', ['104758678#1']], 
3: ['s4-n5', 'x3', ['70438941#5']], 
4: ['s4-n5', 'x4', ['70438941#6']], 
5: ['s4-n5', 'x5', ['-135626769#0', '-135626782', '-68313226#4']], 
6: ['s4-n5', 'x6', ['DestinationN5']], 
7: ['s5-e6', 'x7', ['492981118#0']], 
8: ['s5-e6', 'x8', ['135626792#2']], 
9: ['s5-e6', 'x9', ['135626792#3', '135626792#4']], 
10: ['s5-e6', 'R1_R2_1', ['135626792#6']], 
11: ['s6-w5', 'x10', ['100323308#6', '100323308#7', '100323308#8']], 
12: ['s6-w5', 'x11', ['100323308#9']], 
13: ['s6-w5', 'x12', ['100323308#10']], 
14: ['s6-w5', 'x13', ['DestinationW5']], 
15: ['s7-n4', 'x10', ['100323308#6', '100323308#7', '100323308#8']], 
16: ['s7-n4', 'x11', ['100323308#9']], 
17: ['s7-n4', 'x12', ['100323308#10']], 
18: ['s7-n4', 'x14', ['100323308#11']], 
19: ['s7-n4', 'x15', ['100323308#12', '72084632', '72084610', '85711505#0']], 
20: ['s7-n4', 'x16', ['85711505#1']], 
21: ['s7-n4', 'x17', ['DestinationN4']],
22: ['n1-s6', 'x18', ['-135626792#6']], 
23: ['n1-s6', 'R1_R3_5', ['-100323308#8', '-100323308#7', '-100323308#6']], 
24: ['n3-s7', 'x20', ['OrigionN3']], 
25: ['n3-s7', 'x21', ['-85711505#0', '-72084610', '-72084632', '-100323308#12']], 
26: ['n3-s7', 'x22', ['-100323308#11']],
27: ['n3-s7', 'x23', ['-100323308#10']], 
28: ['n3-s7', 'x24', ['-100323308#9']], 
29: ['n3-s7', 'R1_R3_5', ['-100323308#8', '-100323308#7', '-100323308#6']], 
30: ['n5-w3', 'x25', ['OrigionN5']], 
31: ['n5-w3', 'x26', ['68313226#4', '135626782', '135626769#0', '135626769#1', '135626769#2']], 
32: ['n5-w3', 'x27', ['253924914#2']], 
33: ['n5-w3', 'R1_R3_1', ['253924914#3']], 
34: ['n7-s3', 'x28', ['OrigionN7', '44578496#3']], 
35: ['n7-s3', 'x29', ['104758666', '104758664', '104758665', '104758667#0', '104758667#1', '104758667#2']], 
36: ['n7-s3', 'R1_R3_1', ['253924914#3']], 37: ['n6-e5', 'x30', ['OrigionN6', '-85711505#4']], 
38: ['n6-e5', 'x31', ['-85711505#2']], 
39: ['n6-e5', 'x32', ['-85711505#1']], 
40: ['n6-e5', 'x33', ['473715122#1', '253924912', '253924916']], 
41: ['n6-e5', 'x34', ['38869999#1']], 
42: ['n6-e5', 'x35', ['38869999#2']], 
43: ['n6-e5', 'R1_R2_2', ['38869999#3']], 
44: ['w7-s2', 'x36', ['OrigionW7']], 
45: ['w7-s2', 'x37', ['253924913']], 
46: ['w7-s2', 'x38', ['95775639#0']], 
47: ['w7-s2', 'R1_R3_3', ['95775639#1', '95775639#2']], 
48: ['w2-n6', 'x39', ['240833369#1']], 
49: ['w2-n6', 'x1', ['162259820#0', '162259820#1', '162259820#2', '104758675', '104758670', '104758678#0']], 
50: ['w2-n6', 'x40', ['85711505#4', 'DestinationN6']], 
51: ['e3-n3', 'x41', ['-38869999#3']], 
52: ['e3-n3', 'x42', ['-38869999#2', '-38869999#1']], 
53: ['e3-n3', 'x43', ['-253924916', '-253924912', '-473715122#1']], 
54: ['e3-n3', 'x44', ['DestinationN3']], 
55: ['e1-w5', 'x41', ['-38869999#3']], 
56: ['e1-w5', 'x22', ['-100323308#11']], 
57: ['e1-w5', 'x13', ['DestinationW5']], 
58: ['n4-w2', 'x45', ['OrigionN4']], 
59: ['n4-w2', 'x46', ['85711505#2']], 
60: ['n4-w2', 'x29', ['104758666', '104758664', '104758665', '104758667#0', '104758667#1', '104758667#2']], 
61: ['n4-w2', 'R1_R3_2', ['162259815#0', '162259815#1', '162259815#2']], 
62: ['w9-n3', 'x47', ['OrigionW9']], 
63: ['w9-n3', 'x48', ['240833369#4']], 
64: ['w9-n3', 'x49', ['240833369#5', '240833369#6']], 
65: ['w9-n3', 'x50', ['240833369#7', '135626758', '135626792#0', '135626792#1']], 
66: ['w9-n3', 'x51', ['492981118#1']], 
67: ['w9-n3', 'x52', ['492981118#2']], 
68: ['w9-n3', 'x43', ['-253924916', '-253924912', '-473715122#1']], 
69: ['w9-n3', 'x44', ['DestinationN3']], 
70: ['w9-n1', 'x47', ['OrigionW9']], 
71: ['w9-n1', 'x48', ['240833369#4']], 
72: ['w9-n1', 'x49', ['240833369#5', '240833369#6']], 
73: ['w9-n1', 'x50', ['240833369#7', '135626758', '135626792#0', '135626792#1']], 
74: ['w9-n1', 'x8', ['135626792#2']], 
75: ['w9-n1', 'x9', ['135626792#3', '135626792#4']], 
76: ['w9-n1', 'R1_R2_1', ['135626792#6']], 
77: ['w7-s7', 'x36', ['OrigionW7']], 
78: ['w7-s7', 'x53', ['135626788#1', '135626788#2', '135626788#3', '135626760', '38869999#0']], 
79: ['w7-s7', 'x34', ['38869999#1']], 
80: ['w7-s7', 'x54', ['68313224#0']], 
81: ['w7-s7', 'x55', ['68313224#1']], 
82: ['w7-s7', 'R1_R3_4', ['68313224#2']],
83: ['w5-w9', 'x56', ['OrigionW5']], 
84: ['w5-w9', 'x23', ['-100323308#10']], 
85: ['w5-w9', 'x57', ['68313226#0']], 
86: ['w5-w9', 'x58', ['68313226#1', '68313226#2']], 
87: ['w5-w9', 'x59', ['68313226#3']], 
88: ['w5-w9', 'x26', ['68313226#4', '135626782', '135626769#0', '135626769#1', '135626769#2']], 
89: ['w5-w9', 'x60', ['135626769#3']], 
90: ['w5-w9', 'x38', ['95775639#0']], 
91: ['w5-w9', 'x61', ['DestinationW9']]
}

s_R1={
's0': 'R1_Junction16_2', 
's1': 'R1_Junction13_3',
's2': 'R1_Junction10_2',
's3': 'R1_Junction17_2',
's4': 'R1_Junction9_1', 
's5': 'R1_Junction8_1',
's6': 'R1_Junction7_1',
's7': 'R1_Junction7_3', 
's8': 'R1_Junction3_3',
's9': 'R1_Junction1_1', 
's10': 'R1_Junction15_2', 
's11': 'R1_Junction7_2',  
's12': 'R1_Junction1_3', 
's13': 'R1_Junction11_2',  
's14': 'R1_Junction13_4', 
's15': 'R1_Junction13_1',
's16': 'R1_Junction15_1',
's17': 'R1_Junction2_3', 
's18': 'R1_Junction3_1',
's19': 'R1_Junction18_1',
's20': 'R1_Junction12_2',
's21': 'R1_Junction16_1',
's22': 'R1_Junction2_1', 
's23': 'R1_Junction1_2',
's24': 'R1_Junction3_2', 
's25': 'R1_Junction15_3',
's26': 'R1_Junction13_2', 
's27': 'R1_Junction12_1',
's28': 'R1_Junction11_1',
's29': 'R1_Junction10_1',
's30': 'R1_Junction9_2',  
's31': 'R1_Junction5_2',
's32': 'R1_Junction2_2',
's33': 'R1_Junction4_2',
's34': 'R1_Junction8_2',
's35': 'R1_Junction4_1',
's36': 'R1_Junction5_1',
's37': 'R1_Junction17_1',  
's38': 'R1_Junction18_2'}


y_R1={
###PathID="s2-n7"
'y0': ["s2-n7",'R1_Junction16', '2', 2, 'x0', 'x1', 1],
'y1': ["s2-n7",'R1_Junction13', '3', 2, 'x1', 'x2', 1],
##PathID="s4-n5"
'y2': ["s4-n5",'R1_Junction10', '2', 1, 'x3', 'x4 x5', 1],
'y3': ["s4-n5",'R1_Junction17', '2', 1, 'x4 x5', 'x6', 1],
##PathID="s5-e6"
'y4': ["s5-e6",'R1_Junction9', '1', 1, 'x7', 'x8', 1],
'y5': ["s5-e6",'R1_Junction8', '1', 1, 'x8', 'x9', 0.5],
'y6': ["s5-e6",'R1_Junction7', '1', 1, 'x9', 'R1_R2_1', 0.5],
##PathID="s6-w5"
'y7': ["s6-w5",'R1_Junction7', '3', 1, 'x10', 'x11 x12 x13', 0.5], 
##PathID="s7-n4"
'y8':["s7-n4",'R1_Junction7', '3', 1, 'x10', 'x11 x12 x14', 0.5],
'y9':["s7-n4",'R1_Junction3', '3', 2, 'x11 x12 x14', 'x15',1],
'y10':["s7-n4",'R1_Junction1', '1', 1, 'x15', 'x16',1],
'y11': ["s7-n4",'R1_Junction15', '2', 1, 'x16', 'x17',1],
##PathID="n1-s6"
'y12': ["n1-s6",'R1_Junction7', '2', 1, 'x18', 'R1_R3_5',1], 
##PathID="n3-s7"
'y13': ["n3-s7",'R1_Junction1', '3', 1, 'x20', 'x21',1], 
'y14': ["n3-s7",'R1_Junction3', '3', 2, 'x21', 'x22 x23 x24',1], 
'y15': ["n3-s7",'R1_Junction7', '3', 2, 'x22 x23 x24', 'R1_R3_5',1], 
###PathID="n5-w3"
'y16': ["n5-w3",'R1_Junction17', '2', 1, 'x25', 'x26 x27',1], 
'y17': ["n5-w3",'R1_Junction11', '2', 1, 'x26 x27', 'R1_R3_1',1], 
##PathID="n7-s3"
'y18': ["n7-s3",'R1_Junction13', '4', 2, 'x28', 'x29',1], 
'y19': ["n7-s3",'R1_Junction16', '2', 2, 'x29', 'R1_R3_2',0.5], 
##PathID="n6-e5"
'y20': ["n6-e5",'R1_Junction13', '1', 1, 'x30', 'x31',1], 
'y21': ["n6-e5",'R1_Junction15', '1', 1, 'x31', 'x32',1], 
'y22': ["n6-e5",'R1_Junction1', '1', 1, 'x32', 'x33',1], 
'y23': ["n6-e5",'R1_Junction2', '3', 1, 'x33', 'x34 x35',1], 
'y24': ["n6-e5",'R1_Junction3', '1', 1, 'x34 x35', 'R1_R2_2',1], 
##PathID="w7-s2"
'y25': ["w7-s2",'R1_Junction18', '1', 1, 'x36 x37', 'x38',1], 
'y26': ["w7-s2",'R1_Junction12', '2', 1, 'x38', 'R1_R3_3',1], 
## PathID="w2-n6"
'y27': ["w2-n6",'R1_Junction16', '1', 2, 'x39', 'x1',1],
'y28': ["w2-n6",'R1_Junction13', '3', 1, 'x1', 'x40',1], 
###PathID="e3-n3"
'y29': ["e3-n3",'R1_Junction3', '1', 1, 'x41', 'x42',1], 
'y30': ["e3-n3",'R1_Junction2', '1', 1, 'x42', 'x43',1],
'y31': ["e3-n3",'R1_Junction1', '2', 2, 'x43', 'x44',0.5], 
###PathID="e1-w5"
'y32': ["e1-w5",'R1_Junction3', '2', 1, 'x41', 'x22 x13',1], 
##PathID="n4-w2"
'y33': ["n4-w2",'R1_Junction15', '3', 1, 'x45', 'x46',1], 
'y34': ["n4-w2",'R1_Junction13', '2', 1, 'x46', 'x29',1], 
'y35': ["n4-w2",'R1_Junction16', '2', 2, 'x29', 'R1_R3_2',0.5], 
###PathID="w9-n3"
'y36': ["w9-n3",'R1_Junction12', '1', 2, 'x47', 'x48',0.5], 
'y37': ["w9-n3",'R1_Junction11', '1', 2, 'x48', 'x49',0.5], 
'y38': ["w9-n3",'R1_Junction10', '1', 2, 'x49', 'x50',0.5], 
'y39': ["w9-n3",'R1_Junction9', '2', 1, 'x50', 'x51',1], 
'y40': ["w9-n3",'R1_Junction5', '2', 2, 'x51', 'x52',1], 
'y41': ["w9-n3",'R1_Junction2', '2', 2, 'x52', 'x43',1], 
'y42': ["w9-n3",'R1_Junction1', '2', 2, 'x43', 'x44',0.5], 
###PathID="w9-n1"
'y43': ["w9-n1",'R1_Junction12', '1', 2, 'x47', 'x48',0.5], 
'y44': ["w9-n1",'R1_Junction11', '1', 2, 'x48', 'x49',0.5], 
'y45': ["w9-n1",'R1_Junction10', '1', 2, 'x49', 'x50',0.5], 
'y46': ["w9-n1",'R1_Junction9', '2', 1, 'x50', 'x8',1], 
'y47': ["w9-n1",'R1_Junction8', '1', 1, 'x8', 'x9', 0.5],
'y48': ["w9-n1",'R1_Junction7', '1', 1, 'x9', 'R1_R2_1', 0.5],  
#### PathID="w7-s7"
'y49': ["w7-s7",'R1_Junction2', '1', 1, 'x36 x53', 'x34 x54',1], 
'y50': ["w7-s7",'R1_Junction4', '2', 1, 'x34 x54', 'x55',1], 
'y51': ["w7-s7",'R1_Junction8', '2', 1, 'x55', 'R1_R3_4',1],
#### PathID="w5-w9"
'y52': ["w5-w9",'R1_Junction4', '1', 1, 'x56 x23 x57', 'x58',1], 
'y53': ["w5-w9",'R1_Junction5', '1', 1, 'x58', 'x59',1], 
'y54': ["w5-w9",'R1_Junction17', '1', 1, 'x59', 'x26 x60',1], 
'y55': ["w5-w9",'R1_Junction18', '2', 1, 'x26 x60', 'x38',1], 
'y56': ["w5-w9",'R1_Junction12', '2', 1, 'x38', 'x61',1]
}


# ## generate the x_variable
# i = 0
# x_path_R1 = defaultdict(list)
# for j in xrange(len(y_R1)):	
# 	links = y_R1['y'+str(j)][4].split()
# 	for link in links:
# 		x_path_R1[i].append(y_R1['y'+str(j)][0])
# 		x_path_R1[i].append(link)
# 		x_path_R1[i].append(States_R1[link])
# 		i+=1
# 	if j<len(y_R1)-1 and y_R1['y'+str(j)][0]!=y_R1['y'+str(j+1)][0]:
# 		links = y_R1['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R1[i].append(y_R1['y'+str(j)][0])
# 			x_path_R1[i].append(link)
# 			x_path_R1[i].append(States_R1[link])
# 			i+=1
# 	elif j==len(y_R1)-1:
# 		links = y_R1['y'+str(j)][5].split()
# 		for link in links:
# 			x_path_R1[i].append(y_R1['y'+str(j)][0])
# 			x_path_R1[i].append(link)
# 			x_path_R1[i].append(States_R1[link])
# 			i+=1



States_R1 = {
'x0': ['135626776#6', '135626776#7'], 
'x1': ['162259820#0', '162259820#1', '162259820#2', '104758675', '104758670', '104758678#0'], 
'x2': ['104758678#1'], 
'x3': ['70438941#5'],
'x4': ['70438941#6'],
'x5': ['-135626769#0', '-135626782', '-68313226#4'],
'x6': ['DestinationN5'],
'x7': ['492981118#0'],  
'x8': ['135626792#2'], 
'x9': ['135626792#3', '135626792#4'],
'x10': ['100323308#6', '100323308#7', '100323308#8'],
'x11': ['100323308#9'],
'x12': ['100323308#10'],
'x13': ['DestinationW5'],
'x14': ['100323308#11'],
'x15': ['100323308#12', '72084632', '72084610', '85711505#0'],
'x16': ['85711505#1'],
'x17': ['DestinationN4'],
'x18': ['-135626792#6'],
'R1_R3_5': ['-100323308#8', '-100323308#7','-100323308#6'],
'x20': ['OrigionN3'],
'x21': ['-85711505#0', '-72084610', '-72084632', '-100323308#12'],
'x22': ['-100323308#11'],
'x23': ['-100323308#10'],
'x24': ['-100323308#9'],
'x25': ['OrigionN5'],
'x26': ['68313226#4', '135626782', '135626769#0','135626769#1','135626769#2'],
'x27': ['253924914#2'],
'x28': ['OrigionN7', '44578496#3'],
'x29': ['104758666','104758664', '104758665', '104758667#0', '104758667#1', '104758667#2'],
'x30': ['OrigionN6','-85711505#4'],
'x31': ['-85711505#2'],   
'x32': ['-85711505#1'],
'x33': ['473715122#1', '253924912', '253924916'],
'x34': ['38869999#1'],
'x35': ['38869999#2'],
'x36': ['OrigionW7'],
'x37': ['253924913'],
'x38': ['95775639#0'],
'x39': ['240833369#1'],
'x40': ['85711505#4','DestinationN6'],
'x41': ['-38869999#3'],
'x42': ['-38869999#2','-38869999#1'],
'x43': ['-253924916','-253924912','-473715122#1'],
'x44': ['DestinationN3'], 
'x45': ['OrigionN4'],
'x46': ['85711505#2'],
'x47': ['OrigionW9'],
'x48': ['240833369#4'],
'x49': ['240833369#5','240833369#6'],
'x50': ['240833369#7','135626758', '135626792#0', '135626792#1'],
'x51': ['492981118#1'], 
'x52': ['492981118#2'],
'x53': ['135626788#1', '135626788#2', '135626788#3', '135626760', '38869999#0'],
'x54': ['68313224#0'],
'x55': ['68313224#1'], 
'x56': ['OrigionW5'],
'x57': ['68313226#0'], 
'x58': ['68313226#1','68313226#2'],
'x59': ['68313226#3'], 
'x60': ['135626769#3'], 
'x61': ['DestinationW9'],
'R1_R2_1':['135626792#6'],
'R1_R2_2':['38869999#3'],
'R1_R3_1':['253924914#3'],
'R1_R3_2':['162259815#0','162259815#1','162259815#2'],
'R1_R3_3':['95775639#1','95775639#2'],
'R1_R3_4':['68313224#2']
}






x_len = len(x_R1)
s_len = len(s_R1)
y_len = len(y_R1)

tc = 6

EqCons = 1000 ## the number of equition constraints
x_Eq = np.zeros((EqCons,x_len*tc))
s_Eq = np.zeros((EqCons,s_len*tc))
y_Eq = np.zeros((EqCons,y_len*tc))
v_Eq = np.zeros((EqCons,s_len*tc))
e_Eq = np.zeros((EqCons,s_len*tc))
b_Eq = np.zeros(EqCons)

IneqCons = 1000 ## the number of equition constraints
x_Ineq = np.zeros((IneqCons,x_len*tc))
s_Ineq = np.zeros((IneqCons,s_len*tc))
y_Ineq = np.zeros((IneqCons,y_len*tc))
v_Ineq = np.zeros((IneqCons,s_len*(tc-1)))
e_Ineq = np.zeros((EqCons,s_len*(tc-1)))
b_Ineq = np.zeros(IneqCons)

# print x_len,s_len,y_len



### Equition constraints 
yo_Mat = np.eye(tc)
yi_Mat = -np.eye(tc)
x_Mat = np.zeros((tc,tc))
x_Mat[0,0]=1
for i in range(1,tc):
	x_Mat[i,i-1]=-1
	x_Mat[i,i]=1
# print yi_Mat,yo_Mat,x_Mat

#####generate PathInput and PathWeight
# PathInput = defaultdict(list)
# PathWeight = defaultdict(lambda:1)
# for i in range(y_len):
# 	if i in [0,2,4,7,8,12,13,16,18,20,25,27,29,32,33,36,43,49,52]:
# 		name = y_R1['y'+str(i)][0]
# 		PathWeight[name]=1
# 		InputLink = y_R1['y'+str(i)][4].split()
# 		for link in InputLink:
# 			for key in States_R1.keys():
# 				if link==key:
# 					PathInput[name]+=States_R1[key]
# print PathInput,PathWeight

PathInput={
's4-n5': ['70438941#5'], 
's7-n4': ['100323308#6', '100323308#7', '100323308#8'], 
'n5-w3': ['OrigionN5'], 
'e1-w5': ['-38869999#3'], 
'n1-s6': ['-135626792#6'], 
'n7-s3': ['OrigionN7', '44578496#3'], 
's5-e6': ['492981118#0'], 
's2-n7': ['135626776#6', '135626776#7'], 
'w2-n6': ['240833369#1'], 
'n4-w2': ['OrigionN4'], 
'n3-s7': ['OrigionN3'], 
'w7-s7': ['OrigionW7', '135626788#1', '135626788#2', '135626788#3', '135626760', '38869999#0'], 
's6-w5': ['100323308#6', '100323308#7', '100323308#8'], 
'w9-n3': ['OrigionW9'], 
'w7-s2': ['OrigionW7', '253924913'], 
'e3-n3': ['-38869999#3'], 
'n6-e5': ['OrigionN6', '-85711505#4'], 
'w9-n1': ['OrigionW9'], 
'w5-w9': ['OrigionW5', '-100323308#10', '68313226#0']}

PathWeight={
's4-n5': 1, 's7-n4': 1, 'n5-w3': 1, 'e1-w5': 1, 'n1-s6': 1, 'n7-s3': 1, 's5-e6': 1, 's2-n7': 1, 
'w2-n6': 1, 'n4-w2': 1, 'n3-s7': 1, 'w7-s7': 1, 's6-w5': 1, 'w9-n3': 1, 'w7-s2': 1, 'e3-n3': 1, 
'n6-e5': 1, 'w9-n1': 1, 'w5-w9': 1}



##0: the input number of vehicles through the first link (estimated demand)
##1: the total number of vehicles in all the links (initial value)
PathInputValue = defaultdict(lambda:[0]*2)
PathInputValue['s2-n7']=[0,1] 

########################################################### Equition constraints flow conservation ############################################
#### Path1
#'y0': ["s2-n7",'R1_Junction16', '2', 2, 'x0', 'x1'],
# x0(k+1)=x0(k)+d_R3_R1(k)-y0(k)
# xL = 0
# yoL = 0
# x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
# y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
# b_Eq[row*tc:(row+1)*tc] = PathInputValue['s2-n7'][0]*np.ones(tc)
# b_Eq[row*tc] += PathInputValue['s2-n7'][1]
# row += 1

xL = 0
yoL = 0
yiL = 0
row = 0
for j in range(y_len):
	temp = y_R1['y'+str(j)] 
	links = temp[4].split()
	path = temp[0]
	if j in [0,2,4,7,8,12,13,16,18,20,25,27,29,32,33,36,43,49,52]:
		for i in range(x_len):
			if x_R1[i][0]==path and x_R1[i][1] in links:
				xL = i 
				x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat				
		yoL = j				
		y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
		b_Eq[row*tc:(row+1)*tc] = PathInputValue[path][0]*np.ones(tc)
		b_Eq[row*tc] += PathInputValue[path][1]
		row += 1
	else:
		for i in range(x_len):
			if x_R1[i][0]==path and x_R1[i][1] in links:
				xL = i 
		yoL = j
		yiL = j-1
		x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
		y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
		y_Eq[row*tc:(row+1)*tc,yiL*tc:(yiL+1)*tc] = yi_Mat
		b_Eq[row*tc:(row+1)*tc] = np.zeros(tc)
		row += 1

########################################################## Equition constraints for signals##########################################################
###get junction name
sone_Mat = np.eye(tc)
ssum_Mat = np.ones(tc)
Junction_name = []
for junction in s_R1.values():
	Junction_name.append(junction[:-2])
Junction_name=set(Junction_name)
# print Junction_name

###junction phase label--{junction name{pahsesequence:label}}
JpL = defaultdict(dict) 
for junction in Junction_name:	 
	for i in xrange(s_len):
		name = s_R1['s'+str(i)][:-2]
		if name==Junction:
			PhaseSequence = int(s_R1['s'+str(i)][-1])
			JpL[name][PhaseSequence]=i 
	################ only one phase can be activated at one time
	for pL in JpL[junction].values():
		s_Eq[row*tc:(row+1)*tc,pL*tc:(pL+1)*tc] = sone_Mat
	b_Eq[row*tc:(row+1)*tc] = np.ones(tc)
	row+=1

############## the sum of the signal phase equal to tc #############
row = row*tc
for junction in JpL.keys():
	for pL in junction.values():
		s_Eq[row,pL*tc:(pL+1)*tc] = np.ones(tc)
	b_Eq[row] = tc
	row+=1


########################################################### Equition constraints for auxilary variables ########################################
saturationflow = 0.5*period
InitVehNum_x_R1 = defaultdict(lambda:0)
InitCoefficient= defaultdict(lambda:0)
for i in range(s_len):
	junction = s_R1['s'+str(i)][:-2]
	pahsesequence = s_R1['s'+str(i)][-1]
	
	for j in range(y_len):
		temp = y_R1['y'+str(j)]
		if temp[1]==junction and temp[2]==pahsesequence:
			path = temp[0]
			lane_num = temp[3]
			uplinks = temp[4].split()
			downlinks = temp[5].split()
			ratio = temp[6]
			coeff = PathWeight[path]*ratio*saturationflow*lane_num
			for k in range(x_len):
				if path==x_R1[k][0] and x_R1[k][1] in uplinks:
					xL=k
					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = coeff*np.eye(tc-1)	
					InitCoefficient[i]=InitCoefficient[i]+coeff*InitVehNum_x_R1[xL]
						
				elif path==x_R1[k][0] and x_R1[k][1] in downlinks:
					xL=k
					x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = -1*coeff*np.eye(tc-1)
					InitCoefficient[i]=InitCoefficient[i]-coeff*InitVehNum_x_R1[xL]
					
	eL = i
	e_Eq[row:row+tc-1,eL*(tc-1):(eL+1)*(tc-1)]=-1*np.eyes(tc-1)
	b_Eq[row:row+tc-1] = np.zeros(tc-1)
	row = row+tc-1

print row
#############################################################################################################################
################################################ Inequition constraints #################################################
row = 0

################################### minimum function ###############################
for i in range(y_len):
	yL = i
	temp = y_R1['y'+str(j)]
	path = temp[0]
	junction = temp[1]
	pahsesequence = temp[2]
	lane_num = temp[3]
	uplinks = temp[4].split()	
	ratio = temp[6]
	## -x+y<=0
	InitVehNum = 0
	for k in range(x_len):
		if path==x_R1[k][0] and x_R1[k][1] in uplinks:
			xL=k
			InitVehNum = InitVehNum + InitVehNum_x_R1[xL] ##initial time of control
			x_Ineq[row+1:row+tc,xL*tc:(xL+1)*tc-1] = -1*np.eye(tc-1)	
	
	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
	b_Ineq[row] = InitVehNum
	b_Ineq[row+1:row+tc]=np.zeros(tc)
	row = row+tc

	## -c*s*r+y<=0
	for j in range(s_len):
		if s_R1['s'+str(j)] == junction+'_'+pahsesequence:
			sL = j
			coeff = saturationflow*lane_num*ratio
			s_Ineq[row:row+tc,sL*tc:(sL+1)*tc]=-1*coeff*np.eye(tc)
	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
	b_Ineq[row:row+tc]=np.zeros(tc)
	row = row+tc


############################# auxilary constraints ################################
emin = -1000
emax = 1000
for j in range(s_len):
	sL = j 
	## -v+emin*s<=0
	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=emin*np.eye(tc-1)
	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
	b_Ineq[row:row+tc-1]=np.zeros(tc-1)
	row=row+tc-1

	## v-emax*s<=0
	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=-1*emax*np.eye(tc-1)
	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
	b_Ineq[row:row+tc-1]=np.zeros(tc-1)
	row=row+tc-1

	## v-e+emax(1-s)>=0
	## -v+e+emax*s<=emax
	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=emax*np.eye(tc-1)
	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
	e_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
	b_Ineq[row:row+tc-1]=emax*np.ones(tc-1)
	row=row+tc-1

	## v-e+emin(1-s)<=0
	## v-e-emin*s<=-emin
	s_Ineq[row:row+tc-1,sL*tc+1:(sL+1)*tc]=-1*emin*np.eye(tc-1)
	v_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=np.eye(tc-1)
	e_Ineq[row:row+tc-1,sL*(tc-1):(sL+1)*(tc-1)]=-1*np.eye(tc-1)
	b_Ineq[row:row+tc-1]=-!*emin*np.ones(tc-1)
	row=row+tc-1

##################### -y<0 #######################################
for i in range(y_len):
	yL = i 
	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc]=-1*np.eye(tc)
	b_Ineq[row:row+tc]=np.zeros(tc)
	row=row+tc

##################### 0<=x<xmax #######################################
for i in range(x_len):
	xL = i 

	### -x<=0
	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=-1*np.eye(tc)
	b_Ineq[row:row+tc]=np.zeros(tc)
	row=row+tc

	### x<=xmax
	links = x_R1[i][2]
	occup=0
	for link in links:
		occup+=Occupy[link]
	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=np.eye(tc)
	b_Ineq[row:row+tc]=occup*np.ones(tc)
	row=row+tc

print row


#########################################################################################################################
####################################################### Objective function ###############################################
f = np.zeros((x_len+y_len+s_len*3)*tc)
fweight = 10


##### Combine
## varibale x-y-s-e-v
Aeq = np.hstack((x_Eq,y_Eq,s_Eq,e_Eq,v_Eq))
Aineq = np.hstack((x_Ineq,y_Ineq,s_Ineq,e_Ineq,v_Ineq))
		


			
















