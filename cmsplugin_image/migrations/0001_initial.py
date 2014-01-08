# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageSize'
        db.create_table('image_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('aspect_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('cmsplugin_image', ['ImageSize'])

        # Adding model 'ImageCrop'
        db.create_table('image_crop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crop_x', self.gf('django.db.models.fields.IntegerField')()),
            ('crop_y', self.gf('django.db.models.fields.IntegerField')()),
            ('crop_w', self.gf('django.db.models.fields.IntegerField')()),
            ('crop_h', self.gf('django.db.models.fields.IntegerField')()),
            ('variable_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smartsnippets.SmartSnippetVariable'])),
        ))
        db.send_create_signal('cmsplugin_image', ['ImageCrop'])


    def backwards(self, orm):
        # Deleting model 'ImageSize'
        db.delete_table('image_size')

        # Deleting model 'ImageCrop'
        db.delete_table('image_crop')


    models = {
        'cmsplugin_image.imagecrop': {
            'Meta': {'object_name': 'ImageCrop', 'db_table': "'image_crop'"},
            'crop_h': ('django.db.models.fields.IntegerField', [], {}),
            'crop_w': ('django.db.models.fields.IntegerField', [], {}),
            'crop_x': ('django.db.models.fields.IntegerField', [], {}),
            'crop_y': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'variable_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippetVariable']"})
        },
        'cmsplugin_image.imagesize': {
            'Meta': {'object_name': 'ImageSize', 'db_table': "'image_size'"},
            'aspect_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'smartsnippets.smartsnippet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SmartSnippet'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'documentation_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'template_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'template_path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'smartsnippets.smartsnippetvariable': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('snippet', 'name'),)", 'object_name': 'SmartSnippetVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippet']"}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cmsplugin_image']