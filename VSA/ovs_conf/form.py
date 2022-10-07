
from ovs_conf.models import OvsBridge, Port
from django import forms
class BridgeForm(forms.ModelForm):
   
   class Meta:
     model = OvsBridge
     fields = ('name','rstp_enable','enable_ipv6')
     labels ={
      'name' : ''        
     }
     widgets ={
         'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Bridge name'}),
         'rstp_enable' : forms.CheckboxInput(attrs={'class':'form-check-label'}),
         'enable_ipv6' : forms.CheckboxInput(attrs={'class':'form-check-label'})
     }
     
     
     
     
class PortForm(forms.ModelForm):
   class Meta:
    model = Port
    fields = '__all__'
    
    