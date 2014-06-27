# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.reply_count'
        db.add_column(u'aakashuser_post', 'reply_count',
                      self.gf('django.db.models.fields.IntegerField')(default=9),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.reply_count'
        db.delete_column(u'aakashuser_post', 'reply_count')


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
            'reply_count': ('django.db.models.fields.IntegerField', [], {'default': '9'}),
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
            'closed_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 26, 0, 0)'}),
            'created_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 27, 0, 0)'}),
            'duration_for_reply': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'overdue_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 28, 0, 0)'}),
            'reopened_date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 26, 0, 0)'}),
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