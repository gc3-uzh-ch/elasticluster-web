# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClusterTemplate'
        db.create_table(u'elasticluster_base_clustertemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'elasticluster_base', ['ClusterTemplate'])

        # Adding model 'UserCloudServiceGoogle'
        db.create_table(u'elasticluster_base_usercloudservicegoogle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cloud_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elasticluster_base.CloudService'])),
            ('gce_client_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gce_client_secret', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gce_project_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'elasticluster_base', ['UserCloudServiceGoogle'])

        # Adding model 'Ec2CloudService'
        db.create_table(u'elasticluster_base_ec2cloudservice', (
            (u'cloudservice_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['elasticluster_base.CloudService'], unique=True, primary_key=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'elasticluster_base', ['Ec2CloudService'])

        # Adding model 'ClusterNodeGroups'
        db.create_table(u'elasticluster_base_clusternodegroups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ansible_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cluster_template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elasticluster_base.ClusterTemplate'])),
        ))
        db.send_create_signal(u'elasticluster_base', ['ClusterNodeGroups'])

        # Adding model 'UserCloudServiceEC2'
        db.create_table(u'elasticluster_base_usercloudserviceec2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cloud_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elasticluster_base.CloudService'])),
            ('ec2_access_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ec2_secret_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'elasticluster_base', ['UserCloudServiceEC2'])

        # Adding model 'CloudService'
        db.create_table(u'elasticluster_base_cloudservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('default_image', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('default_flavor', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('default_security_group', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'elasticluster_base', ['CloudService'])


    def backwards(self, orm):
        # Deleting model 'ClusterTemplate'
        db.delete_table(u'elasticluster_base_clustertemplate')

        # Deleting model 'UserCloudServiceGoogle'
        db.delete_table(u'elasticluster_base_usercloudservicegoogle')

        # Deleting model 'Ec2CloudService'
        db.delete_table(u'elasticluster_base_ec2cloudservice')

        # Deleting model 'ClusterNodeGroups'
        db.delete_table(u'elasticluster_base_clusternodegroups')

        # Deleting model 'UserCloudServiceEC2'
        db.delete_table(u'elasticluster_base_usercloudserviceec2')

        # Deleting model 'CloudService'
        db.delete_table(u'elasticluster_base_cloudservice')


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
            'default_security_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        u'elasticluster_base.clusternodegroups': {
            'Meta': {'object_name': 'ClusterNodeGroups'},
            'ansible_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cluster_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.ClusterTemplate']"}),
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
        u'elasticluster_base.usercloudserviceec2': {
            'Meta': {'object_name': 'UserCloudServiceEC2'},
            'cloud_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.CloudService']"}),
            'ec2_access_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ec2_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'elasticluster_base.usercloudservicegoogle': {
            'Meta': {'object_name': 'UserCloudServiceGoogle'},
            'cloud_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elasticluster_base.CloudService']"}),
            'gce_client_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gce_client_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gce_project_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['elasticluster_base']