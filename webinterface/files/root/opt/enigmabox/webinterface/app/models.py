from django.db import models
from subprocess import Popen, PIPE

class Address(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    ipv6 = models.CharField(max_length=39)
    phone = models.IntegerField(max_length=7, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Peering(models.Model):
    address = models.CharField(max_length=30)
    public_key = models.CharField(max_length=54)
    password = models.CharField(max_length=64)
    country = models.CharField(max_length=2, blank=True)
    description = models.TextField(null=True, blank=True)
    custom = models.BooleanField(default=False)

    def __unicode__(self):
        return self.address

class Country(models.Model):
    countrycode = models.CharField(max_length=2)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(max_length=2)

    def __unicode__(self):
        return self.countrycode

class HypeAccess(models.Model):
    appname = models.CharField(max_length=20)
    addresses = models.ManyToManyField(Address, blank=True)

    def __unicode__(self):
        return self.appname

class PortForward(models.Model):
    port = models.IntegerField(max_length=5, unique=True)
    hw_address = models.CharField(max_length=17)
    description = models.CharField(max_length=100, null=True, blank=True)
    access = models.CharField(max_length=10)

    def __unicode__(self):
        return self.port

class PortForwardAccess(models.Model):
    port = models.IntegerField(max_length=5, unique=True)
    addresses = models.ManyToManyField(Address, blank=True)

    def __unicode__(self):
        return self.port

class Volume(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    size = models.IntegerField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    use = models.BooleanField(default=False)

    def __unicode__(self):
        return self.identifier

class Option(models.Model):
    key = models.CharField(max_length=50)
    value = models.TextField()

    def __unicode__(self):
        return self.key

    def get_ipv6(self):
        try:
            ipv6 = Option.objects.filter(key='ipv6')[0].value
        except:
            ifconfig = Popen(["/sbin/ifconfig", "tun0"], stdout=PIPE).communicate()[0]
            ipv6 = ifconfig.split('inet6 addr: ')[1].split('/8 Scope:Global')[0]
            if ipv6:
                o = Option()
                o.key = 'ipv6'
                o.value = ipv6
                o.save()

        return ipv6

    def config_changed(self, setval=None):
        if setval is True:
            try:
                o = Option.objects.filter(key='config_changed')[0]
            except:
                o = Option()
                o.key = 'config_changed'
            o.value = '1'
            o.save()

        if setval is False:
            try:
                o = Option.objects.filter(key='config_changed')[0]
            except:
                o = Option()
                o.key = 'config_changed'
            o.value = '0'
            o.save()

        try:
            cc = Option.objects.filter(key='config_changed')[0]
            return cc.value == '1'
        except:
            return False

    def get_value(self, option_key, default=None):
        try:
            o = Option.objects.filter(key=option_key)[0]
            return o.value
        except:
            return default

    def set_value(self, option_key, option_value):
        try:
            o = Option.objects.filter(key=option_key)[0]
        except:
            o = Option()
            o.key = option_key
        o.value = option_value
        o.save()

    def toggle_value(self, option_key):
        try:
            o = Option.objects.filter(key=option_key)[0]
            option_value = o.value
        except:
            o = Option()
            o.key = option_key
            option_value = '0'
        if option_value == '1':
            o.value = '0'
        else:
            o.value = '1'
        o.save()



# autocreate superuser
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

# From http://stackoverflow.com/questions/1466827/ --
#
# Prevent interactive question about wanting a superuser created.  (This code
# has to go in this otherwise empty "models" module so that it gets processed by
# the "syncdb" command during database creation.)
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')


# Create our own test user automatically.

def create_testuser(app, created_models, verbosity, **kwargs):
  if not settings.DEBUG:
    return
  try:
    auth_models.User.objects.get(username='admin')
  except auth_models.User.DoesNotExist:
    print '*' * 80
    print 'Creating admin user -- login: admin, password: admin'
    print '*' * 80
    assert auth_models.User.objects.create_superuser('admin', 'x@x.com', 'admin')
  else:
    print 'Test user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='common.models.create_testuser')
