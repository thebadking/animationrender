#!/usr/bin/env python
# encoding: utf-8

# Copyright © 2016 Collabora Ltd. <http://www.collabora.co.uk/>
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

from distutils.dir_util import copy_tree, mkpath
from distutils.file_util import copy_file
from setuptools.dist import Distribution
from setuptools import setup, Extension
import os
import subprocess
import sys

if os.path.exists('.version'):
    version = open('.version').read().strip()
else:
    version = subprocess.check_output(['autoconf', '--trace', 'AC_INIT:$2',
        'configure.ac']).decode('utf-8').strip()

class Build(Distribution().get_command_class('build')):
    """Dummy version of distutils build which runs an Autotools build system
    instead.
    """

    def run(self):
        srcdir = os.getcwd()
        builddir = os.path.join(srcdir, self.build_temp)
        configure = os.path.join(srcdir, 'configure')
        mkpath(builddir)

        if not os.path.exists(configure):
            configure = os.path.join(srcdir, 'autogen.sh')

        subprocess.check_call([
                configure,
                '--disable-maintainer-mode',
                'PYTHON=' + sys.executable,
                # Put the documentation, etc. out of the way: we only want
                # the Python code and extensions
                '--prefix=' + os.path.join(builddir, 'prefix'),
            ],
            cwd=builddir)
        make_args = [
            'pythondir=' + os.path.join(srcdir, self.build_lib),
            'pyexecdir=' + os.path.join(srcdir, self.build_lib),
        ]
        subprocess.check_call(['make', '-C', builddir] + make_args)
        subprocess.check_call(['make', '-C', builddir, 'install'] + make_args)

class BuildExt(Distribution().get_command_class('build_ext')):
    def run(self):
        pass

class BuildPy(Distribution().get_command_class('build_py')):
    def run(self):
        pass

dbus_bindings = Extension('_dbus_bindings',
        sources=['dbus_bindings/module.c'])
dbus_glib_bindings = Extension('_dbus_glib_bindings',
        sources=['dbus_glib_bindings/module.c'])

setup(
    name='dbus-python',
    version=version,
    description='Python bindings for libdbus',
    long_description=open('README').read(),
    maintainer='The D-Bus maintainers',
    maintainer_email='dbus@lists.freedesktop.org',
    download_url='http://dbus.freedesktop.org/releases/dbus-python/',
    url='http://www.freedesktop.org/wiki/Software/DBusBindings/#python',
    packages=['dbus'],
    ext_modules=[dbus_bindings, dbus_glib_bindings],
    license='Expat (MIT/X11)',
    classifiers=[
        'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Object Brokering',
    ],
    cmdclass={
        'build': Build,
        'build_py': BuildPy,
        'build_ext': BuildExt,
    },
    tests_require=['tap.py'],
)
