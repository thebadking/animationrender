import os, bpy, datetime, time, pickle, string, random
from pathlib import Path
from animationrender.render import RenderProcess
global basePath
def getBasePath():
    global basePath
    basePath = bpy.context.preferences.addons['animationrender'].preferences.directoryQueue


def ShowMessageBox(message = "", title = "Info:", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def listFiles():
    getBasePath()
    global files
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(basePath):
        for file in f:
            if '.blend' in file:
                files.append(os.path.join(r, file))
    totalJobs = 0
    global fileTime
    fileTime = []
    for f in files:
        time = os.path.getmtime(f)
        totalJobs = totalJobs + 1
        fileTime.append(time)
    global indexMin
    if len(fileTime) > 0:
        indexMin = min(range(len(fileTime)), key=fileTime.__getitem__)


def addManager():
    getBasePath()
    os.makedirs(os.path.dirname(basePath + "data"), exist_ok=True)
    getBase = bpy.data.filepath
    currentFile = (os.path.basename(getBase))
    print('Current File: ' + currentFile)
    #now = str(time.time())
    rndm = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    stampedFile = rndm + '-' + currentFile
    destFile = basePath + stampedFile
    try:
        print(destFile)
        bpy.ops.wm.save_as_mainfile(filepath=destFile, check_existing=True, copy=True)
        f = open(basePath + "data", 'ab+')
        pickle.dump(destFile, f)
        f.close()
    except RuntimeError:
        ShowMessageBox("Go to animationrender settings and create/select folder for storing queue files using the folder button", "Folder missing:")
    f = open(basePath + "data", 'rb')
    print(f.readlines())
    f.close()


def arrQueue():
    newindex=1
    oldindex=3
    list.insert(newindex, list.pop(oldindex))

def startManager():
    listFiles()
    if len(fileTime) > 0:
        getBasePath()
        if Path(basePath + 'running').is_file():
            ShowMessageBox("This queue is already running!", "Warning:")
        else:
            print ("Manager Starting")
            f= open(basePath + 'running', "w+")
            f.close()
            print ("Locked and ready to render")
            listFiles()
            file=files[indexMin]
            while len(files) > 0:
                listFiles()
                file=files[indexMin]
                bpy.ops.wm.open_mainfile(filepath=file, use_scripts=True)
                RenderProcess()
                if Path(basePath + 'running').is_file():
                    print("Job complete:" + file)
                    Current_Date = datetime.datetime.today().strftime ('%d-%b-%Y')
                    Current_Date = "." + str(Current_Date)
                    finished = file[:-6] + Current_Date + '.finished'
                    os.rename(file, finished)
                    listFiles()
                else:
                    break
            else:
                stopManager()
                print("Nothing to do")
                return {"FINISHED"}
    else:
        ShowMessageBox("There are no Jobs in the queue", "Warning:")
        

def stopManager():
    getBasePath()
    os.remove(basePath + 'running')

def clearFinished():
    getBasePath()
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(basePath):
        for file in f:
            if '.finished' in file:
                files.append(os.path.join(r, file))
    for f in files:
        os.remove(f)







