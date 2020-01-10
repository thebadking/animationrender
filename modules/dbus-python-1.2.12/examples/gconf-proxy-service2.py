#!/usr/bin/env python

# Example of implementing an entire subtree of objects using
# a FallbackObject.
#
# This is not a particularly realistic example of real-world code any more,
# because GConf now uses D-Bus internally itself, and is deprecated;
# but it's a valid example of a FallbackObject.

# Copyright (C) 2004-2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2005-2007 Collabora Ltd. <http://www.collabora.co.uk/>
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

import dbus
import dbus.mainloop.glib
import dbus.service

from gi.repository import GLib
import gconf

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# there is a real service called "org.gnome.GConf"; don't collide with it.
name = dbus.service.BusName("com.example.GConfProxy", dbus.SessionBus())

class GConfObject(dbus.service.FallbackObject):
    def __init__(self):
        dbus.service.FallbackObject.__init__(self, dbus.SessionBus(), '/org/gnome/GConf')
        self.client = gconf.client_get_default()

    @dbus.service.method("org.gnome.GConf", in_signature='', out_signature='s', rel_path_keyword='object_path')
    def getString(self, object_path):
        return self.client.get_string(object_path)

    @dbus.service.method("org.gnome.GConf", in_signature='s', out_signature='', rel_path_keyword='object_path')
    def setString(self, value, object_path):
        self.client.set_string(object_path, value)

    @dbus.service.method("org.gnome.GConf", in_signature='', out_signature='i', rel_path_keyword='object_path')
    def getInt(self, object_path):
        return self.client.get_int(object_path)

    @dbus.service.method("org.gnome.GConf", in_signature='i', out_signature='', rel_path_keyword='object_path')
    def setInt(self, value, object_path):
        self.client.set_int(object_path, value)

gconf_service = GConfObject()

print ("GConf Proxy service started.")
print ("Run 'gconf-proxy-client.py' to fetch a GConf key through the proxy...")

mainloop = GLib.MainLoop()
mainloop.run()
