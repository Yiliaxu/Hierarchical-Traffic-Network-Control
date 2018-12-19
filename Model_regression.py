import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import numpy as np 
import matplotlib.pyplot as plt
import pdb
import GPy
import pickle


path = os.getcwd()
TotalData = np.load(path+'\\TotalData.npy').item()

for zone in ["R1","R2","R3"]:
	fig, ax = plt.subplots()
	ax.scatter(TotalData[zone][:,1],TotalData[zone][:,0])
	plt.title('Subregion '+zone)
	plt.xlabel('Vehicle number')
	plt.ylabel('Average traffic flow per hour')


# plt.show()

for zone in ["R1","R2","R3"]:#,]:

	Train_X = TotalData[zone][:,1]
	Train_Y = TotalData[zone][:,0]

	k=GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.) # + GPy.kern.Bias(1)
	m=GPy.models.GPRegression(Train_X.reshape((len(Train_X),1)),Train_Y.reshape((len(Train_Y),1)),k)

	# m=GPy.models.GPRegression(np.array(x).reshape((len(x),1)),np.array(y).reshape((len(x),1)),k)
	m.optimize()
	m.plot()
	# # Mesh the input space for evaluations of the real function, the prediction and
	# # its MSE np.max(TotalData[zone][:,1])
	x = np.linspace(0,3000,1000)
	y_pred, var=m.predict(x.reshape((len(x),1)))
	sigma = np.sqrt(var)

	# # Plot the function, the prediction and the 95% confidence interval based on
	# # the MSE
	plt.figure()
	plt.scatter(Train_X, Train_Y,label=u'Observations')
	plt.plot(x, y_pred, 'b-', label=u'Prediction')
	plt.fill(np.concatenate([x, x[::-1]]),
	         np.concatenate([y_pred - 1.9600 * sigma,
	                        (y_pred + 1.9600 * sigma)[::-1]]),
	         alpha=.5, fc='b', ec='None', label='95% confidence interval')
	plt.xlabel('$x$')
	plt.ylabel('$f(x)$')
	plt.ylim(0,np.max(Train_Y)+100)
	xlim = {"R1":2825,"R2":1400,"R3":3200}
	plt.xlim(0,xlim[zone])
	plt.legend(loc='upper left')
	plt.title('Subregion '+zone)

	##save the model to the disk
	# filename = 'MFD_'+zone+'.sav'
	# pickle.dump(m, open(filename,'wb'))

	# model = pickle.load(open('MFD_R1.sav','rb'))
	# x=np.array([100])
	
	# y_pre, var = model.predict(x.reshape((len(x),1)))

	# print y_pre,var


plt.show()