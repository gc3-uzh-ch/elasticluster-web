#! /usr/bin/env python
#
#   Copyright (C) 2013 GC3, University of Zurich
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'

from django import forms
from django.forms.models import ModelForm

from elasticluster_base.models import CloudService, ClusterTemplate, \
    UserCloudService


class StartClusterTopForm(forms.Form):
    name = forms.CharField(required=True)
    cloud = forms.ModelChoiceField(
        queryset=CloudService.objects.all().order_by('name'), required=True)
    cluster = forms.ModelChoiceField(
        queryset=ClusterTemplate.objects.all().order_by('name'), required=True)


class UserCloudServiceForm(ModelForm):
    class Meta:
        model = UserCloudService
        exclude = ['user', ]
        widgets = {
            'ec2_access_key': forms.PasswordInput(),
            'ec2_secret_key': forms.PasswordInput(),
        }
