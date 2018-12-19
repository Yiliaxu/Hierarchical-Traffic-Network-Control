from Upper_ctrl import Update_policy
import numpy as np
from scipy.stats import norm 
from scipy.stats import poisson
import matplotlib.pyplot as plt
from collections import defaultdict
import os, sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc

doc1 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSAction.xml')
ActionRoot = doc1.getroot()
doc2 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
RouteRoot = doc2.getroot()
doc3 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\loops_ctrl.xml')
LoopsRoot = doc3.getroot()
doc4 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_ctrl.net.xml')
NetRoot = doc4.getroot()
doc5 = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSconnections.xml')
PhaseRoot = doc5.getroot()

EdgeTypes = ['R1_IN','R1_OUT','R1-R2','R1-R3','R2_IN','R2_OUT','R2-R1','R2-R3','R3_IN','R3_OUT','R3-R1','R3-R2']

#### get the interregional links and the boundary links of each region
LinksTypes = defaultdict(list)
for edge in NetRoot.findall('edge'):
	edge_id = edge.get('id')
	region_id = edge.get('Region')
	between= edge.get('between')
	lanes = edge.findall('lane')
	edgeinfo = str(len(lanes))+edge_id ### the number of lanes + the edge id

	for region in ['R1','R2','R3']:
		if edge_id[0:7]=='Origion' and region_id==region:
			LinksTypes[region+'_IN'].append(edgeinfo)
		if edge_id[0:11]=="Destination" and region_id==region:
			LinksTypes[region+'_OUT'].append(edgeinfo)
		if between!=None and region_id==region:
			LinksTypes[between].append(edgeinfo)

print LinksTypes

for linktype in ['R1-R2','R1-R3','R2-R1','R2-R3','R3-R1','R3-R2']:
	for link in LinksTypes[linktype]:
		link_id = link[1:]
		for intersection in PhaseRoot.findall('Intersection'):
			intersection_id = intersection.get('id')
			region_id = intersection_id[0:2]
			for connection in intersection.findall('connection'):
				to = connection.get('to')
				phase = connection.get('phase')
				if phase!=None and region_id==linktype[0:2] and to==link_id:
					connection.set('between',linktype)

doc5.write('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\TLSconnections.xml')
