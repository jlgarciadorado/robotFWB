#Robot for web browsing based on Selenium
#OUT: 	outfile.log, visits records
#	  	outfile.pcap, traffic DNS generated, concurrently execute, eg: tcpdump -i eth0 udp port 53 -w outfile.pcap 
#INPUT:	list_of_websites, webs to visit
#		PARAMETERS

import random
import time
import math
import datetime
from selenium import webdriver
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#PARAMETERS
outfile_name='./outfile.log'
list_of_websites="./example.webs"
revisitation=0.5
visit_time_mean=120
web_updates_mean=5
users_sessions=5
num_visits_mean=15
num_web_visits_history=25
num_web_visits_history_ini=5
timeoutwebpage=60
SO='F' # SO='C'

web_visited_counter=0
f = os.popen('ifconfig eth0 | grep "inet" | cut -d: -f2 | cut -d" " -f1')
ip_aux=f.read()
ip=ip_aux.split("\n")[0]
f.close()

webs_visited=[]
outfile_name2=outfile_name +'-'+ip +'-' +str(int(time.mktime(datetime.datetime.now().timetuple()))) +'-'+str(revisitation)+'-'+str(visit_time_mean)+'-'+str(web_updates_mean)+'-'+str(users_sessions)+'-'+str(num_visits_mean)+'-'+str(num_web_visits_history)+'.txt'
outfile=open(outfile_name2, 'w+',0)
outfile.write('#IP user browser visitNum date time UnixTime(UTC) random Nweb_to_visit typeWeb website revisitation visiting_time\n')
  
infile = open(list_of_websites)
webs_aux = infile.readlines()
infile.close()
webs_aux = [x for x in webs_aux if not x.startswith('#')]
webs_aux = map(lambda s: s.strip(), webs_aux)
webs = map(lambda s: (s.split())[0],webs_aux)
tipowebs = map(lambda s: (s.split())[1],webs_aux)

for k in range(users_sessions):
    if SO == 'C':  
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") 
    else:
	driver = webdriver.Firefox()
  
    driver.set_page_load_timeout(timeoutwebpage)      
    print 'User session',k
    print datetime.datetime.now()

    num_visits=int(math.ceil(random.expovariate(1./num_visits_mean)))
    for i in range(num_visits):      
        print 'Num. visit ',i
        print datetime.datetime.now()  
        aleat=random.random()
        if aleat<=revisitation or len(webs_visited)<num_web_visits_history_ini:
            nweb_to_visit=int((random.random()*len(webs)))
            print 'Web to visit:', webs[nweb_to_visit]
            web_to_visit=webs[nweb_to_visit]
            tipoweb_to_visit=tipowebs[nweb_to_visit]       
            
            webs_visited.append(nweb_to_visit)
            if(len(webs_visited)>num_web_visits_history):
                del webs_visited[0]            
        else:
            nweb_to_visit_axu=int(random.random()*len(webs_visited))
            nweb_to_visit=webs_visited[nweb_to_visit_axu]
            print 'Web to visit:',webs[nweb_to_visit]
            web_to_visit=webs[nweb_to_visit]
            tipoweb_to_visit=tipowebs[nweb_to_visit]  
    
	web_visited_counter=web_visited_counter+1
        web_to_visit='http://www.'+web_to_visit
	web_updates=int(math.ceil(random.expovariate(1./web_updates_mean)))
        for j in range(web_updates): 
            time_of_visit=random.expovariate(1./visit_time_mean)
            print 'time_of_visit', time_of_visit   
            try:
                driver.get(web_to_visit)
            except:                             
                exit
            
            print 'Web visited:',web_to_visit,' time:' ,  j
            aux=datetime.datetime.now()
            line=ip;            
            line+=' '
            line+=str(k);
            line+=' '
            line+=SO;
            line+=' '
            line+=str(i);
            line+=' '
            line+=aux.strftime("%Y-%m-%d %H:%M");
            line+=' '
            line+=str(int(time.mktime(aux.timetuple())))
            line+=' '
            line+=str(round(aleat,2))
            line+=' '
            line+=str(nweb_to_visit)
            line+=' '
            line+=tipoweb_to_visit            
            line+=' '
            line+=web_to_visit   
            line+=' '
            line+=str(j)
            line+=' '
            line+=str(round(time_of_visit,2))
            line+='\n'
            print line
            outfile.write(line)

            time.sleep(time_of_visit)
            
    driver.close()  
    webs_visited=[]

outfile.close()

