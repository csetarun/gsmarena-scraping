import pyexcel as pe
import json
import re
from bs4 import BeautifulSoup
import requests
records=pe.get_records(file_name='Book1.xlsx')
nums=[]
rg_url=re.compile('in\/[a-z][a-z0-9-_]*/',re.I)
fi=open('final.txt','w')
patterns={'memory':['(\\d+ GB)','(\\d+GB)','(\\d+MB)'],'battery':['(\\d+mAh)','(\\d+ mAh)','(\\d+mAH)'],'camera':['(\\d+MP)','(\\d+ MP)','(\\d+MP )'],'processor':['(\\d+ GHZ)','(\\d+GHZ)','(Snapdragon\\s+.*?\\s+.*?)','(Mediatek\\s+.*?\\s+.*?)'],'resolution':['(\\d+ x \\d+)','(\\d+x\\d+)'],'color':['black','red','white','orange','cyan','oramge','grey','silver']}
found={'memory':[],'battery':[],'camera':[],'processor':[],'resolution':[],'color':[]}
def check(mode,spec):
        for i in mode:
                if i in spec:
                        return True
        return False
def distance(a,b,x):
        if((a not in x) or (b not in x)):
                return len(x)
        start=x.find(a)
        end=x.find(b)
        if start>end:start,end=end,start
        return(len(x[start+len(a):end].split()))
def output(string,link):
	#string=string.encode(encoding="utf-8", errors="ignore")
        refined={'memory':[],'battery':[],'camera':[],'processor':[],'resolution':[],'color':[]}
        front=['front','secondary']
        rear=['rear','primary']
        ram=['RAM'];internal=['internal']
        data=string.split("\n")
        for sentence in data:
                sentence=sentence.strip()
                for key in patterns:
                        for reg in patterns[key]:
                                val_reg=re.compile(reg,re.IGNORECASE&re.DOTALL)
                                if (re.search(val_reg,sentence)):
                                        found[key].append(sentence)
                                        refined[key].extend(re.findall(val_reg,sentence))
        for key in refined:
                refined[key]=[i.strip() for i in refined[key]]
                refined[key]=list(set(refined[key]))
                found[key]=list(set(found[key]))

        for sen in found['camera']:
                for value in refined['camera']:
                        for index in range(len(front)):
                                       spl=len(sen)
                                       if (distance(front[index],value,sen)<distance(rear[index],value,sen)):
                                               refined['front']=value
                                       elif(distance(front[index],value,sen)==spl and (distance(rear[index],value,sen)==spl)):
                                               pass
                                       else:
                                                refined['rear']=value
        del refined['camera']
        for sen in found['memory']:
                for value in refined['memory']:
                        for index in range(len(ram)):
                                       spl=len(sen)
                                       if (distance(ram[index],value,sen)<distance(internal[index],value,sen)):
                                               refined['RAM']=value
                                       elif(distance(ram[index],value,sen)==spl and (distance(internal[index],value,sen)==spl)):
                                               pass
                                       else:
                                                refined['Internal']=value
        del refined['memory']
        for i in refined:
                if (type(refined[i])==list):
                        if(len(refined[i])==0):
                                refined[i]='None'
                        else:
                                refined[i]=refined[i][0].encode('ascii')
                else:
                        refined[i]=refined[i].encode('ascii')
        if not(refined.get('RAM')):refined['RAM']='None'
        if not(refined.get('Internal')):refined['Internal']='None'
        if not(refined.get('rear')):refined['rear']='None'
        if not(refined.get('front')):refined['front']='None'
        return refined
        #refined['link']=link
       #with open('data.txt', 'a') as outfile:
            #json.dump(refined, outfile)
def scrap(link):
    user_agent = {'User-agent': 'Chrome/39.0.2171.95'}
    data=requests.get(link,headers=user_agent)
    soups=BeautifulSoup(data.content)
    feat=0
    for di in soups.find_all('div',{'class':'a-container'}):
        for dis in di.find_all('div',{'class':'feature'}):
                for k in dis.find_all('div',{'id':'feature-bullets'}):
                        for i in k.find_all('ul',{'class':'a-vertical a-spacing-none'}):
                                feat=i.text

    soup=BeautifulSoup(data.content,'html5lib')
    dis=soup.select('#productDescription > div.aplus')
    if(dis and feat):
            req=str(dis[0])
            soup2=BeautifulSoup(req)
            for i in soup2.find_all('p'):
                    feat=feat+i.text.encode('ascii','ignore')
            for i in soup2.find_all('h4'):
                    feat=feat+i.text.encode('ascii','ignore')
    #print output(feat,link)
    if(feat):
            return output(feat,link)
    else:
             return 'None'
        
for i in range(len(records)):
                a=records[i]['amazon_url'].encode('ascii')
                f=re.findall(rg_url,a)
                if(f):
                        print f[0]
                        fi.write(f[0][3:-1])
                        fi.write('\n')
                dic=scrap(a) if(a!='a' and 'amazon' in a) else 'None'
                if (dic!='None'):
                        wri_me=dic['RAM']+'\t'+str(records[i]['ram_memory'])+'\n'+dic['Internal']+'\t'+str(records[i]['internal_memory'])+'\n'+dic['battery']+'\t'+str(records[i]['battery_capacity'])+'\n'
                        wri_me=wri_me+dic['front']+'\t'+str(records[i]['front_camera_resolution'])+'\n'+dic['rear']+'\t'+str(records[i]['primary_camera_resolution'])+'\n'+dic['processor']+'\t'+str(records[i]['processor_type'])+'\n'+dic['resolution']+'\t'+str(records[i]['display_resolution'])+'\n'+dic['color']+'\t'+str(records[i]['available_colors'])
                        fi.write(wri_me)
                        fi.write('\n\n\n')
                else:
                        fi.write('No URL')
                        fi.write('\n\n\n')
                        
fi.close()
