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
    ### check for existing already taken bus
    ##exemple of PCI device{'type': 'pci', 'domain': '0x0000', 'bus': '0x06', 'slot': '0x00', 'function': '0x0'}
    pciUsed = []
    for element in root.iter('address'):
        pciUsed.append({'bus':element.get('bus'),'slot':element.get('slot')})        
            # print("%s - %s" % (element.get('bus'),element.get('slot')))
    
    #add an interface
    address="52:54:00:11:19:22"
    bus="0x08"
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
    print (ET.tostring(root))
    # root.write(media_root+'templateUpdated.xml')
        
    return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges,'pciUsed':pciUsed})



    return objects 