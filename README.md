***Blender Animation Render***
***Process that bypasses GUI to avoid crashes***

Tested on macOS, Windows and Linux. (from blender 2.80 to 2.83)

Animation render is an addon for blender, it renders by python script bypassing the GUI, avoiding all the crashes that are GUI related while rendering. It works for cycles and eevee. It allows you to render an interval of frames grabing the details from context like first frame and last frame, output path and all the details required for rendering, it adds some buttons on the Output menu like:
- Render Animation
- Enable notifications (OS notifications since Blender GUI is frozen while processing)
- Save file before Rendering
- Sound per frame and/or sound at completion (for macOS only) for windows and linux there is allways a system sound associated, mute it or unmute as necessary

Notifications include how many frames are to be rendered, current frame, percentage of completion and time estimate for completion

If you are having problems rendering even one frame you can set the first and the last frame to be the one you need rendered.

Disabling the Notification check will enable output to console.

>USE ONLY TO RENDER TO SEQUENCIAL IMAGE FILES
It will not work if you try to output directly to a video file.

>The blender file needs to be saved at least once somewhere if you want the autosave function to work, it exists because since you cannot stop the Rendering process, if you really need to stop it, you have to force close Blender, and at that time you cannot save the file, it will save you a lot of headaches. (Client calls you and wants something changed while it was rendering, and you forgot to save the file)

>**IMPORTANT NOTICE FOR macOS:**

Installing the addon on macOS should be done manually as the decompression method from blender destroys a binary necessary for notification.
you can install the addon like this:
uncompress both folders ( animationrender and modules )
place them on:
/Users/"YOUR USERNAME"/Library/Application Support/Blender/"YOUR BLENDER VERSION"/scripts/addons/

>**IMPORTANT NOTICE FOR LINUX:**

Restart blender after activation of the add-on or notifications will not work until restart

***Screenshot WINDOWS***

![](https://raw.githubusercontent.com/thebadking/animationrender/master/screenshots/Screenshot.png)

***Screenshot MAC***

![](https://raw.githubusercontent.com/thebadking/animationrender/master/screenshots/screenshot_macOS.png)
