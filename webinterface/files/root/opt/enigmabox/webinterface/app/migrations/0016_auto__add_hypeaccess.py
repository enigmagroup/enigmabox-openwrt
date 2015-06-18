# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HypeAccess'
        db.create_table('app_hypeaccess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appname', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('app', ['HypeAccess'])

        # Adding M2M table for field boxes on 'HypeAccess'
        m2m_table_name = db.shorten_name('app_hypeaccess_boxes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hypeaccess', models.ForeignKey(orm['app.hypeaccess'], null=False)),
            ('address', models.ForeignKey(orm['app.address'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hypeaccess_id', 'address_id'])


    def backwards(self, orm):
        # Deleting model 'HypeAccess'
        db.delete_table('app_hypeaccess')

        # Removing M2M table for field boxes on 'HypeAccess'
        db.delete_table(db.shorten_name('app_hypeaccess_boxes'))


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
            'appname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'boxes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app.Address']", 'symmetrical': 'False', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['app']