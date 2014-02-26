from django import template
from app.models import *
from condtag import *
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if not request:
        return ''
    if request.path.startswith('/' + pattern):
        return 'active'
    return ''

@register.simple_tag
def btn_state(variable, value, on_success, on_failure):
    if variable == value:
        return on_success
    return on_failure

@register.simple_tag
def form_error(errors):
    if errors:
        return 'style="background: #fbb;"'
    return ''

@register.simple_tag
def display_ip():
    o = Option()
    return o.get_ipv6()

@register.simple_tag
def display_version():
    f = open('VERSION', 'r')
    version = f.read()
    f.close()
    return version

@register.simple_tag
def peer_status(peer_name, sip_peers):
    try:
        ret = re.search(peer_name + '.*5060(.*)', sip_peers).group(1).strip()
    except:
        ret = '-'
    return ret

@register.simple_tag
def display_applyconfig_button():
    o = Option(key='config_changed')
    return o

@register.tag
@condition_tag
def if_config_changed(object, __=None):
    o = Option()
    return o.config_changed()

