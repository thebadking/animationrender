#!/usr/bin/env python

# Copyright (C) 2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import unittest

try:
    from tap.runner import TAPTestRunner
except ImportError:
    print('1..0 # SKIP cannot import TAPTestRunner')
    raise SystemExit(0)

import dbus

from dbus_py_test import UnusableMainLoop

class Test(unittest.TestCase):
    def test_unusable_main_loop(self):
        UnusableMainLoop(set_as_default=True)
        self.assertRaises(ValueError, lambda: dbus.SessionBus())

if __name__ == '__main__':
    runner = TAPTestRunner()
    runner.set_stream(True)
    unittest.main(testRunner=runner)
