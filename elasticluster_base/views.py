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
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>, Antonio Messina <antonio.s.messina@gmail.com>'

from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse, Http404

from elasticluster_base.forms import StartClusterTopForm, UserCloudServiceForm
from elasticluster_base.service import UserService, ElasticlusterProxy
from elasticluster_base.models import CloudService, ClusterNodeGroup, ClusterTemplate, UserCloudService, Cluster, ClusterNode


def login(request):
    return render(request, 'auth/login.html', None)

@login_required
def index(request):
    user = request.user
    user_service = UserService(user)
    elasticluster = ElasticlusterProxy(user_service)
    elasticluster.create_config()
    context = {}
    return render(request, 'index.html', context)


class StartCluster(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StartCluster, self).dispatch(*args, **kwargs)

    def get(self, request):
        start_form = StartClusterTopForm()
        credentials_form = UserCloudServiceForm()
        context = {'top_form': start_form, 'cred_form': credentials_form}
        return render(request, 'start.html', context)

    def post(self, request):
        name = request.POST['name']
        cloud_id = request.POST['cloud']
        cluster_template_id = request.POST['cluster']
        image = request.POST['image']
        flavor = request.POST['flavor']
        security_group = request.POST['security_group']
        image_user = request.POST['image_user']

        cloud = UserCloudService.objects.get(cloud_service__id=cloud_id)
        cluster_template = ClusterTemplate.objects.get(id=cluster_template_id)

        cluster = Cluster()
        cluster.user = request.user
        cluster.cloud_service = cloud
        cluster.cluster_template = cluster_template
        cluster.name = name
        cluster.flavor = flavor
        cluster.image = image
        cluster.security_group = security_group
        cluster.image_user = image_user

        cluster.save()

        node_groups = ClusterNodeGroup.objects.filter(cluster_template__id=cluster_template_id)
        for group in node_groups:
            node = ClusterNode()
            node.node_group = group
            node.value = request.POST[group.ansible_name]
            node.cluster = cluster
            node.save()

        return HttpResponse("")


class StartClusterCloudCheck(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StartClusterCloudCheck, self).dispatch(*args, **kwargs)

    def post(self, request):
        id = request.POST['id']

        user_cloud = None
        cloud = None
        if id:
            cloud = CloudService.objects.get(id=id)
            if cloud:
                try:
                    user_cloud = UserCloudService.objects.get(cloud_service__id=id)
                except Exception as e:  # todo: figure out which error to except.
                    user_cloud = ""
                if user_cloud:
                    cloud_json = serializers.serialize('json', [cloud])
                    user_cloud_json = serializers.serialize('json', [user_cloud])
                    context = '{"cloud_service": %s, "user_cloud": %s}' % (cloud_json, user_cloud_json)

                    return HttpResponse(context)

        if cloud:
            cloud_json = serializers.serialize('json', [cloud])
        else:
            cloud_json = ""
        return HttpResponse('{"user_cloud":"", "cloud_service": %s}' % cloud_json)


class CloudServiceCredentials(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CloudServiceCredentials, self).dispatch(*args, **kwargs)

    def post(self, request, cloud_id):
        form = UserCloudServiceForm(request.POST)
        form.instance.user_id = request.user.id
        form.instance.user = request.user
        form.save()

        return HttpResponse('{"error":false}')


class StartClusterNodeOptions(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StartClusterNodeOptions, self).dispatch(*args, **kwargs)

    def get(self, request, cluster_template_id):
        nodes = ClusterNodeGroup.objects.filter(cluster_template__id=cluster_template_id)

        return HttpResponse(serializers.serialize("json", nodes))
