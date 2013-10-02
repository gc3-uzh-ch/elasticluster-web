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

from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from elasticluster_base.forms import CloudProviderForm, ClusterForm
from elasticluster_base.service import UserService, ConfigService


@login_required
def index(request):
    user = request.user
    user_service = UserService(user)
    settings_warning = not user_service.check_user_settings()
    context = {'settings_warning': settings_warning}
    return render(request, 'index.html', context)


@login_required
def settings(request):
    user = request.user
    user_service = UserService(user)
    config_service = user_service.get_configuration_service()

    if request.method == 'POST':
        cloud_formset = formset_factory(CloudProviderForm)
        formset = cloud_formset(request.POST, request.FILES)
        if formset.is_valid():
            # save the values back and print a message
            if formset.has_changed():
                conf = dict()
                for form in formset:
                    data = form.cleaned_data
                    config_service.save_cloud_configuration(data['cloud_name'], **data)


    else:
        clouds = config_service.get_cloud_configurations()
        form_init = list()
        for cloud, settings in clouds.iteritems():
            cloud_dict = dict()
            cloud_dict['cloud_name'] = cloud
            cloud_dict['ec2_access_key'] = settings['ec2_access_key']
            cloud_dict['ec2_secret_key'] = settings['ec2_secret_key']
            form_init.append(cloud_dict)

        cloud_formset = formset_factory(CloudProviderForm, max_num=len(form_init))
        formset = cloud_formset(initial=form_init)

    context = {'formset': formset}
    return render(request, 'settings.html', context)


def login(request):
    return render(request, 'auth/login.html', None)


def start_cluster(request):
    user = request.user
    user_service = UserService(user)
    config_service = user_service.get_configuration_service()

    cluster_conf = config_service.get_cluster_configurations()

    form = ClusterForm(cluster_conf)


    context = {'form': form}
    return render(request, 'start.html', context)