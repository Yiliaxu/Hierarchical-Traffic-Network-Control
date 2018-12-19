import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc


Chj_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_junction_label.net.xml')
NetRoot = Chj_net.getroot()

def get_region(node):
	region = 'R0'
	for junction in NetRoot.findall('junction'):
		if junction.get('id')==node:
			region = junction.get('Region')
	return region

for edge in NetRoot.findall('edge'):
	down_node = edge.get('to')
	region = get_region(down_node)
	edge.set('Region',region)

Chj_net.write('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_edge_label.net.xml')
