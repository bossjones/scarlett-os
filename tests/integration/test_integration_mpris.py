#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_integration_mpris
----------------------------------
"""

import os
import sys
import signal
import pytest
import builtins
import threading

import unittest
import unittest.mock as mock

# pydbus.request_name.NameOwner

import pydbus
import scarlett_os
import scarlett_os.exceptions

done = 0


class TestScarlettSpeaker(object):

    def test_bus_works(self, session_bus):
        bus = session_bus
        assert type(bus) == pydbus.request_name.NameOwner
        # In [5]: _session = _dr.get_session_bus()

        # In [6]: _session
        # Out[6]: <pydbus.bus.Bus at 0x7fa552e8ef60>

        # In [7]: _session.request_name('org.scarlett')
        # Out[7]: <pydbus.request_name.NameOwner at 0x7fa55a0e1bb8>

        # In [8]:



# class TestScarlettSpeaker(unittest.TestCase):

    # def __load_dbus_service(self):

    #   bus = get_session_bus()

    #   sl = mpris.ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')

    #   pass


    # def setUp(self):  # noqa: N802

    #     # import faulthandler
    #     # faulthandler.register(signal.SIGUSR2, all_threads=True)

    #     # from scarlett_os.internal.debugger import init_debugger
    #     # from scarlett_os.internal.debugger import set_gst_grapviz_tracing
    #     # init_debugger()
    #     # set_gst_grapviz_tracing()
    #     # # Example of how to use it
    #     # from pydbus import SessionBus
    #     # bus = SessionBus()
    #     # bus.own_name(name='org.scarlett')
    #     # sl = ScarlettListener(bus=bus.con, path='/org/scarlett/Listener')
    #     # loop.run()

    #     # def sigint_handler(*args):
    #     #     """Exit on Ctrl+C"""

    #     #     # Unregister handler, next Ctrl-C will kill app
    #     #     # TODO: figure out if this is really needed or not
    #     #     signal.signal(signal.SIGINT, signal.SIG_DFL)

    #     #     sl.Quit()

    #     # signal.signal(signal.SIGINT, sigint_handler)

    #     pass

    # def tearDown(self):
    #     pass

