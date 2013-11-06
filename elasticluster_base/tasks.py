#!/usr/bin/env python
# -*- coding: utf-8 -*-#
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
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'


import sys
import subprocess
from celery import task

from celery.utils.log import get_task_logger

from elasticluster_base.models import Cluster


logger = get_task_logger(__name__)


@task
def start_cluster(cluster, config, storage, log):
    name = str(cluster.name)
    config_path = str(config)
    storage_path = str(storage)

    cluster.status = Cluster.STATUS_STARTING
    cluster.save()

    command = ['elasticluster', '-c', config_path, '-s', storage_path,
               'start', name]
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, ''):
        logger.info("out changed: %s" % line)
        log.log = log.log + line
        log.save()
        sys.stdout.flush()

    if 'error' in log.log.lower():
        cluster.status = Cluster.STATUS_ERROR
    else:
        cluster.status = Cluster.STATUS_STARTED
    cluster.save()