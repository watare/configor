from ovs_conf.models import OvsBridge
from django import forms
class BridgeForm(forms.ModelForm):
   class Meta:
     model = OvsBridge
     fields = '__all__'