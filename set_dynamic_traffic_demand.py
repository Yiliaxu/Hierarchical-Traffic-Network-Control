import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import random

period_num = 1
period = 3600
demand_level = 8

# Flow_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
# FlowRoot = Flow_net.getroot()

Flow_net = etree.parse('./Chj_final.rou.xml')
FlowRoot = Flow_net.getroot()

DynamicFlows_files = doc.Document()
DynamicFlows = DynamicFlows_files.createElement('flows')
DynamicFlows_files.appendChild(DynamicFlows)

routes = DynamicFlows_files.createElement('routes')
for route in FlowRoot.iter('route'):
	for i in xrange(period_num):
		route_copy = DynamicFlows_files.createElement('route')
		route_copy.setAttribute('edges',route.get('edges'))
		route_copy.setAttribute('id',route.get('id')+'_'+str(i))
		routes.appendChild(route_copy)
DynamicFlows.appendChild(routes)	

for i in xrange(period_num):
	interval = DynamicFlows_files.createElement('interval')
	start = i*period
	end = (i+1)*period
	interval.setAttribute('begin',str(start))
	interval.setAttribute('end',str(end))
	for flow in FlowRoot.iter('flow'):
		flow_copy = DynamicFlows_files.createElement('flow')
		flow_copy.setAttribute('from',flow.get('from'))
		flow_copy.setAttribute('id',flow.get('id')+'_'+str(i))
		traffic_demand = period*float(flow.get('number'))/3600
		traffic_demand = int(traffic_demand)*(i+demand_level)
		# traffic_demand = random.randint(400,1200)
		flow_copy.setAttribute('number',str(traffic_demand))
		flow_copy.setAttribute('to',flow.get('to'))
		flow_copy.setAttribute('route',flow.get('route')+'_'+str(i))
		interval.appendChild(flow_copy)
	DynamicFlows.appendChild(interval)




# fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_Dynamic.rou.xml','w')
fp = open('./Chj_Dynamic.rou.xml','w')
	
try:
	DynamicFlows_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 