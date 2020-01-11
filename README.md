***Blender Animation Render***
***Process that bypasses GUI to avoid crashes***

Tested on macOS, Windows and Linux. (from blender 2.80 to 2.83)

Animation render is an addon for blender, it renders by python script bypassing the GUI, avoiding all the crashes that are GUI related while rendering. It works for cycles and eevee. It allows you to render an interval of frames grabing the details from context like first frame and last frame, output path and all the details required for rendering, it adds some buttons on the Output menu like:
- Render Animation
- Enable notifications
- Save file before Rendering
- Sound per frame and/or sound at completion (for macOS only)

Notifications include how many frames are to be rendered, current frame, percentage of completion and time estimate for completion

If you are having problems rendering even one frame you can set the first and the last frame to be the one you need rendered.

Disabling the Notification check will enable output to console.
Its not possible to interrupt the render process and thats why it saves the blender file before starting(option), if you want to interrupt the process you will have to force close blender.

>**IMPORTANT NOTICE FOR MAC:**

Installing the addon on mac should be done manually as the decompression method from blender destroys a binary necessary for notification.
you can install the addon like this:
uncompress both folders ( animationrender and modules )
place them on:
/Users/"YOUR USERNAME"/Library/Application Support/Blender/"YOUR BLENDER VERSION"/scripts/addons/

>**IMPORTANT NOTICE FOR LINUX:**

Restart blender after activation module or notifications will not work until restart


***Screenshot MAC***

![](https://raw.githubusercontent.com/thebadking/animationrender/master/screenshots/screenshot_macOS.png)
