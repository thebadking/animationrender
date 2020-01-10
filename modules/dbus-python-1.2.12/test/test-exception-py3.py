#!/usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT

import unittest

try:
    from tap.runner import TAPTestRunner
except ImportError:
    print('1..0 # SKIP cannot import TAPTestRunner')
    raise SystemExit(0)

import dbus

# from test-service.py
class ServiceError(dbus.DBusException):
    """Exception representing a normal "environmental" error"""
    include_traceback = False
    _dbus_error_name = 'com.example.Networking.ServerError'


class DBusExceptionTestCase(unittest.TestCase):

    def test_dbus_exception(self):
        e = dbus.exceptions.DBusException("bäää")
        msg = e.get_dbus_message()
        self.assertEqual(msg, "bäää")
        self.assertEqual(str(e), "bäää")

    def test_subclass_exception(self):
        e = ServiceError("bäää")
        msg = e.get_dbus_message()
        self.assertEqual(msg, "bäää")
        self.assertEqual(str(e), "com.example.Networking.ServerError: bäää")


if __name__ == "__main__":
    runner = TAPTestRunner()
    runner.set_stream(True)
    unittest.main(testRunner=runner)
