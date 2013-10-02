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
from django.db.models.fields import DecimalField

__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'

from django import forms


class CloudProviderForm(forms.Form):
    cloud_name = forms.CharField(widget=forms.HiddenInput)
    ec2_access_key = forms.CharField()
    ec2_secret_key = forms.CharField()


class ClusterForm(forms.Form):
    name = forms.CharField()
    cluster = forms.ChoiceField()
    flavor = forms.CharField()
    image = forms.CharField()

    def __init__(self, cluster_conf, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)
        clusters = []
        for cluster, properties in cluster_conf.iteritems():
            clusters.append((cluster, cluster))

            for key, property in properties.iteritems():
                if '_node' in key:
                    self.fields['cluster_nodes_%s_%s' % (cluster, key)] = forms.DecimalField()
                    pass

        self.fields['cluster'] = forms.ChoiceField(choices=clusters)