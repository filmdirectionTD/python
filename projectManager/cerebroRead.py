import os
import sys
sys.path.append('/fd/lib/python/cerebroServiceTools')

from py_cerebro2 import database
import filters
#import shutil

#---------------------------------FUNCTIONDS-----------------------------------
# Create folder but check it first
def CreateProjectFolder(path):
    # first check if folder exists
    folderCheck = os.path.isdir(path)
    if(folderCheck):
        print path + " ... Already Exists"
    else:
        os.mkdir(path)
        print path + " ... Created"

# Get list of Project names
def GetRootProjects(cerebroDataBase):
    # Get rootTasks Table
    rootProjectsTask = cerebroDataBase.root_tasks()
    # Convert it to projects list;
    projectsList = []
    for task in rootProjectsTask:

        # Ignore finished projects:
        if(int(task[12]) == 100):
            continue
        else:
            # Check if projects has scenes in it
            scenesCHCK = cerebroDataBase.task_by_url(("/" + task[4] + "/episodes"))
            if(scenesCHCK[0] == None):
                continue
            else:
                projectsList.append(task[4])

    return projectsList


# Get project Assets
def GetRootAssets(project, cerebroDataBase):
    # Get project taskID
    assetsID = cerebroDataBase.task_by_url("/"+ project + "/assets")
    childrenTable = cerebroDataBase.task_children(assetsID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList


def GetEpisodes(project, cerebroDataBase):
    scenesID = cerebroDataBase.task_by_url("/"+ project + "/episodes")
    childrenTable = cerebroDataBase.task_children(scenesID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList


def GetShots(project, episode, cerebroDataBase):
    shotsID = cerebroDataBase.task_by_url("/"+ project + "/episodes/" + episode)
    childrenTable = cerebroDataBase.task_children(shotsID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList


def GetRootShots(project, cerebroDataBase):
    shotsID = cerebroDataBase.task_by_url("/"+ project + "/SCENES")
    childrenTable = cerebroDataBase.task_children(shotsID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList


def GetJobs(project, episode, shot, cerebroDataBase):
    jobsID = cerebroDataBase.task_by_url("/"+ project + "/episodes/" + episode + "/" + shot)
    childrenTable = cerebroDataBase.task_children(jobsID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList


def GetJobsFromRoot(project, shot, cerebroDataBase):
    jobsID = cerebroDataBase.task_by_url("/"+ project + "/SCENES/" + shot)
    childrenTable = cerebroDataBase.task_children(jobsID[0])
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])
    return childrenList



def RenderProjectTree(project, cerebroDataBase):
    print("/" + project)
    scenes = GetEpisodes(project, cerebroDataBase)
    for scene in scenes:
        print("    " + scene)
        shots = GetShots(project, scene, cerebroDataBase)
        for shot in shots:
            print("        " + shot)
            jobs = GetJobs(project, scene, shot, cerebroDataBase)
            for job in jobs:
                print("            " + job)



def CheckIfTaskIsShot(taskID, cerebroDataBase):

    # Get all children
    childrenTable = cerebroDataBase.task_children(taskID)
    # Get list of children names
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])

    # Check if some of children tasks in jobs
    for taskName in childrenList:
        if(filters.CheckIfJob(taskName)):
            return True


def CheckIfTaskIsAsset(taskID, cerebroDataBase):

    # Get all children
    childrenTable = cerebroDataBase.task_children(taskID)
    # Get list of children names
    childrenList = []
    for task in childrenTable:
        childrenList.append(task[4])

    # Check if some of children tasks in jobs
    for taskName in childrenList:
        if(filters.CheckIfAssetJob(taskName)):
            return True


# --------------------------- PROJECT CLASS --------------------------------

class CrAsset():
    def __init__(self):
        self.name = ""
        self.taskID = 0
        self.fullURL = ""


class CrShot():
    def __init__(self):
        self.name = ""
        self.taskID = 0
        self.fullURL = ""
        self.jobs = []

    def Clear(self):
        self.jobs[:] = []



class CrEpisode():
    def __init__(self):
        self.name = ""
        self.taskID = 0
        self.fullURL = ""
        self.shots = []

    def LoadShots(self, project, cerebroDatabase):
        shotsList = GetShots(project, self.name, cerebroDatabase)
        filteredShotsList = filters.FilterShots(shotsList)
        filteredShotsList.sort()

        for shot in filteredShotsList:
            # Create shot Object
            shotObj = CrShot()
            # Name
            shotObj.name = shot
            # URL
            shotObj.fullURL = self.fullURL + "/" + shot
            # ID
            shotObj.taskID = cerebroDatabase.task_by_url(shotObj.fullURL)[0]
            # Jobs
            shotObj.jobs = GetJobs(project, self.name, shot, cerebroDatabase)


            self.shots.append(shotObj)
            print "   " + shot

    def Clear(self):
        # Clear shots
        for shot in self.shots:
            shot.Clear()

        self.shots[:] = []



class CrProject():
    def __init__(self):
        self.name = ""
        self.taskID = 0
        self.fullURL = ""
        self.episodes = []
        self.assets = []
        print "Project initialized"


    def LoadScenes(self, cerebroDatabase):
        print "LOADING SCENES:  ...  --------------->"
        episodesList = GetEpisodes(self.name, cerebroDatabase)
        filteredEpisodesList = filters.FilterScenes(episodesList)
        filteredEpisodesList.sort()

        for episode in filteredEpisodesList:
            print episode
            # Create scene object:
            episodeObj = CrEpisode()
            # Name
            episodeObj.name = episode
            # Full URL
            episodeObj.fullURL = "/" + self.name + "/episodes/" + episode
            # ID
            episodeTaskID = cerebroDatabase.task_by_url(episodeObj.fullURL)[0]
            episodeObj.taskID = episodeTaskID
            # Load shots for current episode
            episodeObj.LoadShots(self.name, cerebroDatabase)

            self.episodes.append(episodeObj)

    def LoadAssets(self, cerebroDatabase):
        print "LOADING ASSETS: ...  --------------->"

        assetsList = GetRootAssets(self.name, cerebroDatabase)
        assetsList.sort()

        for asset in assetsList:
            assetObj = CrAsset()
            assetObj.name = asset
            assetObj.fullURL = "/" + self.name + "/assets/" + asset
            assetObj.taskID = cerebroDatabase.task_by_url(assetObj.fullURL)[0]

            self.assets.append(assetObj)

            print "    " + asset

    def CreateFolderStrusture(self):
        print "CREATING FOLDER STRUCTURE FOR " + self.name

        basePath = "/projects/fd/projects"

        # 1. Root Project folder
        rootPath = os.path.join(basePath, self.name.lower()) # LOWER USED !!!!!!!!!! TODO
        CreateProjectFolder(rootPath)

        # 2. Root Folders
        docsPath = os.path.join(rootPath, "docs")
        CreateProjectFolder(docsPath)
        editPath = os.path.join(rootPath, "editorial")
        CreateProjectFolder(editPath)
        inPath = os.path.join(rootPath, "in")
        CreateProjectFolder(inPath)
        outPath = os.path.join(rootPath, "out")
        CreateProjectFolder(outPath)
        tmpPath = os.path.join(rootPath, "tmp")
        CreateProjectFolder(tmpPath)
        referencePath = os.path.join(rootPath, "reference")
        CreateProjectFolder(referencePath)

        # Lib - for project related otls icons scripts etc
        libPath = os.path.join(rootPath, "lib")
        CreateProjectFolder(libPath)
        houdiniLibPath = os.path.join(libPath, "houdini")
        CreateProjectFolder(houdiniLibPath)
        nukeLibPath = os.path.join(libPath, "nuke")
        CreateProjectFolder(nukeLibPath)

        otlLibPath = os.path.join(houdiniLibPath, "otl")
        CreateProjectFolder(otlLibPath)
        hScriptsLibPath = os.path.join(houdiniLibPath, "scripts")
        CreateProjectFolder(hScriptsLibPath)

        # 3. Episodes structure
        # Episodes Root
        episodesRootPath = os.path.join(rootPath, "episodes")
        CreateProjectFolder(episodesRootPath)

        for episode in self.episodes:
            # Episode folder
            episodePath = os.path.join(episodesRootPath, episode.name)
            CreateProjectFolder(episodePath)

            for shot in episode.shots:
                # Shot folder
                shotPath = os.path.join(episodePath, shot.name)
                CreateProjectFolder(shotPath)

                # Shot Root Folders
                dataPath = os.path.join(shotPath, "data")
                CreateProjectFolder(dataPath)
                hiresPath = os.path.join(shotPath, "hires")
                CreateProjectFolder(hiresPath)
                renderPath = os.path.join(shotPath, "render")
                CreateProjectFolder(renderPath)
                scansPath = os.path.join(shotPath, "scans")
                CreateProjectFolder(scansPath)
                scenesPath = os.path.join(shotPath, "scenes")
                CreateProjectFolder(scenesPath)

                # Data Folders
                cachePath = os.path.join(dataPath, "cache")
                CreateProjectFolder(cachePath)

                animationCachePath = os.path.join(cachePath, "animation")
                CreateProjectFolder(animationCachePath)
                compCachePath = os.path.join(cachePath, "comp")
                CreateProjectFolder(compCachePath)
                fxCachePath = os.path.join(cachePath, "fx")
                CreateProjectFolder(fxCachePath)
                layoutCachePath = os.path.join(cachePath, "layout")
                CreateProjectFolder(layoutCachePath)
                lightingCachePath = os.path.join(cachePath, "lighting")
                CreateProjectFolder(lightingCachePath)
                previsCachePath = os.path.join(cachePath, "previs")
                CreateProjectFolder(previsCachePath)
                trackingCachePath = os.path.join(cachePath, "tracking")
                CreateProjectFolder(trackingCachePath)

                # Tex
                texDatapath = os.path.join(dataPath, "tex")
                CreateProjectFolder(texDatapath)

                # Render folders
                animationRenderPath = os.path.join(renderPath, "animation")
                CreateProjectFolder(animationRenderPath)
                compRenderPath = os.path.join(renderPath, "comp")
                CreateProjectFolder(compRenderPath)
                fxRenderPath = os.path.join(renderPath, "fx")
                CreateProjectFolder(fxRenderPath)
                layoutRenderPath = os.path.join(renderPath, "layout")
                CreateProjectFolder(layoutRenderPath)
                lightingRenderPath = os.path.join(renderPath, "lighting")
                CreateProjectFolder(lightingRenderPath)
                previsRenderPath = os.path.join(renderPath, "previs")
                CreateProjectFolder(previsRenderPath)
                trackingRenderPath = os.path.join(renderPath, "tracking")
                CreateProjectFolder(trackingRenderPath)

                # Scenes Folder
                animationScenesPath = os.path.join(scenesPath, "animation")
                CreateProjectFolder(animationScenesPath)
                compScenesPath = os.path.join(scenesPath, "comp")
                CreateProjectFolder(compScenesPath)
                fxScenesPath = os.path.join(scenesPath, "fx")
                CreateProjectFolder(fxScenesPath)
                layoutScenesPath = os.path.join(scenesPath, "layout")
                CreateProjectFolder(layoutScenesPath)
                lightingScenesPath = os.path.join(scenesPath, "lighting")
                CreateProjectFolder(lightingScenesPath)
                previsScenesPath = os.path.join(scenesPath, "previs")
                CreateProjectFolder(previsScenesPath)
                trackingScenesPath = os.path.join(scenesPath, "tracking")
                CreateProjectFolder(trackingScenesPath)

        # 4. Assets Structure
        assetsRootPath = os.path.join(rootPath, "assets")
        CreateProjectFolder(assetsRootPath)

        for asset in self.assets:
            assetPath = os.path.join(assetsRootPath, asset.name)
            CreateProjectFolder(assetPath)

            # Asset Root folders
            dataAssetPath = os.path.join(assetPath, "data")
            CreateProjectFolder(dataAssetPath)
            referenceAssetPath = os.path.join(assetPath, "reference")
            CreateProjectFolder(referenceAssetPath)
            renderAssetPath = os.path.join(assetPath, "render")
            CreateProjectFolder(renderAssetPath)
            scenesAssetPath = os.path.join(assetPath, "scenes")
            CreateProjectFolder(scenesAssetPath)


            # Data paths
            cacheAssetPath = os.path.join(dataAssetPath, "cache")
            CreateProjectFolder(cacheAssetPath)
            texAssetPath = os.path.join(dataAssetPath, "tex")
            CreateProjectFolder(texAssetPath)

            conceptCachePath = os.path.join(cacheAssetPath, "concept")
            CreateProjectFolder(conceptCachePath)
            hairCachePath = os.path.join(cacheAssetPath, "hair")
            CreateProjectFolder(hairCachePath)
            modelingCachePath = os.path.join(cacheAssetPath, "modeling")
            CreateProjectFolder(modelingCachePath)
            riggingCachePath = os.path.join(cacheAssetPath, "rigging")
            CreateProjectFolder(riggingCachePath)
            shadingCachePath = os.path.join(cacheAssetPath, "shading")
            CreateProjectFolder(shadingCachePath)
            texturingCachePath = os.path.join(cacheAssetPath, "texturing")
            CreateProjectFolder(texturingCachePath)

            # Render Paths
            conceptRenderPath = os.path.join(renderAssetPath, "concept")
            CreateProjectFolder(conceptRenderPath)
            hairRenderPath = os.path.join(renderAssetPath, "hair")
            CreateProjectFolder(hairRenderPath)
            modelingRenderPath = os.path.join(renderAssetPath, "modeling")
            CreateProjectFolder(modelingRenderPath)
            riggingRenderPath = os.path.join(renderAssetPath, "rigging")
            CreateProjectFolder(riggingRenderPath)
            shadingRenderPath = os.path.join(renderAssetPath, "shading")
            CreateProjectFolder(shadingRenderPath)
            texturingRenderPath = os.path.join(renderAssetPath, "texturing")
            CreateProjectFolder(texturingRenderPath)

            # Scenes Paths
            conceptScenesPath = os.path.join(scenesAssetPath, "concept")
            CreateProjectFolder(conceptScenesPath)
            hairScenesPath = os.path.join(scenesAssetPath, "hair")
            CreateProjectFolder(hairScenesPath)
            modelingScenesPath = os.path.join(scenesAssetPath, "modeling")
            CreateProjectFolder(modelingScenesPath)
            riggingScenesPath = os.path.join(scenesAssetPath, "rigging")
            CreateProjectFolder(riggingScenesPath)
            shadingScenesPath = os.path.join(scenesAssetPath, "shading")
            CreateProjectFolder(shadingScenesPath)
            texturingScenesPath = os.path.join(scenesAssetPath, "texturing")
            CreateProjectFolder(texturingScenesPath)




    def Clear(self):
        # Clear all episodes
        for episode in self.episodes:
            episode.Clear()

        self.assets[:] = []
        self.episodes[:] = []






































