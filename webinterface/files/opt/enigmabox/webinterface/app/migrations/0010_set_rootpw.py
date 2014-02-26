# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.auth.models import User
from crypt import crypt
from subprocess import Popen, PIPE
import random, string

class Migration(DataMigration):

    def forwards(self, orm):

        # generate a password
        password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        hashed_password = crypt(password, "$6$" + salt + "$")

        # set root password
        Popen(['sudo', 'usermod', '-p', hashed_password, 'root'], stdout=PIPE).communicate()[0]

        # set django admin password
        u = User.objects.get(username__exact='admin')
        u.set_password(password)
        u.save()

        # save password into db
        o = orm.Option()
        o.key = 'root_password'
        o.value = password
        o.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'app.address': {
            'Meta': {'object_name': 'Address'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv6': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        },
        'app.option': {
            'Meta': {'object_name': 'Option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'app.peering': {
            'Meta': {'object_name': 'Peering'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'custom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '54'})
        },
        'app.puppetmaster': {
            'Meta': {'object_name': 'Puppetmaster'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['app']
    symmetrical = True
