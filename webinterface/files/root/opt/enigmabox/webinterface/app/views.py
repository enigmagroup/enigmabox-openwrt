from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from subprocess import Popen, PIPE
from app.models import *
from app.forms import *
import random
import string
import json
import re
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from slugify import slugify
from helpers import *



def home(request):
    o = Option()

    if request.session.get('django_language') == None:
        language = o.get_value('language', 'de')
        request.session['django_language'] = language
        return redirect('/')

    language = request.session.get('django_language')

    netstat = {
        'dhcp': '0',
        'dhcp_conflict': False,
        'internet': '0',
        'cjdns': '0',
        'cjdns_internet': '0',
    }

    try:
        internet_access = o.get_value('internet_access')
        dt = datetime.strptime(internet_access, '%Y-%m-%d')

        if language == 'en':
            internet_access_formatted = dt.strftime('%m %d, %Y')
        else:
            internet_access_formatted = dt.strftime('%d.%m.%Y')

    except Exception:
        internet_access = ''
        internet_access_formatted = ''

    for key, value in netstat.items():
        try:
            with open('/tmp/netstat-' + key, 'r') as f:
                netstat[key] = f.read().strip()
        except Exception:
            pass

    lan_first_ip = '192.168.' + str(o.get_value('lan_range_first', 100)) + '.1'

    try:
        with open('/tmp/cjdns_org_gw', 'r') as f:
            gateway_ip = f.read().strip()
    except Exception:
        gateway_ip = ''

    # expiration notice
    try:
        dt = datetime.strptime(internet_access, '%Y-%m-%d')
        now = datetime.utcnow()
        internet_access_valid = '1' if now < dt else '0'
    except Exception:
        internet_access_valid = '0'

    global_availability = o.get_value('global_availability', '0')
    global_hostname = o.get_value('global_hostname', '')
    global_phone = o.get_value('global_phone', '')

    network_devices = {}
    network_devices["internet"] = []
    network_devices["lan1"] = []
    network_devices["lan2"] = []

    try:
        with open('/etc/enigmabox/network-profile', 'r') as f:
            network_profile = f.read().strip()
    except Exception:
        network_profile = 'apu'

    if network_profile == 'alix':
        iface_map = {
            "eth0": "internet",
            "eth1": "lan1",
            "eth2": "lan2",
        }
    if network_profile == 'apu':
        iface_map = {
            "eth2": "internet",
            "eth1": "lan1",
            "eth0": "lan2",
        }
    if network_profile == 'raspi':
        iface_map = {
            "eth1": "internet",
            "eth0": "lan1",
        }

    try:
        arp = Popen(["cat", "/proc/net/arp"], stdout=PIPE).communicate()[0].strip().split('\n')
        arp = arp[1:]
        for device in arp:
            ip = re.split(r' +', device)[0]
            mac = re.split(r' +', device)[3]
            iface = re.split(r' +', device)[5]

            interface = iface_map[iface]

            network_devices[interface].append({
                'ip': ip,
            })

            try:
                ports = []
                db_ports = Portforward.objects.filter(hw_address=mac)
                for p in db_ports:
                    ports.append(str(p.dstport))

                max_ports_to_display = 3
                if len(ports) > max_ports_to_display:
                    ports = ports[0:max_ports_to_display]
                    ports.append("...")
                network_devices[interface][-1]["portfwd"] = ", ".join(ports)
            except Exception:
                pass

    except Exception:
        network_devices = {}

    countries_trans = {
        'ch': _('Switzerland'),
        'se': _('Sweden'),
        'hu': _('Hungary'),
        'ru': _('Mother Russia'),
        'fr': _('France'),
        'de': _('Germany'),
        'us': _('United Stasi of America'),
    }

    selected_country = o.get_value('selected_country', 'ch')
    selected_country_text = countries_trans[selected_country]

    if request.is_ajax():
        return render_to_response('home/system_status.html', {
            'hostid': o.get_value('hostid'),
            'ipv6': o.get_value('ipv6'),
            'netstat': netstat,
            'internet_access': internet_access,
            'internet_access_valid': internet_access_valid,
            'internet_access_formatted': internet_access_formatted,
            'selected_country': selected_country,
            'selected_country_text': selected_country_text,
            'teletext_enabled': o.get_value('teletext_enabled', 0),
            'personal_website': o.get_value('personal_website', 0),
            'dokuwiki': o.get_value('dokuwiki', 0),
            'owncloud': o.get_value('owncloud', 0),
            'pastebin': o.get_value('pastebin', 0),
            'root_password': o.get_value('root_password'),
            'lan_first_ip': lan_first_ip,
            'gateway_ip': gateway_ip,
            'global_availability': global_availability,
            'global_hostname': global_hostname,
            'global_phone': global_phone,
            'network_devices': network_devices,
        }, context_instance=RequestContext(request))

    else:
        return render_to_response('home/overview.html', {
            'hostid': o.get_value('hostid'),
            'ipv6': o.get_value('ipv6'),
            'netstat': netstat,
            'internet_access': internet_access,
            'internet_access_valid': internet_access_valid,
            'internet_access_formatted': internet_access_formatted,
            'selected_country': selected_country,
            'selected_country_text': selected_country_text,
            'teletext_enabled': o.get_value('teletext_enabled', 0),
            'personal_website': o.get_value('personal_website', 0),
            'dokuwiki': o.get_value('dokuwiki', 0),
            'owncloud': o.get_value('owncloud', 0),
            'pastebin': o.get_value('pastebin', 0),
            'root_password': o.get_value('root_password'),
            'lan_first_ip': lan_first_ip,
            'gateway_ip': gateway_ip,
            'global_availability': global_availability,
            'global_hostname': global_hostname,
            'global_phone': global_phone,
            'network_devices': network_devices,
        }, context_instance=RequestContext(request))



# language switcher

def switch_language(request, language):
    o = Option()
    language = o.set_value('language', language)
    request.session['django_language'] = language
    return redirect('/')



# Addressbook

def addressbook(request):
    if request.POST:
        form = AddressbookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a = Address()
            a.name = cd['name'].strip()
            a.display_name = cd['name'].replace('-', ' ').title()
            a.ipv6 = normalize_ipv6(cd['ipv6'].strip())
            a.phone = cd['phone']
            a.save()
            o = Option()
            o.config_changed(True)
            return redirect('/addressbook/')
    else:
        form = AddressbookForm()

    order = request.GET.get('order', 'id')
    addresses = Address.objects.all().order_by(order)
    sip_peers = Popen(["asterisk", "-rx", "sip show peers"], stdout=PIPE).communicate()[0]

    if request.is_ajax():
        return render_to_response('addressbook/address_table.html', {
            'addresses': addresses,
            'sip_peers': sip_peers,
            'order': order,
        }, context_instance=RequestContext(request))

    else:
        return render_to_response('addressbook/overview.html', {
            'addresses': addresses,
            'form': form,
            'sip_peers': sip_peers,
            'order': order,
        }, context_instance=RequestContext(request))

def addressbook_edit(request, addr_id):
    if request.POST:
        if request.POST.get('submit') == 'delete':
            a = Address.objects.get(pk=addr_id)
            a.delete()
            o = Option()
            o.config_changed(True)
            return redirect('/addressbook/')

        form = AddressbookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a = Address.objects.get(pk=addr_id)
            a.name = cd['name'].strip()
            a.display_name = cd['display_name'].strip()
            a.ipv6 = normalize_ipv6(cd['ipv6'].strip())
            a.phone = cd['phone']
            a.save()
            o = Option()
            o.config_changed(True)
            return redirect('/addressbook/')
    else:
        a = Address.objects.get(pk=addr_id)
        form = AddressbookForm(initial={
            'name': a.name,
            'display_name': a.display_name,
            'ipv6': a.ipv6,
            'phone': a.phone,
        })

    address = Address.objects.get(pk=addr_id)
    return render_to_response('addressbook/detail.html', {
        'address': address,
        'form': form,
    }, context_instance=RequestContext(request))

def addressbook_global(request):
    o = Option()

    if request.POST.get('global-availability'):
        o.toggle_value('global_availability')
        o.config_changed(True)
        return redirect('/addressbook-global/')

    global_hostname = o.get_value('global_hostname')
    global_phone = o.get_value('global_phone')
    global_address_status = o.get_value('global_address_status')
    global_availability = o.get_value('global_availability')
    ipv6 = o.get_value('ipv6')
    ipv6 = normalize_ipv6(ipv6)

    import sqlite3
    db = sqlite3.connect('/etc/enigmabox/addressbook.db')
    db.text_factory = sqlite3.OptimizedUnicode
    db_cursor = db.cursor()
    db_cursor.execute("SELECT ipv6, hostname, phone FROM addresses ORDER BY id desc")
    db_addresses = db_cursor.fetchall()

    addresses = []
    for adr in db_addresses:
        addresses.append({
            'ipv6': adr[0],
            'name': adr[1],
            'phone': adr[2],
            'mine': '1' if normalize_ipv6(adr[0]) == ipv6 else '0',
        })

    return render_to_response('addressbook/overview-global.html', {
        'global_hostname': global_hostname,
        'global_phone': global_phone,
        'global_address_status': global_address_status,
        'global_availability': global_availability,
        'addresses': addresses,
    }, context_instance=RequestContext(request))

def addressbook_global_edit(request):
    o = Option()
    global_hostname = o.get_value('global_hostname', '')
    global_phone = o.get_value('global_phone', '')

    if request.POST.get('submit') == 'save':
        form = GlobalAddressbookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name'].strip()
            phone = cd['phone']
            o.set_value('global_hostname', name)
            o.set_value('global_phone', phone)
            o.set_value('global_address_status', 'pending')
            return redirect('/addressbook-global/')

    elif request.POST.get('submit') == 'delete':
        o.set_value('global_hostname', '')
        o.set_value('global_phone', '')
        o.set_value('global_address_status', 'pending')
        return redirect('/addressbook-global/')

    else:
        form = GlobalAddressbookForm(initial={
            'name': global_hostname,
            'phone': global_phone,
        })

    return render_to_response('addressbook/overview-global-edit.html', {
        'form': form,
        'global_hostname': global_hostname,
        'global_phone': global_phone,
    }, context_instance=RequestContext(request))



# Passwords

def passwords(request):
    o = Option()

    return render_to_response('passwords/overview.html', {
        'webinterface_password': o.get_value('webinterface_password', ''),
        'mailbox_password': o.get_value('mailbox_password', ''),
    }, context_instance=RequestContext(request))

def password_edit(request, subject):
    o = Option()

    if subject not in ['webinterface', 'mailbox']:
        raise ValueError('allowed subjects: webinterface, mailbox')

    if request.POST.get('submit') == 'save':
        form = PasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            o.set_value(subject + '_password', cd['password'])
            o.config_changed(True)
            return redirect('/passwords/')
    elif request.POST.get('submit') == 'unset':
        o.set_value(subject + '_password', '')
        o.config_changed(True)
        return redirect('/passwords/')
    else:
        password = o.get_value(subject + '_password', '')

        form = PasswordForm(initial={
            'password': password,
            'password_repeat': password,
        })

    return render_to_response('passwords/edit.html', {
        'subject': subject,
        'form': form,
    }, context_instance=RequestContext(request))



# Updates

def updates(request):
    o = Option()
    output_window = False
    loader_hint = ''

    if o.get_value('autoupdates', None) == None:
        o.set_value('autoupdates', '1')

    if request.POST.get('autoupdates'):
        o.toggle_value('autoupdates')
        o.config_changed(True)

    if request.POST.get('check'):
        Popen(["/usr/sbin/updater", "check"], stdout=PIPE).communicate()[0]
        return redirect('/updates/')

    if request.POST.get('apply_updates'):
        o.set_value('updater_running', True)
        output_window = True
        loader_hint = 'run'
        Popen(["/usr/sbin/updater", "apply", "bg"], stdout=PIPE, close_fds=True)

    try:
        f = open('/tmp/updates_output', 'r')
        upgr_content = f.read()
    except Exception:
        upgr_content = ''

    upgradables = []
    for line in upgr_content.split('\n'):
        if line != '':
            upgradables.append(line.split(' - '))

    return render_to_response('updates/overview.html', {
        'output_window': output_window,
        'loader_hint': loader_hint,
        'upgradables': upgradables,
        'autoupdates': o.get_value('autoupdates'),
    }, context_instance=RequestContext(request))



# Upgrade

def upgrade(request):
    import os.path
    o = Option()
    firmware_file = "/tmp/fw.img.gz"
    download_ok = False
    verify_ok = False
    writing = False

    if request.POST.get('download') == '1':
        Popen(["/usr/sbin/upgrader", "download"], stdout=PIPE).communicate()[0]

    if request.POST.get('verify') == '1':
        Popen(["/usr/sbin/upgrader", "verify"], stdout=PIPE).communicate()[0]

    if request.POST.get('write') == '1':
        writing = True
        Popen(["/usr/sbin/upgrader", "write"], stdout=PIPE, close_fds=True)

    if os.path.isfile(firmware_file):
        download_ok = True

    if os.path.isfile("/tmp/fw_sig_ok"):
        verify_ok = True

    return render_to_response('upgrade/overview.html', {
        'download_ok': download_ok,
        'verify_ok': verify_ok,
        'writing': writing,
    }, context_instance=RequestContext(request))



# Backup & restore

def backup(request):
    return render_to_response('backup/overview.html', context_instance=RequestContext(request))

def backup_system(request):
    return render_to_response('backup/system.html', {
    }, context_instance=RequestContext(request))

def backup_system_backupwizard(request):
    step = 'check_usb'
    show_output = False
    errormsg = ''

    if request.POST.get('check_usb') == '1':
        result = Popen(["/bin/busybox sh /usr/sbin/backup-stuff check_usb"], shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        result = result.strip()
        if result == 'yes':
            step = 'format_usb'
        elif result == 'sizefail':
            step = 'check_usb'
            errormsg = 'sizefail'
        elif result == 'nodrive':
            step = 'check_usb'
            errormsg = 'nodrive'

    if request.POST.get('format_usb') == '1':
        Popen(["/bin/busybox sh /usr/sbin/backup-stuff format_usb"], shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        step = 'backup_to_usb'

    if request.POST.get('backup_to_usb') == '1':
        Popen(["/bin/busybox sh /usr/sbin/backup-stuff backup_to_usb 2>&1 > /tmp/dynamic_output"], shell=True, stdout=PIPE, close_fds=True)
        show_output = True
        step = 'backup_to_usb'

    if request.POST.get('proceed_to_step_4') == '1':
        step = 'ensure_usb_unplugged'

    if request.POST.get('ensure_usb_unplugged') == '1':
        result = Popen(["/bin/busybox sh /usr/sbin/backup-stuff check_usb"], shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        result = result.strip()
        if result == 'nodrive':
            return redirect('/')
        else:
            step = 'ensure_usb_unplugged'
            errormsg = 'usbfail'

    return render_to_response('backup/backupwizard/' + step + '.html', {
        'show_output': show_output,
        'errormsg': errormsg,
    }, context_instance=RequestContext(request))

def backup_system_restorewizard(request):
    step = 'check_usb'
    show_output = False
    errormsg = ''

    if request.session.get('django_language') == None:
        o = Option()
        language = o.get_value('language', 'de')
        request.session['django_language'] = language
        return redirect('/backup/system/restorewizard/?step=usb')

    if request.POST.get('check_usb') == '1':
        result = Popen(["/usr/sbin/restore-stuff check_usb"], shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        result = result.strip()
        if result == 'yes':
            step = 'restore_from_usb'
        elif result == 'nodrive':
            step = 'check_usb'
            errormsg = 'nodrive'

    if request.POST.get('restore_from_usb') == '1':
        import os
        os.system("/usr/sbin/restore-stuff usbstick &")

    if request.GET.get('step') == 'usb':
        step = 'ensure_usb_unplugged'

    if request.POST.get('ensure_usb_unplugged') == '1':
        result = Popen(["/usr/sbin/restore-stuff check_usb"], shell=True, stdout=PIPE, close_fds=True).communicate()[0]
        result = result.strip()
        if result == 'nodrive':
            return redirect('/')
        else:
            step = 'ensure_usb_unplugged'
            errormsg = 'usbfail'

    return render_to_response('backup/restorewizard/' + step + '.html', {
        'show_output': show_output,
        'errormsg': errormsg,
    }, context_instance=RequestContext(request))

def backup_sslcerts(request):
    o = Option()
    hostid = o.get_value('hostid')
    if hostid is None:
        hostid = '$hostid'
    filename = '/tmp/sslcerts-' + hostid + '.zip'
    msg = False

    if request.POST.get('backup'):
        import os
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper

        try:
            Popen(["/usr/sbin/backup-stuff", "sslcerts"], stdout=PIPE).communicate()[0]

            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename=sslcerts-' + hostid + '.zip'
            response['Content-Length'] = os.path.getsize(filename)
            return response

        except Exception:
            msg = 'backuperror'

    if request.POST.get('restore'):

        try:
            filename = '/tmp/' + request.FILES['file'].name
            destination = open(filename, 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()

            Popen(["/usr/sbin/restore-stuff", "sslcerts"], stdout=PIPE).communicate()[0]
            msg = 'restoresuccess'

        except Exception:
            msg = 'restoreerror'

    return render_to_response('backup/sslcerts.html', {
        'msg': msg,
        'hostid': hostid,
    }, context_instance=RequestContext(request))



# Subscription

def subscription(request):
    o = Option()
    currency = request.POST.get('currency', 'CHF')
    subscription = request.POST.get('subscription', '1')

    amount_table = {}
    amount_table['CHF'] = {
        '1': 120,
        '5': 500,
        'lt': 1000,
    }
    amount_table['EUR'] = {
        '1': 120,
        '5': 500,
        'lt': 1000,
    }
    amount_table['USD'] = {
        '1': 120,
        '5': 500,
        'lt': 1000,
    }

    amount = amount_table[currency][subscription]

    return render_to_response('subscription/overview.html', {
        'hostid': o.get_value('hostid'),
        'show_invoice': request.POST.get('show_invoice'),
        'currency': currency,
        'subscription': subscription,
        'amount': amount,
    }, context_instance=RequestContext(request))

def subscription_hide_notice(request):
    o = Option()

    o.set_value('expiration_notice_confirmed', '1')

    try:
        Popen(["/usr/sbin/hide-expiration-notice"], stdout=PIPE).communicate()[0]
    except Exception:
        pass

    try:
        referrer = request.META['HTTP_REFERER']
    except Exception:
        referrer = 'http://box/'

    return redirect(referrer)



# Peerings

def peerings(request):
    o = Option()

    if request.POST.get('allow_peering'):

        if o.get_value('peering_password') is None:
            o.set_value('peering_password', ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30)))
        if o.get_value('peering_port') is None:
            o.set_value('peering_port', random.randint(2000, 60000))

        ap = o.get_value('allow_peering')
        if ap == '1':
            o.set_value('allow_peering', 0)
        else:
            o.set_value('allow_peering', 1)
        o.config_changed(True)

    if request.POST.get('autopeering'):
        ap = o.get_value('autopeering')
        if ap == '1':
            o.set_value('autopeering', 0)
        else:
            o.set_value('autopeering', 1)
        o.config_changed(True)

    if request.POST.get('save_peeringinfo'):
        o.set_value('peering_port', request.POST.get('peering_port'))
        o.set_value('peering_password', request.POST.get('peering_password'))
        o.config_changed(True)

    peerings = Peering.objects.filter(custom=True).order_by('id')

    return render_to_response('peerings/overview.html', {
        'peerings': peerings,
        'allow_peering': o.get_value('allow_peering'),
        'autopeering': o.get_value('autopeering'),
        'peering_port': o.get_value('peering_port'),
        'peering_password': o.get_value('peering_password'),
        'public_key': o.get_value('public_key'),
    }, context_instance=RequestContext(request))

def peerings_edit(request, peering_id=None):
    peering = ''
    form = ''

    if request.POST:
        if request.POST.get('submit') == 'delete':
            p = Peering.objects.get(pk=peering_id)
            p.delete()
            o = Option()
            o.config_changed(True)
            return redirect('/peerings/')

        form = PeeringsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if peering_id == None:
                p = Peering()
            else:
                p = Peering.objects.get(pk=peering_id)
            p.address = cd['address'].strip()
            p.public_key = cd['public_key'].strip()
            p.password = cd['password'].strip()
            p.description = cd['description'].strip()
            p.custom = True
            p.save()
            o = Option()
            o.config_changed(True)
            return redirect('/peerings/')
    else:
        if peering_id:
            peering = Peering.objects.get(pk=peering_id)
            form = PeeringsForm(initial={
                'address': peering.address,
                'public_key': peering.public_key,
                'password': peering.password,
                'description': peering.description,
            })

    return render_to_response('peerings/detail.html', {
        'peering': peering,
        'form': form,
    }, context_instance=RequestContext(request))



# Lan Range

def lan_range(request):
    o = Option()

    if request.POST.get('save'):
        lan_range_first = int(request.POST.get('lan_range_first', 100))
        lan_range_second = lan_range_first + 1
        o.set_value('lan_range_first', lan_range_first)
        o.set_value('lan_range_second', lan_range_second)
        Popen(['/usr/sbin/cfengine-apply'], stdout=PIPE).communicate()[0]
        Popen(['/sbin/reboot'], stdout=PIPE, close_fds=True)

    ip_range_first = []
    for i in range(1, 250):
        ip_range_first.append(i)

    ip_range_second = []
    for i in range(2, 251):
        ip_range_second.append(i)

    ip_range_router = False
    try:
        with open('/tmp/netstat-dhcp_conflict', 'r') as f:
            ip_range_router = f.read().strip().split('.')[2]
    except Exception:
        pass

    return render_to_response('lan_range/overview.html', {
        'lan_range_first': int(o.get_value('lan_range_first', 100)),
        'lan_range_second': int(o.get_value('lan_range_second', 101)),
        'ip_range_first': ip_range_first,
        'ip_range_second': ip_range_second,
        'ip_range_router': int(ip_range_router),
        'ip_range_router_prev': int(ip_range_router) - 1,
    }, context_instance=RequestContext(request))



# Country selection

def countryselect(request):
    o = Option()

    if request.POST.get('default_country', False):
        o.set_value('default_country', request.POST.get('default_country'))
        return redirect('/countryselect/')

    country = request.POST.get('country', False)
    if country:
        o.set_value('selected_country', country)
        Popen(['/usr/sbin/set-country'], stdout=PIPE, close_fds=True)
        return redirect('/')

    country_active = request.POST.get('country-active', False)
    if country_active:
        c = Country.objects.get(countrycode=country_active)
        c.active = False
        c.save()

    country_inactive = request.POST.get('country-inactive', False)
    if country_inactive:
        c = Country.objects.get(countrycode=country_inactive)
        c.active = True
        c.save()

    peerings = Peering.objects.filter(custom=False)
    for p in peerings:
        country = Country.objects.filter(countrycode=p.country)
        if len(country) < 1:
            c = Country()
            c.countrycode = p.country
            c.priority = 0
            c.save()

    # kick out countrys which aren't in the peerings anymore
    countries = Country.objects.all()
    for c in countries:
        peering = Peering.objects.filter(country=c.countrycode)
        if len(peering) < 1:
            c.delete()

    countries_trans = {
        'ch': _('Switzerland'),
        'se': _('Sweden'),
        'hu': _('Hungary'),
        'ru': _('Mother Russia'),
        'fr': _('France'),
        'de': _('Germany'),
        'us': _('United Stasi of America'),
    }

    db_countries = Country.objects.all().order_by('priority')
    countries = []
    for c in db_countries:
        countries.append({
            'countrycode': c.countrycode,
            'active': c.active,
            'priority': c.priority,
            'countryname': countries_trans.get(c.countrycode),
        })

    return render_to_response('countryselect/overview.html', {
        'countries': countries,
        'countries_trans': countries_trans,
        'selected_country': o.get_value('selected_country', 'ch'),
        'default_country': o.get_value('default_country', 'ch'),
    }, context_instance=RequestContext(request))



# Web filter

def webfilter(request):
    o = Option()

    if request.POST:
        o.config_changed(True)

        # always send that data, even if its an empty string
        o.set_value('webfilter_custom-rules-text', request.POST.get('custom-rules-text'))

    settings_fields = ['filter-ads', 'block-win10stasi', 'filter-headers', 'disable-browser-ident', 'block-facebook', 'block-google', 'block-twitter', 'custom-rules']

    for postval in settings_fields:
        if request.POST.get(postval):
            o.toggle_value('webfilter_' + postval)

    settings = {}
    for getval in settings_fields:
        field_name = getval.replace('-', '_')
        setting_name = 'webfilter_' + getval
        settings[field_name] = o.get_value(setting_name, '')

    settings['custom_rules_text'] = o.get_value('webfilter_custom-rules-text', '')

    return render_to_response('webfilter/overview.html', settings, context_instance=RequestContext(request))



# WLAN settings

def wlan_settings(request):
    o = Option()

    output_window = False
    wlan_opmode = o.get_value('wlan_opmode', 'mesh')

    if request.POST:
        if wlan_opmode == 'client':
            o.set_value('wlan_ssid', request.POST.get('ssid'))
            o.set_value('wlan_pass', request.POST.get('pass'))
            o.set_value('wlan_security', request.POST.get('security'))
        output_window = True
        Popen(["/usr/sbin/setup-cjdns-networking", "startwifi", "bg"], stdout=PIPE, close_fds=True)

    return render_to_response('wlan_settings/overview.html', {
        'wlan_opmode': wlan_opmode,
        'wlan_ssid': o.get_value('wlan_ssid', ''),
        'wlan_pass': o.get_value('wlan_pass', ''),
        'wlan_security': o.get_value('wlan_security', 'WPA2'),
        'output_window': output_window,
    }, context_instance=RequestContext(request))

def set_opmode(request, wlan_opmode):
    o = Option()
    o.set_value('wlan_opmode', wlan_opmode)
    return redirect('/wlan_settings/')

def wlan_scan(request):
    o = Option()

    if request.POST:
        o.set_value('wlan_ssid', request.POST.get('ssid'))
        o.set_value('wlan_security', request.POST.get('security'))
        o.set_value('wlan_group', request.POST.get('group'))
        o.set_value('wlan_pairwise', request.POST.get('pairwise'))
        return redirect('/wlan_settings/')

    final_cells = []

#    Popen(["ifconfig", "ah0", "down"], stdout=PIPE).communicate()[0]
#    Popen(["ifconfig", "wlan0", "up"], stdout=PIPE).communicate()[0]
    scan = Popen(["iwlist", "wlan0", "scanning"], stdout=PIPE).communicate()[0]

    cells = re.split('Cell.*', scan)
    for cell in cells:

        try:
            ssid = cell.split('ESSID:')[1].split('\n')[0].replace('"', '').strip()
#            signal = cell.split('Signal level:')[1].split(' ')[0].strip()
#            signal = int(100 + float(signal))
            signal = 'unknown'

            try:
                group = cell.split('Group Cipher')[1].split('\n')[0].strip()
                if 'CCMP' in group:
                    group = 'CCMP'
                else:
                    group = 'TKIP'

            except Exception:
                group = ''

            try:
                pairwise = cell.split('Pairwise Ciphers')[1].split('\n')[0].strip()
                if 'CCMP' in pairwise:
                    pairwise = 'CCMP'
                else:
                    pairwise = 'TKIP'

            except Exception:
                pairwise = ''

            if group == '' and pairwise == '':
                security = 'WEP'
            else:
                security = 'WPA'

            final_cells.append({
                'ssid': ssid,
                'signal': signal,
                'security': security,
                'group': group,
                'pairwise': pairwise,
            })

        except Exception:
            pass

    final_cells = sorted(final_cells, key=lambda k: k['signal'], reverse=True)

    return render_to_response('wlan_settings/scan.html', {
        'cells': final_cells,
    }, context_instance=RequestContext(request))



# Port forwarding

def portforwarding(request):
    o = Option()

    # read arp table
    arp_result = Popen(["cat", "/proc/net/arp"], stdout=PIPE).communicate()[0]

    return render_to_response('portforwarding/overview.html', {
        'portforwardings': Portforward.objects.all().order_by('port'),
        'arp_table': arp_result,
        'ipv6': o.get_value('ipv6'),
    }, context_instance=RequestContext(request))

def portforwarding_edit(request, port=None):
    o = Option()
    form = ''

    # read arp table
    arp_result = Popen(["cat", "/proc/net/arp"], stdout=PIPE).communicate()[0]

    # get internet interface to exclude it later
    try:
        with open('/etc/enigmabox/network-profile', 'r') as f:
            network_profile = f.read().strip()
    except Exception:
        network_profile = 'apu'

    if network_profile == 'alix':
        internet_interface = 'eth0'
    if network_profile == 'apu':
        internet_interface = 'eth2'
    if network_profile == 'raspi':
        internet_interface = 'eth1'

    # assemble results
    results = {}
    r = 0
    for row in arp_result.split('\n'):
        results[r] = []
        fields = row.split(' ')
        for f in fields:
            f.strip(' ')
            if f != '':
                results[r].append(f)
        r += 1

    device_list = []
    for d in range(1, len(results) - 1):
        if results[d][5] != internet_interface:
            device_list.append({
                "ip": results[d][0],
                "hw": results[d][3],
            })

    if request.POST:
        if request.POST.get('submit') == 'delete':
            p = Portforward.objects.get(port=port)
            p.delete()
            pfa = PortforwardAccess.objects.get(port=port)
            pfa.delete()
            o = Option()
            o.config_changed(True)
            return redirect('/portforwarding/')

        form = PortforwardingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if port == None:
                p = Portforward()
            else:
                p = Portforward.objects.get(port=port)
            p.port = cd['port']
            p.dstport = cd['dstport']
            p.hw_address = cd['hw_address'].strip()
            p.description = cd['description'].strip()
            p.access = 'none'
            p.save()
            try:
                pfa = PortforwardAccess()
                pfa.port = cd['port']
                pfa.save()
            except Exception:
                pass
            o = Option()
            o.config_changed(True)
            return redirect('/portforwarding/')
    else:
        if port:
            portforwarding = Portforward.objects.get(port=port)
            form = PortforwardingForm(initial={
                'port': portforwarding.port,
                'dstport': portforwarding.dstport,
                'hw_address': portforwarding.hw_address,
                'description': portforwarding.description,
            })

    return render_to_response('portforwarding/detail.html', {
        'port': port,
        'device_list': device_list,
        'form': form,
    }, context_instance=RequestContext(request))

def portforwarding_setaccess(request, port=None, mode="none"):
    o = Option()
    p = Portforward.objects.get(port=port)
    p.access = mode
    p.save()
    o = Option()
    o.config_changed(True)

    if mode == "specific":
        addresses = Address.objects.exclude(pk__in=PortforwardAccess.objects.filter(port=port).values('addresses').query)
        if len(addresses) == 0:
            addresses = Address.objects.all().order_by('id')

        access_list = PortforwardAccess.objects.get(port=port).addresses.all()
        if len(access_list) == len(Address.objects.all()):
            addresses = []

        if request.POST.get('grant'):
            portforwardaccess = PortforwardAccess.objects.get(port=port)
            #portforwardaccess.addresses.clear()
            userlist = request.POST.getlist('userlist')
            for address in userlist:
                db_address = Address.objects.get(ipv6=address)
                portforwardaccess.addresses.add(db_address)
                #portforwardaccess.save()
            o.config_changed(True)
            return redirect('/portforwarding/' + port + '/set_access/specific/')

        if request.POST.get('revoke'):
            portforwardaccess = PortforwardAccess.objects.get(port=port)
            accesslist = request.POST.getlist('accesslist')
            for address in accesslist:
                db_address = Address.objects.get(ipv6=address)
                portforwardaccess.addresses.remove(db_address)
                #portforwardaccess.save()
            o.config_changed(True)
            return redirect('/portforwarding/' + port + '/set_access/specific/')

        return render_to_response('portforwarding/manage_access.html', {
            'port': port,
            'addresses': addresses,
            'access_list': access_list,
        }, context_instance=RequestContext(request))

    else:
        return redirect('/portforwarding/')

def portforwarding_check(request, port=None):
    import socket

    resp = {}
    resp['result'] = 'failed'

    try:
        p = Portforward.objects.get(port=port)
        arp_table = Popen(["cat", "/proc/net/arp"], stdout=PIPE).communicate()[0]
    except Exception:
        resp['msg'] = 'port not found or arp table lookup failed'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    try:
        mapping = {line.split()[3]: line.split()[0] for line in arp_table.strip().split('\n')}
        ip = mapping[p.hw_address]
    except Exception:
        resp['msg'] = 'IP not found'
        ip = '-'

    s = socket.socket()
    s.settimeout(1)
    address = ip
    port = int(p.dstport)

    try:
        s.connect((address, port))
        if s is not None:
            resp['result'] = 'up'
    except Exception:
        resp['msg'] = 'connect failed'
    finally:
        s.close()

    return HttpResponse(json.dumps(resp), content_type='application/json')



# Teletext

def teletext(request):
    o = Option()

    if request.POST:
        o.toggle_value('teletext_enabled')
        o.config_changed(True)

    return render_to_response('teletext/overview.html', {
        'teletext_enabled': o.get_value('teletext_enabled', 0),
    }, context_instance=RequestContext(request))



# Hypesites

def hypesites(request):
    o = Option()

    hypesites = []

    try:
        import sqlite3
        db = sqlite3.connect('/etc/enigmabox/hypesites.db')
        db.text_factory = sqlite3.OptimizedUnicode
        c = db.cursor()
        c.execute("SELECT ipv6,hostname,last_seen FROM hypesites")

        for a in c.fetchall():
            hypesites.append({
                'ipv6': a[0],
                'hostname': a[1],
                'last_seen': datetime.fromtimestamp(a[2]),
            })

    except Exception:
        pass

    return render_to_response('hypesites/overview.html', {
        'ipv6': o.get_value('ipv6'),
        'hypesites': hypesites,
    }, context_instance=RequestContext(request))

def configure_hypesites(request):
    o = Option()

    if request.POST.get('access_global'):
        o.set_value('hypesites_access', 'global')
        o.config_changed(True)

    if request.POST.get('access_friends'):
        o.set_value('hypesites_access', 'friends')
        o.config_changed(True)

    if request.POST.get('access_off'):
        o.set_value('hypesites_access', 'off')
        o.config_changed(True)

    if request.POST.get('access_internal'):
        o.set_value('hypesites_access', 'internal')
        o.config_changed(True)

    if request.POST.get('personal_website'):
        o.toggle_value('personal_website')
        o.config_changed(True)

    if request.POST.get('dokuwiki'):
        o.toggle_value('dokuwiki')
        o.config_changed(True)

    if request.POST.get('owncloud'):
        o.toggle_value('owncloud')
        o.config_changed(True)

    if request.POST.get('pastebin'):
        o.toggle_value('pastebin')
        o.config_changed(True)

    return render_to_response('hypesites/configure.html', {
        'webserver_enabled': o.get_value('webserver_enabled', 0),
        'hypesites_access': o.get_value('hypesites_access', 'off'),
        'personal_website': o.get_value('personal_website', 0),
        'dokuwiki': o.get_value('dokuwiki', 0),
        'owncloud': o.get_value('owncloud', 0),
        'pastebin': o.get_value('pastebin', 0),
        'hype_access_site': o.get_value('hype_access_site', 'all'),
        'hype_access_dokuwiki': o.get_value('hype_access_dokuwiki', 'all'),
        'hype_access_owncloud': o.get_value('hype_access_owncloud', 'all'),
        'ipv6': o.get_value('ipv6'),
    }, context_instance=RequestContext(request))

def hypesites_access(request, webservice):
    o = Option()

    addresses = Address.objects.exclude(pk__in=HypeAccess.objects.filter(appname=webservice).values('addresses').query)
    if len(addresses) == 0:
        addresses = Address.objects.all().order_by('id')
    try:
        access_list = HypeAccess.objects.get(appname=webservice).addresses.all()
    except Exception:
        ha = HypeAccess()
        ha.appname = webservice
        ha.save()
        access_list = HypeAccess.objects.get(appname=webservice).addresses.all()
    if len(access_list) == len(Address.objects.all()):
        addresses = []

    if request.POST.get('access_all'):
        o.set_value('hype_access_' + webservice, 'all')
        o.config_changed(True)
        return redirect('/hypesites/configure/' + webservice + '/access/')

    if request.POST.get('access_friends'):
        o.set_value('hype_access_' + webservice, 'friends')
        o.config_changed(True)
        return redirect('/hypesites/configure/' + webservice + '/access/')

    if request.POST.get('access_specific'):
        o.set_value('hype_access_' + webservice, 'specific')
        o.config_changed(True)
        return redirect('/hypesites/configure/' + webservice + '/access/')

    if request.POST.get('grant'):
        hypeaccess = HypeAccess.objects.get(appname=webservice)
        #hypeaccess.addresses.clear()
        userlist = request.POST.getlist('userlist')
        for address in userlist:
            db_address = Address.objects.get(ipv6=address)
            hypeaccess.addresses.add(db_address)
            #hypeaccess.save()
        o.config_changed(True)
        return redirect('/hypesites/configure/' + webservice + '/access/')

    if request.POST.get('revoke'):
        hypeaccess = HypeAccess.objects.get(appname=webservice)
        accesslist = request.POST.getlist('accesslist')
        for address in accesslist:
            db_address = Address.objects.get(ipv6=address)
            hypeaccess.addresses.remove(db_address)
            #hypeaccess.save()
        o.config_changed(True)
        return redirect('/hypesites/configure/' + webservice + '/access/')

    return render_to_response('hypesites/manage_access.html', {
        'webserver_enabled': o.get_value('webserver_enabled', 0),
        'webservice': webservice,
        'hype_access_webservice': o.get_value('hype_access_' + webservice, 'all'),
        'addresses': addresses,
        'access_list': access_list,
        'hypesites_access': o.get_value('hype_access_' + webservice, 'off'),
    }, context_instance=RequestContext(request))



# Storage

def storage(request):
    o = Option()

    failed_mount_device = ''

    if request.POST.get('set_name', False):
        form = VolumesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            v = Volume.objects.get(identifier=request.POST.get('identifier'))
            v.name = cd['name'].strip()
            v.save()
    else:
        form = VolumesForm()

    if request.POST.get('use', False):
        v = Volume.objects.get(identifier=request.POST.get('identifier'))
        v.use = True
        v.save()
        mount_result = Popen(["volumes-mounter", "mount_drive", v.identifier, v.name], stdout=PIPE).communicate()[0]
        if 'failed' in mount_result:
            failed_mount_device = v
        o.config_changed(True)

    if request.POST.get('nouse', False):
        v = Volume.objects.get(identifier=request.POST.get('identifier'))
        v.use = False
        v.save()
        Popen(["volumes-mounter", "umount_drive", v.identifier, v.name], stdout=PIPE).communicate()[0]
        o.config_changed(True)

    if request.POST.get('remove', False):
        v = Volume.objects.get(identifier=request.POST.get('identifier'))
        v.delete()
        o.config_changed(True)

    # get all volumes via script
    volumes = Popen(["volumes-mounter", "list_drives"], stdout=PIPE).communicate()[0]

    # add them to db
    for volume in volumes.split('\n'):
        if volume != '':
            try:
                v = Volume()
                v.identifier = volume
                v.save()
            except Exception:
                pass

    # get stats for each volume
    db_volumes = Volume.objects.all().order_by('id')
    volumes = []
    for volume in db_volumes:
        try:
            stats = Popen(["volumes-mounter", "get_drive_stat", volume.identifier], stdout=PIPE).communicate()[0]
            mounted = stats.split('vol_mounted:')[1].split(' ')[0]
            size = stats.split('vol_size:')[1].split(' ')[0]
            v = Volume.objects.get(identifier=volume.identifier)
            v.status = 'mounted' if mounted == '1' else 'unmounted'
            v.size = size
            v.save()
        except Exception:
            v = Volume.objects.get(identifier=volume.identifier)
            v.status = 'unmounted'
            v.save()

    # get the updated volumes
    db_volumes = Volume.objects.all().order_by('id')

    return render_to_response('storage/overview.html', {
        'volumes': db_volumes,
        'form': form,
        'failed_mount_device': failed_mount_device,
    }, context_instance=RequestContext(request))



# Changes

@csrf_exempt
def apply_changes(request):
    if request.POST.get('apply_changes') == 'run':
        Popen(["/usr/sbin/cfengine-apply", "-b"], stdout=PIPE, close_fds=True)
        return HttpResponse('ok')

    return HttpResponse('')



# Format drive

@csrf_exempt
def format_drive(request):
    if request.POST.get('format_drive') == 'run':
        Popen(["/usr/sbin/volumes-mounter", "format_drive", request.POST.get('identifier')], stdout=PIPE, close_fds=True)
        return HttpResponse('ok')

    return HttpResponse('')



# Dynamic output

def dynamic_output(request):
    try:
        with open('/tmp/dynamic_output', 'r') as f:
            output = f.read()
    except Exception:
        output = ''

    from ansi2html import Ansi2HTMLConverter
    from django.http import HttpResponse
    conv = Ansi2HTMLConverter()
    html = conv.convert(output, full=False)
    return HttpResponse(html)



def dynamic_status(request):

    if request.GET.get('key') == 'applynow':
        import os.path
        if os.path.isfile('/tmp/apply-in-progress'):
            return HttpResponse('in progress')
        else:
            return HttpResponse('done')

    if request.GET.get('key') == 'restore':
        import os.path
        if os.path.isfile('/tmp/restore-in-progress'):
            return HttpResponse('in progress')
        else:
            return HttpResponse('done')

    if request.GET.get('key') == 'formatdrive':
        import os.path
        if os.path.isfile('/tmp/format-in-progress'):
            return HttpResponse('in progress')
        else:
            return HttpResponse('done')



# API

@csrf_exempt
def api_v1(request, api_url):
    from django.http import HttpResponse
    resp = {}
    resp['result'] = 'failed'

    if api_url == 'get_option':
        try:
            o = Option()
            r = o.get_value(request.POST['key'])
            resp['value'] = r
            resp['result'] = 'success'
        except Exception:
            resp['message'] = 'option not found or POST.key parameter missing'

    if api_url == 'set_option':
        try:
            o = Option()
            o.set_value(request.POST['key'], request.POST['value'])
            resp['result'] = 'success'
        except Exception:
            resp['message'] = 'error setting option'

    if api_url == 'get_missioncontrol':
        try:
            resp['value'] = _get_missioncontrol()
            resp['result'] = 'success'
        except Exception:
            resp['message'] = 'fail'

    if api_url == 'get_contacts':
        try:
            contacts = Address.objects.all().order_by('id')
            data = []
            for ct in contacts:
                data.append({
                    'name': ct.name,
                    'display_name': ct.display_name,
                    'ipv6': ct.ipv6,
                })
            resp['value'] = data
            resp['result'] = 'success'
        except Exception:
            resp['message'] = 'fail'

    if api_url == 'add_contact':
        try:
            hostname = request.POST.get('hostname', '').strip()
            hostname = slugify(hostname)
            ipv6 = request.POST.get('ipv6', '').strip()

            if hostname != '' and ipv6 != '':
                a = Address()
                a.name = hostname
                a.display_name = hostname.replace('-', ' ').title()
                a.ipv6 = ipv6
                a.save()
                resp['addrbook_url'] = 'http://enigma.box/addressbook/edit/' + str(a.id) + '/'
                resp['result'] = 'success'
                o = Option()
                o.config_changed(True)
            else:
                raise

        except Exception:
            resp['message'] = 'fail'

    if api_url == 'set_countries':
        try:
            countries = request.POST.get('countries', '').strip()
            prio = 1
            for country in countries.split(','):
                c = Country.objects.get(countrycode=country)
                c.priority = prio
                c.save()
                prio = prio + 1

            resp['result'] = 'ok'

        except Exception:
            resp['message'] = 'fail'

    if api_url == 'toggle_country':
        try:
            countrycode = request.POST.get('countrycode', '').strip()
            c = Country.objects.get(countrycode=countrycode)
            c.active = True if c.active == False else False
            c.save()

            resp['result'] = 'ok'

        except Exception:
            resp['message'] = 'fail'

    if api_url == 'set_next_country':
        our_default = 'ch'

        o = Option()
        current_country = o.get_value('selected_country')
        countries = Country.objects.filter(active=True).order_by('priority')
        if len(countries) < 1:
            next_country = our_default
        else:
            no_next_country = True
            i = 0
            for c in countries:
                if c.countrycode == current_country:
                    no_next_country = False
                    try:
                        next_country = countries[i+1].countrycode
                    except Exception:
                        try:
                            next_country = countries[0].countrycode
                        except Exception:
                            next_country = our_default
                i = i + 1

            if no_next_country:
                next_country = countries[0].countrycode

        o.set_value('selected_country', next_country)

        resp['value'] = next_country
        resp['result'] = 'success'

    if api_url == 'set_default_country':

        o = Option()
        default_country = o.get_value('default_country', 'ch')
        o.set_value('selected_country', default_country)

        resp['value'] = default_country
        resp['result'] = 'success'

    if api_url == 'get_hashed_rootpw':
        from crypt import crypt

        o = Option()
        password = o.get_value('root_password')
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        hashed_password = crypt(password, "$6$" + salt + "$")

        return HttpResponse(hashed_password)

    if api_url == 'get_firefoxAddon_info':
        o = Option()
        netstat = {
            'dhcp': '0',
            'dhcp_conflict': False,
            'internet': '0',
            'cjdns': '0',
            'cjdns_internet': '0',
        }
        
        message = "";
        
        for key, value in netstat.items():
            try:
                with open('/tmp/netstat-' + key, 'r') as f:
                    message += str(f.read().strip()) + "\n"
            except Exception:
                pass
        
        message += str(o.get_value('internet_access')) + "\n" + str(o.get_value('webfilter_filter-ads', 0)) + "\n" + str(o.get_value('selected_country', 'ch')) + "\n" + str(o.get_value('teletext_enabled', 0)) + "\n" + str(o.get_value('personal_website', 0)) + "\n" + str(o.get_value('dokuwiki', 0)) + "\n" + str(o.get_value('owncloud', 0)) + "\n" + str(o.get_value('pastebin', 0)) + "\n" + o.get_value('ipv6').strip()
        
        return HttpResponse(message)

    return HttpResponse(json.dumps(resp), content_type='application/json')



# Sites

def cfengine_site(request):
    from unidecode import unidecode
    o = Option()

    cjdns_ipv6 = o.get_value('ipv6').strip()
    cjdns_public_key = o.get_value('public_key')
    cjdns_private_key = o.get_value('private_key')
    cjdns_version = 'v16'
    selected_country = o.get_value('selected_country', 'ch')
    hostid = ''
    internet_access_formatted = ''
    addresses = []
    internet_gateway = []
    peerings = []
    display_expiration_notice = '0'
    is_alix = False
    is_apu = False
    is_raspi = False

    language = o.get_value('language', 'de')

    # get Enigmabox-specific server data, when available
    try:
        f = open('/box/server.json', 'r')
        json_data = json.load(f)

        hostid = json_data['hostid']
        internet_access = json_data['internet_access']
        password = json_data['password']

        try:
            cjdns_version = json_data['cjdns_version']
        except Exception:
            pass

        if cjdns_version == 'v16':
            try:
                # check for AVX support
                avxinfo = Popen(["grep", " avx ", "/proc/cpuinfo"], stdout=PIPE).communicate()[0]
                if len(avxinfo) > 0:
                    cjdns_version = 'v16_avx'
            except Exception:
                pass

        # allow version to be overridden by webinterface
        cjdns_version = o.get_value('cjdns_version', cjdns_version)

        o.set_value('hostid', hostid)
        o.set_value('internet_access', internet_access)
        o.set_value('password', password)

        try:
            dt = datetime.strptime(internet_access, '%Y-%m-%d')

            if language == 'en':
                internet_access_formatted = dt.strftime('%m %d, %Y')
            else:
                internet_access_formatted = dt.strftime('%d.%m.%Y')

        except Exception:
            internet_access_formatted = ''

        Peering.objects.filter(custom=False).delete()

        if cjdns_version == 'v6':
            json_peerings = json_data['peerings']
        else:
            json_peerings = json_data['peerings_topo128']

        for address, peering in json_peerings.items():
            p = Peering()
            p.address = address
            p.public_key = peering['publicKey']
            p.password = peering['password']
            p.country = peering['country']
            p.save()

        try:
            internet_gateway_db = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1][0]
            internet_gateway_db.public_key

        except Exception:
            try:
                one_active_country = Country.objects.filter(active=True).order_by('priority')[0]
                internet_gateway_db = Peering.objects.filter(custom=False,country=one_active_country).order_by('id')[:1][0]
                internet_gateway_db.public_key

            except Exception:
                try:
                    any_country = Country.objects.all().order_by('priority')[0]
                    internet_gateway_db = Peering.objects.filter(custom=False,country=any_country).order_by('id')[0]
                    internet_gateway_db.public_key

                except Exception:
                    internet_gateway_db = { 'public_key': '' }

        internet_gateway = {
            'public_key': internet_gateway_db.public_key,
        }

        # expiration notice
        dt = datetime.strptime(internet_access, '%Y-%m-%d')
        now = datetime.utcnow()
        three_weeks = timedelta(days=20)
        expiration_notice_confirmed = o.get_value('expiration_notice_confirmed', False)

        if (now + three_weeks) > dt:
            display_expiration_notice = '1'

        if expiration_notice_confirmed:
            display_expiration_notice = '0'

        # well, umm, leave it hidden, in case the box didn't get the update
        #if now > dt:
        #    display_expiration_notice = '1'

    except Exception:
        # no additional server data found, moving on...
        pass

    try:
        with open('/etc/enigmabox/network-profile', 'r') as f:
            network_profile = f.read().strip()
            if network_profile == 'alix':
                is_alix = True
            if network_profile == 'apu':
                is_apu = True
            if network_profile == 'raspi':
                is_raspi = True
    except Exception:
        pass

    #server_peerings = Peering.objects.filter(custom=False).order_by('id')
    server_peerings = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1]
    for p in server_peerings:
        peerings.append({
            'ip': p.address.split(':')[0],
            'address': p.address,
            'password': p.password,
            'public_key': p.public_key,
        })

    custom_peerings = Peering.objects.filter(custom=True).order_by('id')
    for p in custom_peerings:
        peerings.append({
            'ip': p.address.split(':')[0],
            'address': p.address,
            'password': p.password,
            'public_key': p.public_key,
        })

    db_addresses = Address.objects.filter().order_by('id')
    for a in db_addresses:
        addresses.append({
            'ipv6': a.ipv6,
            'hostname': a.name,
            'display_name': unidecode(a.display_name),
            'phone': a.phone,
        })

    global_addresses = []
    try:
        import sqlite3
        db = sqlite3.connect('/etc/enigmabox/addressbook.db')
        db.text_factory = sqlite3.OptimizedUnicode
        c = db.cursor()
        c.execute("SELECT ipv6,hostname,phone FROM addresses")

        for address in c.fetchall():
            global_addresses.append({
                'ipv6': address[0],
                'hostname': address[1],
                'phone': address[2],
            })

    except Exception:
        pass

    volumes = []
    db_volumes = Volume.objects.filter(use=True).order_by('id')
    for v in db_volumes:
        volumes.append({
            'identifier': v.identifier,
            'name': v.name,
        })

    portforwardings = []
    pfw = Portforward.objects.all().order_by('port')
    for p in pfw:
        acl = PortforwardAccess.objects.get(port=p.port).addresses.all()
        access_list = []
        for a in acl:
            access_list.append({
                'ipv6': a.ipv6,
            })
        portforwardings.append({
            'port': p.port,
            'mac': p.hw_address,
            'dstport': p.dstport,
            'access': p.access,
            'access_list': access_list,
        })

    webinterface_password = o.get_value('webinterface_password', '')
    mailbox_password = o.get_value(u'mailbox_password')

    if mailbox_password is None:
        mailbox_password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(64))
        o.set_value('mailbox_password', mailbox_password)

    mailbox_password = mailbox_password.encode('utf-8')

    # hash the password
    import hashlib
    import base64
    p = hashlib.sha1(mailbox_password)
    mailbox_password = base64.b64encode(p.digest())

    # webfilter: format custom rules
    custom_rules_text = o.get_value('webfilter_custom-rules-text', '')
    custom_rules_text_array = []
    for crt in custom_rules_text.split('\n'):
        crt = crt.strip()
        if crt == '':
            continue
        crt = crt.lower()
        custom_rules_text_array.append({'rule': crt})
    custom_rules_text = custom_rules_text_array

    wlan_opmode = o.get_value('wlan_opmode', 'mesh')
    meshmode = (wlan_opmode == 'mesh')

    # autopeering
    if o.get_value('autopeering', 0) == '1':

        try:
            with open('/etc/enigmabox/network-profile', 'r') as f:
                network_profile = f.read().strip()

            if network_profile == 'alix':
                autopeering = [
                    {
                        'interface': 'eth0',
                    },
                    {
                        'interface': 'eth1',
                    },
                    {
                        'interface': 'eth2',
                    },
                ]
            if network_profile == 'apu':
                autopeering = [
                    {
                        'interface': 'eth0',
                    },
                    {
                        'interface': 'eth1',
                    },
                    {
                        'interface': 'eth2',
                    },
                ]
            if network_profile == 'raspi':
                autopeering = [
                    {
                        'interface': 'eth0',
                    },
                ]

        except Exception:
            autopeering = 0

    else:
        autopeering = 0

    volumes = []
    db_volumes = Volume.objects.filter(use=True).order_by('id')
    for v in db_volumes:
        volumes.append({
            'identifier': v.identifier,
            'name': v.name,
        })

    hypesites_access = o.get_value('hypesites_access', 'off'),
    hype_access_off = (hypesites_access[0] == 'off')
    hype_access_internal = (hypesites_access[0] == 'internal')
    hype_access_friends = (hypesites_access[0] == 'friends')
    hype_access_global = (hypesites_access[0] == 'global')

    hype_access_site = o.get_value('hype_access_site', 'all')
    hype_access_dokuwiki = o.get_value('hype_access_dokuwiki', 'all')
    hype_access_owncloud = o.get_value('hype_access_owncloud', 'all')

    my_ip = o.get_value('ipv6', '')

    addresslist = []
    if hype_access_site == 'friends':
        addresslist = Address.objects.all().order_by('id')
    elif hype_access_site == 'specific':
        addresslist = HypeAccess.objects.get(appname='site').addresses.all()
    hype_site_accesslist = [{'ipv6': my_ip}]
    for address in addresslist:
        hype_site_accesslist.append({'ipv6': address.ipv6})
    hype_access_site_all = (hype_access_site == 'all')

    addresslist = []
    if hype_access_dokuwiki == 'friends':
        addresslist = Address.objects.all().order_by('id')
    elif hype_access_dokuwiki == 'specific':
        addresslist = HypeAccess.objects.get(appname='dokuwiki').addresses.all()
    hype_dokuwiki_accesslist = [{'ipv6': my_ip}]
    for address in addresslist:
        hype_dokuwiki_accesslist.append({'ipv6': address.ipv6})
    hype_access_dokuwiki_all = (hype_access_dokuwiki == 'all')

    addresslist = []
    if hype_access_owncloud == 'friends':
        addresslist = Address.objects.all().order_by('id')
    elif hype_access_owncloud == 'specific':
        addresslist = HypeAccess.objects.get(appname='owncloud').addresses.all()
    hype_owncloud_accesslist = [{'ipv6': my_ip}]
    for address in addresslist:
        hype_owncloud_accesslist.append({'ipv6': address.ipv6})
    hype_access_owncloud_all = (hype_access_owncloud == 'all')

    # Transform hostid
    hostid_phonetic = hostid.replace('', ', ')

    # language usable for mustache
    try:
        language_de = language == 'de'
        language_en = language != 'de'
    except Exception:
        language_de = False
        language_en = True

    response_data = {
        'hostid': hostid,
        'internet_access_formatted': internet_access_formatted,
        'hostid_phonetic': hostid_phonetic,
        'language': language,
        'language_de': language_de,
        'language_en': language_en,
        'cjdns_ipv6': cjdns_ipv6,
        'cjdns_public_key': cjdns_public_key,
        'cjdns_private_key': cjdns_private_key,
        'cjdns_version': cjdns_version,
        'cjdns_v6': cjdns_version == 'v6',
        'addresses': addresses,
        'global_addresses': global_addresses,
        'global_availability': o.get_value('global_availability', 0),
        'missioncontrol': _get_missioncontrol(),
        'autoupdates': o.get_value('autoupdates', '1'),
        'wlan_ssid': o.get_value('wlan_ssid'),
        'wlan_opmode': wlan_opmode,
        'meshmode': meshmode,
        'is_alix': is_alix,
        'is_apu': is_apu,
        'is_raspi': is_raspi,
        'wlan_pass': o.get_value('wlan_pass'),
        'wlan_security': o.get_value('wlan_security'),
        'wlan_group': o.get_value('wlan_group'),
        'wlan_pairwise': o.get_value('wlan_pairwise'),
        'lan_range_first': o.get_value('lan_range_first', 100),
        'lan_range_second': o.get_value('lan_range_second', 101),
        'peerings': peerings,
        'portforwardings': portforwardings,
        'internet_gateway': internet_gateway,
        'autopeering': autopeering,
        'allow_peering': o.get_value('allow_peering', 0),
        'peering_port': o.get_value('peering_port'),
        'peering_password': o.get_value('peering_password'),
        'webinterface_password': webinterface_password,
        'mailbox_password': mailbox_password,
        'webfilter_filter_ads': o.get_value('webfilter_filter-ads', 0),
        'webfilter_block-win10stasi': o.get_value('webfilter_block-win10stasi', 0),
        'webfilter_filter_headers': o.get_value('webfilter_filter-headers', 0),
        'webfilter_disable_browser_ident': o.get_value('webfilter_disable-browser-ident', 0),
        'webfilter_block_facebook': o.get_value('webfilter_block-facebook', 0),
        'webfilter_block_google': o.get_value('webfilter_block-google', 0),
        'webfilter_block_twitter': o.get_value('webfilter_block-twitter', 0),
        'webfilter_custom_rules': o.get_value('webfilter_custom-rules', 0),
        'webfilter_custom_rules_text': custom_rules_text,
        'teletext_enabled': o.get_value('teletext_enabled', 0),
        'hype_access_off': hype_access_off,
        'hype_access_internal': hype_access_internal,
        'hype_access_friends': hype_access_friends,
        'hype_access_global': hype_access_global,
        'hype_personal_site': o.get_value('personal_website', 0),
        'hype_dokuwiki': o.get_value('dokuwiki', 0),
        'hype_owncloud': o.get_value('owncloud', 0),
        'hype_pastebin': o.get_value('pastebin', 0),
        'hype_access_site_all': hype_access_site_all,
        'hype_access_dokuwiki_all': hype_access_dokuwiki_all,
        'hype_access_owncloud_all': hype_access_owncloud_all,
        'hype_site_accesslist': hype_site_accesslist,
        'hype_dokuwiki_accesslist': hype_dokuwiki_accesslist,
        'hype_owncloud_accesslist': hype_owncloud_accesslist,
        'display_expiration_notice': display_expiration_notice,
        'volumes': volumes,
    }

    # and this, ladies and gentlemen, is a workaround for mustache
    r2 = {}
    for key in response_data:
        if str(response_data[key]) == '0':
            response_data[key] = False

        r2['if_' + key] = bool(response_data[key])
        r2[key] = response_data[key]

    response_data = r2

    return HttpResponse(json.dumps(response_data,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    ), content_type="application/json")



def _get_missioncontrol():
    missioncontrol = []

    try:
        with open('/box/.missioncontrol', 'r') as f:
            missioncontrol_content = f.read().strip()

        for mc in missioncontrol_content.split('\n'):
            missioncontrol.append({
                'ip': mc.split(' ')[0],
                'hostname': mc.split(' ')[1],
            })

    except Exception:
        pass

    return missioncontrol
