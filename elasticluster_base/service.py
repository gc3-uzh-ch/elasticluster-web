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
import hashlib
import os
import shutil
import shlex
from subprocess import Popen

from elasticluster_web import settings


class UserService(object):
    """
    Enhances the user object with stateless functionality. Since the django integrated user model is used for
    authentication, we won't be able to change it's source. Therefore this class holds extended behavior for the user
    model.
    """

    def __init__(self, user):
        """
        :param user: user
        :type user:`django.contrib.auth.models.User`
        """
        self.user = user

    def check_user_settings(self):
        """
        Checks if the user settings are complete:
        * cloud: access and secret key
        * login: ssh keys
        :param user: user to get the home directory for
        :type user:`django.contrib.auth.models.User`
        :return: boolean (True on success, False on uncompleted settings)
        """
        # check config
        config = self.get_user_config()
        config_service = ConfigService(config)
        if not config_service.check_access_keys():
            return False

        # check ssh keys
        if not config_service.check_ssh_keys(keys=self.get_ssh_keys()):
            return False

        return True

    def create_user_home(self, home_path=None):
        """
        Creates the user home directory. This involves copying the default configuration, create the storage path and
        the ssh keys.
        :param user: user to get the home directory for
        :type user:`django.contrib.auth.models.User`
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
        config_path = os.path.join(home_path, 'config')
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        config = os.path.join(config_path, 'config')
        if not os.path.exists(config):
            template = settings.CONFIG_TEMPLATE_PATH
            shutil.copyfile(template, os.path.join(config_path, 'config'))

        # create ssh keys
        ssh_path = os.path.join(home_path, 'ssh')
        if not os.path.exists(ssh_path):
            os.makedirs(ssh_path)
            key_path = os.path.join(ssh_path, 'elasticluster')
            args = shlex.split('ssh-keygen -b 2048 -t rsa -q -N "" -f ')
            args.append(key_path)
            # todo: exception handling
            p = Popen(args)
            p.communicate()

    def get_home_path(self):
        """
        Finds the home path of the user. The home path contains ssh keys, configuration and the storage path for
        elasticluster. Creates the user home path if it doesn't already exist.
        :param user: user to get the home directory for
        :type user:`django.contrib.auth.models.User`
        :return: path to home directory as str
        """
        home = settings.USER_HOME_PATH
        user_id = self._get_user_identifier()
        home_path = os.path.join(home, user_id)

        if os.path.exists(home_path):
            return home_path
        else:
            self.create_user_home(home_path)

    def get_user_config(self):
        """
        Gets the users config file.
        :param user: user to get the home directory for
        :type user:`django.contrib.auth.models.User`
        :return: path to config file as str
        """
        home = self.get_home_path()
        config_path = os.path.join(home, 'config', 'config')
        return config_path

    def _get_user_identifier(self):
        """
        Returns the identifier for the given user.
        :param user: user to get the home directory for
        :type user:`django.contrib.auth.models.User`
        :return: identifier str
        """
        hasher = hashlib.sha256()
        hasher.update(self.user.username)
        return hasher.hexdigest()

    def get_ssh_keys(self):
        """
        Gets the ssh keys for the given user.
        :return: dictionary with 'user_key_name', 'user_key_public', 'user_key_private' entries, where public and
                 private hold the path
        """
        home = self.get_home_path()
        ssh_path = os.path.join(home, 'ssh')
        key = dict()
        key['user_key_private'] = os.path.join(ssh_path, 'elasticluster')
        key['user_key_public'] = os.path.join(ssh_path, 'elasticluster.pub')
        key['user_key_name'] = 'elasticluster'
        return key

    def get_configuration_service(self):
        config = self.get_user_config()
        config_service = ConfigService(config)

        return config_service


class ConfigService(object):
    """
    Handles the interaction with a user configuration.
    """
    key_options = ['ec2_access_key', 'ec2_secret_key']
    login_option = ['user_key_name', 'user_key_private', 'user_key_public']

    def __init__(self, path):
        """
        :param path: path to the configuration file of the user
        :type path: str
        """
        self.path = path
        self.config = ConfigParser()
        self.config.read(self.path)


    def get_cluster_configurations(self):
        cluster_conf = dict()
        for section in self.config.sections():
            if 'cluster/' in section and section.count("/") == 1:
                name = section.split('/')[1]
                cluster_conf[name] = dict(self.config.items(section))

        return cluster_conf

    def get_cloud_configurations(self):
        """

        """
        cloud_conf = dict()
        for section in self.config.sections():
            if 'cloud/' in section:
                name = section.split('/')[1]
                cloud_conf[name] = dict(self.config.items(section))

        return cloud_conf

    def save_cloud_configuration(self, name, **conf):
        name = 'cloud/%s' % name
        if self.config.has_section(name):
            for key, value in conf.iteritems():
                self.config.set(name, key, value)
            self.config.write(file(self.path, 'w'))

    def check_access_keys(self):
        """
        Reads the configuration of the given path.
        :param path: path to the configuration file
        :type path: str
        :return:
        """
        for section in self.config.sections():
            if 'cloud/' in section:
                for option in ConfigService.key_options:
                    if self.config.has_option(section, option):
                        value = self.config.get(section, option)
                        if value == '****' or not value:
                            return False
        return True

    def check_ssh_keys(self, keys=None):
        """
        Checks if the ssh keys are stored in the configuration file.
        If ssh keys are passed for this user, they will be stored and the method succeeds.
        :return boolean, true=ssh keys found, false=ssh keys not found
        """
        for section in self.config.sections():
            if 'login/' in section:
                for option in ConfigService.login_option:
                    if self.config.has_option(section, option):
                        value = self.config.get(section, option)
                        if value == '****' or not value:
                            if keys:
                                self.config.set(section, option, keys[option])
                                self.config.write(file(self.path, 'w'))
                            else:
                                return False

        return True


