import os,sys
import xml.etree.ElementTree as etree
import xml.dom.minidom as doc
import random

 
demand_level = 5

# Flow_net = etree.parse('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_final.rou.xml')
# FlowRoot = Flow_net.getroot()

sumocfg = etree.parse('./chj.sumocfg')
CfgRoot = sumocfg.getroot()

Sumocfg_files = doc.Document()
sumocfg = Sumocfg_files.createElement('configuration')
Sumocfg_files.appendChild(sumocfg)

inputs = Sumocfg_files.createElement('input')
netfile = Sumocfg_files.createElement('net-file')
netfile.setAttribute('value',"Chj_final.net.xml")
inputs.appendChild(netfile)
routefile = Sumocfg_files.createElement('route-files')
routefile.setAttribute('value',"Chj_Demand"+str(demand_level)+".rou.xml")
inputs.appendChild(routefile)
additionalfile = Sumocfg_files.createElement('additional-files')
additionalfile.setAttribute('value',"loops.xml")
inputs.appendChild(additionalfile)
sumocfg.appendChild(inputs)

time = Sumocfg_files.createElement('time')
begin = Sumocfg_files.createElement('begin')
begin.setAttribute('value','0')
time.appendChild(begin)
end = Sumocfg_files.createElement('end')
end.setAttribute('value','3600')
time.appendChild(end)
sumocfg.appendChild(time)

outputs = Sumocfg_files.createElement('output')
queueoutput = Sumocfg_files.createElement('queue-output')
queueoutput.setAttribute('value','FTCqueue'+str(demand_level)+".xml")
outputs.appendChild(queueoutput)
summary = Sumocfg_files.createElement('summary')
summary.setAttribute('value','FTCsummary'+str(demand_level)+".xml")
outputs.appendChild(summary)
tripinfo = Sumocfg_files.createElement('tripinfo-output')
tripinfo.setAttribute('value','FTCtripinfo'+str(demand_level)+".xml")
outputs.appendChild(tripinfo)
sumocfg.appendChild(outputs)


report = Sumocfg_files.createElement('report')
xmlvalidation = Sumocfg_files.createElement('xml-validation')
xmlvalidation.setAttribute('value','never')
report.appendChild(xmlvalidation)
duration = Sumocfg_files.createElement('duration-log.disable')
duration.setAttribute('value','true')
report.appendChild(duration)
nostep = Sumocfg_files.createElement('no-step-log')
nostep.setAttribute('value','true')
report.appendChild(nostep)
sumocfg.appendChild(report)


# fp = open('D:\\Journal_paper\\hierarchical control based on Markov decision process and path-based signal control\\simulation\\Chj_Dynamic.rou.xml','w')
fp = open('./fixchj'+str(demand_level)+'.sumocfg','w')
	
try:
	Sumocfg_files.writexml(fp,indent='\t', addindent='\t',newl='\n',encoding="utf-8")
except:
	trackback.print_exc() 
finally: 
	fp.close() 