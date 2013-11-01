# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CloudService.default_image_user'
        db.add_column(u'elasticluster_base_cloudservice', 'default_image_user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CloudService.default_image_user'
        db.delete_column(u'elasticluster_base_cloudservice', 'default_image_user')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elasticluster_base.cloudservice': {
            'Meta': {'object_name': 'CloudService'},
            'default_flavor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'default_image': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'default_image_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'default_security_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        u'elasticluster_base.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'cloud_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.UserCloudService']"}),
            'cluster_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.ClusterTemplate']"}),
            'flavor': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'security_group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'elasticluster_base.clusternode': {
            'Meta': {'object_name': 'ClusterNode'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.Cluster']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.ClusterNodeGroup']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elasticluster_base.clusternodegroup': {
            'Meta': {'object_name': 'ClusterNodeGroup'},
            'ansible_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cluster_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.ClusterTemplate']"}),
            'default_value': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elasticluster_base.clustertemplate': {
            'Meta': {'object_name': 'ClusterTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elasticluster_base.ec2cloudservice': {
            'Meta': {'object_name': 'Ec2CloudService', '_ormbases': [u'elasticluster_base.CloudService']},
            u'cloudservice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['elasticluster_base.CloudService']", 'unique': 'True', 'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'elasticluster_base.usercloudservice': {
            'Meta': {'object_name': 'UserCloudService'},
            'cloud_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.CloudService']"}),
            'ec2_access_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ec2_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['elasticluster_base']