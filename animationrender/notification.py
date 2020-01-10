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
import bpy, os, sys, platform
from datetime import datetime

ver = bpy.app.version_string
sVer = str(ver[0:4])
pyVer=sys.version[0:3]
oSystem = platform.system()

if oSystem == "Darwin":
    try:
        from pync import Notifier
    except ImportError as error:
        print("IMPORT ERROR")
    print("Running Blender " + sVer + " on macOS")
elif oSystem == "Windows" or oSystem == "Linux":
    try:
        from plyer import notification
    except ImportError as error:
        print("IMPORT ERROR")
        print("SYS PATH 10") #C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\2.81\scripts\addons\modules
        print("SYS PATH 12") #C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\2.81\scripts\addons
    print("Running Blender "+sVer+" on " +oSystem)

def showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step):
    if bpy.context.scene.my_tool.notify_check == True:
        title = "Blender"
        renderingText = " - Rendering"
        osSound = 'Submarine'
        if oSystem == "Windows":
            icopath = sys.path[12]+'\\animationrender\\ico\\Icon3.ico'
        if oSystem == "Linux":
            icopath = 
        percentage = 0
        
        if step != totalFrames + 1:
            totalTime = datetime.now() - renderStartTime
            print(totalTime)
            timeRemaining = (totalTime / step) * (totalFrames - step)
            timeRemaining = str(timeRemaining)[:-7]
            totalTime = str(totalTime)[:-7]
            percentage = "%.1f" % ((step - 1) / totalFrames * 100)
            if step == 1:
                percentage = 0
                timeRemaining = "Calculating!"
            messageM = "Rendering Frame({}): {} out of {} Frames\nProgress: {}% Time remaining: {}".format(currentFrame, step, totalFrames, percentage, timeRemaining)
            messageW = "Frame({}): {} out of {} Frames\nTime remaining: {}".format(currentFrame, step, totalFrames, timeRemaining)
            print(messageM)
            if oSystem == "Darwin" and bpy.context.scene.my_tool.f_sound_check == True:
                Notifier.notify(message=messageM, title=title, sound=osSound, group=os.getpid())
            elif oSystem == "Windows" or oSystem == "Linux":
                notification.notify(message=messageW, title=title+renderingText, app_icon=icopath)
            if oSystem == "Windows":
                    notification.notify(message=messageW, title=title+renderingText, app_icon=icopath)
                if oSystem == "Linux":
                    notification.notify(message=messageW, title=title+renderingText, app_icon=icopathL)

        elif step == totalFrames + 1:
            totalTime = datetime.now() - renderStartTime
            totalTime = str(totalTime)[:-7]
            print(totalTime)
            print("FINISHED")
            percentage = 100
            messageM = "Animation rendered in: {}\n{} Frames rendered. {}%".format(totalTime, totalFrames, percentage)
            messageW = "Animation rendered in: {}\n{} Frames rendered".format(totalTime, totalFrames)
            print(messageM)
            if oSystem == "Darwin" and bpy.context.scene.my_tool.l_sound_check == True:
                Notifier.notify(message=messageM, title=title, sound=osSound, group=os.getpid())
            else:
                if oSystem == "Darwin":
                    Notifier.notify(message=messageM, title=title, group=os.getpid())
                if oSystem == "Windows":
                    notification.notify(message=messageW, title=title+renderingText, app_icon=icopath)
                if oSystem == "Linux":
                    notification.notify(message=messageW, title=title+renderingText, app_icon=icopathL)
