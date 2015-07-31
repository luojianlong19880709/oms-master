# -*- coding: utf-8 -*-
from django import forms
from asset.models import *

class HostsListForm(forms.ModelForm):
    class Meta:
        model = HostList_yz1
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'product': forms.TextInput(attrs={'class': 'form-control'}),
          'application': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
	  'monitor': forms.TextInput(attrs={'class': 'form-control'}),  
        }

class HostsListForm_yz2(forms.ModelForm):
    class Meta:
	model = HostList_yz2
	widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'product': forms.TextInput(attrs={'class': 'form-control'}),
          'application': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
	  'monitor': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HostsListForm_cer(forms.ModelForm):
    class Meta:
        model = HostList_cer
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'product': forms.TextInput(attrs={'class': 'form-control'}),
          'application': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'status': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
	  'monitor': forms.TextInput(attrs={'class': 'form-control'}),
        }



class search(forms.Form):
	search = forms.CharField(widget=forms.TextInput(attrs={'size':'30'}))



class NetworkAssetForm(forms.ModelForm):
    class Meta:
        model = NetworkAsset
        widgets = {
          'ip': forms.TextInput(attrs={'class': 'form-control'}),
          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
          'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
          'productname': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_jg': forms.TextInput(attrs={'class': 'form-control'}),
          'service_tag': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }

class IdcAssetForm(forms.ModelForm):
    class Meta:
        model = IdcAsset
        widgets = {
          'idc_name': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_type': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_location': forms.TextInput(attrs={'class': 'form-control'}),
          'contract_date': forms.TextInput(attrs={'class': 'form-control'}),
          'idc_contacts': forms.TextInput(attrs={'class': 'form-control'}),
          'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }


