from re import sub
from statistics import median
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
# from rest_framework import serializers
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
import yaml
from boltons.iterutils import remap
from ovs_conf.form import DomainVmForm, MemoryVmForm,DomainVm,MemoryVm
from lxml import etree as ET
from django.conf import settings
import os
import random
from ovs_conf.views.foo import Elem


        
def generateVmConfiguration(request) :
    ## VM model

    bridges = OvsBridge.objects.all()
    # media_root= settings.MEDIA_ROOT    
    # path = media_root+'template.xml'
    # tree = ET.parse(path)
    # root = tree.getroot()
    
    ## parsing
    
    # all_objects = [*bridges, *Port.objects.all()]
    # data = media_root+'simpletemplate.xml'
    # xml = serializers.serialize("xml", all_objects)
    # print(ET.tostring(arbre,encoding='Unicode',pretty_print=True))
    
    # print(xml)    
         

               
    ## Generation d'un bus aléatoire non utilise
    # pciUsed = []
    # for element in root.iter('address'):
    #     pciUsed.append({'bus':element.get('bus'),'slot':element.get('slot')})
    
    # newBus= hex(random.randint(5,255))
    # while any(d['bus'] == newBus for d in pciUsed):
    #     newBus=hex(random.randint(5,255))
    # # print(newBus)
    
    # ## Generation random  MAC address
    
    # macUsed = []
    # for element in root.iter('mac'):
    #     macUsed.append({'address':element.get('address')})

    # # The first line is defined for specified vendor
    # mac = [ 0x54, 0x52, 0x00,
    # random.randint(0x00, 0x7f),
    # random.randint(0x00, 0xff),
    # random.randint(0x00, 0xff) ]
    # macAddress =':'.join(map(lambda x: "%02x" % x, mac))
    # while any(d['address'] == macAddress for d in macUsed):
    #     mac = [ 0x54, 0x52, 0x00,
    #     random.randint(0x00, 0x7f),
    #     random.randint(0x00, 0xff),
    #     random.randint(0x00, 0xff) ]
    #     macAddress =':'.join(map(lambda x: "%02x" % x, mac)) 
           
    # #add an interface
    # address=macAddress
    # bus=newBus
    # devices  = root.find('devices')
    # interface = ET.SubElement(devices,"interface",type="ethernet")
    # mac = ET.SubElement(interface,"mac",address=address)
    # target = ET.SubElement(interface,"target",dev="FOO.0",managed="no")
    # model = ET.SubElement(interface,"model",type="virtio")
    # pci = ET.SubElement(interface,
    #                     "address",type="pci",
    #                     domain="0x0000",
    #                     bus=bus,
    #                     slot="0x00",
    #                     function="0x0")
    # #Export to file
    # tree=ET.ElementTree(root)
    # ET.indent(tree, space="\t", level=0)
    # with open(media_root+'templateUPdated.xml', 'wb') as f:
    #     tree.write(f,encoding="utf-8")
    # #print (ET.tostring(root))
    
    if request.method == 'POST':
        domainVm = DomainVmForm(request.POST,prefix='domain')
        memoryVm = MemoryVmForm(request.POST,prefix='memory')
        print("reçu!")
        print(request.POST)
        
        
        if domainVm.is_valid() and memoryVm.is_valid(): 
            print('valid')
            memory = memoryVm.cleaned_data
            # print(memory
                #   )
            domain = domainVm.save()
            #recuperer l'id du domaine pour le passer aux éléments
            domain_id = getattr(domain,'id')
            #mise en BD
            memory = memoryVm.save(commit=False)
            memory.vm = DomainVm.objects.get(pk=domain_id)
            memory.save()

            response = HttpResponse(
            content_type='text-plain')
            response['Content-Disposition'] = 'attachment; filename=ovsConf.yml'
            response.writelines(generateVm(domain))
            return response
        else:
            domainVm = DomainVmForm(prefix='one')    

    else:
        domainVm = DomainVmForm(prefix='domain')  
        memoryVm = MemoryVmForm(prefix='memory')
    return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges,'domainVm':domainVm,'memoryVm':memoryVm})

def generateVm(domain):
    #generation du fichier de configuration de la VM
    ele = Elem('domain')
    ele.attributes['type'] = domain.attr_type
    # ele.text = domain.text_name

    
    # query the database
    child = []
    memory = MemoryVm.objects.filter(vm=domain)
    print(memory)
    for mem in memory:
        print('yo')
        subele = Elem('memory')
        subele.text = str(mem.text_memory)
        ele.children.append(subele)
        print(ele.children[0].name)
        
    root = ele.serialFirst()
    # root = ele.serialFirst
    return ET.tostring(root,encoding='Unicode',pretty_print=True)
    
    
    