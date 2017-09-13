#!/usr/bin/python
import subprocess

import sys
import os

# Get variables from gui
# projectName = sys.argv[1]
# episodeName = sys.argv[2]
# shotName    = sys.argv[3]
# jobName     = sys.argv[4]

projectName = "chernobyl"
episodeName = "ep02"
shotName    = "ep02-0010"
jobName     = "animation"

# Project management variables
# PRJ project root path
PRJ = os.path.join("/fd/projects", projectName)
# JOB  path to current shot root
JOB = os.path.join(PRJ, "episodes", episodeName, shotName)
# SCENES path to current folder for scenes
SCENES = os.path.join(JOB, "scenes")

# RENDER folder for renders dependent on jobname
RENDER = ""
if(jobName == "animation"):
    RENDER = os.path.join(JOB, "render", "animation")
elif(jobName == "fx"):
    RENDER = os.path.join(JOB, "render", "fx")
elif (jobName == "layout"):
    RENDER = os.path.join(JOB, "render", "layout")
elif (jobName == "lighting"):
    RENDER = os.path.join(JOB, "render", "lighting")
elif (jobName == "previs"):
    RENDER = os.path.join(JOB, "render", "previs")
elif (jobName == "tracking"):
    RENDER = os.path.join(JOB, "render", "tracking")

# DATA path to data folders
DATA = os.path.join(JOB, "data")
CACHE = os.path.join(DATA, "cache")
ANIMCACHE = os.path.join(CACHE, "animation")
FXCACHE = os.path.join(CACHE, "fx")
CAMERA = os.path.join(CACHE, "tracking")
TEX = os.path.join(DATA, "tex")

ASSETS = os.path.join(PRJ, "assets")

# Maya setup related variables
FDBIN = "/fd/lib/maya"

MAYA_SCRIPT_PATH = os.path.join(FDBIN, "mel")
PYTHONPATH = os.path.join(FDBIN, "python")
XBMLANGPATH = "/fd/lib/icons/%B"
MAYA_DISABLE_CIP = "1"


print 'PRJ:               ' + PRJ
print 'JOB:               ' + JOB
print 'SCENES:            ' + SCENES
print 'RENDER:            ' + RENDER
print 'DATA:              ' + DATA
print 'CACHE:             ' + CACHE
print 'ANIMCACHE:         ' + ANIMCACHE
print 'FXCACHE:           ' + FXCACHE
print 'CAMERA:            ' + CAMERA
print 'TEX:               ' + TEX
print 'ASSETS:            ' + ASSETS

print 'MAYA_SCRIPT_PATH:  ' + ASSETS
print 'PYTHONPATH:        ' + PYTHONPATH
print 'XBMLANGPATH:       ' + XBMLANGPATH
print 'MAYA_DISABLE_CIP:  ' + MAYA_DISABLE_CIP


# INITIALIZE VARIABLES

os.environ["PRJ"] = PRJ
os.environ["JOB"] = JOB
os.environ["SCENES"] = SCENES
os.environ["RENDER"] = RENDER
os.environ["DATA"] = DATA
os.environ["CACHE"] = CACHE
os.environ["ANIMCACHE"] = ANIMCACHE
os.environ["FXCACHE"] = FXCACHE
os.environ["CAMERA"] = CAMERA
os.environ["TEX"] = TEX
os.environ["ASSETS"] = ASSETS

os.environ["MAYA_SCRIPT_PATH"] = os.path.join(FDBIN, "mel")
os.environ["PYTHONPATH"] = os.path.join(FDBIN, "python")
os.environ["XBMLANGPATH"] = XBMLANGPATH
os.environ["MAYA_DISABLE_CIP"] = "1"




mayaProcess = subprocess.Popen(("maya -proj " + PRJ), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=1)
with mayaProcess.stdout:
    for line in iter(mayaProcess.stdout.readline, b''):
        sys.stdout.write(line)
mayaProcess.wait()

raw_input("Maya Was Closed")