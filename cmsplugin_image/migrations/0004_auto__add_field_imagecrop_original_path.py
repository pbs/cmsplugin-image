# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ImageCrop.original_path'
        db.add_column('image_crop', 'original_path',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ImageCrop.original_path'
        db.delete_column('image_crop', 'original_path')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmsplugin_image.imagecrop': {
            'Meta': {'object_name': 'ImageCrop', 'db_table': "'image_crop'"},
            'crop_h': ('django.db.models.fields.IntegerField', [], {}),
            'crop_w': ('django.db.models.fields.IntegerField', [], {}),
            'crop_x': ('django.db.models.fields.IntegerField', [], {}),
            'crop_y': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_path': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.Variable']"})
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
        'smartsnippets.smartsnippetpointer': {
            'Meta': {'object_name': 'SmartSnippetPointer', 'db_table': "'cmsplugin_smartsnippetpointer'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['smartsnippets.SmartSnippet']"})
        },
        'smartsnippets.smartsnippetvariable': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('snippet', 'name'),)", 'object_name': 'SmartSnippetVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippet']"}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'smartsnippets.variable': {
            'Meta': {'unique_together': "(('snippet_variable', 'snippet'),)", 'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetPointer']"}),
            'snippet_variable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': "orm['smartsnippets.SmartSnippetVariable']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['cmsplugin_image']