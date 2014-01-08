# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageSizeContext'
        db.create_table('cmsplugin_image_imagesizecontext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsplugin_image.ImageSize'], null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('cmsplugin_image', ['ImageSizeContext'])

        # Adding unique constraint on 'ImageSizeContext', fields ['content_type', 'object_id']
        db.create_unique('cmsplugin_image_imagesizecontext', ['content_type_id', 'object_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ImageSizeContext', fields ['content_type', 'object_id']
        db.delete_unique('cmsplugin_image_imagesizecontext', ['content_type_id', 'object_id'])

        # Deleting model 'ImageSizeContext'
        db.delete_table('cmsplugin_image_imagesizecontext')


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
        'cmsplugin_image.imagesizecontext': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'ImageSizeContext'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmsplugin_image.ImageSize']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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