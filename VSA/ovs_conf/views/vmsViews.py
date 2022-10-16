from statistics import median
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
import yaml
from boltons.iterutils import remap
from ovs_conf.form import BridgeForm, BridgeFormSelect, PortForm, BridgeFormRo,PortFormAdd  
from lxml import etree as ET
from django.conf import settings
import os
import random

def generateVmConfiguration(request) :
    bridges = OvsBridge.objects.all()
    media_root= settings.MEDIA_ROOT    
    path = media_root+'template.xml'
    tree = ET.parse(path)
    root = tree.getroot()
           
    ## Generation d'un bus aléatoire non utilise
    pciUsed = []
    for element in root.iter('address'):
        pciUsed.append({'bus':element.get('bus'),'slot':element.get('slot')})
    
    newBus= hex(random.randint(5,255))
    while any(d['bus'] == newBus for d in pciUsed):
        newBus=hex(random.randint(5,255))
    # print(newBus)
    
    ## Generation random  MAC address
    
    macUsed = []
    for element in root.iter('mac'):
        macUsed.append({'address':element.get('address')})

    # The first line is defined for specified vendor
    mac = [ 0x54, 0x52, 0x00,
    random.randint(0x00, 0x7f),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff) ]
    macAddress =':'.join(map(lambda x: "%02x" % x, mac))
    while any(d['address'] == macAddress for d in macUsed):
        mac = [ 0x54, 0x52, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
        macAddress =':'.join(map(lambda x: "%02x" % x, mac)) 
           
    #add an interface
    address=macAddress
    bus=newBus
    devices  = root.find('devices')
    interface = ET.SubElement(devices,"interface",type="ethernet")
    mac = ET.SubElement(interface,"mac",address=address)
    target = ET.SubElement(interface,"target",dev="FOO.0",managed="no")
    model = ET.SubElement(interface,"model",type="virtio")
    pci = ET.SubElement(interface,
                        "address",type="pci",
                        domain="0x0000",
                        bus=bus,
                        slot="0x00",
                        function="0x0")
    #Export to file
    tree=ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    with open(media_root+'templateUPdated.xml', 'wb') as f:
        tree.write(f,encoding="utf-8")
    #print (ET.tostring(root))
        
    return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges,'pciUsed':pciUsed})



    return objects 