# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('venture_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venture.Room'], blank=True)),
            ('money', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('venture', ['Person'])

        # Adding M2M table for field items on 'Person'
        db.create_table('venture_person_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['venture.person'], null=False)),
            ('item', models.ForeignKey(orm['venture.item'], null=False))
        ))
        db.create_unique('venture_person_items', ['person_id', 'item_id'])

        # Adding M2M table for field quests on 'Person'
        db.create_table('venture_person_quests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['venture.person'], null=False)),
            ('quest', models.ForeignKey(orm['venture.quest'], null=False))
        ))
        db.create_unique('venture_person_quests', ['person_id', 'quest_id'])

        # Adding model 'Room'
        db.create_table('venture_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('venture', ['Room'])

        # Adding model 'Exit'
        db.create_table('venture_exit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exit', to=orm['venture.Room'])),
            ('to_room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entrance', to=orm['venture.Room'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('key_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venture.Item'], null=True, blank=True)),
            ('transition_message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('venture', ['Exit'])

        # Adding model 'Item'
        db.create_table('venture_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('inroom_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venture.Room'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('venture', ['Item'])

        # Adding model 'Quest'
        db.create_table('venture_quest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('time_limit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('payout', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('venture', ['Quest'])

        # Adding M2M table for field items on 'Quest'
        db.create_table('venture_quest_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quest', models.ForeignKey(orm['venture.quest'], null=False)),
            ('item', models.ForeignKey(orm['venture.item'], null=False))
        ))
        db.create_unique('venture_quest_items', ['quest_id', 'item_id'])

    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('venture_person')

        # Removing M2M table for field items on 'Person'
        db.delete_table('venture_person_items')

        # Removing M2M table for field quests on 'Person'
        db.delete_table('venture_person_quests')

        # Deleting model 'Room'
        db.delete_table('venture_room')

        # Deleting model 'Exit'
        db.delete_table('venture_exit')

        # Deleting model 'Item'
        db.delete_table('venture_item')

        # Deleting model 'Quest'
        db.delete_table('venture_quest')

        # Removing M2M table for field items on 'Quest'
        db.delete_table('venture_quest_items')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'venture.exit': {
            'Meta': {'object_name': 'Exit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'from_room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exit'", 'to': "orm['venture.Room']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venture.Item']", 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entrance'", 'to': "orm['venture.Room']"}),
            'transition_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'venture.item': {
            'Meta': {'object_name': 'Item'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inroom_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venture.Room']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'venture.person': {
            'Meta': {'object_name': 'Person'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['venture.Item']", 'symmetrical': 'False', 'blank': 'True'}),
            'money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'quests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['venture.Quest']", 'symmetrical': 'False', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venture.Room']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'venture.quest': {
            'Meta': {'object_name': 'Quest'},
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['venture.Item']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'payout': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'venture.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'exits': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['venture.Room']", 'symmetrical': 'False', 'through': "orm['venture.Exit']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['venture']