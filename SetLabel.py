import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
from collections import defaultdict
import pickle


PathCtrl_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\PathsControlled.xml')
PathCtrlRoot = PathCtrl_net.getroot()

Label_files = doc.Document()
Variable = Label_files.createElement('Variable')
Label_files.appendChild(Variable)
Link=Label_files.createElement('Link')
Phase =Label_files.createElement('Phase')

i = 1 ## route number
j = 1 ## phase number
Region = PathCtrlRoot.find('R3')
# Region = PathCtrlRoot
for route in Region.iter('route'):
	edges = route.get('Path').split()
	CombinedLink = []
	for edge in edges:
		if edge[3:6]!='Jun':
			CombinedLink.append(edge)
		else:
			link = Label_files.createElement('variable')
			link.setAttribute('id','x'+str(i))
			i+=1
			link.setAttribute('IncludeLinks',' '.join(CombinedLink))
			CombinedLink = []
			Link.appendChild(link)
			junction = Label_files.createElement('variable')
			junction.setAttribute('id','s'+str(j))
			j+=1
			junction.setAttribute('JunctionID',edge)
			MovementNum=0
			for connection in route.findall('connection'):
				if connection.get('JunctionID')==edge:
					MovementNum+=1
					index = connection.get('PhaseIndex')
			junction.setAttribute('index',index)
			junction.setAttribute('LanesNum',str(MovementNum))
			Phase.appendChild(junction)

Variable.appendChild(Link)
Variable.appendChild(Phase)



fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Label.xml','w')
	
try:
	Label_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 


Variables = defaultdict()
i = 0 ## route number
j = 0 ## phase number
for route in Region.iter('route'):
	edges = route.get('Path').split()
	JunctionNum = 0
	for edge in edges:
		if 'Junction' in edge:
			JunctionNum+=1
	# print JunctionNum
	CombinedLink = []
	Jnum = 1
	flag=0
	for num,edge in enumerate(edges,start=0):
		if edge[3:6]!='Jun':
			CombinedLink.append(edge)
		elif edge[3:6]=='Jun' and Jnum<JunctionNum:
			Jnum+=1
			if CombinedLink not in Variables.values():
				for label,clink in Variables.items():
					if set(clink).issubset(set(CombinedLink)):
						flag=1
						Variables[label]=CombinedLink
				if flag==0:
					Variables['x'+str(i)]=CombinedLink
					i+=1
				else:
					flag=0
			CombinedLink=[]
			for connection in route.findall('connection'):
				if connection.get('JunctionID')==edge:
					index = connection.get('PhaseIndex')
			if edge+'_'+index not in Variables.values():
				Variables['s'+str(j)]=edge+'_'+index
				j+=1
		elif edge[3:6]=='Jun' and Jnum==JunctionNum:
			if CombinedLink not in Variables.values():
				for label,clink in Variables.items():
					if set(clink).issubset(set(CombinedLink)):
						flag=1
						Variables[label]=CombinedLink
				if flag==0:
					Variables['x'+str(i)]=CombinedLink
					i+=1
				else:
					flag=0
			CombinedLink=[]
			for connection in route.findall('connection'):
				if connection.get('JunctionID')==edge:
					index = connection.get('PhaseIndex')
			if edge+'_'+index not in Variables.values():
				Variables['s'+str(j)]=edge+'_'+index
				j+=1
			CombinedLink = edges[num+1:]
			# print CombinedLink
			if CombinedLink not in Variables.values() and CombinedLink!=[]:
				Variables['x'+str(i)]=CombinedLink
				i+=1
			CombinedLink = []

print Variables

Connection = defaultdict(list)
k=0 ## connection number 
MovementNum = 0
for route in Region.iter('route'):
	edges = route.get('Path').split()
	for edge in edges:
		if edge[3:6]=='Jun':
			for connection in route.findall('connection'):
				if connection.get('JunctionID')==edge:
					MovementNum+=1
					index = connection.get('PhaseIndex')
					uplink = connection.get('from')
					downlink = connection.get('to')
			attri=[0]*5
			attri[0] = edge
			attri[1] = index
			attri[2] = MovementNum 
			for label,link in Variables.items():
				if label[0]=='x' and uplink in link:
					attri[3]=label
				if label[0]=='x' and downlink in link:
					attri[4]=label
			Connection['y'+str(k)]=attri
			k+=1
			MovementNum = 0
		
print Connection,k

filename = 'Network_variables.sav'
pickle.dump(Variables, open(filename,'wb'))
filename = 'Network_connections.sav'
pickle.dump(Connection, open(filename,'wb'))
