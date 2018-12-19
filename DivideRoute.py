import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
from collections import defaultdict

Chj_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_ctrl.net.xml')
NetRoot = Chj_net.getroot()
TLS_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSconnections.xml')
TLSRoot = TLS_net.getroot()
Route_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
RouteRoot = Route_net.getroot()

CtrlPath_files = doc.Document()
PathCtrl = CtrlPath_files.createElement('PathsControlled')
CtrlPath_files.appendChild(PathCtrl)

Record = defaultdict()
for zone in ['R1','R2','R3']:
	Record[zone] = CtrlPath_files.createElement(zone)

# PathsInR1 = CtrlPath_files.createElement('R1')
# PathsInR2 = CtrlPath_files.createElement('R2')
# PathsInR3 = CtrlPath_files.createElement('R3')

for route in RouteRoot.iter('route'):
	edges = route.get('edges').split()
	route_id = route.get('id')
	# print edges
	PassZones = []
	for i in xrange(len(edges)):
		#edge[i] edge[i+1]
		for net_edge in NetRoot.iter('edge'):
			net_edge_id = net_edge.get('id')
			if edges[i]==net_edge_id:
				edge_region = net_edge.get('Region')
				PassZones.append(edge_region)
				break
	SubRecord = defaultdict()
	print list(set(PassZones))
	for zone in list(set(PassZones)):
		SubRecord[zone] = CtrlPath_files.createElement('route')

	SplitPaths = defaultdict(list)
	for i in range(len(edges)-1):
		SplitPaths[PassZones[i]].append(edges[i])
		l=0
		l1=0
		for intersection in TLSRoot.findall('Intersection'):
			for connection in intersection.findall('connection'):
				uplink = connection.get('from')
				downlink = connection.get('to')
				if uplink==edges[i] and downlink==edges[i+1]:
					intersection_id = intersection.get('id')
					region_id = intersection_id[0:2]
					if l==0:
						SplitPaths[region_id].append(intersection_id)
						l=1
					subconnection = CtrlPath_files.createElement('connection')
					subconnection.setAttribute('JunctionID',intersection_id)
					subconnection.setAttribute('dir',connection.get('dir'))
					subconnection.setAttribute('from',connection.get('from'))
					subconnection.setAttribute('PhaseIndex',connection.get('phase'))
					subconnection.setAttribute('to',connection.get('to'))
					subconnection.setAttribute('LinkIndex',connection.get('linkIndex'))
					SubRecord[region_id].appendChild(subconnection)

					if i+1==len(edges)-1 and l1==0:
						SplitPaths[PassZones[i+1]].append(edges[i+1])
						l1=1


		# SplitPaths[PassZones[i+1]].append(edges[i+1])
	for zone in list(set(PassZones)):
		SubRecord[zone].setAttribute('Path',' '.join(SplitPaths[zone]))
		SubRecord[zone].setAttribute('PathID',route_id)
		Record[zone].appendChild(SubRecord[zone])

for zone in ['R1','R2','R3']:
	PathCtrl.appendChild(Record[zone])

fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\PathsControlled.xml','w')
	
try:
	CtrlPath_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 