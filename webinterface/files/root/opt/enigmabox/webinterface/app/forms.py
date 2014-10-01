import re
from django import forms
from django.core import exceptions
from django.core.validators import validate_slug, validate_ipv6_address
from app.models import *

class AddressbookForm(forms.Form):
    def validate_hostname(value):
        if re.search("[^a-z0-9-]", value):
            raise exceptions.ValidationError('Der Hostname darf nur aus Kleinbuchstaben, Zahlen und Bindestrichen (-) bestehen.')

# todo: find out how to bypass this on edits
    def validate_unique_hostname(value):
        return True
        if Address.objects.filter(name=value):
            raise exceptions.ValidationError('Dieser Hostname ist schon vergeben.')

    def validate_unique_ipv6(value):
        return True
        if Address.objects.filter(ipv6=value):
            raise exceptions.ValidationError('Diese IPv6-Adresse ist schon vergeben.')

    def validate_unique_phone(value):
        return True
        if Address.objects.filter(phone=value):
            raise exceptions.ValidationError('Diese Telefonnummer ist schon vergeben.')

    name = forms.CharField(initial='', required=True, min_length=1, max_length=60, validators=[validate_hostname, validate_unique_hostname])
    display_name = forms.CharField(initial='', required=False)
    ipv6 = forms.CharField(initial='', validators=[validate_ipv6_address, validate_unique_ipv6])
    phone = forms.IntegerField(initial='', min_value=10, required=False, validators=[validate_unique_phone])

class GlobalAddressbookForm(forms.Form):
    def validate_hostname(value):
        if re.search("[^a-z0-9-]", value):
            raise exceptions.ValidationError('Der Hostname darf nur aus Kleinbuchstaben, Zahlen und Bindestrichen (-) bestehen.')

    name = forms.CharField(initial='', required=True, min_length=1, max_length=50, validators=[validate_hostname])
    phone = forms.IntegerField(initial='', min_value=10, required=True)

class PeeringsForm(forms.Form):
    address = forms.CharField(initial='', required=True)
    public_key = forms.CharField(initial='', required=True, min_length=54, max_length=54)
    password = forms.CharField(initial='', required=True)
    country = forms.CharField(initial='', required=False, min_length=2, max_length=2)
    description = forms.CharField(initial='', required=False)

