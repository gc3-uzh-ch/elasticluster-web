#! /usr/bin/env python
#
# Copyright (C) 2013 GC3, University of Zurich
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.db.models.fields import IntegerField

__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'

from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CloudService(models.Model):
    PROVIDER_CHOICES = (
        ('ec2_boto', 'EC2 Compatible'),
        ('google', 'Google Compute Engine API'),
    )
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=300)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    region = models.CharField(max_length=150)
    default_image = models.CharField(max_length=50, blank=True)
    default_flavor = models.CharField(max_length=50, blank=True)
    default_security_group = models.CharField(max_length=100, blank=True)
    default_image_user = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '%s' % self.name


class UserCloudService(models.Model):
    user = models.ForeignKey(User)
    cloud_service = models.ForeignKey(CloudService)
    ec2_access_key = models.CharField(max_length=100)
    ec2_secret_key = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % (self.cloud_service.name)


class ClusterTemplate(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.name


class ClusterNodeGroup(models.Model):
    name = models.CharField(max_length=100)
    ansible_name = models.CharField(max_length=50)
    default_value = models.IntegerField(blank=True, default=0)
    cluster_template = models.ForeignKey(ClusterTemplate)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.ansible_name)


class Cluster(models.Model):
    STATUS_NONE = 0
    STATUS_STARTING = 10
    STATUS_STARTED = 11
    STATUS_STOPPING = 20
    STATUS_STOPPED = 21
    STATUS_RESIZING = 30
    STATUS_ERROR = 100
    STATUS_CHOICES = (
        (STATUS_NONE, 'None'),
        (STATUS_STARTING, 'Starting'),
        (STATUS_STARTED, 'Started'),
        (STATUS_STOPPING, 'Stopping'),
        (STATUS_STOPPED, 'Stopped'),
        (STATUS_RESIZING, 'Resizing'),
        (STATUS_ERROR, 'Error'),
    )
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    cluster_template = models.ForeignKey(ClusterTemplate)
    cloud_service = models.ForeignKey(UserCloudService)
    flavor = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    security_group = models.CharField(max_length=100)
    image_user = models.CharField(max_length=100)
    status = IntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):
        return '%s' % self.name


class ClusterNode(models.Model):
    cluster = models.ForeignKey(Cluster)
    node_group = models.ForeignKey(ClusterNodeGroup)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return 'cluster: %s, node_group: %s, value: %s' \
               % (self.cluster.name, self.node_group.name, self.value)


class ClusterLog(models.Model):
    cluster = models.ForeignKey(Cluster)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices=Cluster.STATUS_CHOICES)
    log = models.TextField()

    def __unicode__(self):
        return '%s\t%s\t%s' % (self.cluster.name, self.date, self.title)