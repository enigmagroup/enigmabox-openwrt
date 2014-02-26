# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('app_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ipv6', self.gf('django.db.models.fields.CharField')(max_length=39)),
            ('phone', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Address'])

        # Adding model 'Option'
        db.create_table('app_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['Option'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('app_address')

        # Deleting model 'Option'
        db.delete_table('app_option')


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