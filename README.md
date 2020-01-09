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


Tested on macOS and Windows
