

from ovs_conf.models import DomainVm,MemoryVm
from django import forms

class VmForm(forms.Form):
  name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-check-label' ,'placeholder':'name'})
    )
  memory = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-check-label' ,'placeholder':'memory(Kib)'})
    )
  vcpu = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-check-label' ,'placeholder':'vcpu'})
    )
  
  PARTITIONS = (
    ("/nort","non rt"),
    ("/rt","rt")
  )
  partition = forms.ChoiceField(choices=PARTITIONS,
                               label='',
                               widget=forms.RadioSelect(attrs={'class':'form-check-label' ,'placeholder':'partition'}))
  
