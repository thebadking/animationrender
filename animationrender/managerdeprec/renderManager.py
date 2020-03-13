import os
import bpy
from pathlib import Path
from shutil import copyfile
import animationrender.render
import time
import sys
import datetime
#queue = "\\Queue\\"
#basePath = sys.path[5]
#basePath = str(basePath)
#basePath = basePath + queue
global basePath
basePath = "\\Queue\\"

def listFiles():
    global files
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(basePath):
        for file in f:
            if '.blend' in file:
                files.append(os.path.join(r, file))
    global total
    total = 0
    global fileTime
    fileTime = []
    for f in files:
        time = os.path.getmtime(f)
        total = total + 1
        #print(f)
        #print(time)
        fileTime.append(time)
    global indexMin
    if total > 0:
        indexMin = min(range(len(fileTime)), key=fileTime.__getitem__)

def addManager():
    getBase = bpy.data.filepath
    currentFile = (os.path.basename(getBase))
    print('Current File: ' + currentFile)
    now = time.time()
    now = str(now)
    stampedFile = now + '-' + currentFile
    file = basePath + stampedFile
    bpy.ops.wm.save_as_mainfile(filepath=file, check_existing=True, copy=True)


def openFile(path):
    bpy.ops.wm.open_mainfile(filepath = path, load_ui=False)


def render(file):
    command = "cd / | blender -b "+ file + " -P " + basePath + "init.py"
    os.system(command)
    print("render complete:" + file)
    Current_Date = datetime.datetime.today().strftime ('%d-%b-%Y')
    Current_Date = "." + str(Current_Date)
    finished = file[:-6] + Current_Date + '.finished'
    os.rename(file, finished)
    print("job finished")

def checkQueueStart():
    if Path(basePath + 'trigger').is_file():
        listFiles()
        print ("LETS GO")
        os.remove(basePath + 'trigger')
        while total > 0:
            render(files[indexMin])
            listFiles()
        else:
            stopManager()


def startManager():    
    if Path(basePath + 'running').is_file():
        print ("Manager Already Running")
    else:
        print ("Manager Starting")
        f= open(basePath + 'running',"w+")
        f.close()
        t= open(basePath + 'trigger',"w+")
        t.close()
        print ("Locked and ready to render")
        
        
        
def stopManager():
    os.remove(basePath + 'running')

def clearFinished():
    path = basePath
    global files
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.finished' in file:
                files.append(os.path.join(r, file))
    for f in files:
        os.remove(f)