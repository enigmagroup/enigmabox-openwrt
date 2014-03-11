# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        try:
            f = open('/box/cjdroute.conf', 'r')
            content = f.read()

            try:
                private_key = content.split('"privateKey": "')[1].split('",')[0]
            except:
                private_key = False
            try:
                public_key = content.split('"publicKey": "')[1].split('",')[0]
            except:
                public_key = False
            try:
                ipv6 = content.split('"ipv6": "')[1].split('",')[0]
            except:
                ipv6 = False

            d = {'private_key': private_key, 'public_key': public_key, 'ipv6': ipv6}

            for key, value in d.items():
                if value:
                    try:
                        o = orm.Option.objects.get(key=key)
                    except:
                        o = orm.Option()
                        o.key = key
                    o.value = value
                    o.save()

        except:
            print 'no cjdroute.conf found, moving on...'

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
