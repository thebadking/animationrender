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
from animationrender.notification import showNotify
from datetime import datetime
from pathlib import Path

def render(tempPath):
    if bpy.context.scene.my_tool.camera_angle == 0:
        cameraAngle = ""
    else:
        baseName = bpy.path.basename(bpy.context.blend_data.filepath)
        if bpy.context.scene.my_tool.camera_angle == "0":
            stringAdd = "/" + baseName[9:-6] + "/"
        else:
            stringAdd = "/" + baseName[9:-6] + " - Camera Angle: " + bpy.context.scene.my_tool.camera_angle + "/"

    bpy.context.scene.render.filepath = tempPath+stringAdd+str(bpy.context.scene.frame_current)
    bpy.ops.render.render(write_still=True)
    bpy.context.scene.frame_set(bpy.context.scene.frame_current+bpy.context.scene.frame_step)

def RenderProcess():
    #if bpy.context.scene.my_tool.saveFile == True:
    #    bpy.ops.wm.save_mainfile()
    tempPath = bpy.context.scene.render.filepath[:]
    firstFrame = bpy.context.scene.frame_start
    lastFrame = bpy.context.scene.frame_end
    bpy.context.scene.frame_set(firstFrame)
    currentFrame = bpy.context.scene.frame_current
    renderStartTime = datetime.now()
    step = 1
    print("Starting Render:")
    totalFrames = (lastFrame - firstFrame + 1)
    if(totalFrames % bpy.context.scene.frame_step != 0):
        totalFrames = int((totalFrames/bpy.context.scene.frame_step) + 1)
    basePath = bpy.context.preferences.addons['animationrender'].preferences.directoryQueue
    while bpy.context.scene.frame_current <= lastFrame:
        if Path(basePath + 'running').is_file():
            frameStartTime = datetime.now()
            currentFrame = bpy.context.scene.frame_current
            showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step)
            render(tempPath)
            step = step + 1
        else:
            break
    showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step)
    bpy.context.scene.render.filepath = tempPath
    print("RENDER DONE!")

