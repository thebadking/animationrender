#!/usr/bin/env python

"""Tests that don't need an active D-Bus connection to run, but can be
run in isolation.
"""

# Copyright (C) 2006 Collabora Ltd. <http://www.collabora.co.uk/>
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

from __future__ import unicode_literals

import struct
import sys
import os
import unittest

try:
    from tap.runner import TAPTestRunner
except ImportError:
    print('1..0 # SKIP cannot import TAPTestRunner')
    raise SystemExit(0)

import _dbus_bindings
import dbus
import dbus.lowlevel as lowlevel
import dbus.types as types
from dbus._compat import is_py2, is_py3

if is_py3:
    def make_long(n):
        return n
else:
    def make_long(n):
        return long(n)

if 'DBUS_TEST_UNINSTALLED' in os.environ:
    builddir = os.path.normpath(os.environ["DBUS_TOP_BUILDDIR"])
    pydir = os.path.normpath(os.environ["DBUS_TOP_SRCDIR"])
    pkg = dbus.__file__

    if not pkg.startswith(pydir):
        raise Exception("DBus modules (%s) are not being picked up from the "
                "package" % pkg)

    if not _dbus_bindings.__file__.startswith(builddir):
        raise Exception("DBus modules (%s) are not being picked up from the "
                "package" % _dbus_bindings.__file__)

    assert _dbus_bindings.__version__ == os.environ['DBUS_PYTHON_VERSION'], \
            '_dbus_bindings was compiled as version %s but Automake says '\
            'we should be version %s' \
            % (_dbus_bindings.__version__, os.environ['DBUS_PYTHON_VERSION'])

assert (_dbus_bindings._python_version & 0xffff0000
        == sys.hexversion & 0xffff0000), \
        '_dbus_bindings was compiled for Python %x but this is Python %x, '\
        'a different major version'\
        % (_dbus_bindings._python_version, sys.hexversion)

def uni(x):
    """Return a Unicode string consisting of the single Unicode character
    with the given codepoint (represented as a surrogate pair if this is
    a "narrow" Python build). This is a generalization of unichr().

    uni(0x0001f639) == u'\\U0001f639' in versions where that syntax is
    supported.
    """
    if x <= 0xFFFF:
        if is_py3:
            return chr(x)
        else:
            return unichr(x)
    else:
        return struct.pack('>I', x).decode('utf_32_be')

class TestTypes(unittest.TestCase):

    def test_Dictionary(self):
        self.assertEqual(types.Dictionary({'foo':'bar'}), {'foo':'bar'})
        self.assertEqual(types.Dictionary({}, variant_level=2), {})
        self.assertEqual(types.Dictionary({}, variant_level=2).variant_level, 2)

    def test_Array(self):
        self.assertEqual(types.Array(['foo','bar']), ['foo','bar'])
        self.assertEqual(types.Array([], variant_level=2), [])
        self.assertEqual(types.Array([], variant_level=2).variant_level, 2)

    def test_Double(self):
        self.assertEqual(types.Double(0.0), 0.0)
        self.assertEqual(types.Double(0.125, variant_level=2), 0.125)
        self.assertEqual(types.Double(0.125, variant_level=2).variant_level, 2)

    def test_Struct(self):
        x = types.Struct(('',))
        self.assertEqual(x.variant_level, 0)
        self.assertEqual(x, ('',))
        x = types.Struct('abc', variant_level=42)
        self.assertEqual(x.variant_level, 42)
        self.assertEqual(x, ('a','b','c'))

    def test_Byte(self):
        self.assertEqual(types.Byte(b'x', variant_level=2),
                          types.Byte(ord('x')))
        self.assertEqual(types.Byte(1), 1)
        self.assertEqual(types.Byte(make_long(1)), 1)
        self.assertRaises(Exception, lambda: types.Byte(b'ab'))
        self.assertRaises(TypeError, types.Byte, '\x12xxxxxxxxxxxxx')

        # Byte from a unicode object: what would that even mean?
        self.assertRaises(Exception,
                lambda: types.Byte(b'a'.decode('latin-1')))

    def test_ByteArray(self):
        self.assertEqual(types.ByteArray(b''), b'')

    def test_object_path_attr(self):
        class MyObject(object):
            __dbus_object_path__ = '/foo'
        from _dbus_bindings import SignalMessage
        self.assertEqual(SignalMessage.guess_signature(MyObject()), 'o')

    def test_integers(self):
        subclasses = [int]
        if is_py2:
            subclasses.append(long)
        subclasses = tuple(subclasses)
        # This is an API guarantee. Note that exactly which of these types
        # are ints and which of them are longs is *not* guaranteed.
        for cls in (types.Int16, types.UInt16, types.Int32, types.UInt32,
            types.Int64, types.UInt64):
            self.assertTrue(issubclass(cls, subclasses))
            self.assertTrue(isinstance(cls(0), subclasses))
            self.assertEqual(cls(0), 0)
            self.assertEqual(cls(23, variant_level=1), 23)
            self.assertEqual(cls(23, variant_level=1).variant_level, 1)

    def test_integer_limits_16(self):
        self.assertEqual(types.Int16(0x7fff), 0x7fff)
        self.assertEqual(types.Int16(-0x8000), -0x8000)
        self.assertEqual(types.UInt16(0xffff), 0xffff)
        self.assertRaises(Exception, types.Int16, 0x8000)
        self.assertRaises(Exception, types.Int16, -0x8001)
        self.assertRaises(Exception, types.UInt16, 0x10000)

    def test_integer_limits_32(self):
        self.assertEqual(types.Int32(0x7fffffff), 0x7fffffff)
        self.assertEqual(types.Int32(make_long(-0x80000000)), 
                         make_long(-0x80000000))
        self.assertEqual(types.UInt32(make_long(0xffffffff)), 
                         make_long(0xffffffff))
        self.assertRaises(Exception, types.Int32, make_long(0x80000000))
        self.assertRaises(Exception, types.Int32, make_long(-0x80000001))
        self.assertRaises(Exception, types.UInt32, make_long(0x100000000))

    def test_integer_limits_64(self):
        self.assertEqual(types.Int64(make_long(0x7fffffffffffffff)), 
                         make_long(0x7fffffffffffffff))
        self.assertEqual(types.Int64(make_long(-0x8000000000000000)), 
                         make_long(-0x8000000000000000))
        self.assertEqual(types.UInt64(make_long(0xffffffffffffffff)), 
                         make_long(0xffffffffffffffff))
        self.assertRaises(Exception, types.Int16, 
                          make_long(0x8000000000000000))
        self.assertRaises(Exception, types.Int16, 
                          make_long(-0x8000000000000001))
        self.assertRaises(Exception, types.UInt16, 
                          make_long(0x10000000000000000))

    def test_Signature(self):
        self.assertRaises(Exception, types.Signature, 'a')
        self.assertEqual(types.Signature('ab', variant_level=23), 'ab')
        self.assertTrue(isinstance(types.Signature('ab'), str))
        self.assertEqual(tuple(types.Signature('ab(xt)a{sv}')),
                         ('ab', '(xt)', 'a{sv}'))
        self.assertTrue(isinstance(tuple(types.Signature('ab'))[0],
                                   types.Signature))


class TestMessageMarshalling(unittest.TestCase):

    def test_path(self):
        s = lowlevel.SignalMessage('/a/b/c', 'foo.bar', 'baz')
        self.assertEqual(s.get_path(), types.ObjectPath('/a/b/c'))
        self.assertEqual(type(s.get_path()), types.ObjectPath)
        self.assertEqual(s.get_path_decomposed(), ['a', 'b', 'c'])
        # this is true in both major versions: it's a bytestring in
        # Python 2 and a Unicode string in Python 3
        self.assertEqual(type(s.get_path_decomposed()[0]), str)
        self.assertTrue(s.has_path('/a/b/c'))
        self.assertFalse(s.has_path('/a/b'))
        self.assertFalse(s.has_path('/a/b/c/d'))

        s = lowlevel.SignalMessage('/', 'foo.bar', 'baz')
        self.assertEqual(s.get_path(), types.ObjectPath('/'))
        self.assertEqual(s.get_path().__class__, types.ObjectPath)
        self.assertEqual(s.get_path_decomposed(), [])
        self.assertTrue(s.has_path('/'))
        self.assertFalse(s.has_path(None))

    def test_sender(self):
        s = lowlevel.SignalMessage('/a/b/c', 'foo.bar', 'baz')
        self.assertEqual(s.get_sender(), None)
        self.assertFalse(s.has_sender(':1.23'))
        s.set_sender(':1.23')
        self.assertEqual(s.get_sender(), ':1.23')
        # bytestring in Python 2, Unicode string in Python 3
        self.assertEqual(type(s.get_sender()), str)
        self.assertTrue(s.has_sender(':1.23'))

    def test_destination(self):
        s = lowlevel.SignalMessage('/a/b/c', 'foo.bar', 'baz')
        self.assertEqual(s.get_destination(), None)
        self.assertFalse(s.has_destination(':1.23'))
        s.set_destination(':1.23')
        self.assertEqual(s.get_destination(), ':1.23')
        # bytestring in Python 2, Unicode string in Python 3
        self.assertEqual(type(s.get_destination()), str)
        self.assertTrue(s.has_destination(':1.23'))

    def test_interface(self):
        s = lowlevel.SignalMessage('/a/b/c', 'foo.bar', 'baz')
        self.assertEqual(s.get_interface(), 'foo.bar')
        # bytestring in Python 2, Unicode string in Python 3
        self.assertEqual(type(s.get_interface()), str)
        self.assertTrue(s.has_interface('foo.bar'))

    def test_member(self):
        s = lowlevel.SignalMessage('/a/b/c', 'foo.bar', 'baz')
        self.assertEqual(s.get_member(), 'baz')
        # bytestring in Python 2, Unicode string in Python 3
        self.assertEqual(type(s.get_member()), str)
        self.assertTrue(s.has_member('baz'))

    def test_count(self):
        from _dbus_bindings import SignalMessage
        s = SignalMessage('/', 'foo.bar', 'baz')
        try:
            s.append('a', signature='ss')
        except TypeError:
            pass
        else:
            raise AssertionError('Appending too few things in a message '
                                 'should fail')
        s = SignalMessage('/', 'foo.bar', 'baz')
        try:
            s.append('a','b','c', signature='ss')
        except TypeError:
            pass
        else:
            raise AssertionError('Appending too many things in a message '
                                 'should fail')

    def test_append(self):
        aeq = self.assertEqual
        from _dbus_bindings import SignalMessage
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append([types.Byte(1)], signature='ay')
        aeq(s.get_signature(), 'ay')
        aeq(s.get_args_list(), [[types.Byte(1)]])

        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append([], signature='ay')
        aeq(s.get_args_list(), [[]])

    def test_append_Byte(self):
        aeq = self.assertEqual
        from _dbus_bindings import SignalMessage

        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(0xFE, signature='y')
        aeq(s.get_args_list(), [types.Byte(0xFE)])

        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(b'\xfe', signature='y')
        aeq(s.get_args_list(), [types.Byte(0xFE)])

        # appending a unicode object (including str in Python 3)
        # is not allowed
        s = SignalMessage('/', 'foo.bar', 'baz')
        self.assertRaises(Exception,
                lambda: s.append('a'.decode('latin-1'), signature='y'))

        s = SignalMessage('/', 'foo.bar', 'baz')
        self.assertRaises(Exception,
                lambda: s.append(b'ab', signature='y'))

    def test_append_ByteArray(self):
        aeq = self.assertEqual
        from _dbus_bindings import SignalMessage
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(types.ByteArray(b'ab'), signature='ay')
        aeq(s.get_args_list(), [[types.Byte(b'a'), types.Byte(b'b')]])
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(types.ByteArray(b'ab'), signature='av')
        aeq(s.get_args_list(), [[types.Byte(b'a'), types.Byte(b'b')]])
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(types.ByteArray(b''), signature='ay')
        aeq(s.get_args_list(), [[]])
        aeq(s.get_args_list(byte_arrays=True), [types.ByteArray(b'')])

    def test_append_Variant(self):
        aeq = self.assertEqual
        from _dbus_bindings import SignalMessage
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(types.Int32(1, variant_level=0),
                 types.String('a', variant_level=42),
                 types.Array([types.Byte(b'a', variant_level=1),
                              types.UInt32(123, variant_level=1)],
                             signature='v'),
                 signature='vvv')
        aeq(s.get_signature(), 'vvv')
        args = s.get_args_list()
        aeq(args[0].__class__, types.Int32)
        aeq(args[0].variant_level, 1)
        aeq(args[1].__class__, types.String)
        aeq(args[1].variant_level, 42)
        aeq(args[2].__class__, types.Array)
        aeq(args[2].variant_level, 1)
        aeq(args[2].signature, 'v')

    def test_guess_signature(self):
        aeq = self.assertEqual
        from _dbus_bindings import Message
        aeq(Message.guess_signature(('a','b')), '(ss)')
        aeq(Message.guess_signature('a','b'), 'ss')
        aeq(Message.guess_signature(['a','b']), 'as')
        aeq(Message.guess_signature(('a',)), '(s)')
        aeq(Message.guess_signature('abc'), 's')
        aeq(Message.guess_signature(types.Int32(123)), 'i')
        aeq(Message.guess_signature(types.ByteArray(b'abc')), 'ay')
        aeq(Message.guess_signature(('a',)), '(s)')
        aeq(Message.guess_signature(['a']), 'as')
        aeq(Message.guess_signature({'a':'b'}), 'a{ss}')
        aeq(Message.guess_signature(types.ObjectPath('/')), 'o')
        aeq(Message.guess_signature(types.Signature('x')), 'g')

    def test_guess_signature_python_ints(self):
        aeq = self.assertEqual
        from _dbus_bindings import Message
        aeq(Message.guess_signature(7), 'i')
        if is_py2:
            aeq(Message.guess_signature(make_long(7)), 'x')

    def test_guess_signature_dbus_types(self):
        aeq = self.assertEqual
        from _dbus_bindings import Message
        gs = Message.guess_signature
        aeq(gs(types.Dictionary({'a':'b'})), 'a{ss}')
        aeq(gs(types.Dictionary({'a':'b'}, signature='sv')), 'a{sv}')
        aeq(gs(types.Dictionary({}, signature='iu')), 'a{iu}')
        aeq(gs(types.Array([types.Int32(1)])), 'ai')
        aeq(gs(types.Array([types.Int32(1)], signature='u')), 'au')

    def test_get_args_options(self):
        aeq = self.assertEqual
        s = _dbus_bindings.SignalMessage('/', 'foo.bar', 'baz')
        s.append(b'b', b'bytes', -1, 1, 'str', 'var', signature='yayiusv')
        aeq(s.get_args_list(), [
            ord('b'), 
            [ord('b'),ord('y'),ord('t'),ord('e'), ord('s')], 
            -1, 1, 'str', 'var'
            ])
        byte, bytes, int32, uint32, string, variant = s.get_args_list()
        aeq(byte.__class__, types.Byte)
        aeq(bytes.__class__, types.Array)
        aeq(bytes[0].__class__, types.Byte)
        aeq(int32.__class__, types.Int32)
        aeq(uint32.__class__, types.UInt32)
        aeq(string.__class__, types.String)
        aeq(string.variant_level, 0)
        aeq(variant.__class__, types.String)
        aeq(variant.variant_level, 1)

        byte, bytes, int32, uint32, string, variant = s.get_args_list(
                byte_arrays=True)
        aeq(byte.__class__, types.Byte)
        aeq(bytes.__class__, types.ByteArray)
        aeq(bytes, b'bytes')
        if is_py3:
            aeq(bytes[0].__class__, int)
        else:
            aeq(bytes[0].__class__, str)
        aeq(int32.__class__, types.Int32)
        aeq(uint32.__class__, types.UInt32)
        aeq(string.__class__, types.String)
        aeq(variant.__class__, types.String)
        aeq(variant.variant_level, 1)

        kwargs = {}
        if is_py2:
            kwargs['utf8_strings'] = True
        byte, bytes, int32, uint32, string, variant = s.get_args_list(
            **kwargs)
        aeq(byte.__class__, types.Byte)
        aeq(bytes.__class__, types.Array)
        aeq(bytes[0].__class__, types.Byte)
        aeq(int32.__class__, types.Int32)
        aeq(uint32.__class__, types.UInt32)
        if is_py2:
            aeq(string.__class__, types.UTF8String)
        aeq(string, 'str')
        if is_py2:
            aeq(variant.__class__, types.UTF8String)
        aeq(variant.variant_level, 1)
        aeq(variant, 'var')

    def test_object_path_attr(self):
        from _dbus_bindings import SignalMessage
        class MyObject(object):
            __dbus_object_path__ = '/foo'
        s = SignalMessage('/', 'foo.bar', 'baz')
        s.append(MyObject(), signature='o')
        s.append(MyObject())
        self.assertEqual(s.get_args_list(), ['/foo', '/foo'])

    def test_struct(self):
        from _dbus_bindings import SignalMessage
        s = SignalMessage('/', 'foo.bar', 'baz')
        try:
            s.append(('a',), signature='(ss)')
        except TypeError:
            pass
        else:
            raise AssertionError('Appending too few things in a struct '
                                 'should fail')
        s = SignalMessage('/', 'foo.bar', 'baz')
        try:
            s.append(('a','b','c'), signature='(ss)')
        except TypeError:
            pass
        else:
            raise AssertionError('Appending too many things in a struct '
                                 'should fail')

    def test_utf8(self):
        from _dbus_bindings import SignalMessage

        for bad in [
                uni(0xD800),
                b'\xed\xa0\x80',
                ]:
            s = SignalMessage('/', 'foo.bar', 'baz')
            try:
                s.append(bad, signature='s')
            except UnicodeError:
                pass
            else:
                raise AssertionError('Appending %r should fail' % bad)
        for good in [
                uni(0xfdcf),
                uni(0xfdf0),
                uni(0xfeff),
                uni(0x0001feff),
                uni(0x00020000),
                uni(0x0007feff),
                uni(0x00080000),
                uni(0x0010feff),
                ]:
            s = SignalMessage('/', 'foo.bar', 'baz')
            s.append(good, signature='s')
            s.append(good.encode('utf-8'), signature='s')
        for noncharacter in [
                uni(0xFDD0),
                b'\xef\xb7\x90',
                uni(0xFDD7),
                b'\xef\xb7\x97',
                uni(0xFDEF),
                b'\xef\xb7\xaf',
                uni(0xFFFE),
                b'\xef\xbf\xbe',
                uni(0xFFFF),
                b'\xef\xbf\xbf',
                uni(0x0001FFFE),
                b'\xf0\x9f\xbf\xbe',
                uni(0x0001FFFF),
                b'\xf0\x9f\xbf\xbf',
                uni(0x0007FFFE),
                b'\xf1\xbf\xbf\xbe',
                uni(0x0007FFFF),
                b'\xf1\xbf\xbf\xbf',
                uni(0x0010FFFE),
                b'\xf4\x8f\xbf\xbe',
                uni(0x0010FFFF),
                b'\xf4\x8f\xbf\xbf',
                ]:
            s = SignalMessage('/', 'foo.bar', 'baz')
            try:
                s.append(noncharacter, signature='s')
            except UnicodeError:
                raise AssertionError(
                    'Appending %r should succeed' % noncharacter)
            else:
                pass  # libdbus >= 1.6.10 allows noncharacters

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix")
    def test_unix_fd(self):
        plain_fd = os.open('/dev/null', os.O_RDONLY)

        try:
            with open('/dev/null', 'r') as file_like_object:
                fd = types.UnixFd(plain_fd)
                self.assertEqual(fd.variant_level, 0)
                other = fd.take()
                os.close(other)

                with self.assertRaises(ValueError):
                    fd.take()

                fd = types.UnixFd(plain_fd, variant_level=42)
                self.assertEqual(fd.variant_level, 42)

                fd = types.UnixFd(file_like_object)
                self.assertEqual(fd.variant_level, 0)

                fd = types.UnixFd(file_like_object, variant_level=42)
                self.assertEqual(fd.variant_level, 42)

                with self.assertRaises(TypeError):
                    types.UnixFd(plain_fd, invalid_kwarg='nope')

                with self.assertRaises(TypeError):
                    types.UnixFd(plain_fd, variant_level='nope')
        finally:
            os.close(plain_fd)

class TestMatching(unittest.TestCase):
    def setUp(self):
        from _dbus_bindings import SignalMessage
        from dbus.connection import SignalMatch
        self._message = SignalMessage('/', 'a.b', 'c')
        class FakeConn(object): pass
        def ignore_cb(*args, **kws): pass
        self._match = SignalMatch(FakeConn(), None, '/', None, None, 
                                  ignore_cb, arg0='/')

    def test_string_match(self):
        self._message.append('/', signature='s')
        self.assertTrue(self._match.maybe_handle_message(self._message))

    def test_object_path_no_match(self):
        self._message.append('/', signature='o')
        self.assertFalse(self._match.maybe_handle_message(self._message))

class TestVersion(unittest.TestCase):
    if sys.version_info[:2] < (2, 7):
        def assertGreater(self, first, second):
            self.assertTrue(first > second)

        def assertLess(self, first, second):
            self.assertTrue(first < second)

    def test_version(self):
        self.assertGreater(dbus.version, (0, 41))
        self.assertLess(dbus.version, (23, 0))
        self.assertGreater(dbus.__version__, '0')
        self.assertLess(dbus.__version__, '9')

if __name__ == '__main__':
    runner = TAPTestRunner()
    runner.set_stream(True)
    unittest.main(testRunner=runner, verbosity=2)
