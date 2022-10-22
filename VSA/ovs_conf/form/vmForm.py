
from email.policy import default
from faulthandler import disable
from unicodedata import name
from ovs_conf.models import DomainVm,MemoryVm
from django import forms

class DomainVmForm(forms.ModelForm):
  class Meta:
    model = DomainVm
    fields = ('text_name','attr_type')
    labels ={
    'text_name' : 'name',
    'attr_type' : 'type'        
    }
    widgets ={
          'name' : forms.TextInput(attrs={'class':'form-control'}),
          'type' : forms.TextInput(attrs={'class':'form-control'})     
    }
    
class MemoryVmForm(forms.ModelForm):
  class Meta:
    model = MemoryVm
    fields = ('text_memory',)
    labels ={
    'text_memory' : 'memory',        
    }
    widgets ={
          'memory' : forms.NumberInput(attrs={'class':'form-control'}),
    }
# class BridgeForm(forms.ModelForm):
#   select = forms.BooleanField(
#       label='select',
      
#       widget=forms.CheckboxInput(attrs={'class':'form-check-label'})
#       )
#   class Meta:
#     model = OvsBridge
#     fields = ('name','rstp_enable','enable_ipv6')
#     labels ={
#     'name' : ''        
#     }
#     widgets ={
#          'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Bridge name'}),
#          'rstp_enable' : forms.CheckboxInput(attrs={'class':'form-check-label'}),
#          'enable_ipv6' : forms.CheckboxInput(attrs={'class':'form-check-label'})
#     }
     
# class BridgeFormRo(forms.ModelForm):
   
#    class Meta:
#      model = OvsBridge
#      fields = ('name','rstp_enable','enable_ipv6')
#      labels ={
#       'name' : ''        
#      }
#      widgets ={
#          'name' : forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
#          'rstp_enable' : forms.CheckboxInput(attrs={'class':'form-check-label'}),
#          'enable_ipv6' : forms.CheckboxInput(attrs={'class':'form-check-label'})
#      }     
     
     
# class PortForm(forms.ModelForm):
#    class Meta:
#     model = Port
#     fields = {'bridge','name','type','interface','tag','vlan_mode','mac','remote_ip','remote_port','key','active'}
#     labels ={
#       'name' : '',
#       'type' : '',
#       'interface': '',
#       'tag': '',
#       'vlan_mode' : '',
#       'mac' : '',
#       'remote_ip':'',
#       'remote_port':'',
#       'key':''
       
#     }
#     widgets ={
#          'name' : forms.TextInput(attrs={'class':'form-control'}),
#          'type' : forms.Select(attrs={'class': 'form-control selectpicker'}),
#          'interface' : forms.TextInput(attrs={'class':'form-control'}),
#          'tag' : forms.TextInput(attrs={'class':'form-control'}),
#          'vlan_mode' : forms.Select(attrs={'class': 'form-control selectpicker'}),
#          'mac' : forms.TextInput(attrs={'class':'form-control'}),
#          'remote_ip' : forms.TextInput(attrs={'class':'form-control'}),
#          'remote_port' : forms.TextInput(attrs={'class':'form-control'}),
#          'key' : forms.TextInput(attrs={'class':'form-control'}),

#      }
    
