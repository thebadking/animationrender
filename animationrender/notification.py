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
stopNotify = False

if oSystem == "Darwin":
    try:
        from pync import Notifier
    except ImportError as error:
        print("pync IMPORT ERROR")
        stopNotify = True
        print("Running Blender " + sVer + " on macOS System Notification will not work")

elif oSystem == "Windows" or oSystem == "Linux":
    try:
        from plyer import notification
    except ImportError as error:
        stopNotify = True
        print("Plyer Import Error")
        print("WINDOWS: SYS PATH 10") #C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\2.81\scripts\addons\modules
        print("WINDOWS: SYS PATH 12") #C:\Users\USER\AppData\Roaming\Blender Foundation\Blender\2.81\scripts\addons
        print("LINUX: SYS PATH 8")  #/home/USER/.config/blender/2.81/scripts/addons/modules
        print("LINUX: SYS PATH 10") #/home/USER/.config/blender/2.81/scripts/addons
        print("Running Blender "+sVer+" on " +oSystem+ " System Notification will not work")

def showNotify(firstFrame, lastFrame, currentFrame, totalFrames, frameStartTime, renderStartTime, step):
    title = "Blender"
    renderingText = " - Rendering"
    osSound = 'Submarine'
    percentage = 0
    if oSystem == "Windows":
        icopath = sys.path[12]+'\\animationrender\\ico\\Icon3.ico'
    elif oSystem == "Linux":
        icopath = sys.path[10]+'/animationrender/ico/Icon1.ico'

    if step != totalFrames + 1:
        totalTime = datetime.now() - renderStartTime
        timeRemaining = (totalTime / step) * (totalFrames - step)
        timeRemaining = str(timeRemaining)[:-7]
        totalTime = str(totalTime)[:-7]
        percentage = "%.1f" % ((step - 1) / totalFrames * 100)
        if step == 1:
            percentage = 0
            timeRemaining = "Calculating!"
        messageM = "Rendering Frame({}): {} out of {} Frames\nProgress: {}% Time remaining: {}".format(currentFrame, step, totalFrames, percentage, timeRemaining)
        messageW = "Frame({}): {} out of {} Frames\nTime remaining: {}".format(currentFrame, step, totalFrames, timeRemaining)
        if stopNotify == False and bpy.context.scene.my_tool.notify_check == True:
            if oSystem == "Darwin":
                if bpy.context.scene.my_tool.f_sound_check == True:
                    Notifier.notify(message=messageM, title=title, sound=osSound, group=os.getpid())
                else:
                    Notifier.notify(message=messageM, title=title, group=os.getpid())
            elif oSystem == "Windows" or "Linux":
                notification.notify(message=messageW, title=title+renderingText, app_icon=icopath)

    elif step == totalFrames + 1:
        totalTime = datetime.now() - renderStartTime
        totalTime = str(totalTime)[:-7]
        percentage = 100
        messageM = "Animation rendered in: {}\n{} Frames rendered. {}%".format(totalTime, totalFrames, percentage)
        messageW = "Animation rendered in: {}\n{} Frames rendered".format(totalTime, totalFrames)
        if stopNotify == False and bpy.context.scene.my_tool.notify_check == True:
            if oSystem == "Darwin":
                if bpy.context.scene.my_tool.l_sound_check == True:
                    Notifier.notify(message=messageM, title=title, sound=osSound, group=os.getpid())
                else:
                    Notifier.notify(message=messageM, title=title, group=os.getpid())
            elif oSystem == "Windows" or "Linux":
                notification.notify(message=messageW, title=title+renderingText, app_icon=icopath)    

    if stopNotify == True or bpy.context.scene.my_tool.notify_check == False:
        if step != totalFrames + 1:
            print("TOTAL TIME: "+ totalTime)
            print("Rendering Frame({}): {} out of {} Frames\nProgress: {}% Time remaining: {}".format(currentFrame, step, totalFrames, percentage, timeRemaining))
        elif step == totalFrames + 1:
            print("FINISHED")
            print("Animation rendered in: {}\n{} Frames rendered. {}%".format(totalTime, totalFrames, percentage))
