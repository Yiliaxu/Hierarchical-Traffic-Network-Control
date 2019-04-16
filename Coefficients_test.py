import numpy as np 
from collections import defaultdict
from NetLabels import *

class Coefficients():
	def __init__(self,region,tc,period,PathWeights,PathInputValue,ObjWeight,InitVehNum_x,LinksOccupy_x,Action,Interval):
		self.region = region
		self.x = NetInfoX[region]
		self.y = NetInfoY[region]
		self.s = NetInfoS[region]
		self.links = NetLinks[region]
		self.tc = tc
		self.period = period
		self.xlen = len(self.x)
		self.ylen = len(self.y)
		self.slen = len(self.s)
		self.PathWeights = PathWeights
		self.ObjWeight = ObjWeight
		self.PathInput = PathInputValue
		self.InitVehNum_x = InitVehNum_x
		self.LinksOccupy_x = LinksOccupy_x
		self.action_interval = Interval

		if region=='R1':
			self.action_constraints={'R1_R2':Action[0],'R1_R3':Action[1]}
		elif region=='R2':
			self.action_constraints={'R2_R1':Action[2],'R2_R3':Action[3]}
		elif region=='R3':
			self.action_constraints={'R3_R1':Action[4],'R3_R2':Action[5]}

		self.saturationflow = 0.8 * self.period



		# print self.xlen,self.ylen,self.slen


	#############################################################################################################################
	################################################ Equition constraints #################################################			
	def EqCoeff(self):
		tc = self.tc
		EqCons = 2000 ## the number of equition constraints
		x_Eq = np.zeros((EqCons,self.xlen*tc))
		s_Eq = np.zeros((EqCons,self.slen*tc))
		y_Eq = np.zeros((EqCons,self.ylen*tc))
		v_Eq = np.zeros((EqCons,self.slen*(self.tc-1)))
		e_Eq = np.zeros((EqCons,self.slen*(self.tc-1)))
		b_Eq = np.zeros(EqCons)

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

		row = 0
		yo_Mat = np.eye(tc)
		yi_Mat = -np.eye(tc)
		x_Mat = np.zeros((tc,tc))
		x_Mat[0,0]=1
		for i in range(1,tc):
			x_Mat[i,i-1]=-1
			x_Mat[i,i]=1
		
		xL = 0
		yoL = 0
		yiL = 0		
		for j in range(self.ylen):

			temp = self.y['y'+str(j)]
			links = temp[4].split()
			path = temp[0]
			if j in FirstMovement[self.region]:
				for i in range(self.xlen):
					if self.x[i][0]==path and self.x[i][1] in links:
						xL = i
						x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
				yoL = j
				y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
				b_Eq[row*tc:(row+1)*tc] = self.PathInput[path][0]*np.ones(tc)
				b_Eq[row*tc] += self.PathInput[path][1]
				row += 1
			else:
				for i in range(self.xlen):
					if self.x[i][0]==path and self.x[i][1] in links:
						xL = i
						x_Eq[row*tc:(row+1)*tc,xL*tc:(xL+1)*tc] = x_Mat
				yoL = j
				yiL = j-1
				y_Eq[row*tc:(row+1)*tc,yoL*tc:(yoL+1)*tc] = yo_Mat
				y_Eq[row*tc:(row+1)*tc,yiL*tc:(yiL+1)*tc] = yi_Mat
				b_Eq[row*tc:(row+1)*tc] = np.zeros(tc)
				row += 1

		########################################################## Equition constraints for signals##########################################################
		###get junction name
		sone_Mat = np.eye(tc)
		ssum_Mat = np.ones(tc)
		Junction_name = []
		for junction in self.s.values():
			Junction_name.append(junction[:-2])
		Junction_name=set(Junction_name)
		# print Junction_name

		###junction phase label--{junction name{pahsesequence:label}}
		JpL = defaultdict(dict) 
		for junction in Junction_name:	 
			for i in xrange(self.slen):
				name = self.s['s'+str(i)][:-2]
				if name==junction:
					PhaseSequence = int(self.s['s'+str(i)][-1])
					JpL[name][PhaseSequence]=i 
			################ only one phase can be activated at one time
			for pL in JpL[junction].values():
				s_Eq[row*tc:(row+1)*tc,pL*tc:(pL+1)*tc] = sone_Mat
			b_Eq[row*tc:(row+1)*tc] = np.ones(tc)
			row+=1



		############## the sum of the signal phase equal to tc #############
		row = row*tc
		for junction in JpL.values():
			for pL in junction.values():
				s_Eq[row,pL*tc:(pL+1)*tc] = np.ones(tc)
			b_Eq[row] = tc
			row+=1


		########################################################### Equition constraints for auxilary variables ########################################

		
		InitCoefficient= defaultdict(lambda:0)
		for i in range(self.slen):

			junction = self.s['s'+str(i)][:-2]
			pahsesequence = self.s['s'+str(i)][-1]

			for j in range(self.ylen):
				temp = self.y['y'+str(j)]
				if temp[1]==junction and temp[2]==pahsesequence:
					path = temp[0]
					lane_num = temp[3]
					uplinks = temp[4].split()
					downlinks = temp[5].split()
					ratio = temp[6]
					coeff = self.PathWeights[self.region][path]*ratio*self.saturationflow*lane_num
					for k in range(self.xlen):
						if path==self.x[k][0] and self.x[k][1] in uplinks:
							xL=k
							x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = coeff*np.eye(tc-1)
							InitCoefficient[i]=InitCoefficient[i]+coeff*self.InitVehNum_x[xL]

						elif path==self.x[k][0] and self.x[k][1] in downlinks:
							xL=k
							x_Eq[row:row+tc-1,xL*tc:(xL+1)*tc-1] = -1*coeff*np.eye(tc-1)
							InitCoefficient[i]=InitCoefficient[i]-coeff*self.InitVehNum_x[xL]

			eL = i
			e_Eq[row:row+tc-1,eL*(tc-1):(eL+1)*(tc-1)]=-1*np.eye(tc-1)
			b_Eq[row:row+tc-1] = np.zeros(tc-1)
			row = row+tc-1

		self.InitCoefficient = InitCoefficient


		return x_Eq[0:row,:],y_Eq[0:row,:],s_Eq[0:row,:],e_Eq[0:row,:],v_Eq[0:row,:],b_Eq[0:row],row

	#############################################################################################################################
	################################################ Inequition constraints #################################################
	def IneqCoeff(self):

		tc = self.tc
		IneqCons = 2000 # the number of equition constraints
		x_Ineq = np.zeros((IneqCons,self.xlen*self.tc))
		s_Ineq = np.zeros((IneqCons,self.slen*self.tc))
		y_Ineq = np.zeros((IneqCons,self.ylen*self.tc))
		v_Ineq = np.zeros((IneqCons,self.slen*(self.tc-1)))
		e_Ineq = np.zeros((IneqCons,self.slen*(self.tc-1)))
		b_Ineq = np.zeros(IneqCons)
		# slack_Ineq = np.zeros((IneqCons,2))

		
		row = 0

		################################### minimum function ###############################
		for i in range(self.ylen):
			yL = i
			temp = self.y['y'+str(i)]
			path = temp[0]
			junction = temp[1]
			pahsesequence = temp[2]
			lane_num = temp[3]
			uplinks = temp[4].split()
			ratio = temp[6]
			## -x+y<=0
			InitVehNum = 0
			for k in range(self.xlen):
				if path==self.x[k][0] and self.x[k][1] in uplinks:
					xL=k
					InitVehNum = InitVehNum + self.InitVehNum_x[xL] ##initial time of control
					x_Ineq[row+1:row+tc,xL*tc:(xL+1)*tc-1] = -1*np.eye(tc-1)

			y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
			b_Ineq[row] = InitVehNum
			b_Ineq[row+1:row+tc]=np.zeros(tc-1)
			row = row+tc

		for i in range(self.ylen):
			#if i!=16:
			yL = i
			temp = self.y['y'+str(i)]
			path = temp[0]
			junction = temp[1]
			pahsesequence = temp[2]
			lane_num = temp[3]
			uplinks = temp[4].split()
			ratio = temp[6]
			## -c*s*r+y<=0
			for j in range(self.slen):
				if self.s['s'+str(j)] == junction+'_'+pahsesequence:
					sL = j
					coeff = self.saturationflow*lane_num*ratio
					s_Ineq[row:row+tc,sL*tc:(sL+1)*tc]=-1*coeff*np.eye(tc)
			y_Ineq[row:row+tc,yL*tc:(yL+1)*tc] =np.eye(tc)
			b_Ineq[row:row+tc]=np.zeros(tc)
			row = row+tc


		############################# auxilary constraints ################################
		emin = -1000000
		emax = 1000000
		for j in range(self.slen):
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
			b_Ineq[row:row+tc-1]=-1*emin*np.ones(tc-1)
			row=row+tc-1



        ###############################signal inequation constraints##################################################
		##s1+s3-s2<1
		temp = np.array([[1,-1,1,0,0,0],[0,1,-1,1,0,0],[0,0,1,-1,1,0],[0,0,0,1,-1,1],[1,-1,0,1,0,0],[0,1,-1,0,1,0],[0,0,1,-1,0,1,],[1,-1,0,0,1,0],[0,1,-1,0,0,1],[1,-1,0,0,0,1]])
		num = len(temp)
		for j in xrange(self.slen):
			sL = j
			s_Ineq[row:row+num,sL*tc:(sL+1)*tc]=temp
			b_Ineq[row:row+num]=np.ones(num)
			row = row+num

		#### sum(s)>1
		for j in xrange(self.slen):
			sL = j
			s_Ineq[row,sL*tc:(sL+1)*tc]=-1*np.ones((1,tc))
			b_Ineq[row]=-1
			row = row+1

		############################# constraints from upper level #######################################
		# connections = self.action_constraints.keys()
		# for i, connection in enumerate(connections):
		# 	if connection=='R1_R2':
		# 		action_interval = self.action_interval[0]
		# 	elif connection=='R1_R3':
		# 		action_interval = self.action_interval[1]
		# 	elif connection=='R2_R1':
		# 		action_interval = self.action_interval[2]
		# 	elif connection=='R2_R3':
		# 		action_interval = self.action_interval[3]
		# 	elif connection=='R3_R1':
		# 		action_interval = self.action_interval[4]
		# 	elif connection=='R3_R2':
		# 		action_interval = self.action_interval[5]

		# 	for j in range(self.ylen):
		# 		temp = self.y['y' + str(j)]
		# 		downlinks = temp[5]
		# 		if connection in downlinks:
		# 			yL = j
		# 			#### y1+y2+y3-d<=(action+interval)
		# 			y_Ineq[row + 2*i, yL * tc:(yL + 1) * tc] = np.ones(tc)
		# 			slack_Ineq[row + 2*i,0]=-1
		# 			b_Ineq[row + 2*i] = self.action_constraints[connections[i]] + action_interval
		# 			#### -y1-y2-y3-c<=-(action-interval)
		# 			y_Ineq[row + 2*i+1, yL * tc:(yL + 1) * tc] = -1*np.ones(tc)
		# 			slack_Ineq[row + 2 * i+1, 1] = -1
		# 			b_Ineq[row + 2 * i+1] = action_interval - self.action_constraints[connections[i]]



		# row = row + len(connections)*2

		# return x_Ineq[0:row, :], y_Ineq[0:row, :], s_Ineq[0:row, :], e_Ineq[0:row, :], v_Ineq[0:row, :], b_Ineq[0:row], slack_Ineq[0:row,:], row
		return x_Ineq[0:row, :], y_Ineq[0:row, :], s_Ineq[0:row, :], e_Ineq[0:row, :], v_Ineq[0:row, :], b_Ineq[0:row], row




		# ##################### -y<0 #######################################
		# for i in range(self.ylen):
		# 	yL = i 
		# 	y_Ineq[row:row+tc,yL*tc:(yL+1)*tc]=-1*np.eye(tc)
		# 	b_Ineq[row:row+tc]=np.zeros(tc)
		# 	row=row+tc

		# ##################### 0<=x<xmax #######################################
		# for i in range(self.xlen):
		# 	xL = i 

		# 	### -x<=0
		# 	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=-1*np.eye(tc)
		# 	b_Ineq[row:row+tc]=np.zeros(tc)
		# 	row=row+tc

		# 	### x<=xmax			
		# 	x_Ineq[row:row+tc,xL*tc:(xL+1)*tc]=np.eye(tc)
		# 	b_Ineq[row:row+tc]=self.LinksOccupy_x[i]*np.ones(tc)
		# 	row=row+tc





	#########################################################################################################################
	####################################################### Objective function ###############################################
	def ObjCoeff(self):
		### max
		tc = self.tc

		x_obj = np.zeros(tc*self.xlen)
		for i in range(self.xlen):
			path = self.x[i][0]
			temp = -1*self.PathWeights[self.region][path]*self.ObjWeight/self.LinksOccupy_x[i]
			x_obj[i*tc:(i+1)*tc]=temp*np.ones(tc)
	
		y_obj = np.ones(tc*self.ylen) ### maxmize y

		s_obj = np.zeros(tc*self.slen)
		for i in range(self.slen): 
			s_obj[i*tc]=self.InitCoefficient[i]

		e_obj = np.ones((tc-1)*self.slen)

		v_obj = np.zeros((tc-1)*self.slen)
		# slack_obj = -1*np.ones(2)

		return x_obj,y_obj,s_obj,e_obj,v_obj#,slack_obj
		



		
		


			




