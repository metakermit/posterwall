# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('events_event', 'link', 'url')
        # Changing field 'Event.url'
        db.alter_column('events_event', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Adding field 'Event.img_url'
        db.add_column('events_event', 'img_url',
                      self.gf('django.db.models.fields.URLField')(null=True, max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        db.alter_column('events_event', 'url', self.gf('django.db.models.fields.URLField')(default='', max_length=200))
        db.rename_column('events_event', 'url', 'link')

        # Deleting field 'Event.img_url'
        db.delete_column('events_event', 'img_url')


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
