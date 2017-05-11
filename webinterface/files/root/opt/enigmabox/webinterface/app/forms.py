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

class PortforwardingForm(forms.Form):
    port = forms.IntegerField(initial='', required=True)
    hw_address = forms.CharField(initial='', required=True, min_length=17, max_length=17)
    description = forms.CharField(initial='', required=False, max_length=100)

class PasswordForm(forms.Form):
    password = forms.CharField(initial='', required=True, max_length=100)
    password_repeat = forms.CharField(initial='', required=True)

    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        try:
            password.encode('ascii')
        except Exception:
            raise forms.ValidationError('Aus technischen Gruenden koennen keine Umlaute oder Zeichen ausserhalb des ASCII-Zeichensatzes verwendet werden. Python, Unicode und so... Seufz.')

        if password and password != password_repeat:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class VolumesForm(forms.Form):
    def validate_name(value):
        if re.search("[^a-z0-9-]", value):
            raise exceptions.ValidationError('Der Name darf nur aus Kleinbuchstaben, Zahlen und Bindestrichen (-) bestehen.')

    name = forms.CharField(initial='', required=True, min_length=1, max_length=20, validators=[validate_name])

