import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc


Chj_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_ctrl.net.xml')
NetRoot = Chj_net.getroot()

loops_files = doc.Document()
addition = loops_files.createElement('additional')
loops_files.appendChild(addition)


for edge in NetRoot.findall('edge'):	
	region = edge.get('Region')
	edge_id = edge.get('id') 
	connection = edge.get('between')
	for lane in edge.findall('lane'):
		lane_id = lane.get('id')
		loop = loops_files.createElement('inductionLoop')
		loop.setAttribute('id',region+lane_id)
		if connection!=None:
			loop.setAttribute('position',connection)
		elif edge_id[0:7]=="Origion":
			loop.setAttribute('position','BoundaryIn')
		elif edge_id[0:11]=="Destination":
			loop.setAttribute('position','BoundaryOut')
		else:
			loop.setAttribute('position','Inside')
		loop.setAttribute('ForRoads',edge_id)
		loop.setAttribute('lane',lane_id)
		loop.setAttribute('pos','5')
		loop.setAttribute('freq','60')
		loop.setAttribute('file','DetInfo.xml')
		addition.appendChild(loop)

fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops_ctrl.xml','w')
	
try:
	loops_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 