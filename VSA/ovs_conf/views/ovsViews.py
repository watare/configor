from django.forms import formset_factory
from turtle import end_fill
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from ovs_conf.models import OvsBridge,OtherBridgeConfig,Port,TrunkPort,IpPort,OtherPortConfig
import yaml
from boltons.iterutils import remap
from ovs_conf.form import BridgeForm, BridgeFormSelect, PortForm, BridgeFormRo,PortFormAdd    
def base(request):
    bridges= OvsBridge.objects.all()
    return render(request, "ovs_conf/base.html", {'bridges':bridges})

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
    bridges = OvsBridge.objects.all()
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
    return render(request,'ovs_conf/bridgeDetails.html',{'bridgeForm':bridgeForm,'portsList':portsList,'newPort':newPort,'bridges':bridges})
            
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
    bridgeList = []
    for bridge in bridges:
        bridgeList.append(
            {'name':bridge,'select':''})
    # print(fList)
    
    Formset = formset_factory(BridgeFormSelect,extra=0)
    formset = Formset(initial=bridgeList)
    # print(formset.as_table())
    if request.method == 'POST':
        reqDic = dict(request.POST)
        # i=0
        # print(reqDic['form-'+str(i)+'-select'][0])
        bridgetoSet = []
        for i in range(0,int(reqDic['form-TOTAL_FORMS'][0])):
            # pass
            if ('form-'+str(i)+'-select') in reqDic:
                # print (reqDic['form-'+str(i)+'-select'])
                bridgetoSet.append(OvsBridge.objects.get(name=reqDic['form-'+str(i)+'-name'][0]))
        print(bridgetoSet)
        
        response = HttpResponse(
        content_type='text-plain')
        response['Content-Disposition'] = 'attachment; filename=ovsConf.yml'
        
        response.writelines(generate_ovs_param(bridgetoSet))
        return response
        # return redirect('/generate_ovs/',bridgetoSet)
            
   # form = PortForm(request.POST)
   # if form.is_valid():
   #     port = form.save()
   #     print(name)
    return render(request,'ovs_conf/generateOvsConfiguration.html',{'formset':formset,'bridges':bridges})      
  
def generate_ovs_param(bridgeList):
    # generate the ovs configuration from the database
    # serving the file
    
    
    # query the database
    ovsbridges = bridgeList
    print(ovsbridges)
    
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
    return ovs_conf
def generate_ovs(request,bridgetoSet):
    # generate the ovs configuration from the database
    # serving the file
    response = HttpResponse(
        content_type='text-plain')
    response['Content-Disposition'] = 'attachment; filename=ovs.yml'
    
    # query the database
    ovsbridges = OvsBridge.objects.filter(name=bridgetoSet)
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