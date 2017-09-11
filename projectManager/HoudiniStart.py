#!/usr/bin/python

import subprocess
import sys
import os

# Get variables
projectName = "chernobyl"
episodeName = "ep02"
shotName    = "ep02-" + sys.argv[1]
jobName     = "lighting"




# project structure: OLD
oldProjects = ["SKIF", "IKARIA", "SALUT"]
newProjects = ["chernobyl"]

if(projectName in oldProjects):
    # Generate variables
    PRJ = os.path.join("/projects", projectName)

    HOUDINI_OTLSCAN_PATH = '/prefs/houdini/LIGHTING_PREFS/otls:/projects/'+projectName+'/3D/OTL:&'
    RAT = os.path.join(PRJ, "3D", "DATA", "RAT")
    RSTEX = os.path.join(PRJ, "3D", "DATA", "RSTEX")
    LIGHTING = os.path.join(PRJ, "3D", "LIGHTING", episodeName, shotName)
    FX = os.path.join(PRJ, "3D", "FX", episodeName, shotName)
    ANIMATION = os.path.join(PRJ, "3D", "DATA", episodeName, shotName, "ANIMATION")
    FXCACHE = os.path.join(PRJ, "3D", "DATA", episodeName, shotName, "FX")
    RENDER = os.path.join(PRJ, "SRC", "RENDER", episodeName, shotName, jobName)
    TRACKING = os.path.join(PRJ, "3D", "TRACKING", episodeName, shotName)

    print "PRJ:                  " + PRJ
    print "HOUDINI_OTLSCAN_PATH: " + HOUDINI_OTLSCAN_PATH
    print "RAT:                  " + RAT
    print "RSTEX:                " + RSTEX
    print "LIGHTING:             " + LIGHTING
    print "FX:                   " + FX
    print "ANIMATION:            " + ANIMATION
    print "FXCACHE:              " + FXCACHE
    print "RENDER:               " + RENDER
    print "TRACKING:             " + TRACKING


    # Set Variables
    os.environ["PRJ"] = PRJ
    os.environ["HOUDINI_OTLSCAN_PATH"] = HOUDINI_OTLSCAN_PATH
    os.environ["RAT"] = RAT
    os.environ["RSTEX"] = RSTEX
    os.environ["LIGHTING"] = LIGHTING
    os.environ["FX"] = FX
    os.environ["ANIMATION"] = ANIMATION
    os.environ["FXCACHE"] = FXCACHE
    os.environ["RENDER"] = RENDER

    # Redshift variables
    os.environ["REDSHIFT_COREDATAPATH"] = "/opt/redshift"
    os.environ["HOUDINI_DSO_ERROR"] = "2"
    os.environ["PATH"] = "/opt/redshift/bin:$PATH"
    os.environ["HOUDINI_PATH"] = "/opt/redshift/redshift4houdini/16.0.534:&"

    houdiniProcess = subprocess.Popen("/opt/hfs16.0.539/bin/houdinifx", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=1)
    with houdiniProcess.stdout:
        for line in iter(houdiniProcess.stdout.readline, b''):
            sys.stdout.write(line)
    houdiniProcess.wait()

if(projectName in newProjects):
    # Generate variables
    PRJ = os.path.join("/fd/projects", projectName)

    HOUDINI_OTLSCAN_PATH = '/prefs/houdini/LIGHTING_PREFS/otls:' + '/fd/projects/chernobyl/lib/houdini/otls:&'
    RAT = os.path.join(PRJ, "episodes", episodeName, shotName, "data", "tex")
    RSTEX = os.path.join(PRJ, "episodes", episodeName, shotName, "data", "tex")
    LIGHTING = os.path.join(PRJ, "episodes", episodeName, shotName, "scenes", "lighting")
    FX = os.path.join(PRJ, "episodes", episodeName, shotName, "scenes", "fx")
    ANIMATION = os.path.join(PRJ, "episodes", episodeName, shotName, "scenes", "animation")
    CACHE = os.path.join(PRJ, "episodes", episodeName, shotName, "data", "cache")
    FXCACHE = os.path.join(PRJ, "3D", "DATA", episodeName, shotName, "FX")
    RENDER = os.path.join(PRJ, "episodes", episodeName, shotName, "render", jobName)
    TRACKING = os.path.join(PRJ, "3D", "TRACKING", episodeName, shotName)
    ASSETS = "/fd/projects/chernobyl/assets/"

    print "PRJ:                  " + PRJ
    print "HOUDINI_OTLSCAN_PATH: " + HOUDINI_OTLSCAN_PATH
    print "RAT:                  " + RAT
    print "RSTEX:                " + RSTEX
    print "LIGHTING:             " + LIGHTING
    print "FX:                   " + FX
    print "ANIMATION:            " + ANIMATION
    print "CACHE:                " + CACHE
    print "ASSETS:               " + ASSETS
    print "RENDER:               " + RENDER
    print "TRACKING:             " + TRACKING


    # Set Variables
    os.environ["PRJ"] = PRJ
    os.environ["HOUDINI_OTLSCAN_PATH"] = HOUDINI_OTLSCAN_PATH
    os.environ["RAT"] = RAT
    os.environ["RSTEX"] = RSTEX
    os.environ["LIGHTING"] = LIGHTING
    os.environ["FX"] = FX
    os.environ["ANIMATION"] = ANIMATION
    os.environ["FXCACHE"] = FXCACHE
    os.environ["CACHE"] = CACHE
    os.environ["ASSETS"] = ASSETS
    os.environ["RENDER"] = RENDER

    # Redshift variables
    os.environ["REDSHIFT_COREDATAPATH"] = "/opt/redshift"
    os.environ["HOUDINI_DSO_ERROR"] = "2"
    os.environ["PATH"] = "/opt/redshift/bin:$PATH"
    os.environ["HOUDINI_PATH"] = "/opt/redshift/redshift4houdini/16.0.534:&"

    houdiniProcess = subprocess.Popen("/software/hfs/16.0.671/bin/houdinifx", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=1)
    with houdiniProcess.stdout:
        for line in iter(houdiniProcess.stdout.readline, b''):
            sys.stdout.write(line)
    houdiniProcess.wait()


raw_input("Houdini Was Closed")







