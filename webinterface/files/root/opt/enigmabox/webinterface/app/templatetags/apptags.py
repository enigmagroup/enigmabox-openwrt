from django import template
from app.models import *
from django.utils.translation import ugettext as _
from condtag import *
from datetime import datetime, timedelta
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
def display_version(slugify=False):
    with open('VERSION', 'r') as f:
        version = f.read().strip()
    if slugify == '1':
        return template.defaultfilters.slugify(version)
    else:
        return version

@register.simple_tag
def display_space_usage():
    try:
        df = Popen(["df", "-h"], stdout=PIPE).communicate()[0].strip().split('\n')
        df = df[1]
        used_space = re.split(r' +', df)[2]
        total_space = re.split(r' +', df)[1]
        space_usage = re.split(r' +', df)[4]
        return """<small>""" + _('Space usage') + """</small><br>
        <strong>""" + used_space + """</strong> """ + _('of') + """ """ + total_space + """ """ + _('used') + """
        <div class="progress">
            <div class="progress-bar progress-bar-info" role="progressbar" style="width: """ + space_usage + """">""" + space_usage + """</div>
        </div>"""
    except Exception:
        return ''

@register.simple_tag
def updates_count():
    o = Option()
    uc = o.get_value('updates_count', '')
    return uc

@register.simple_tag
def peer_status(peer_name, sip_peers):
    try:
        status = re.search('\n' + peer_name + '\s.*5060(.*)', sip_peers).group(1).strip()
    except Exception:
        status = '-'

    ret = '<span class="label label-default">-</span>'
    if 'OK' in status:
        ret = '<span class="label label-success" title="' + status + '">OK</span>'
    if 'LAGGED' in status:
        ret = '<span class="label label-warning" title="' + status + '">OK</span>'
    if 'UNREACHABLE' in status:
        ret = '<span class="label label-default">Offline</span>'
    return ret

@register.simple_tag
def hw_ip(hw_address, arp_table):
    try:
        mapping = {line.split()[3]: line.split()[0] for line in arp_table.strip().split('\n')}
        ip = mapping[hw_address]
    except Exception:
        ip = '-'

    return ip

@register.simple_tag
def display_applyconfig_button():
    o = Option(key='config_changed')
    return o

@register.tag
@condition_tag
def if_config_changed(object, __=None):
    o = Option()
    return o.config_changed()

@register.tag
@condition_tag
def if_updates(object, __=None):
    o = Option()
    return o.get_value('hostid', False)

@register.tag
@condition_tag
def if_show_upgrader(object, __=None):
    o = Option()
    if o.get_value('hostid', False):
        try:
            with open('/etc/enigmabox/network-profile', 'r') as f:
                output = f.read().strip()
            return output in ['alix', 'apu']
        except Exception:
            return False

@register.tag
@condition_tag
def if_show_storage(object, __=None):
    o = Option()
    return o.get_value('owncloud', '0') == '1'

@register.tag
@condition_tag
def if_internet_access_expiring(object, __=None):
    o = Option()
    internet_access = o.get_value('internet_access')

    try:
        dt = datetime.strptime(internet_access, '%Y-%m-%d')
        now = datetime.utcnow()
        hundred_days = timedelta(days=100)
        if (now + hundred_days) > dt:
            return True

    except Exception:
        return False

