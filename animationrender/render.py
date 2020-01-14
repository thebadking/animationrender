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

def render(context, tempPath):
    context.scene.render.filepath = tempPath+str(context.scene.frame_current)
    bpy.ops.render.render(write_still=True)
    context.scene.frame_set(context.scene.frame_current+context.scene.frame_step)

def RenderProcess(context):
    if bpy.context.scene.my_tool.saveFile == True:
        bpy.ops.wm.save_mainfile()
    tempPath = context.scene.render.filepath[:]
    firstFrame = context.scene.frame_start
    lastFrame = context.scene.frame_end
    context.scene.frame_set(firstFrame)
    currentFrame = context.scene.frame_current
    renderStartTime = datetime.now()
    step = 1
    print("Starting Render:")
    totalFrames = (lastFrame - firstFrame + 1)
    if(totalFrames % context.scene.frame_step != 0):
        totalFrames = int((totalFrames/context.scene.frame_step) + 1)
    while context.scene.frame_current <= lastFrame:
        frameStartTime = datetime.now()
        currentFrame = context.scene.frame_current
        showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step)
        render(context, tempPath)
        step = step + 1
    showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step)
    context.scene.render.filepath = tempPath
    print("RENDER DONE!")

