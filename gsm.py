import pyexcel as pe
import re
import requests
from bs4 import BeautifulSoup
user_agent = {'User-agent': 'Chrome/39.0.2171.95'}
#url=''
#a=requests.get(a,headers=user_agent)
#soup=BeautifulSoup(a.content)
a=open('gsm_data.txt','r').read()
soup=BeautifulSoup(a)
soup2=BeautifulSoup(str(soup.select('#specs-list > table')))
attr_arr=soup2.find_all('td',{'class':'ttl'})
val_arr=soup2.find_all('td',{'class':'nfo'})
disp=['Super AMOLED','IPS LCD','AMOLED']
def OS(text):
    ios=re.search('ios[a-z0-9-._]*',text)
    ver=re.search('v[0-9.]*',text)
    os=ios.group(0).split('ios')[1] if ios else ver.group(0)[1:]
    return os
for i in range(len(attr_arr)):
    attr=attr_arr[i].text.encode('ascii','ignore')
    val=val_arr[i].text.encode('ascii','ignore')
    prim=re.search('\\d+ MP',val)
    mem=re.findall('[0-9]* GB',val)
    if('Resolution' in attr):
        display_resolution=val.split('pixels')[0]
    elif('OS' in attr):
        version=OS(val.encode('ascii','ignore'))
    elif('Sensor' in attr):
        sensors=val
    elif('Primary' in attr):
        aper=re.search('f[0-9./]*',val)
        flash_type='LED' if('LED' in val) else 'No'
        auto_focus='Yes' if('autofocus' in val) else 'No'
        aperture=aper.group(0) if aper else 'No'
        if prim: primary_camera_resolution=prim.group(0).split('MP')[0]
    elif('Features' in attr):
        primary_camera_features=val
    elif('Secondary' in attr):
        if prim: front_camera_resolution=prim.group(0).split('MP')[0]
    elif('Radio' in attr):
        FM='Yes' if ('FM' in val) else 'No'
    elif('WLAN' in attr):
        wifi_type=val
    elif('Bluetooth' in attr):
        bluetooth_type=val
    elif('Weight' in attr):
        weight=val
    elif('Type' in attr):
        for i in disp:
            if(i in val):
                display_type=i
                break
    elif('Protection' in attr):
        screen_protection=val    
    elif('Colors' in attr):
        available_colors=val
    elif('Size' in attr):
        screen_size=val[:3]
#screen_pixel_density
    elif('USB' in attr):
        usb_type=val
    elif('SIM' in attr):
         sim_type=val
    elif('battery' in val):
        val=val.split(' ')
        non_removable_battery='Yes' if('Non' in val[0]) else 'No'
        battery_type=val[1]
        battery_capacity=val[2]
    elif('Card slot' in attr):
        expandable_memory=mem[0][:-2]
    elif('Internal' in attr):
        ram_memory=mem[1][:-3]
        internal_memory=mem[0][:-3]
    elif('GPU' in attr):
        gpu=val
    elif('Chipset' in attr):
        processor_type=val
    elif('CPU' in attr):
        cp=re.search('[0-9.]* GHz',val)
        processor_frequency=cp.group(0)[:-4]
        no_of_cores=val.split(' ')[0]
lis=['display_resolution','version','sensors','flash_type','auto_focus','aperture','primary_camera_resolution','primary_camera_features','FM','wifi_type','bluetooth_type','weight','display_type','screen_protection','available_colors','usb_type','screen_size','sim_type','non_removable_battery','battery_type','battery_capacity','expandable_memory','ram_memory','internal_memory','processor_frequency','processor_type','gpu','no_of_cores']
lis_data=[display_resolution,version,sensors,flash_type,auto_focus,aperture,primary_camera_resolution,primary_camera_features,FM,wifi_type,bluetooth_type,weight,display_type,screen_protection,available_colors,usb_type,screen_size,sim_type,non_removable_battery,battery_type,battery_capacity,expandable_memory,ram_memory,internal_memory,processor_frequency,processor_type,gpu,no_of_cores]
sheet = pe.get_sheet(file_name="gsm_data.xlsx")
sheet.row += lis
sheet.row +=lis_data
sheet.save_as("gsm_data.xlsx")
