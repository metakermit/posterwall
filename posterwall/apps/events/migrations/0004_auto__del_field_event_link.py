# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.link'
        db.delete_column('events_event', 'link')


    def backwards(self, orm):
        # Adding field 'Event.link'
        db.add_column('events_event', 'link',
                      self.gf('django.db.models.fields.URLField')(max_length=200, default=''),
                      keep_default=False)


    models = {
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['events']