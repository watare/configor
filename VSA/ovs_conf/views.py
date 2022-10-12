from django.forms import formset_factory
from turtle import end_fill
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
import yaml
from boltons.iterutils import remap
from ovs_conf.form import BridgeForm, BridgeFormSelect, PortForm, BridgeFormRo,PortFormAdd    
def bridge_create(request):
    bridges = OvsBridge.objects.all()
    if request.method == 'POST':
        form = BridgeForm(request.POST)
        if form.is_valid():
            bridge = form.save()
            return redirect('bridgeDetails',bridge.id)  
    else:
        form = BridgeForm()
    return render(request,'ovs_conf/bridge_create.html',{'form':form,'bridges':bridges})

def bridge_list(request):
    bridges = OvsBridge.objects.all()
    return render(
        request,
        'ovs_conf/bridge_list.html',
        {'bridges' : bridges})

def bridgeDetails(request,id):
    bridge = OvsBridge.objects.get(id=id)
    bridgeForm = BridgeFormRo(instance=bridge)
    ports = Port.objects.filter(bridge=id)
    portsList = []
    newPort = PortFormAdd() 
    for port in ports:
        portForm = PortForm(instance=port)
        portsList.append(portForm)
    if request.method == 'POST':
        newPort = PortFormAdd(request.POST,initial={'bridge':bridge})
        print(newPort.errors)

        if newPort.is_valid():
            newPort.save()
            print("save ok!!")
            return redirect('bridgeDetails',id)  
        else:
            print('fail add_port')
            newPort = PortFormAdd() 
    return render(request,'ovs_conf/bridgeDetails.html',{'bridgeForm':bridgeForm,'portsList':portsList,'newPort':newPort})
            
def ports_create(request,name):
    ports = Port.objects.filter(id=name)
    if request.method == 'POST':
        form = PortForm(request.POST)
        if form.is_valid():
            port = form.save()
            print(name)
            return redirect('ports_create',name)
    else:
            
        form = PortForm()
        #print("toto"+ form.get_initial_for_field(form.fields['name'], 'name'))
        
    return render(request,'ovs_conf/ports_create.html',{'form':form ,'ports':ports})


def generateOvsConfiguration(request):
    bridges = OvsBridge.objects.all()
    bridgeList = []
    for bridge in bridges:
        bridgeList.append(
            BridgeForm(instance=OvsBridge.objects.get(pk=bridge.id))
        )

    bridges = bridgeList
    
    Formset = formset_factory(BridgeFormSelect,extra=1)
    formset = Formset(initial=[{'name':'toto','select':''}])
    print(formset.as_table())
    if request.method == 'POST':
        bridgetoSet = []
        reqDic = dict(request.POST)
        print(reqDic)
        # for i in range (0,len(reqDic['name'])-1):
            
        #     if (reqDic['select'][i] == 'on'):
        #         # pass
        #         bridgetoSet.append(reqDic['name'][i])
        # # print(bridgetoSet)
        # return redirect('/generate_ovs/',bridgetoSet)
            
   # form = PortForm(request.POST)
   # if form.is_valid():
   #     port = form.save()
   #     print(name)
    return render(request,'ovs_conf/generateOvsConfiguration.html',{'bridges':bridges,'formset':formset})      
  
def generate_ovs_param(request,bridgeList):
    # generate the ovs configuration from the database
    # serving the file
    response = HttpResponse(
        content_type='text-plain')
    response['Content-Disposition'] = 'attachment; filename=ovs.yml'
    
    # query the database
    ovsbridges = bridgeList
    ovsdic = []
    
    # Loop based on foreing keys to retreive all elements for each bridge
    for ovsbridge in ovsbridges:        
        ports = Port.objects.filter(bridge=ovsbridge)
        otherbridgeconfigs = OtherBridgeConfig.objects.filter(bridge=ovsbridge)
        
        otherbridgedic =  []
        for otherbridgeconfig in otherbridgeconfigs:
            otherbridgedic.append(otherbridgeconfig.other_config)
            
        portdic = []
        for port in ports:
            otherportconfigs = OtherPortConfig.objects.filter(port=port)
            ipport = IpPort.objects.filter(port=port) #unused
            trunkports = TrunkPort.objects.filter(port=port)
            
            otherportconfigdic = []
            for otherportconfig in otherportconfigs:
                otherportconfig.append(otherportconfig.other_config)
                
            trunkdic = []    
            for trunkport in trunkports:
                trunkdic.append(trunkport.trunk)     
            
            
            portdic.append({'name': port.name,
                            'type': port.type,
                            'interface': port.interface,
                            'tag': port.tag,
                            'trunks': trunkdic,
                           'other_config': otherportconfigdic,
                           })
        ovsdic.append({'name': ovsbridge.name,
                       'rstp_enable': ovsbridge.rstp_enable,
                       'enable_ipv6' :ovsbridge.enable_ipv6,
                       'other_config' : otherbridgedic,
                       'ports': portdic
                       })
        # clean and serve the data in a yaml format
        drop_falsey = lambda path, key, value: bool(value)
        ovsdiccleaned = remap(ovsdic, visit=drop_falsey)
        ovs_conf = yaml.dump(ovsdiccleaned,sort_keys=False)

    response.writelines(ovs_conf)
    return response
def generate_ovs(request):
    # generate the ovs configuration from the database
    # serving the file
    response = HttpResponse(
        content_type='text-plain')
    response['Content-Disposition'] = 'attachment; filename=ovs.yml'
    
    # query the database
    ovsbridges = OvsBridge.objects.all()
    ovsdic = []
    
    # Loop based on foreing keys to retreive all elements for each bridge
    for ovsbridge in ovsbridges:        
        ports = Port.objects.filter(bridge=ovsbridge)
        otherbridgeconfigs = OtherBridgeConfig.objects.filter(bridge=ovsbridge)
        
        otherbridgedic =  []
        for otherbridgeconfig in otherbridgeconfigs:
            otherbridgedic.append(otherbridgeconfig.other_config)
            
        portdic = []
        for port in ports:
            otherportconfigs = OtherPortConfig.objects.filter(port=port)
            ipport = IpPort.objects.filter(port=port) #unused
            trunkports = TrunkPort.objects.filter(port=port)
            
            otherportconfigdic = []
            for otherportconfig in otherportconfigs:
                otherportconfig.append(otherportconfig.other_config)
                
            trunkdic = []    
            for trunkport in trunkports:
                trunkdic.append(trunkport.trunk)     
            
            
            portdic.append({'name': port.name,
                            'type': port.type,
                            'interface': port.interface,
                            'tag': port.tag,
                            'trunks': trunkdic,
                           'other_config': otherportconfigdic,
                           })
        ovsdic.append({'name': ovsbridge.name,
                       'rstp_enable': ovsbridge.rstp_enable,
                       'enable_ipv6' :ovsbridge.enable_ipv6,
                       'other_config' : otherbridgedic,
                       'ports': portdic
                       })
        # clean and serve the data in a yaml format
        drop_falsey = lambda path, key, value: bool(value)
        ovsdiccleaned = remap(ovsdic, visit=drop_falsey)
        ovs_conf = yaml.dump(ovsdiccleaned,sort_keys=False)

    response.writelines(ovs_conf)
    return response