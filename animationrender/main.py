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

import bpy, os, platform, sys
from animationrender.manager import addManager, startManager, stopManager, clearFinished

####################################### GUI INTERFACE

oSystem = platform.system()

class AddQueue(bpy.types.Operator):
    bl_idname = "add.queue"
    bl_label = "Add to Queue"
    bl_description = "Add to queue for Animation Render"
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        addManager()
        return {"FINISHED"}

class RenderQueue(bpy.types.Operator):
    bl_idname = "render.queue"
    bl_label = "Render Queue"
    bl_description = "Start queue for Animation Render"
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        startManager()
        return {"FINISHED"}

class StopQueue(bpy.types.Operator):
    bl_idname = "stop.queue"
    bl_label = "Stop Queue"
    bl_description = "Stop queue"
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        stopManager()
        return {"FINISHED"}

class clearCached(bpy.types.Operator):
    bl_idname = "clear.finished"
    bl_label = "Clear Finished"
    bl_description = "Clear Finished"
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        clearFinished()
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
    camera_angle: aList(
        items=[
            ('0', 'None', '', '', 0),
            ('1', '1', '', '', 1),
            ('2', '2', '', '', 2),
            ('3', '3', '', '', 3),
            ('4', '4', '', '', 4),
            ('5', '5', '', '', 5),
            ('6', '6', '', '', 6),
            ('7', '7', '', '', 7),
            ('8', '8', '', '', 8),
            ('9', '9', '', '', 9)
        ],
        default='0',
        name='Camera Angle'
    )
#PANEL-----------------------------------------------------
class RenderProcessPnl(bpy.types.Panel):
    bl_label = "Animation Render Manager"
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
        createProperty("camera_angle")
        self.layout.operator("add.queue")
        self.layout.operator("render.queue")
        self.layout.operator("stop.queue")
        self.layout.operator("clear.finished")
        
#-------------------------------------------------------------------------------------------

def register():
    bpy.utils.register_class(MySettings)
    bpy.utils.register_class(RenderProcessPnl)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)
    bpy.utils.register_class(AddQueue)
    bpy.utils.register_class(RenderQueue)
    bpy.utils.register_class(StopQueue)
    bpy.utils.register_class(clearCached)

def unregister():
    bpy.utils.unregister_class(MySettings)
    bpy.utils.unregister_class(RenderProcessPnl)
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(AddQueue)
    bpy.utils.unregister_class(RenderQueue)
    bpy.utils.unregister_class(StopQueue)
    bpy.utils.unregister_class(clearCached)

if __name__ == "__main__":
    register()

