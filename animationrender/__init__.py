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


import sys, bpy, platform
from animationrender import prefs, main, render, notification
oSystem = platform.system()
# register the addon + modules found in globals()
bl_info = {
    "name": "Animation Render",
    "author": "André Ferreira",
    "version": (1, 0, 0),
    "blender": (2, 81),
    "location": "Scene: Output Properties",
    "description": "A rendering process that bypasses GUI to avoid crashes",
    "warning": "",
    "wiki_url": "https://github.com/thebadking/animationrender",
    "tracker_url": "",
    "category": "Render",
}


class animationRenderPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    soundList: bpy.props.EnumProperty(
        items=[
            ('Baso', 'Baso ', '', '', 0),
            ('Blow', 'Blow', '', '', 1),
            ('Bottle', 'Bottle', '', '', 2),
            ('Frog', 'Frog', '', '', 3),
            ('Funk', 'Funk', '', '', 4),
            ('Glass', 'Glass', '', '', 5),
            ('Hero', 'Hero', '', '', 6),
            ('Morse', 'Morse', '', '', 7),
            ('Ping', 'Ping', '', '', 8),
            ('Pop', 'Pop', '', '', 9),
            ('Purr', 'Purr', '', '', 10),
            ('Sosumi', 'Sosumi', '', '', 11),
            ('Submarine', 'Submarine', '', '', 12),
            ('Tink', 'Tink', '', '', 13)
            ],
        default='Submarine',
        name = 'Sound List'
    )
    if oSystem == "Darwin": 
        def draw(self, context):
            layout = self.layout
            layout.label(text='Sound Selection for notification:')
            row = layout.row()
            row.prop(self, 'soundList', expand=False)



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
    bpy.utils.register_class(animationRenderPreferences)


def unregister():
    bpy.utils.unregister_class(animationRenderPreferences)
    _call_globals("unregister")
    _flush_modules("animationrender")  # reload animationrender
    
