***Blender Animation Render Manager Queue V2.0***
Now added a queue manager

On Plugin settings you have the output folder for the queued files (default: /tmp/queue/)

On the output separator you have the Manager buttons.

Adding to the manager will make a copy of the current state of the Blender file you are edditing with all the context settings.
So you can queue multiple times the same file by chosing the diferent camera angle value it will create a folder with that camera angle together with the project name, so you have the output images organized and separated, chosing none on the camera angle will output the files to a folder with the name of the project only. All this outputs are inside the output location defined in "Output" in the context, dont forget to define it before adding to queue.

IMPORTANT
when pressing "RENDER QUEUE" it will start rendering the jobs and you won't be able to use that instance of Blender,
I advice for you to open another instance of blender to start the Render Process, and you can continue working on the other instance.

You can stop the rendering process from any Blender instance that is not rendering

At the moment you can only use one machine to render the queue, I will be adding the option to render the same queue with several machines, and after that a manager accessible from a webpage so you can see the progress from your phone or any device connected to the internet.

***Process that bypasses GUI to avoid crashes***

Tested on macOS, Windows and Linux. Blender 2.83

Animation render Manager is an addon for blender, it renders by python script bypassing the GUI, avoiding all the crashes that are GUI related while rendering. It works for cycles and eevee. It allows you to render an interval of frames grabing the details from context like first frame and last frame, output path and all the details required for rendering, it adds some buttons on the Output menu like:
- Enable notifications (OS notifications since Blender GUI is frozen while processing)
- Save file before Rendering
- Sound per frame and/or sound at completion (for macOS only) for windows and linux there is allways a system sound associated, mute it or unmute as necessary
- Queue manager buttons

Notifications include how many frames are to be rendered, current frame, percentage of completion and time estimate for completion

Disabling the Notification check will enable output to console.

>USE ONLY TO RENDER TO SEQUENCIAL IMAGE FILES
It will not work if you try to output directly to a video file.

>**IMPORTANT NOTICE FOR macOS:**

Installing the addon on macOS should be done manually as the decompression method from blender destroys a binary necessary for notification.
you can install the addon like this:
uncompress both folders ( animationrender and modules )
place them on:
/Users/"YOUR USERNAME"/Library/Application Support/Blender/"YOUR BLENDER VERSION"/scripts/addons/

>**IMPORTANT NOTICE FOR LINUX:**

Restart blender after activation of the add-on or notifications will not work until restart

***Screenshot***

![](https://raw.githubusercontent.com/thebadking/animationrender/master/screenshots/Animation_render_manager.png)

