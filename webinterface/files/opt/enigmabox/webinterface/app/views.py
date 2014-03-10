from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from subprocess import Popen, PIPE
from app.models import *
from app.forms import *
import random
import string
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from slugify import slugify



def home(request):
    o = Option()

    if request.session.get('django_language') == None:
        language = o.get_value('language', 'de')
        request.session['django_language'] = language
        return redirect('/')

    netstat = {
        'dhcp': '0',
        'internet': '0',
        'cjdns': '0',
        'cjdns_internet': '0',
    }

    for key, value in netstat.items():
        try:
            with open('/tmp/netstat-' + key, 'r') as f:
                netstat[key] = f.read().strip()
        except:
            pass

    return render_to_response('home.html', {
        'hostid': o.get_value('hostid'),
        'internet_access': o.get_value('internet_access'),
        'teletext_enabled': o.get_value('teletext_enabled'),
        'root_password': o.get_value('root_password'),
        'netstat': netstat,
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
            a.ipv6 = cd['ipv6'].strip()
            a.phone = cd['phone']
            a.save()
            o = Option()
            o.config_changed(True)
            return redirect('/addressbook/')
    else:
        form = AddressbookForm()

    addresses = Address.objects.all().order_by('id')
    sip_peers = Popen(["sudo", "asterisk", "-rx", "sip show peers"], stdout=PIPE).communicate()[0]

    return render_to_response('addressbook/overview.html', {
        'addresses': addresses,
        'form': form,
        'sip_peers': sip_peers,
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
            a.ipv6 = cd['ipv6'].strip()
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



# Passwords

def passwords(request):

    o = Option()

    if request.POST.get('set_webinterface_password'):
        o.set_value('webinterface_password', request.POST.get('webinterface_password'))
        o.config_changed(True)

    if request.POST.get('set_mailbox_password'):
        o.set_value('mailbox_password', request.POST.get('mailbox_password'))
        o.config_changed(True)

    return render_to_response('passwords.html', {
        'webinterface_password': o.get_value('webinterface_password'),
        'mailbox_password': o.get_value('mailbox_password'),
    }, context_instance=RequestContext(request))



# Backup & restore

def backup(request):

    o = Option()

    if request.POST.get('set_webinterface_password'):
        o.set_value('webinterface_password', request.POST.get('webinterface_password'))
        o.config_changed(True)

    if request.POST.get('set_mailbox_password'):
        o.set_value('mailbox_password', request.POST.get('mailbox_password'))
        o.config_changed(True)

    return render_to_response('backup/overview.html', {
        'webinterface_password': o.get_value('webinterface_password'),
        'mailbox_password': o.get_value('mailbox_password'),
    }, context_instance=RequestContext(request))

def backup_system(request):

    o = Option()
    temp_db = '/tmp/settings.sqlite'
    final_db = '/box/settings.sqlite'
    msg = False

    if request.POST.get('backup'):
        import os
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper

        filename = '/box/settings.sqlite'
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/x-sqlite3')
        response['Content-Disposition'] = 'attachment; filename=settings.sqlite'
        response['Content-Length'] = os.path.getsize(filename)
        return response

    if request.POST.get('upload_check'):
        import sqlite3

        try:
            destination = open(temp_db, 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()

            conn = sqlite3.connect(temp_db)
            c = conn.cursor()
            c.execute('select value from app_option where key = "ipv6"')
            msg = c.fetchone()[0]
            conn.close()
        except:
            msg = 'invalid'

    if request.POST.get('restore'):
        import shutil

        shutil.move(temp_db, final_db)

        o.config_changed(True)
        o.set_value('internet_requested', 0)
        return redirect('/backup/system/')

    return render_to_response('backup/system.html', {
        'msg': msg,
    }, context_instance=RequestContext(request))

def backup_emails(request):

    o = Option()
    filename = '/tmp/emails.tar.gz'
    msg = False

    if request.POST.get('backup'):
        import os
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper

        try:
            Popen(["sudo", "/usr/local/sbin/backup-stuff", "emails"], stdout=PIPE).communicate()[0]

            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename=emails.tar.gz'
            response['Content-Length'] = os.path.getsize(filename)
            return response
        except:
            msg = 'backuperror'

    if request.POST.get('restore'):

        try:
            destination = open('/tmp/emails.tar.gz', 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()

            Popen(["sudo", "/usr/local/sbin/restore-stuff", "emails"], stdout=PIPE).communicate()[0]
            msg = 'restoresuccess'

        except:
            msg = 'restoreerror'

    return render_to_response('backup/emails.html', {
        'msg': msg,
    }, context_instance=RequestContext(request))

def backup_sslcerts(request):

    o = Option()
    filename = '/tmp/sslcerts.tar.gz'
    msg = False

    if request.POST.get('backup'):
        import os
        from django.http import HttpResponse
        from django.core.servers.basehttp import FileWrapper

        try:
            Popen(["sudo", "/usr/local/sbin/backup-stuff", "sslcerts"], stdout=PIPE).communicate()[0]

            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename=sslcerts.tar.gz'
            response['Content-Length'] = os.path.getsize(filename)
            return response
        except:
            msg = 'backuperror'

    if request.POST.get('restore'):

        try:
            destination = open('/tmp/sslcerts.tar.gz', 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()

            Popen(["sudo", "/usr/local/sbin/restore-stuff", "sslcerts"], stdout=PIPE).communicate()[0]
            msg = 'restoresuccess'

        except:
            msg = 'restoreerror'

    return render_to_response('backup/sslcerts.html', {
        'msg': msg,
    }, context_instance=RequestContext(request))



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



# Country selection

def countryselect(request):

    o = Option()

    if request.POST:
        country = request.POST.get('country')
        o.set_value('selected_country', country)
        o.config_changed(True)

    countries = {
        'hu': _('Hungary'),
        'fr': _('France'),
        'ch': _('Switzerland'),
        'de': _('Germany'),
        'us': _('United Stasi of America'),
    }

    return render_to_response('countryselect/overview.html', {
        'countries': countries,
        'selected_country': o.get_value('selected_country', 'hu'),
    }, context_instance=RequestContext(request))



# Web filter

def webfilter(request):

    o = Option()

    if request.POST:
        o.config_changed(True)

        # always send that data, even if its an empty string
        o.set_value('webfilter_custom-rules-text', request.POST.get('custom-rules-text'))

    settings_fields = ['filter-ads', 'filter-headers', 'disable-browser-ident', 'block-facebook', 'block-google', 'block-twitter', 'custom-rules']

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

    if request.POST:
        o.set_value('wlan_ssid', request.POST.get('ssid'))
        o.set_value('wlan_pass', request.POST.get('pass'))
        o.set_value('wlan_security', request.POST.get('security'))
        o.config_changed(True)

    return render_to_response('wlan_settings/overview.html', {
        'wlan_ssid': o.get_value('wlan_ssid', ''),
        'wlan_pass': o.get_value('wlan_pass', ''),
        'wlan_security': o.get_value('wlan_security', 'WPA2'),
    }, context_instance=RequestContext(request))

def wlan_scan(request):

    o = Option()

    if request.POST:
        o.set_value('wlan_ssid', request.POST.get('ssid'))
        o.set_value('wlan_security', request.POST.get('security'))
        o.set_value('wlan_group', request.POST.get('group'))
        o.set_value('wlan_pairwise', request.POST.get('pairwise'))
        return redirect('/wlan_settings/')

    final_cells = []

    Popen(["sudo", "ifconfig", "wlan0", "up"], stdout=PIPE).communicate()[0]
    scan = Popen(["sudo", "iwlist", "wlan0", "scan"], stdout=PIPE).communicate()[0]

    cells = scan.split('Cell ')
    for cell in cells:
        try:
            ssid = cell.split('ESSID:')[1].split('\n')[0].replace('"', '').strip()
            quality = cell.split('Quality=')[1].split(' ')[0].strip()

            try:
                group = cell.split('Group Cipher')[1].split('\n')[0].split(' ')[-1:][0].strip()
            except:
                group = ''

            try:
                pairwise = cell.split('Pairwise Ciphers')[1].split('\n')[0].split(' ')[-1:][0].strip()
            except:
                pairwise = ''

            if 'WPA' in cell:
                security = 'WPA'
            else:
                security = 'WEP'

            final_cells.append({
                'ssid': ssid,
                'quality': quality,
                'security': security,
                'group': group,
                'pairwise': pairwise,
            })
        except:
            pass

    return render_to_response('wlan_settings/scan.html', {
        'cells': final_cells,
    }, context_instance=RequestContext(request))



# Teletext

def teletext(request):

    o = Option()

    if request.POST:
        o.toggle_value('teletext_enabled')
        o.config_changed(True)

    return render_to_response('teletext/overview.html', {
        'teletext_enabled': o.get_value('teletext_enabled', 0),
    }, context_instance=RequestContext(request))



# Changes

def apply_changes(request):

    output_window = False
    loader_hint = ''

    if request.POST.get('apply_changes') == 'dry_run':
        output_window = True
        loader_hint = 'dry-run'
        Popen(["sudo", "/usr/local/sbin/puppet-apply", "-b"], stdout=PIPE)
    if request.POST.get('apply_changes') == 'run':
        output_window = True
        loader_hint = 'run'
        Popen(["sudo", "/usr/local/sbin/puppet-apply", "-r", "-b"], stdout=PIPE)
    if request.POST.get('apply_changes') == 'back':
        return redirect('/')

    return render_to_response('changes/apply.html', {
        'output_window': output_window,
        'loader_hint': loader_hint,
    }, context_instance=RequestContext(request))

def puppet_output(request):
    with open('/tmp/puppet_output', 'r') as f:
        output = f.read()
    from ansi2html import Ansi2HTMLConverter
    from django.http import HttpResponse
    conv = Ansi2HTMLConverter()
    html = conv.convert(output, full=False)
    return HttpResponse(html)



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
        except:
            resp['message'] = 'option not found or POST.key parameter missing'

    if api_url == 'set_option':
        try:
            o = Option()
            o.set_value(request.POST['key'], request.POST['value'])
            resp['result'] = 'success'
        except:
            resp['message'] = 'error setting option'

    if api_url == 'get_puppetmasters':
        try:
            puppetmasters = Puppetmaster.objects.all().order_by('priority')
            data = []
            for pm in puppetmasters:
                data.append(pm.hostname)
            resp['value'] = data
            resp['result'] = 'success'
        except:
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
        except:
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

        except:
            resp['message'] = 'fail'

    return HttpResponse(json.dumps(resp), content_type='application/json')



# Sites

def puppet_site(request, program):

    if program == 'puppet':
        template = 'puppet/site.pp'
    else:
        template = 'ansible/site.yml'

    o = Option()

    box = {}
    box['ipv6'] = o.get_value('ipv6').strip()
    box['public_key'] = o.get_value('public_key')
    box['private_key'] = o.get_value('private_key')
    selected_country = o.get_value('selected_country', 'hu')
    addresses = ''
    puppetmasters = ''
    internet_gateway = ''
    peerings = ''

    # get Enigmabox-specific server data, when available
    try:
        f = open('/box/server.json', 'r')
        json_data = json.load(f)

        hostid = json_data['hostid']
        internet_access = json_data['internet_access']
        password = json_data['password']
        puppetmasters = json_data['puppetmasters']
        peerings = json_data['peerings']

        o.set_value('hostid', hostid)
        o.set_value('internet_access', internet_access)
        o.set_value('password', password)

        Puppetmaster.objects.all().delete()

        for pm in puppetmasters:
            p = Puppetmaster()
            p.ip = pm[0]
            p.hostname = pm[1]
            p.priority = pm[2]
            p.save()

        Peering.objects.filter(custom=False).delete()

        for address, peering in peerings.items():
            p = Peering()
            p.address = address
            p.public_key = peering['publicKey']
            p.password = peering['password']
            p.country = peering['country']
            p.save()

        puppetmasters = Puppetmaster.objects.all().order_by('priority')
        internet_gateway = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1][0]

    except:
        # no additional server data found, moving on...
        pass

    peerings = []

    server_peerings = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1]
    for peering in server_peerings:
        peerings.append(peering)

    custom_peerings = Peering.objects.filter(custom=True).order_by('id')
    for peering in custom_peerings:
        peerings.append(peering)

    addresses = Address.objects.all().order_by('id')

    webinterface_password = o.get_value('webinterface_password')
    mailbox_password = o.get_value(u'mailbox_password')

    if webinterface_password is None:
        webinterface_password = ''

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
    # four backslashes: django -> puppet -> tinyproxy-regex
    custom_rules_text = custom_rules_text.replace('.', '\\\\.')
    custom_rules_text = custom_rules_text.replace('-', '\\\\-')

    return render_to_response(template, {
        'box': box,
        'addresses': addresses,
        'puppetmasters': puppetmasters,
        'wlan_ssid': o.get_value('wlan_ssid'),
        'wlan_pass': o.get_value('wlan_pass'),
        'wlan_security': o.get_value('wlan_security'),
        'wlan_group': o.get_value('wlan_group', ''),
        'wlan_pairwise': o.get_value('wlan_pairwise', ''),
        'peerings': peerings,
        'internet_gateway': internet_gateway,
        'autopeering': o.get_value('autopeering'),
        'allow_peering': o.get_value('allow_peering'),
        'peering_port': o.get_value('peering_port'),
        'peering_password': o.get_value('peering_password'),
        'webinterface_password': webinterface_password,
        'mailbox_password': mailbox_password,
        'webfilter_filter_ads': o.get_value('webfilter_filter-ads', ''),
        'webfilter_filter_headers': o.get_value('webfilter_filter-headers', ''),
        'webfilter_disable_browser_ident': o.get_value('webfilter_disable-browser-ident', ''),
        'webfilter_block_facebook': o.get_value('webfilter_block-facebook', ''),
        'webfilter_block_google': o.get_value('webfilter_block-google', ''),
        'webfilter_block_twitter': o.get_value('webfilter_block-twitter', ''),
        'webfilter_custom_rules': o.get_value('webfilter_custom-rules', ''),
        'webfilter_custom_rules_text': custom_rules_text,
        'teletext_enabled': o.get_value('teletext_enabled', '0'),
    })

def cfengine_site(request):

    o = Option()

    cjdns_ipv6 = o.get_value('ipv6').strip()
    cjdns_public_key = o.get_value('public_key')
    cjdns_private_key = o.get_value('private_key')
    selected_country = o.get_value('selected_country', 'hu')
    addresses = ''
    puppetmasters = ''
    internet_gateway = ''
    peerings = ''

    # get Enigmabox-specific server data, when available
    try:
        f = open('/box/server.json', 'r')
        json_data = json.load(f)

        hostid = json_data['hostid']
        internet_access = json_data['internet_access']
        password = json_data['password']
        puppetmasters = json_data['puppetmasters']
        peerings = json_data['peerings']

        o.set_value('hostid', hostid)
        o.set_value('internet_access', internet_access)
        o.set_value('password', password)

        Puppetmaster.objects.all().delete()

        for pm in puppetmasters:
            p = Puppetmaster()
            p.ip = pm[0]
            p.hostname = pm[1]
            p.priority = pm[2]
            p.save()

        Peering.objects.filter(custom=False).delete()

        for address, peering in peerings.items():
            p = Peering()
            p.address = address
            p.public_key = peering['publicKey']
            p.password = peering['password']
            p.country = peering['country']
            p.save()

        puppetmasters = Puppetmaster.objects.all().order_by('priority')
        internet_gateway = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1][0]

    except:
        # no additional server data found, moving on...
        pass

    peerings = []

    server_peerings = Peering.objects.filter(custom=False,country=selected_country).order_by('id')[:1]
    for peering in server_peerings:
        peerings.append(peering)

    custom_peerings = Peering.objects.filter(custom=True).order_by('id')
    for peering in custom_peerings:
        peerings.append(peering)

    addresses = []
    db_addresses = Address.objects.filter().order_by('id')
    for address in db_addresses:
        print address
        addresses.append(address)

    webinterface_password = o.get_value('webinterface_password')
    mailbox_password = o.get_value(u'mailbox_password')

    if webinterface_password is None:
        webinterface_password = ''

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
    # four backslashes: django -> puppet -> tinyproxy-regex
    custom_rules_text = custom_rules_text.replace('.', '\\\\.')
    custom_rules_text = custom_rules_text.replace('-', '\\\\-')

    response_data = {
        'cjdns_ipv6': cjdns_ipv6,
        'cjdns_public_key': cjdns_public_key,
        'cjdns_private_key': cjdns_private_key,
        'addresses': addresses,
        'puppetmasters': puppetmasters,
        'wlan_ssid': o.get_value('wlan_ssid'),
        'wlan_pass': o.get_value('wlan_pass'),
        'wlan_security': o.get_value('wlan_security'),
        'wlan_group': o.get_value('wlan_group', ''),
        'wlan_pairwise': o.get_value('wlan_pairwise', ''),
        'peerings': peerings,
        'internet_gateway': internet_gateway,
        'autopeering': o.get_value('autopeering'),
        'allow_peering': o.get_value('allow_peering'),
        'peering_port': o.get_value('peering_port'),
        'peering_password': o.get_value('peering_password'),
        'webinterface_password': webinterface_password,
        'mailbox_password': mailbox_password,
        'webfilter_filter_ads': o.get_value('webfilter_filter-ads', ''),
        'webfilter_filter_headers': o.get_value('webfilter_filter-headers', ''),
        'webfilter_disable_browser_ident': o.get_value('webfilter_disable-browser-ident', ''),
        'webfilter_block_facebook': o.get_value('webfilter_block-facebook', ''),
        'webfilter_block_google': o.get_value('webfilter_block-google', ''),
        'webfilter_block_twitter': o.get_value('webfilter_block-twitter', ''),
        'webfilter_custom_rules': o.get_value('webfilter_custom-rules', ''),
        'webfilter_custom_rules_text': custom_rules_text,
        'teletext_enabled': o.get_value('teletext_enabled', '0'),
    }

    import json

    print response_data

    from django.http import HttpResponse

    return HttpResponse(json.dumps(response_data, sort_keys=True, indent=4, separators=(',', ': ')), content_type="application/json")

