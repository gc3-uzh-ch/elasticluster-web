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

from ConfigParser import ConfigParser
from datetime import datetime
import hashlib
import os
import shlex
from subprocess import Popen

from elasticluster_web import settings
from elasticluster_base.models import Cluster, ClusterNodeGroup, ClusterLog
import elasticluster_base.tasks as tasks


class UserService(object):
    """
    Enhances the user object with stateless functionality.
    Since the django integrated user model is used for
    authentication, we won't be able to change it's source.
    Therefore this class holds extended behavior for the user
    model.
    """

    CONFIG_PATH = 'config'

    def __init__(self, user):
        """
        :param user: user
        :type user:`django.contrib.auth.models.User`
        """
        self.user = user

    def create_user_home(self, home_path=None):
        """
        Creates the user home directory. This involves create the
        storage path and the ssh keys.
        """
        # create home folder
        if not home_path:
            user_id = self._get_user_identifier()
            home = settings.USER_HOME_PATH
            home_path = os.path.join(home, user_id)

        if not os.path.exists(home_path):
            os.makedirs(home_path)

        # create storage path
        storage_path = os.path.join(home_path, 'storage')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        # create config from template
        config_path = os.path.join(home_path, UserService.CONFIG_PATH)
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        # create ssh keys
        ssh_path = os.path.join(home_path, 'ssh')
        if not os.path.exists(ssh_path):
            os.makedirs(ssh_path)
            key_name = self._get_key_name()
            key_path = os.path.join(ssh_path, key_name)
            args = shlex.split('ssh-keygen -b 2048 -t rsa -q -N "" -f ')
            args.append(key_path)
            # todo: exception handling
            p = Popen(args)
            p.communicate()

    def get_home_path(self):
        """
        Finds the home path of the user. The home path contains ssh keys,
        and the storage path for elasticluster. This will creates the
        user home path if it doesn't already exist.
        :return: path to home directory as str
        """
        home = settings.USER_HOME_PATH
        user_id = self._get_user_identifier()
        home_path = os.path.join(home, user_id)

        if os.path.exists(home_path):
            return home_path
        else:
            self.create_user_home(home_path)

    def get_config_path(self):
        self.create_user_home()
        return os.path.join(self.get_home_path(), UserService.CONFIG_PATH,
                            UserService.CONFIG_PATH)

    def get_storage_path(self):
        self.create_user_home()
        return os.path.join(self.get_home_path(), 'storage')

    def _get_user_identifier(self):
        """
        Returns the unique identifier of the user. At the moment this is
        the sha256 encoding of the username.
        :return: identifier str
        """
        hasher = hashlib.sha256()
        hasher.update(self.user.username)
        return hasher.hexdigest()

    def _get_key_name(self):
        return 'elasticluster-%s' % self.user.username

    def get_ssh_keys(self):
        """
        Gets the ssh keys for the given user.
        :return: dictionary with 'user_key_name', 'user_key_public',
                 'user_key_private' entries, where public and private hold
                 the path
        """
        self.create_user_home()
        home = self.get_home_path()
        ssh_path = os.path.join(home, 'ssh')
        username = self.user.username
        key_name = self._get_key_name()
        key = dict()
        key['user_key_private'] = os.path.join(ssh_path, key_name)
        key['user_key_public'] = os.path.join(ssh_path, '%s.pub' % key_name)
        key['user_key_name'] = key_name
        return key


class ElasticlusterAdapter(object):
    """
    Proxy class to enable easy access to elasticluster. The goal of this class
    is to abstract every interaction with elasticluster, since there will be
    an API in the future, this is the only place to implement interaction.
    """

    def __init__(self, user_service):
        """
        :param user_service: user service to access home and keys
        :type user_service: `elasticluster_base.service.UserService`
        """
        self.user_service = user_service

    def start_cluster(self, cluster):
        """
        Starts a cluster using elasticluster.
        :param cluster: cluster to start
        :type cluster: `elasticluster_base.models.Cluster`
        :return: log object to track the state
        """
        config = self._create_config()
        storage_path = self.user_service.get_storage_path()
        log = ClusterLog()
        log.cluster = cluster
        log.date = datetime.now()
        log.title = "Starting cluster `%s`" % cluster.name
        log.status = Cluster.STATUS_STARTING
        log.save()
        tasks.start_cluster.delay(cluster, config, storage_path, log)

        return log

    def _create_config(self):
        """
        The command line elasticluster interfaces needs a configuration file
        in order to start a cluster. This method will create a configuration
        file from the values in the database.
        :return: path to the configuration file
        """
        user = self.user_service.user
        clusters = Cluster.objects.all().filter(user=self.user_service.user)
        config = ConfigParser()
        setup_provider = "ansible"

        for cluster in clusters:
            # write cloud section
            cloud = cluster.cloud_service
            cloud_section = 'cloud/%s' % cloud.cloud_service.name
            if not config.has_section(cloud_section):
                config.add_section(cloud_section)
                config.set(cloud_section, 'provider', cloud.cloud_service.provider)
                config.set(cloud_section, 'ec2_url', cloud.cloud_service.url)
                config.set(cloud_section, 'ec2_access_key',
                           cloud.ec2_access_key)
                config.set(cloud_section, 'ec2_secret_key',
                           cloud.ec2_secret_key)
                config.set(cloud_section, 'ec2_region',
                           cloud.cloud_service.region)

            # write login section
            login_section = 'login/%s-%s' % (user.username,
                                             cloud.cloud_service.name)
            if not config.has_section(login_section):
                config.add_section(login_section)
                keys = self.user_service.get_ssh_keys()
                config.set(login_section, 'image_user', cluster.image_user)
                config.set(login_section, 'image_user_sudo', 'root')
                config.set(login_section, 'image_sudo', 'True')
                config.set(login_section, 'user_key_name',
                           keys['user_key_name'])
                config.set(login_section, 'user_key_private',
                           keys['user_key_private'])
                config.set(login_section, 'user_key_public',
                           keys['user_key_public'])

            # write cluster section
            cluster_section = 'cluster/%s' % (cluster.name)
            if not config.has_section(cluster_section):
                config.add_section(cluster_section)
                config.set(cluster_section, 'cloud',
                           cluster.cloud_service.cloud_service.name)
                config.set(cluster_section, 'login', '%s-%s' \
                                % (user.username, cloud.cloud_service.name))
                config.set(cluster_section, 'setup_provider', setup_provider)
                config.set(cluster_section, 'flavor', cluster.flavor)
                config.set(cluster_section, 'security_group',
                           cluster.security_group)
                config.set(cluster_section, 'image_id', cluster.image)
                config.set(cluster_section, 'security_group',
                           cluster.security_group)
                config.set(cluster_section, 'image_userdata', '')

                nodes = cluster.clusternode_set.all()
                for node in nodes:
                    config.set(cluster_section, '%s_nodes'
                                                % node.node_group.ansible_name,
                                                node.value)

        # if no clusters are created by the user, we should at least
        # provide a sample cluster section
        # to not cause any errors on elasticluster config validation.
        if not clusters:
            pass
            # todo: implement

        # write setup part, this is the same for all clusters
        setup_section = 'setup/%s' % (setup_provider)
        if not config.has_section(setup_section):
            config.add_section(setup_section)
            config.set(setup_section, 'provider', setup_provider)

            node_groups = ClusterNodeGroup.objects.all()
            for group in node_groups:
                config.set(setup_section, '%s_groups' % group.ansible_name,
                           group.ansible_name)

        config_path = self.user_service.get_config_path()
        with open(config_path, 'wb') as configfile:
            config.write(configfile)

        return config_path