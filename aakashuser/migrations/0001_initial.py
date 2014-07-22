# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'aakashuser_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('online_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_type', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('user_skills', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('num_of_posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reply_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'aakashuser', ['UserProfile'])

        # Adding model 'Category'
        db.create_table(u'aakashuser_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'aakashuser', ['Category'])

        # Adding model 'Post'
        db.create_table(u'aakashuser_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.UserProfile'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.Category'])),
            ('post_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_status', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
        ))
        db.send_create_signal(u'aakashuser', ['Post'])

        # Adding M2M table for field userUpVotes on 'Post'
        m2m_table_name = db.shorten_name(u'aakashuser_post_userUpVotes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'aakashuser.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])

        # Adding M2M table for field userDownVotes on 'Post'
        m2m_table_name = db.shorten_name(u'aakashuser_post_userDownVotes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'aakashuser.post'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'user_id'])

        # Adding model 'Reply'
        db.create_table(u'aakashuser_reply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.Post'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.UserProfile'])),
            ('reply_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('file_upload', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reply_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aakashuser', ['Reply'])

        # Adding model 'Comment'
        db.create_table(u'aakashuser_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ans_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.Reply'])),
            ('comment_body', self.gf('django.db.models.fields.TextField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('comment_status', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=0)),
        ))
        db.send_create_signal(u'aakashuser', ['Comment'])

        # Adding model 'Ticket'
        db.create_table(u'aakashuser_ticket', (
            ('user_id', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('topic_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.Category'])),
            ('tab_id', self.gf('django.db.models.fields.IntegerField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('ticket_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 26, 0, 0))),
            ('overdue_date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 27, 0, 0))),
            ('closed_date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 25, 0, 0))),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reopened_date_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 25, 0, 0))),
            ('topic_priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('duration_for_reply', self.gf('django.db.models.fields.IntegerField')(default=24)),
        ))
        db.send_create_signal(u'aakashuser', ['Ticket'])

        # Adding model 'Threads'
        db.create_table(u'aakashuser_threads', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reply', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ticketreply', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aakashuser.Ticket'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'aakashuser', ['Threads'])

        # Adding model 'Tablet_info'
        db.create_table(u'aakashuser_tablet_info', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rcID', self.gf('django.db.models.fields.IntegerField')()),
            ('rcName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_tab_id', self.gf('django.db.models.fields.IntegerField')()),
            ('end_tab_id', self.gf('django.db.models.fields.IntegerField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'aakashuser', ['Tablet_info'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'aakashuser_userprofile')

        # Deleting model 'Category'
        db.delete_table(u'aakashuser_category')

        # Deleting model 'Post'
        db.delete_table(u'aakashuser_post')

        # Removing M2M table for field userUpVotes on 'Post'
        db.delete_table(db.shorten_name(u'aakashuser_post_userUpVotes'))

        # Removing M2M table for field userDownVotes on 'Post'
        db.delete_table(db.shorten_name(u'aakashuser_post_userDownVotes'))

        # Deleting model 'Reply'
        db.delete_table(u'aakashuser_reply')

        # Deleting model 'Comment'
        db.delete_table(u'aakashuser_comment')

        # Deleting model 'Ticket'
        db.delete_table(u'aakashuser_ticket')

        # Deleting model 'Threads'
        db.delete_table(u'aakashuser_threads')

        # Deleting model 'Tablet_info'
        db.delete_table(u'aakashuser_tablet_info')


    models = {
        u'aakashuser.category': {
            'Meta': {'object_name': 'Category'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'aakashuser.comment': {
            'Meta': {'ordering': "['-created_date']", 'object_name': 'Comment'},
            'ans_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.Reply']"}),
            'comment_body': ('django.db.models.fields.TextField', [], {}),
            'comment_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'aakashuser.post': {
            'Meta': {'ordering': "['post_date']", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.Category']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'post_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'post_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'userDownVotes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'postDownVotes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'userUpVotes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'postUpVotes'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'aakashuser.reply': {
            'Meta': {'ordering': "['reply_date']", 'object_name': 'Reply'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'file_upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reply_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'reply_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.Post']"}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.UserProfile']"})
        },
        u'aakashuser.tablet_info': {
            'Meta': {'object_name': 'Tablet_info'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'end_tab_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rcID': ('django.db.models.fields.IntegerField', [], {}),
            'rcName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_tab_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'aakashuser.threads': {
            'Meta': {'object_name': 'Threads'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reply': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ticketreply': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.Ticket']"})
        },
        u'aakashuser.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'closed_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 25, 0, 0)'}),
            'created_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 26, 0, 0)'}),
            'duration_for_reply': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'overdue_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 27, 0, 0)'}),
            'reopened_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 25, 0, 0)'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tab_id': ('django.db.models.fields.IntegerField', [], {}),
            'ticket_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aakashuser.Category']"}),
            'topic_priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user_id': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'aakashuser.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'num_of_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'online_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reply_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_skills': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aakashuser']