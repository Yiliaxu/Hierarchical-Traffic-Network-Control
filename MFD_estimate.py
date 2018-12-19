import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import numpy as np 
import matplotlib.pyplot as plt
import pdb
from sklearn import datasets, linear_model
import pickle


# Chj_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.net.xml')
# NetRoot = Chj_net.getroot()

# Loops = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops.xml')
# LoopRoot = Loops.getroot()

#### find the valid detectors
# ValidLoop = {'R1':[],"R2":[],"R3":[]}
# for loop in LoopRoot.findall('inductionLoop'):
# 	loop_id = loop.get('id')
# 	for interval in DetectorRoot.iter('interval'):
# 		if loop_id==interval.get('id') and interval.get("nVehContrib")!="0":
# 			ValidLoop[loop_id[0:2]].append(loop_id[2:])
# 			break


ValidLoop = {'R1':['-100323308#10_0', '-100323308#10_1', '-100323308#11_0', '-100323308#11_1', '-100323308#12_0', '-100323308#12_1', '-100323308#7_0', '-100323308#7_1', '-100323308#8_0', '-100323308#8_1', '-100323308#9_0', '-100323308#9_1', '-135626769#0_0', '-135626782_0', '-135626792#6_0', 'DestinationW9_0', '-253924912_0', '-253924912_1', '-253924916_0', '-253924916_1', '-38869999#1_0', '-38869999#2_0', '-38869999#3_0', '-473715122#1_0', '-473715122#1_1', '-68313226#4_0', '-72084610_0', '-72084632_0', '-72084632_1', '-85711505#0_0', '-85711505#1_0', '-85711505#2_0', '-85711505#4_0', '100323308#10_0', '100323308#10_1', '100323308#11_0', '100323308#11_1', '100323308#12_0', '100323308#12_1', '100323308#6_0', '100323308#6_1', '100323308#7_0', '100323308#7_1', '100323308#8_0', '100323308#8_1', '100323308#9_0', '100323308#9_1', '104758664_0', '104758664_1', '104758665_0', '104758665_1', '104758666_1', '104758666_2', '104758667#0_0', '104758667#0_1', '104758667#1_0', '104758667#1_1', '104758667#2_0', '104758667#2_1', '104758670_0', '104758670_1', '104758675_0', '104758675_1', '104758678#0_0', '104758678#0_1', '104758678#1_0', '104758678#1_1', '135626758_0', '135626758_1', '135626760_0', '135626769#0_0', '135626769#1_0', '135626769#2_0', '135626769#3_0', '135626776#6_0', '135626776#6_1', '135626776#7_0', '135626776#7_1', '135626782_0', 'OrigionW7_0', '135626788#1_0', '135626788#2_0', '135626788#3_0', '135626792#0_0', '135626792#1_0', '135626792#2_0', '135626792#3_0', '135626792#4_0', '162259815#0_0', '162259815#0_1', '162259820#0_0', '162259820#0_1', '162259820#1_0', '162259820#1_1', '162259820#2_0', '162259820#2_1', '240833369#1_0', '240833369#1_1', 'OrigionW9_0', 'OrigionW9_1', '240833369#4_0', '240833369#4_1', '240833369#5_0', '240833369#5_1', '240833369#6_0', '240833369#6_1', '240833369#7_0', '240833369#7_1', '253924912_0', '253924912_1', '253924913_0', '253924914#2_0', '253924916_0', '253924916_1', '38869999#0_0', '38869999#1_0', '38869999#2_0', '44578496#3_0', '44578496#3_1', '473715122#1_0', '492981118#0_0', '492981118#0_1', '492981118#1_1', '492981118#2_0', '492981118#2_1', '68313224#0_0', '68313224#1_0', '68313226#0_0', '68313226#1_0', '68313226#2_0', '68313226#3_0', '68313226#4_0', '70438941#5_0', '70438941#6_0', '72084610_0', '72084610_1', '72084632_0', '72084632_1', '85711505#0_0', '85711505#1_0', '85711505#2_0', '85711505#4_0', '95775639#0_0', 'DestinationN3_0', 'DestinationN3_1', 'DestinationN4_0', 'DestinationN5_0', 'DestinationN6_0', 'DestinationN7_0', 'DestinationN7_1', 'DestinationW5_0', 'OrigionN3_0', 'OrigionN3_1', 'OrigionN4_0', 'OrigionN5_0', 'OrigionN6_0', 'OrigionN7_0', 'OrigionN7_1', 'OrigionW5_0'],
"R2":['-230239442_0', '-230239443#0_0', '-230239443#1_0', '-230239443#2_0', '-230239444_0', '-230239445#0_0', '-230493745#1_0', '-230493745#2_0', '-230493750#0_0', '-230493751_0', '-24626397_0', '-38867851_0', '-38869048#0_0', '-38869048#1_0', '-38869048#2_0', '-38869999#4_0', '-448953275#1_0', '-492979887#0_0', '-492979887#1_0', '-492979887#2_0', '-492979887#3_0', '-492979892_0', '-492979895#0_0', '-492979895#1_0', '-492979895#2_0', '-69555386#1_0', '-69555386#1_1', '-69555386#2_0', '-69555386#2_1', '-72084599#0_0', '-72084621_0', '135626792#6_0', '230239442_0', '230239443#0_0', '230239443#1_0', '230239443#2_0', '230239444_0', '230239445#0_0', '230493750#0_0', '230493750#1_0', '230493751_0', '230493752#0_0', '230493753_0', '24626397_0', '38869048#0_0', '38869048#1_0', '38869048#2_0', '38869048#3_0', '38869048#4_0', '38869999#3_0', '38869999#4_0', '412826784#1_0', '412826784#1_1', '412826784#2_0', '412826784#2_1', '448953275#1_0', '492979887#0_0', '492979887#1_0', '492979887#2_0', '492979887#3_0', '492979892_0', '492979895#0_0', '492979895#1_0', '492979895#2_0', '492979896#2_0', '69555386#0_0', '69555386#0_1', '69555386#1_0', '69555386#1_1', '69555386#2_0', '69555386#2_1', '72084599#0_0', '72084621_0', '93864593#0_0', '93864593#1_0', 'DestinationE1_0', 'DestinationE3_0', 'DestinationE3_1', 'DestinationE4_0', 'DestinationE5_0', 'DestinationE6_0', 'DestinationE6_1', 'DestinationN1_0', 'DestinationS8_0', 'OrigionE1_0', 'OrigionE3_0', 'OrigionE4_0', 'OrigionE5_0', 'OrigionN1_0', 'OrigionN2_0'],
"R3":['-100323308#5_0', '-100323308#5_1', '-100323308#6_0', '-100323308#6_1', '-135626763#0_0', '-135626763#1_0', '-135626767#3_0', '-135626767#3_1', '-135626767#5_0', '-135626767#5_1', '-135626767#6_0', '-135626767#6_1', '-135626767#7_0', '-135626767#7_1', '-135626787_0', '-230239447_0', '-230239447_1', '-230239448#0_0', '-230239448#0_1', '-230491007_0', '-230491007_1', 'DestinationW8_0', '-38866846#1_0', '-38866846#2_0', '-38866846#3_0', '-492979896#0_0', '-492979896#2_0', '-492981119_0', '-69555386#0_0', '-69555386#0_1', '100323308#2_0', '100323308#2_1', '100323308#3_0', '100323308#3_1', '100323308#5_0', '100323308#5_1', '135626762#0_0', '135626762#0_1', '135626762#1_0', '135626762#1_1', '135626762#2_0', '135626762#2_1', '135626763#0_0', '135626763#1_0', '135626766_0', '135626766_1', '135626767#3_0', '135626767#5_0', '135626767#5_1', '135626767#6_0', '135626767#6_1', '135626767#7_0', '135626767#7_1', '135626776#1_0', '135626776#1_1', '135626776#3_1', '135626776#4_0', '135626776#4_1', '135626776#5_0', '135626776#5_1', '135626779_0', '135626779_1', '135626780#0_0', '135626780#0_1', '135626780#1_0', '135626780#1_1', '135626780#2_0', '135626780#2_1', '135626787_0', '162259815#1_0', '162259815#1_1', '162259815#2_0', '162259815#2_1', '162259815#3_0', '162259815#3_1', '162259815#4_0', '162259815#4_1', '162259815#5_0', '162259815#5_1', '162259815#7_0', '162259815#7_1', '230239447_0', '230239447_1', '230239448#0_0', '230239448#0_1', '230491007_0', '230491007_1', '240833369#0_0', '240833369#0_1', '253924914#3_0', '253924914#4_0', '253924914#5_0', '253924914#6_0', '253924914#7_0', '253924915#0_0', '253924915#0_1', '253924915#1_0', '253924915#1_1', 'OrigionW8_0', '38866846#1_0', '38866846#2_0', '38866846#3_0', '492979883_0', '492979883_1', '492979884#0_0', '492979884#0_1', '492979884#1_0', '492979884#1_1', '492979884#3_0', '492979884#3_1', '492979884#4_0', '492979884#4_1', '492979886_0', '492979896#0_0', '492981119_0', '492981120_0', '492981120_1', '542054843#1_0', '542054843#1_1', '542054843#2_0', '542054843#2_1', '68313224#2_0', '69059186#0_0', '69059186#1_0', '69059186#2_0', '69550029#1_0', '69550029#1_1', '70438941#1_0', '70438941#2_0', '70438941#3_0', '70438941#4_0', '91568767#10_0', '91568767#10_1', '91568767#5_0', '91568767#5_1', '91568767#6_0', '91568767#6_1', '91568767#8_0', '91568767#8_1', '91568767#9_0', '91568767#9_1', '95775639#1_0', '95775639#2_0', '95775639#3_0', '95775639#4_0', '95775639#5_0', 'DestinationS1_0', 'DestinationS1_1', 'DestinationS2_0', 'DestinationS3_0', 'DestinationS3_1', 'DestinationS5_0', 'DestinationS6_0', 'DestinationS6_1', 'DestinationS7_0', 'DestinationS7_1', 'DestinationW2_0', 'DestinationW3_0', 'DestinationW3_1', 'DestinationW4_0', 'DestinationW4_1', 'OrigionS1_0', 'OrigionS2_0', 'OrigionS4_0', 'OrigionS4_1', 'OrigionS5_0', 'OrigionS6_0', 'OrigionS6_1', 'OrigionS7_0', 'OrigionS7_1', 'OrigionW2_0', 'OrigionW3_0', 'OrigionW4_0']}

LinkTypes={'R1_OUT': ['1135626792#6', '138869999#3','2-100323308#6', '2-100323308#7', '2-100323308#8', '2-240833369#1', '2162259815#0', '2162259815#1', '2162259815#2', '1230477506', '1253924914#3', '1253924914#4', '168313224#2', '195775639#1', '195775639#2','1DestinationW7', '2DestinationW9', '2DestinationN3', '1DestinationN4', '1DestinationN5', '1DestinationN6', '2DestinationN7', '1DestinationW1', '1DestinationW5'], 
'R3_OUT': ['1492979896#2', '269555386#0','1-230477506', '2100323308#6', '2100323308#7', '2100323308#8', '2135626776#6', '2135626776#7', '2240833369#1', '2492981118#0', '170438941#4', '170438941#5','1DestinationW8', '2DestinationS1', '1DestinationS2', '2DestinationS3', '1DestinationS5', '2DestinationS6', '2DestinationS7', '1DestinationW2', '2DestinationW3', '2DestinationW4', '1DestinationW6'], 
'R2_OUT': ['1-135626792#6', '1-38869999#3','1-492979896#2', '2-69555386#0','1DestinationE1', '1DestinationE2', '2DestinationE3', '1DestinationE4', '1DestinationE5', '2DestinationE6', '1DestinationN1', '2DestinationN2', '1DestinationS8']}

# pdb.set_trace()
Tsim = 3600
Tc = 60
DataSize = Tsim/Tc

Times = 10
TotalData = {"R1":np.zeros((DataSize*Times,2)),"R2":np.zeros((DataSize*Times,2)),"R3":np.zeros((DataSize*Times,2))}
TotalVehOut = {"R1":np.zeros(DataSize*Times),"R2":np.zeros(DataSize*Times),"R3":np.zeros(DataSize*Times)}


for k in range(0,Times):


	TrainData = {"R1":np.zeros((DataSize,2)),"R2":np.zeros((DataSize,2)),"R3":np.zeros((DataSize,2))}
	VehOut = {"R1":np.zeros(DataSize),"R2":np.zeros(DataSize),"R3":np.zeros(DataSize)}
	# VehNum = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Random'+str(k)+'_VehNum.xml')
	VehNum = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\VehNum'+str(k)+'.xml')

	VehNumRoot = VehNum.getroot()
	# DetectorInfo = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Random'+str(k)+'_DetInfo.xml')
	DetectorInfo = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\DetInfo'+str(k)+'.xml')

	DetectorRoot = DetectorInfo.getroot()


	for interval in DetectorRoot.iter('interval'):
		lane_id = interval.get('id')
		edge_id = lane_id[2:].split('_')[0]
		region_id = lane_id[0:2]
		begin = float(interval.get('begin'))
		if begin<Tsim:
			row = int(begin/Tc)
			flow = float(interval.get('nVehContrib'))
			
			### get the number of vehicles leaving each region
			for zone in ["R1","R2","R3"]:
				for edge in LinkTypes[zone+'_OUT']:
					temp_edge = edge[1:]
					if temp_edge==edge_id:
						VehOut[zone][row]+=flow
			

			### get the average traffic flow for regions
			for zone in ["R1","R2","R3"]:
				if region_id==zone and lane_id[2:] in ValidLoop[zone]:
					TrainData[zone][row,0]+=flow

	# Effective_LoopsNum=np.zeros((Period_Num,3))
	# for interval in DetectorRoot.iter('interval'):
	# 	lane_id = interval.get('id')
	# 	region_id = lane_id[0:2]
	# 	begin = float(interval.get('begin'))
	# 	if begin<Tsim:
	# 		row = int(begin/Tc)
	# 		flow = float(interval.get('nVehContrib'))
	# 		if region_id=="R1" and flow>0:
	# 			R1[row,0] += flow
	# 			Effective_LoopsNum[row,0]+=1
	# 		if region_id=="R2" and flow>0:
	# 			R2[row,0] += flow
	# 			Effective_LoopsNum[row,1]+=1
	# 		elif region_id=="R3" and flow>0:
	# 			R3[row,0] += flow
	# 			Effective_LoopsNum[row,2]+=1

	# for i in xrange(Period_Num):
	# 	R1[i,0]=60*R1[i,0]/Effective_LoopsNum[i,0]
	# 	R2[i,0]=60*R2[i,0]/Effective_LoopsNum[i,1]
	# 	R3[i,0]=60*R3[i,0]/Effective_LoopsNum[i,2]


	for interval in VehNumRoot.iter('interval'):
		edge_id = interval.get('id')
		region_id = edge_id[0:2]
		begin = float(interval.get('begin'))
		if begin<Tsim:
			row = int(begin/Tc)
			for zone in ["R1","R2","R3"]:
				if region_id==zone:
					TrainData[zone][row,1]+=float(interval.get('vehnum'))

	for zone in ["R1","R2","R3"]:
		TotalData[zone][k*DataSize:(k+1)*DataSize,0]=60*TrainData[zone][:,0]/len(ValidLoop[zone])
		TotalData[zone][k*DataSize:(k+1)*DataSize,1]=TrainData[zone][:,1]
		TotalVehOut[zone][k*DataSize:(k+1)*DataSize]=VehOut[zone][:]
		# print len(ValidLoop[zone])


np.save('TotalData.npy',TotalData)
np.savetxt('guanguan.txt',TotalData['R1'],fmt='%.2e')

for zone in ["R1","R2","R3"]:
	fig, ax = plt.subplots()
	ax.scatter(TotalData[zone][:,1],TotalData[zone][:,0])
	plt.title('Subregion '+zone)
	plt.xlabel('Vehicle number')
	plt.ylabel('Average traffic flow per hour')


# #####################################################################
# ############## Create linear regression object
# regr = linear_model.LinearRegression()

# # Train the model using the training sets
# for zone in ['R1','R2','R3']:
# 	Train_X = TotalData[zone][:,0]
# 	Train_Y = TotalVehOut[zone]
# 	regr.fit(Train_X.reshape((len(Train_X),1)),Train_Y.reshape((len(Train_Y),1)))
# 	print('Coefficients: \n', regr.coef_)
# 	print('Coefficients: \n', regr.intercept_ )
# 	x=np.linspace(0,500,100)

# 	# Make predictions using the testing set
# 	y_pred = regr.predict(x.reshape((len(x),1)))
# 	fig, ax = plt.subplots()
# 	ax.scatter(TotalData[zone][:,0],TotalVehOut[zone])
# 	ax.plot(x,y_pred,linewidth=2,color='r')
# 	plt.title('Subregion '+zone)



	# filename = 'LR_'+zone+'.sav'
	# pickle.dump(regr, open(filename,'wb'))




plt.show()


	




