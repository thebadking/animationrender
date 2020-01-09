#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


import sys
from animationrender import prefs, main, render, notification

# register the addon + modules found in globals()
bl_info = {
    "name": "Animation Render",
    "author": "André Ferreira",
    "version": (1, 0, 0),
    "blender": (2, 81),
    "location": "Barcelona",
    "description": "A rendering process that bypasses GUI, adds buttons to output separator",
    "warning": "",
    "wiki_url": "https://github.com/thebadking/animationrender",
    "tracker_url": "",
    "category": "Render",
}


def _call_globals(attr_name):
    for m in globals().values():
        if hasattr(m, attr_name):
            getattr(m, attr_name)()


def _flush_modules(pkg_name):
    pkg_name = pkg_name.lower()
    for k in tuple(sys.modules.keys()):
        if k.lower().startswith(pkg_name):
            del sys.modules[k]


def register():
    _call_globals("register")


def unregister():
    _call_globals("unregister")
    _flush_modules("animationrender")  # reload animationrender
