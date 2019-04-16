import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc


TLS_net = etree.parse('./TLSconnections.xml')
TLSRoot = TLS_net.getroot()



PhaseAction_files = doc.Document()
TLSAction = PhaseAction_files.createElement('TLSAction')
PhaseAction_files.appendChild(TLSAction)


for node in TLSRoot.findall('Intersection'):
	tlType = node.get('tlType')
	if tlType=='actuated':
		node_id = node.get('id')
		linknum = int(node.get('linknum'))
		CtrlNode = PhaseAction_files.createElement('Intersection')
		CtrlNode.setAttribute('id',node_id)	
		phasenum = 0
		for phase in ['1','2','3','4']:
			linkIndex=[]
			for connection in node.findall('connection'):
				if connection.get('phase')==phase:
					linkIndex.append(connection.get('linkIndex'))
			if len(linkIndex)>0:
				phasenum+=1
				action=''
				for i in xrange(linknum):
					if str(i) in linkIndex:
						action+='G'
					else:
						action+='r'
				CtrlNode.setAttribute('phase'+phase,action)
		CtrlNode.setAttribute('PhaseNum',str(phasenum))
		TLSAction.appendChild(CtrlNode)

fp = open('./TLSAction1.xml','w')
	
try:
	PhaseAction_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 