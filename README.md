# Blender Animation Render process that bypasses GUI to avoid crashes

Blender animation render addon (bypasses GUI and solves most crashes)

Animation render is an addon for blender 2.81, it renders by python bypassing the GUI and so solving all the crashes while rendering. It works for cycles and eevee. It allows you to render an interval of frames grabing the details from context like outputh path and all the details required for rendering, it adds some buttons on the Output menu like:

    Render Animation

    First frame

    Last frame

    Prefix for output files

    Enable notifications
    
    Sound per frame and/or sound at completion (for macOS only)

Notifications include how many frames are to be rendered, current frame, percentage of completion and time estimate for completion


Tested on macOS, Windows and Linux
Disabling the Notification check will enable output to console
Its not possible to interrupt the render process and thats why it saves the blender file before starting, if you want to interrupt the process you will have to force close blender.

IMPORTANT NOTICE FOR MAC:
installing the addon on mac should be done manually as the decomression method from blender destroys a binary necessary for notification.
you can install the addon like this:
uncompress both folders ( animationrender and modules )
place them on:
/Users/"YOUR USERNAME"/Library/Application Support/Blender/"YOUR BLENDER VERSION"/scripts/addons/

IMPORTANT NOTICE FOR LINUX:
Restart blender after activation modue or notifications won't work until restart
