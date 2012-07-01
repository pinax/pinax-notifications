# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NoticeType'
        db.create_table('notification_noticetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('default', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('notification', ['NoticeType'])

        # Adding model 'NoticeSetting'
        db.create_table('notification_noticesetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notice_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType'])),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('send', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notification', ['NoticeSetting'])

        # Adding unique constraint on 'NoticeSetting', fields ['user', 'notice_type', 'medium']
        db.create_unique('notification_noticesetting', ['user_id', 'notice_type_id', 'medium'])

        # Adding model 'Notice'
        db.create_table('notification_notice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recieved_notices', to=orm['auth.User'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_notices', null=True, to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('notice_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('unseen', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_site', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notification', ['Notice'])

        # Adding model 'NoticeQueueBatch'
        db.create_table('notification_noticequeuebatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pickled_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notification', ['NoticeQueueBatch'])

        # Adding model 'ObservedItem'
        db.create_table('notification_observeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('notice_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('signal', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notification', ['ObservedItem'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'NoticeSetting', fields ['user', 'notice_type', 'medium']
        db.delete_unique('notification_noticesetting', ['user_id', 'notice_type_id', 'medium'])

        # Deleting model 'NoticeType'
        db.delete_table('notification_noticetype')

        # Deleting model 'NoticeSetting'
        db.delete_table('notification_noticesetting')

        # Deleting model 'Notice'
        db.delete_table('notification_notice')

        # Deleting model 'NoticeQueueBatch'
        db.delete_table('notification_noticequeuebatch')

        # Deleting model 'ObservedItem'
        db.delete_table('notification_observeditem')


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
        'notification.notice': {
            'Meta': {'ordering': "['-added']", 'object_name': 'Notice'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'on_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recieved_notices'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_notices'", 'null': 'True', 'to': "orm['auth.User']"}),
            'unseen': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'notification.noticequeuebatch': {
            'Meta': {'object_name': 'NoticeQueueBatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickled_data': ('django.db.models.fields.TextField', [], {})
        },
        'notification.noticesetting': {
            'Meta': {'unique_together': "(('user', 'notice_type', 'medium'),)", 'object_name': 'NoticeSetting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'notification.noticetype': {
            'Meta': {'object_name': 'NoticeType'},
            'default': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'notification.observeditem': {
            'Meta': {'ordering': "['-added']", 'object_name': 'ObservedItem'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'signal': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['notification']

