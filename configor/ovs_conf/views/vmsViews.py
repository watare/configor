import re
from statistics import median
from sys import prefix
from xml.etree.ElementTree import SubElement
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from ovs_conf.form import VmForm,PortFormSelect
# from rest_framework import serializers
from ovs_conf.models import Port,SubEleModel,OvsBridge
import yaml
from boltons.iterutils import remap
from lxml import etree as ET
from django.conf import settings
import os
import random
from ovs_conf.views.other_functions import Elem
from django.forms import formset_factory

def is_valid_macaddr802(value):
    allowed = re.compile(r"""
                         (
                             ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                            |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                         )
                         """,
                         re.VERBOSE|re.IGNORECASE)

    if allowed.match(value) is None:
        return False
    else:
        return True

def generateVmConfiguration(request):
    bridges = OvsBridge.objects.all()
    # fundtion permettant d'enregistrer un nouvel element dans la BD en prenant en compte la hierarchisation 
    def subEle(subname,parent=None,text=None,**kwargs):
        sub = SubEleModel.objects.createSub(subname,parent=parent,text=text,**kwargs)
        sub.save()
        return sub
    
    ## Selection des bons réseaux 
    
    ports = Port.objects.all()
    PortList = []
    for port in ports:
        bridgeName = port.bridge.name
        PortList.append(
            
            {'bridge': bridgeName,'name':port,'select':''})
    # print(fList)
    
    Formset = formset_factory(PortFormSelect,extra=0)
       
   
    
    
    ## generation du fichier XML
    if request.method == 'POST':
        form = VmForm(request.POST,prefix='vm')
        formset = Formset(request.POST,prefix='formset')
        
        ## creation des bridges
        reqDic = dict(request.POST)
        if form.is_valid() :
            form = form.cleaned_data
            porttoSet = []
            for i in range(0,int(reqDic['formset-TOTAL_FORMS'][0])):
                if ('formset-'+str(i)+'-select') in reqDic:
                    porttoSet.append({'port':Port.objects.get(name=reqDic['formset-'+str(i)+'-name'][0]),'mac':reqDic['formset-'+str(i)+'-mac'][0]})
            print(porttoSet)
            
             ## template initial XML
            domain = subEle('domain',type='kvm')   
            
            os = subEle('os',parent=domain)
            subEle('type',parent=os,text='hvm',arch="x86_64",machine="pc-q35-3.1")
            subEle('boot',parent=os,dev="hd")
            
            features = subEle('features',parent=domain)
            subEle('acpi',parent=features)
            subEle('apic',parent=features)
            
            cpu = subEle('cpu',parent=domain,mode="host-model",match="exact", check="full")
            clock = subEle('clock',parent=domain,offset="utc")
            subEle('timer',parent=clock,name="rtc",tickpolicy="catchup")
            subEle('timer',parent=clock,name="pit",tickpolicy="delay")
            subEle('timer',parent=clock,name="hpet",present="no")
            subEle('on_poweroff',parent=domain,text='destroy')
            subEle('on_reboot',parent=domain,text='restart')
            subEle('on_crash',parent=domain,text='destroy')
            
            pm = subEle('pm',parent=domain)
            subEle('suspend-to-mem',parent=pm,enabled="no")
            subEle('suspend-to-disk',parent=pm,enabled="no")
            
            devices = subEle('devices',parent=domain)
            subEle('emulator',parent=devices,text='/usr/bin/qemu-system-x86_64')
            
            controller = subEle('controller',parent=devices,type="usb",index="0",model="qemu-xhci",ports="15")
            subEle('alias',parent=controller,name="usb")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x02",slot="0x00",function="0x0")
            
            controller = subEle('controller',parent=devices,type="sata",index="0")
            subEle('alias',parent=controller,name="ide")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x1f",function="0x2")
            
            controller = subEle('controller',parent=devices,type="pci",index="0",model="pcie-root")
            subEle('alias',parent=controller,name="pcie.0")
            
            controller = subEle('controller',parent=devices,type="pci",index="1",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="1",port="0x8")
            subEle('alias',parent=controller,name="pci.1")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x0",multifunction="on")
            
            controller = subEle('controller',parent=devices,type="pci",index="2",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="2",port="0x9")
            subEle('alias',parent=controller,name="pci.2")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x1")
            
            controller = subEle('controller',parent=devices,type="pci",index="3",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="3",port="0xa")
            subEle('alias',parent=controller,name="pci.3")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x2")
            
            controller = subEle('controller',parent=devices,type="pci",index="4",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="4",port="0xb")
            subEle('alias',parent=controller,name="pci.4")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x3")
            
            controller = subEle('controller',parent=devices,type="pci",index="5",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="5",port="0xc")
            subEle('alias',parent=controller,name="pci.5")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x4")
            
            controller = subEle('controller',parent=devices,type="pci",index="6",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="6",port="0xd")
            subEle('alias',parent=controller,name="pci.6")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x5")
            
            controller = subEle('controller',parent=devices,type="pci",index="7",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="7",port="0xe")
            subEle('alias',parent=controller,name="pci.7")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x6")
            
            controller = subEle('controller',parent=devices,type="pci",index="8",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="8",port="0xf")
            subEle('alias',parent=controller,name="pci.8")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x01",function="0x7")
            
            controller = subEle('controller',parent=devices,type="pci",index="9",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="9",port="0x10")
            subEle('alias',parent=controller,name="pci.9")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x02",function="0x0",multifunction="on")
            
            controller = subEle('controller',parent=devices,type="pci",index="10",model="pcie-root-port")
            subEle('model',parent=controller,name="pcie-root-port")
            subEle('target',parent=controller,chassis="10",port="0x11")
            subEle('alias',parent=controller,name="pci.10")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x00",slot="0x02",function="0x1")
            
            controller = subEle('controller',parent=devices,type="virtio-serial",index="0")
            subEle('alias',parent=controller,name="virtio-serial0")
            subEle('address',parent=controller,type="pci",domain="0x0000",bus="0x03",slot="0x00",function="0x0")
            
            ## ajout des interfaces réseaux
            i=0
            for port in porttoSet:
                
                print(port['mac'])
                if is_valid_macaddr802(port['mac']):
                    interface = subEle('interface',parent=devices,type="ethernet")
                    subEle('mac',parent=interface,address=port['mac'])
                    subEle('target',parent=interface,dev=port['port'].name,managed="no")
                    subEle('model',parent=interface,type="virtio")
                    subEle('address',parent=interface,type="pci",domain="0x0000",bus="0x01",slot="0x0"+str(i),function="0x0")
                    i+=1

            
            serial = subEle('serial',parent=devices,type='pty')
            subEle('source',parent=serial,path='/dev/pts/0')
            target = subEle('target',parent=serial,type='isa-serial',port='0')
            subEle('model',parent=target,name='isa-serial')
            subEle('alias',parent=serial,name="serial0")
            
            console = subEle('console',parent=devices,type='pty',tty='/dev/pts/0')
            subEle('source',parent=console,path='/dev/pts/0')
            subEle('target',parent=console,type='serial',port='0')
            subEle('alias',parent=console,name="serial0")
            
            channel = subEle('channel',parent=devices,type="unix")
            subEle('source',parent=channel,mode='bind',path='/var/lib/libvirt/qemu/channel/target/domain-25-AHYPE/org.qemu.guest_agent.0')
            subEle('target',parent=channel,type='virtio',name="org.qemu.guest_agent.0",state="disconnected")
            subEle('alias',parent=channel,name="channel0")
            subEle('address',parent=channel,type="virtio-serial",controller="0",bus="0",port="1")
            
            input = subEle('input',parent=devices,type="mouse",bus='ps2')
            subEle('alias',parent=input,name="input0")
            
            input = subEle('input',parent=devices,type="keyboard",bus='ps2')
            subEle('alias',parent=input,name="input1")
            
            rng = subEle('rng',parent=devices,model='virtio')
            subEle('backend',parent=rng,text='/dev/urandom',model='random')
            subEle('alias',parent=rng,name="rng0")
            subEle('address',parent=rng,type="pci",domain="0x0000",bus="0x06",slot="0x00",function="0x0")
            
            subEle('memory',parent=domain,text=str(form['memory']),unit='Kib')
            subEle('vcpu',parent=domain,text=str(form['vcpu']),placement="static")
            subEle('name',parent=domain,text=form['name'])
            resource = subEle('resource',parent=domain)
            subEle('partition',parent=resource,text=form['partition'])
            
            response = HttpResponse(
            content_type='text-plain')
            response['Content-Disposition'] = 'attachment; filename=vm.xml'
            response.writelines(generateVm(domain))
            return response
    else :
        form = VmForm(prefix='vm')
        formset = Formset(initial=PortList,prefix='formset')
    return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges,'formset':formset,'form':form})

# def generateVmConfiguration(request) :
#     ## VM model

#     bridges = OvsBridge.objects.all()
#     # ele = SubEleModel.objects.all()
#     # subelemodel = SubEleModel.objects.createSub('tonton',parent=ele[0],text='ok',key='value')
#     # subelemodel.save(commit = False)
    
#     ## Memoire
    
#     # memModel = SubEleModel.objects.createSub('memory',text='1000',unit='Kib')
    
#     # subelemodel.fkey = ports[0]
#     # subelemodel.save()
#     # subelemodel = SubEleModel.objects.createSub('toto')
#     # print(subelemodel.__dict__)  
#     # media_root= settings.MEDIA_ROOT    
#     # path = media_root+'template.xml'
#     # tree = ET.parse(path)
#     # root = tree.getroot()
    
#     ## parsing
    
#     # all_objects = [*bridges, *Port.objects.all()]
#     # data = media_root+'simpletemplate.xml'
#     # xml = serializers.serialize("xml", all_objects)
#     # print(ET.tostring(arbre,encoding='Unicode',pretty_print=True))
    
#     # print(xml)    
         

               
#     ## Generation d'un bus aléatoire non utilise
#     # pciUsed = []
#     # for element in root.iter('address'):
#     #     pciUsed.append({'bus':element.get('bus'),'slot':element.get('slot')})
    
#     # newBus= hex(random.randint(5,255))
#     # while any(d['bus'] == newBus for d in pciUsed):
#     #     newBus=hex(random.randint(5,255))
#     # # print(newBus)
    
#     # ## Generation random  MAC address
    
#     # macUsed = []
#     # for element in root.iter('mac'):
#     #     macUsed.append({'address':element.get('address')})

#     # # The first line is defined for specified vendor
#     # mac = [ 0x54, 0x52, 0x00,
#     # random.randint(0x00, 0x7f),
#     # random.randint(0x00, 0xff),
#     # random.randint(0x00, 0xff) ]
#     # macAddress =':'.join(map(lambda x: "%02x" % x, mac))
#     # while any(d['address'] == macAddress for d in macUsed):
#     #     mac = [ 0x54, 0x52, 0x00,
#     #     random.randint(0x00, 0x7f),
#     #     random.randint(0x00, 0xff),
#     #     random.randint(0x00, 0xff) ]
#     #     macAddress =':'.join(map(lambda x: "%02x" % x, mac)) 
           
#     # #add an interface
#     # address=macAddress
#     # bus=newBus
#     # devices  = root.find('devices')
#     # interface = ET.SubElement(devices,"interface",type="ethernet")
#     # mac = ET.SubElement(interface,"mac",address=address)
#     # target = ET.SubElement(interface,"target",dev="FOO.0",managed="no")
#     # model = ET.SubElement(interface,"model",type="virtio")
#     # pci = ET.SubElement(interface,
#     #                     "address",type="pci",
#     #                     domain="0x0000",
#     #                     bus=bus,
#     #                     slot="0x00",
#     #                     function="0x0")
#     # #Export to file
#     # tree=ET.ElementTree(root)
#     # ET.indent(tree, space="\t", level=0)
#     # with open(media_root+'templateUPdated.xml', 'wb') as f:
#     #     tree.write(f,encoding="utf-8")
#     # #print (ET.tostring(root))
    
#     if request.method == 'POST':
#         domainVm = DomainVmForm(request.POST,prefix='domain')
#         memoryVm = MemoryVmForm(request.POST,prefix='memory')
#         print("reçu!")
#         print(request.POST)
        
        
#         if domainVm.is_valid() and memoryVm.is_valid(): 
#             print('valid')
#             memory = memoryVm.cleaned_data
#             # print(memory
#                 #   )
#             domain = domainVm.save()
#             #recuperer l'id du domaine pour le passer aux éléments
#             domain_id = getattr(domain,'id')
#             #mise en BD
#             memory = memoryVm.save(commit=False)
#             memory.vm = DomainVm.objects.get(pk=domain_id)
#             memory.save()

            
            
#             response = HttpResponse(
#             content_type='text-plain')
#             response['Content-Disposition'] = 'attachment; filename=ovsConf.yml'
#             response.writelines(generateVm(domain))
#             return response
#         else:
#             domainVm = DomainVmForm(prefix='one')    

#     else:
#         domainVm = DomainVmForm(prefix='domain')  
#         memoryVm = MemoryVmForm(prefix='memory')
#     return render(request,'ovs_conf/generateVmConfiguration.html',{'bridges':bridges,'domainVm':domainVm,'memoryVm':memoryVm})

# def generateVm(domain):
#     #generation du fichier de configuration de la VM
#     ele = Elem('domain')
#     ele.attributes['type'] = domain.attr_type
#     # ele.text = domain.text_name
#     # query the database
#     child = []
#     memory = MemoryVm.objects.filter(vm=domain)
#     print(memory)
#     for mem in memory:
#         print('yo')
#         subele = Elem('memory')
#         subele.text = str(mem.text_memory)
#         ele.children.append(subele)
#         print(ele.children[0].name)
        
#     root = ele.serialFirst()
#     # root = ele.serialFirst
#     return ET.tostring(root,encoding='Unicode',pretty_print=True)

    
def generateVm(domain):
    

    root = Elem(domain.name)
    for k,v in domain.attributes.items():
        root.attributes[k] = v
    # subElements = SubEleModel.objects.filter(fkey=domain)
    
    #transformation des elements de la VM en nested Elements
    def recursive(parent,root):
        subElements = SubEleModel.objects.filter(fkey=parent)
        for subElement in subElements:
            ele = Elem(subElement.name)
            ele.text = subElement.text
        # print (subElement.attributes)
            for k,v in eval(subElement.attributes).items():
                ele.attributes[k] = v
            root.children.append(ele)
            recursive(subElement,ele)  
             
    recursive(domain,root)
    
    # creation du fichier xml
    root = root.serialFirst()
    return ET.tostring(root,encoding='Unicode',pretty_print=True)

        
    # ele.attributes['type'] = domain.attr_type
    # # ele.text = domain.text_name
    # # query the database
    # child = []
    # memory = MemoryVm.objects.filter(vm=domain)
    # print(memory)
    # for mem in memory:
    #     print('yo')
    #     subele = Elem('memory')
    #     subele.text = str(mem.text_memory)
    #     ele.children.append(subele)
    #     print(ele.children[0].name)
        
    # root = ele.serialFirst()
    # root = ele.serialFirst
    # return ET.tostring(root,encoding='Unicode',pretty_print=True)