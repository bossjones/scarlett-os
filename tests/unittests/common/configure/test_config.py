#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------
"""

import imp
import os.path
import sys
import unittest
import unittest.mock as mock

import pytest

import tempfile
import shutil

import scarlett_os
from scarlett_os.common.configure import config


# source: https://github.com/YosaiProject/yosai/blob/master/test/isolated_tests/core/conf/conftest.py
@pytest.fixture(scope='function')
def config_unit_mocker_stopall(mocker):
    "Stop previous mocks, yield mocker plugin obj, then stopall mocks again"
    print('Called [setup]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(config)
    yield mocker
    print('Called [teardown]: mocker.stopall()')
    mocker.stopall()
    print('Called [setup]: imp.reload(player)')
    imp.reload(config)

@pytest.fixture(scope='function')
def fake_config():
    """Create a temporary config file."""
    base = tempfile.mkdtemp()
    config_file = os.path.join(base, 'config.yaml')

    with open(config_file, 'wt') as f:
        f.write('''
# Omitted values in this section will be auto detected using freegeoip.io

# Location required to calculate the time the sun rises and sets.
# Coordinates are also used for location for weather related automations.
# Google Maps can be used to determine more precise GPS coordinates.
latitude: 40.7056308
longitude: -73.9780034

pocketsphinx:
    hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
    lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
    dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
    silprob: 0.1
    wip: 1e-4
    bestpath: 0

# Impacts weather/sunrise data
elevation: 665

# 'metric' for Metric System, 'imperial' for imperial system
unit_system: metric

# Pick yours from here:
# http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
time_zone: America/New_York

# Name of the location where ScarlettOS Assistant is running
name: ScarlettOS

owner: "Hair Ron Jones"

keywords_list:
- 'scarlett'
- 'SCARLETT'

features:
- time
''')
    temp_config = config.Config.from_file(config_file)

    yield temp_config

    shutil.rmtree(base)


# pylint: disable=R0201
# pylint: disable=C0111
# pylint: disable=C0123
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=W0621
# pylint: disable=W0612
@pytest.mark.scarlettonly
@pytest.mark.unittest
@pytest.mark.configtest
@pytest.mark.scarlettonlyunittest
class TestFilterMatcher(object):
    # Borrowed from udiskie

    """
    Tests for the scarlett_os.common.configure.FilterMatcher class.
    """

    def test_config_from_file(self, fake_config):
        """Test Config object and properties."""
        assert fake_config.scarlett_name == 'ScarlettOS'

    # def test_ignored(self):
    #     """Test the FilterMatcher.is_ignored() method."""
    #     self.assertTrue(
    #         self.ignore_device(
    #             TestDev('/ignore', 'vfat', 'IGNORED-device')))
    #     self.assertFalse(
    #         self.ignore_device(
    #             TestDev('/options', 'vfat', 'device-with-options')))
    #     self.assertFalse(
    #         self.ignore_device(
    #             TestDev('/nomatch', 'vfat', 'no-matching-id')))

    # def test_options(self):
    #     """Test the FilterMatcher.get_mount_options() method."""
    #     self.assertEqual(
    #         ['noatime', 'nouser'],
    #         self.mount_options(
    #             TestDev('/options', 'vfat', 'device-with-options')))
    #     self.assertEqual(
    #         ['noatime', 'nouser'],
    #         self.mount_options(
    #             TestDev('/optonly', 'ext', 'device-with-options')))
    #     self.assertEqual(
    #         ['ro', 'nouser'],
    #         self.mount_options(
    #             TestDev('/fsonly', 'vfat', 'no-matching-id')))
    #     self.assertEqual(
    #         None,
    #         self.mount_options(
    #             TestDev('/nomatch', 'ext', 'no-matching-id')))
