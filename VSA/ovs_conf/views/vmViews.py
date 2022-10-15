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

def generateVmConfiguration(request) :
    bridges = OvsBridge.objects.all()
    media_root= settings.MEDIA_ROOT    
    path = media_root+'template.xml'
    tree = ET.parse(path)
    root = tree.getroot()
    # for childs in root:
    #     print(childs.tag, childs.attrib)
    #     for child in childs:
    #         print('  '+ child.tag, child.attrib)
    #         for chil in child:
    #             print('    '+ chil.tag, chil.attrib) 
    for elements in root.iter('devices'):
        for element in elements.iter('controller'):
            for address in element.iter('address'):
                print("%s - %s" % (address.tag, address.attrib))
                #extraire les adresse PCI
                #ajouter un nouvel objet              
    return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges})



    return objects 