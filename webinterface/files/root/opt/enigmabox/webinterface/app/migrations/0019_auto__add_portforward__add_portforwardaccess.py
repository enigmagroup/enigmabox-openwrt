# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Portforward'
        db.create_table('app_portforward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=5)),
            ('dstport', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('hw_address', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('app', ['Portforward'])

        # Adding model 'PortforwardAccess'
        db.create_table('app_portforwardaccess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=5)),
        ))
        db.send_create_signal('app', ['PortforwardAccess'])

        # Adding M2M table for field addresses on 'PortforwardAccess'
        m2m_table_name = db.shorten_name('app_portforwardaccess_addresses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('portforwardaccess', models.ForeignKey(orm['app.portforwardaccess'], null=False)),
            ('address', models.ForeignKey(orm['app.address'], null=False))
        ))
        db.create_unique(m2m_table_name, ['portforwardaccess_id', 'address_id'])


    def backwards(self, orm):
        # Deleting model 'Portforward'
        db.delete_table('app_portforward')

        # Deleting model 'PortforwardAccess'
        db.delete_table('app_portforwardaccess')

        # Removing M2M table for field addresses on 'PortforwardAccess'
        db.delete_table(db.shorten_name('app_portforwardaccess_addresses'))


    models = {
        'app.address': {
            'Meta': {'object_name': 'Address'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipv6': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        },
        'app.country': {
            'Meta': {'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'countrycode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        'app.hypeaccess': {
            'Meta': {'object_name': 'HypeAccess'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Address']", 'symmetrical': 'False', 'blank': 'True'}),
            'appname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'app.portforward': {
            'Meta': {'object_name': 'Portforward'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dstport': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'hw_address': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5'})
        },
        'app.portforwardaccess': {
            'Meta': {'object_name': 'PortforwardAccess'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Address']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5'})
        },
        'app.volume': {
            'Meta': {'object_name': 'Volume'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'use': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['app']