# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from subprocess import Popen, PIPE

class Migration(DataMigration):

    def forwards(self, orm):
        try:
            ifconfig = Popen(["/sbin/ifconfig", "tun0"], stdout=PIPE).communicate()[0]
            ipv6 = ifconfig.split('inet6 addr: ')[1].split('/8 Scope:Global')[0]
            if ipv6:
                o = orm.Option()
                o.key = 'ipv6'
                o.value = ipv6
                o.save()
        except:
            pass

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
        }
    }

    complete_apps = ['app']
    symmetrical = True
