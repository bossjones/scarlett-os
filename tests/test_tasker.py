#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tasker
----------------------------------
"""

import os
import sys

import pytest
import unittest
import unittest.mock as mock

import scarlett_os
from scarlett_os import tasker  # Module with our thing to test
from scarlett_os.utility import gnome  # Module with the decorator we need to replace

import time
from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GLib
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import Gio
import pydbus
from pydbus import SessionBus

# NOTE: We can't add this here, otherwise we won't be able to mock them
# from tests import common
import signal
import builtins
import scarlett_os.exceptions

import imp  # Library to help us reload our tasker module

# py.test -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
# strace -s 40000 -vvtf python setup.py test > ./strace.out.strace 2>&1


class TestScarlettTasker(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_pydbus_SessionBus = mock.patch('pydbus.SessionBus', spec=True, create=True).start()

        # mock_pydbus_SessionBus.return_value

        # mock_time = mock.patch('time.sleep', spec=True, create=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        # mock_pydbus.get.side_effect = Exception('GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files')

        # Exception Thrown from [/home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py] on line [40] via function [get]
        # Exception type Error:
        # GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name
        # org.scarlett was not provided by any .service files

        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_init(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
        tskr = tasker.ScarlettTasker()

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    @mock.patch('scarlett_os.tasker.TaskSignalHandler', spec=scarlett_os.tasker.TaskSignalHandler, name='mock_task_signal_handler')
    @mock.patch('scarlett_os.tasker.time.sleep', name='mock_time_sleep')
    @mock.patch('scarlett_os.tasker.logging.Logger.debug', name='mock_logger_debug')
    @mock.patch('scarlett_os.tasker._IdleObject', name='mock_idle_obj')
    @mock.patch('scarlett_os.utility.thread.time_logger', name='mock_time_logger')
    @mock.patch('scarlett_os.tasker.speaker', name='mock_scarlett_speaker')
    @mock.patch('scarlett_os.tasker.player', name='mock_scarlett_player')
    @mock.patch('scarlett_os.tasker.commands', name='mock_scarlett_commands')
    @mock.patch('scarlett_os.tasker.threading.RLock', spec=scarlett_os.tasker.threading.RLock, name='mock_threading_rlock')
    @mock.patch('scarlett_os.tasker.threading.Event', spec=scarlett_os.tasker.threading.Event, name='mock_threading_event')
    @mock.patch('scarlett_os.tasker.threading.Thread', spec=scarlett_os.tasker.threading.Thread, name='mock_thread_class')
    def test_tasker_reset(self, mock_thread_class, mock_threading_event, mock_threading_rlock, mock_scarlett_commands, mock_scarlett_player, mock_scarlett_speaker, mock_time_logger, mock_idle_obj, mock_logger_debug, mock_time_sleep, mock_task_signal_handler, mock_dbusrunner):
        # dbus mocks
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        # handler mocks
        _handler = mock_task_signal_handler()
        tskr = tasker.ScarlettTasker()

        tskr.reset()

        self.assertEqual(_handler.clear.call_count, 1)

        self.assertIsNone(tskr._failed_signal_callback)
        self.assertIsNone(tskr._ready_signal_callback)
        self.assertIsNone(tskr._keyword_recognized_signal_callback)
        self.assertIsNone(tskr._command_recognized_signal_callback)
        self.assertIsNone(tskr._cancel_signal_callback)
        self.assertIsNone(tskr._connect_signal_callback)


class TestSoundType(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_soundtype_get_path(self):
        path_to_sound = '/home/pi/dev/bossjones-github/scarlett_os/static/sounds'
        self.assertEqual(tasker.STATIC_SOUNDS_PATH, path_to_sound)
        self.assertEqual(type(tasker.SoundType.get_path('pi-cancel')), list)
        self.assertEqual(tasker.SoundType.get_path('pi-cancel'), ["{}/pi-cancel.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-listening'), ["{}/pi-listening.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-response'), ["{}/pi-response.wav".format(path_to_sound)])
        self.assertEqual(tasker.SoundType.get_path('pi-response2'), ["{}/pi-response2.wav".format(path_to_sound)])


class TestTaskSignalHandler(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        TestTaskSignalHandler
        """
        self._handler = tasker.TaskSignalHandler()

        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_pydbus_SessionBus = mock.patch('pydbus.SessionBus', spec=True, create=True).start()

        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator

    def tearDown(self):
        del(self._handler)
        self._handler = None

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_disconnect(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # assertions
        self.assertEqual(len(self._handler._ids), 1)

        bus.subscribe.assert_called_once_with(sender=None,
                                              iface="org.scarlett.Listener",
                                              signal="SttFailedSignal",
                                              object="/org/scarlett/Listener",
                                              arg0=None,
                                              flags=0,
                                              signal_fired=test_cb)

        # Disconnect then test again
        self._handler.disconnect(bus, "SttFailedSignal")

        self.assertEqual(len(self._handler._ids), 0)

    @mock.patch('scarlett_os.utility.dbus_runner.DBusRunner', autospec=True, name='mock_dbusrunner')
    def test_connect_then_clear(self, mock_dbusrunner):
        _dr = mock_dbusrunner.get_instance()
        bus = _dr.get_session_bus()

        def test_cb():
            print('test_cb')

        self._handler.connect(bus, "SttFailedSignal", test_cb)

        # Disconnect then test again
        self._handler.clear()

        self.assertEqual(len(self._handler._ids), 0)


class TestSpeakerType(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        pass

    def test_speakertype_speaker_to_array(self):
        self.assertEqual(type(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM')), list)
        self.assertEqual(tasker.SpeakerType.speaker_to_array('It is now, 05:34 PM'), ['It is now, 05:34 PM'])
