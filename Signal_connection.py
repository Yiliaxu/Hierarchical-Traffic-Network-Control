import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc


Chj_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj-with-tls.net.xml')
NetRoot = Chj_net.getroot()

tls_node = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\tls-node.nod.xml')
TLSRoot = tls_node.getroot()

Signal_connection_files = doc.Document()
TLSconnections = Signal_connection_files.createElement('TLSconnections')
Signal_connection_files.appendChild(TLSconnections)


for node in TLSRoot.findall('node'):
	node_id = node.get('id')
	CtrlNode = Signal_connection_files.createElement('Intersection')
	CtrlNode.setAttribute('id',node_id)
	i = 0
	for connection in NetRoot.findall('connection'):
		if connection.get('tl')==node_id:
			
			movement = Signal_connection_files.createElement('connection')
			movement.setAttribute('dir',connection.get('dir'))
			movement.setAttribute('from',connection.get('from'))
			# movement.setAttribute('fromLane',connection.get('fromLane'))
			movement.setAttribute('linkIndex',connection.get('linkIndex'))
			# movement.setAttribute('state',connection.get('state'))
			# movement.setAttribute('tl',connection.get('tl'))
			movement.setAttribute('to',connection.get('to'))
			# movement.setAttribute('toLane',connection.get('toLane'))
			CtrlNode.appendChild(movement)
			i = i+1
	CtrlNode.setAttribute('linknum',str(i))
	TLSconnections.appendChild(CtrlNode)

fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSconnections1.xml','w')
	
try:
	Signal_connection_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 