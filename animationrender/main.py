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

import bpy
import os
import platform
import sys

####################################### GUI INTERFACE

oSystem = platform.system()

class RenderStart(bpy.types.Operator):
    bl_idname = "render.start"
    bl_label = "Render Animation"
    bl_description = "Initialize Animation Render"
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        from animationrender.render import RenderProcess
        RenderProcess(context)
        return {"FINISHED"}

#PANEL SETTINGS
class MySettings(bpy.types.PropertyGroup): 
    aBool = bpy.props.BoolProperty
    aInt = bpy.props.IntProperty
    aFloat = bpy.props.FloatProperty
    aString = bpy.props.StringProperty
    aList = bpy.props.EnumProperty
    l_sound_check: aBool( name = "Play sound at completion", description = "Play sound at completion of Animation Render", default = True)
    f_sound_check: aBool( name = "Play sound per frame", description = "Play sound at completion of each frame", default = False)
    notify_check: aBool( name = "Enable Notification", description = "It will enable notifications using OS notification", default = True)
    saveFile: aBool( name="Save File", description= "Saves Blender file before rendering", default = True)
#PANEL-----------------------------------------------------
class RenderProcessPnl(bpy.types.Panel):
    bl_label = "Animation Render no Preview"
    bl_idname = "RENDER_PT_RenderProcess"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
            
    def draw(self, context):
        def  createProperty(prop):
            self.layout.prop(context.scene.my_tool, prop)
#DISPLAY PROPERTIES-----------------------------------------
        if oSystem == "Darwin":
            createProperty("l_sound_check")
            createProperty("f_sound_check")
        createProperty("notify_check")
        createProperty("saveFile")

        self.layout.operator("render.start")
        
#-------------------------------------------------------------------------------------------

def register():
    bpy.utils.register_class(MySettings)
    bpy.utils.register_class(RenderProcessPnl)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)
    bpy.utils.register_class(RenderStart)

def unregister():
    bpy.utils.unregister_class(MySettings)
    bpy.utils.unregister_class(RenderProcessPnl)
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(RenderStart)

if __name__ == "__main__":
    register()