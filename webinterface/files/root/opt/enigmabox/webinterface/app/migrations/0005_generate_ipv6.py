# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from subprocess import Popen, PIPE

class Migration(DataMigration):

    def forwards(self, orm):

        try:
            o = orm.Option.objects.get(key='private_key')

        except:
            output = Popen(["cjdroute", "--genconf"], stdout=PIPE).communicate()[0]
            ipv6 = output.split('"ipv6": "')[1].split('",')[0]
            public_key = output.split('"publicKey": "')[1].split('",')[0]
            private_key = output.split('"privateKey": "')[1].split('",')[0]

            d = {'ipv6': ipv6, 'public_key': public_key, 'private_key': private_key}

            for key, value in d.items():
                if value:
                    try:
                        o = orm.Option.objects.get(key=key)
                    except:
                        o = orm.Option()
                        o.key = key
                    o.value = value
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
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '54'})
        }
    }

    complete_apps = ['app']
    symmetrical = True
