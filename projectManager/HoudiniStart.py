#!/usr/bin/python

import subprocess
import sys
import os

# Get variables
projectName = sys.argv[1]
episodeName = sys.argv[2]
shotName    = sys.argv[3]
jobName     = sys.argv[4]

# project structure: OLD
oldProjects = ["SKIF", "IKARIA", "SALUT"]
newProjects = ["chernobyl"]

if(projectName in newProjects):
    # Generate variables
    # PRJ project root path
    PRJ = os.path.join("/fd/projects", projectName)
    # OTL scan path
    HOUDINI_OTLSCAN_PATH = '/fd/lib/houdini/otls:' + PRJ + '/lib/houdini/otls:&'
    # JOB  path to current shot root
    JOB = os.path.join(PRJ, "episodes", episodeName, shotName)
    SHOT = JOB
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


    print "HOUDINI_OTLSCAN_PATH: " + HOUDINI_OTLSCAN_PATH
    print "PRJ:                  " + PRJ
    print "JOB:                  " + JOB
    print "SHOT:                 " + SHOT
    print "SCENES:               " + SCENES
    print "RENDER:               " + RENDER
    print "DATA:                 " + DATA
    print "CACHE:                " + CACHE
    print "ANIMCACHE:            " + ANIMCACHE
    print "FXCACHE:              " + FXCACHE
    print "CAMERA:               " + CAMERA
    print "TEX:                  " + TEX
    print "ASSETS:               " + ASSETS


    # Set Variables
    os.environ["HOUDINI_OTLSCAN_PATH"] = HOUDINI_OTLSCAN_PATH
    os.environ["PRJ"] = PRJ
    os.environ["JOB"] = JOB
    os.environ["SHOT"] = SHOT
    os.environ["SCENES"] = SCENES
    os.environ["RENDER"] = RENDER
    os.environ["DATA"] = DATA
    os.environ["CACHE"] = CACHE
    os.environ["ANIMCACHE"] = ANIMCACHE
    os.environ["FXCACHE"] = FXCACHE
    os.environ["CAMERA"] = CAMERA
    os.environ["TEX"] = TEX
    os.environ["ASSETS"] = ASSETS


    # Redshift variables
    os.environ["REDSHIFT_COREDATAPATH"] = "/opt/redshift"
    os.environ["HOUDINI_DSO_ERROR"] = "2"
    originalPath = os.environ["PATH"]
    os.environ["PATH"] = originalPath + ":/opt/redshift/bin"
    os.environ["HOUDINI_PATH"] = "/opt/redshift/redshift4houdini/16.0.633:&"

    houdiniProcess = subprocess.Popen("/opt/hfs16.0.671/bin/houdinifx", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=1)
    with houdiniProcess.stdout:
        for line in iter(houdiniProcess.stdout.readline, b''):
            sys.stdout.write(line)
    houdiniProcess.wait()


raw_input("Houdini Was Closed")







