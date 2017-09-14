#!/usr/bin/python
from PySide import QtCore, QtGui
import sys
import os

import cerebroRead
import filters

import subprocess

# --------------- Custom Line Edit Class -------------------------------------------------------------------------------

class FDLineEdit(QtGui.QLineEdit):
    def __init__(self, value):
        super(FDLineEdit, self).__init__(value)

    def mousePressEvent(self, QMouseEvent):
        self.emit(QtCore.SIGNAL("clicked()"))




# class FDLineEdit(QtGui.QLineEdit):
#     mousePressed = QtCore.Property(QtGui.QMouseEvent)
#
#     def __init__(self, value):
#         super(FDLineEdit, self).__init__(value)
#
#     def mousePressEvent(self, event):
#         #print 'forwarding to the main window'
#         self.mousePressed.emit(event)


# --------------- GUI class description --------------------------------------------------------------------------------

class FdstarterGUI (QtGui.QWidget):

    def __init__(self):
        super(FdstarterGUI, self).__init__()
        self.setupUI()

        host = 'fs.dkfx.lan'
        port = '5432'

        self.db = cerebroRead.database.Database(host, port)
        self.cerebroProject = cerebroRead.CrProject()
        self.model = QtGui.QStandardItemModel()

        self.filterUsed = False
        self.listShotsToFilter = []

        self.selectedProject = ""
        self.selectedEpisode = ""
        self.selectedShot = ""
        self.selectedJob = ""

        self.bgColors = ["NavajoWhite1", "LightSalmon1", "Grey93", "MistyRose1", "Cornsilk1", "Honeydew2", "LightSteelBlue1", "LightYellow3", "LightSkyBlue1", "SkyBlue1", "Wheat1", "DarkOliveGreen1", "LightCyan3", "White"]



    def setupUI(self):
        # Add UI Elements--------------------------------------
        # SCENES:
        # First Column:
        # Login
        labelUname = QtGui.QLabel("Username: ")
        labelPass  = QtGui.QLabel("Password: ")
        lineInputUname = QtGui.QLineEdit()
        lineInputUname.setAutoFillBackground(True)
        lineInputPass  = QtGui.QLineEdit()
        lineInputPass.setAutoFillBackground(True)
        self.buttonLogin    = QtGui.QPushButton("Login to Cerebro")
        iconLogin = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/login.png'))
        self.buttonLogin.setIcon(iconLogin)

        self.buttonStartHoudini = QtGui.QPushButton("Start Houdini")
        iconHoudini = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/houdini_logo.png'))
        self.buttonStartHoudini.setIcon(iconHoudini)

        self.buttonStartNuke = QtGui.QPushButton("Start Nuke")
        iconNuke = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/nukeIcon.png'))
        self.buttonStartNuke.setIcon(iconNuke)

        self.buttonStartMaya = QtGui.QPushButton("Start Maya")
        iconMaya = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/hsMaya.png'))
        self.buttonStartMaya.setIcon(iconMaya)


        hboxUname = QtGui.QHBoxLayout()
        hboxPass = QtGui.QHBoxLayout()

        loginColumnLayout = QtGui.QVBoxLayout()

        hboxUname.addWidget(labelUname, 0)
        hboxUname.addWidget(lineInputUname, 1)

        hboxPass.addWidget(labelPass, 0)
        hboxPass.addWidget(lineInputPass, 1)

        loginColumnLayout.addItem(hboxUname)
        loginColumnLayout.addItem(hboxPass)
        loginColumnLayout.addWidget(self.buttonLogin, 2)
        loginColumnLayout.addWidget(self.buttonStartHoudini, 3)
        loginColumnLayout.addWidget(self.buttonStartNuke, 4)
        loginColumnLayout.addWidget(self.buttonStartMaya, 5)

        loginColumnLayout.addStretch()

        self.iconGreen = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/GREEN_light.png'))
        self.iconRed = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/RED_light.png'))

        # Second column
        # Projects List

        labelProjects = QtGui.QLabel("Select a Project: ")
        self.listProjects  = QtGui.QListWidget()

        projectsColumnLayout = QtGui.QVBoxLayout()
        projectsColumnLayout.addWidget(labelProjects, 0)
        projectsColumnLayout.addWidget(self.listProjects, 1)

        # Third column
        # Episodes List
        labelEpisodes = QtGui.QLabel("Episodes: ")
        self.listEpisodes = QtGui.QListWidget()

        labelShots = QtGui.QLabel("Shots: ")

        self.lineInputShotFilter = FDLineEdit("")
        self.lineInputShotFilter.setText("type shot name ...")
        self.lineInputShotFilter.setFixedHeight(25)
        # Setup font
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.gray)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lineInputShotFilter.setPalette(palette)
        self.lineInputShotFilter.setFont(font)




        self.listShots = QtGui.QListWidget()
        labelJobs = QtGui.QLabel("Jobs: ")
        self.listJobs = QtGui.QListWidget()

        shotFilterlayout = QtGui.QHBoxLayout()
        shotFilterlayout.addWidget(labelShots, 0)
        shotFilterlayout.addWidget(self.lineInputShotFilter, 1)


        episodesColumnLayout = QtGui.QVBoxLayout()
        episodesColumnLayout.addWidget(labelEpisodes, 0)
        episodesColumnLayout.addWidget(self.listEpisodes, 1)
        episodesColumnLayout.setSpacing(8)

        shotsColumnLayout = QtGui.QVBoxLayout()
        shotsColumnLayout.addItem(shotFilterlayout)
        shotsColumnLayout.addWidget(self.listShots, 1)
        shotsColumnLayout.setSpacing(4)

        jobsColumnLayout = QtGui.QVBoxLayout()
        jobsColumnLayout.addWidget(labelJobs, 0)
        jobsColumnLayout.addWidget(self.listJobs, 1)
        jobsColumnLayout.setSpacing(8)

        episodesGlobalLayout = QtGui.QHBoxLayout()
        episodesGlobalLayout.addItem(episodesColumnLayout)
        episodesGlobalLayout.addItem(shotsColumnLayout)
        episodesGlobalLayout.addItem(jobsColumnLayout)

        # ASSETS
        # Assets tree view
        labelAssetsTree = QtGui.QLabel("Asset Tree:")
        self.assetsTreeView = QtGui.QTreeView()
        self.assetsTreeView.setUniformRowHeights(True)
        self.assetsTreeView.setAnimated(True)
        self.assetsTreeView.setUniformRowHeights(True)


        labelAssetJobsTree = QtGui.QLabel("Jobs List:")
        self.assetJobsList  = QtGui.QListWidget()

        assetTreeLayout = QtGui.QVBoxLayout()
        assetTreeLayout.addWidget(labelAssetsTree, 0)
        assetTreeLayout.addWidget(self.assetsTreeView, 1)

        assetJobsLayout = QtGui.QVBoxLayout()
        assetJobsLayout.addWidget(labelAssetJobsTree, 0)
        assetJobsLayout.addWidget(self.assetJobsList, 1)

        assetsGlobalLayout = QtGui.QHBoxLayout()
        assetsGlobalLayout.addItem(assetTreeLayout)
        assetsGlobalLayout.addItem(assetJobsLayout)

        # Tab Widget for Scenes And Assets
        assetEpisodeTabs = QtGui.QTabWidget()

        # Tab for scenes:
        episodesTab = QtGui.QWidget()
        episodesTab.setLayout(episodesGlobalLayout)
        episodesTab.setAutoFillBackground(True)

        # Tab for assets
        assetsTab = QtGui.QWidget()
        assetsTab.setLayout(assetsGlobalLayout)
        assetsTab.setAutoFillBackground(True)


        # Add tabs
        assetEpisodeTabs.addTab(episodesTab, "Episodes")
        assetEpisodeTabs.addTab(assetsTab, "Assets")

        # Global layout
        globalLayout = QtGui.QHBoxLayout()
        globalLayout.addItem(loginColumnLayout)
        globalLayout.addItem(projectsColumnLayout)
        globalLayout.addWidget(assetEpisodeTabs, 2)

        # StatusLayout
        self.statusBar = QtGui.QStatusBar()

        StatusLayout = QtGui.QVBoxLayout()
        StatusLayout.addItem(globalLayout)
        StatusLayout.addWidget(self.statusBar, 1)
        StatusLayout.setStretch(1, 0)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
        self.statusBar.setPalette(palette)

        self.statusBar.showMessage("Push Login to Cerebro/Get Projects List and Select Project from list ...")

        #Connect slot and widgets
        self.buttonLogin.clicked.connect(self.LoginToCerebro)

        self.listProjects.itemClicked.connect(self.ProjectClicked)
        self.listProjects.itemEntered.connect(self.ProjectClicked)
        #
        self.listEpisodes.itemClicked.connect(self.EpisodeClicked)
        self.listEpisodes.itemEntered.connect(self.EpisodeClicked)
        #
        self.listShots.itemClicked.connect(self.ShotClicked)
        self.listShots.itemEntered.connect(self.ShotClicked)
        #
        self.connect(self.lineInputShotFilter, QtCore.SIGNAL("clicked()"), self.ShotFilterClicked)
        self.lineInputShotFilter.textEdited.connect(self.FilterShots)
        #
        self.listJobs.itemClicked.connect(self.JobClicked)
        self.listJobs.itemEntered.connect(self.JobClicked)
        #
        self.assetsTreeView.clicked.connect(self.AssetClicked)
        self.assetsTreeView.entered.connect(self.AssetClicked)
        #
        self.assetJobsList.itemClicked.connect(self.AssetJobClicked)
        self.assetJobsList.itemEntered.connect(self.AssetJobClicked)

        #
        self.buttonStartHoudini.clicked.connect(self.StartHoudini)
        self.buttonStartMaya.clicked.connect(self.StartMaya)

        #general window setup---------------------------------

        self.setLayout(StatusLayout)
        self.setGeometry(900, 300, 1200, 600)
        self.setWindowTitle("FilmDirectionFX Software Starter")
        self.show()

    def LoginToCerebro(self):
        #login to cerebro with pass and login
        user = 'asknarin'
        password = 'evv250584'

        # clear list widgets adn assets tree widget
        self.listProjects.clear()
        self.listEpisodes.clear()
        self.listShots.clear()
        self.listJobs.clear()
        self.model.clear()

        # Clear list of selected item names
        self.selectedProject = ""
        self.selectedEpisode = ""
        self.selectedShot = ""
        self.selectedJob = ""

        # login
        if self.db.connect_from_cerebro_client() != 0:
            self.db.connect(user, password)

        projectsList = cerebroRead.GetRootProjects(self.db)

        filteredProjectsList = filters.FilterProjects(projectsList)
        filteredProjectsList.sort()

        for project in filteredProjectsList:
            self.listProjects.addItem(project)

        self.statusBar.showMessage("Select Project:")

    def ProjectClicked(self, item):
        # Clear
        self.listEpisodes.clear()
        self.listShots.clear()
        self.listJobs.clear()
        self.model.clear()
        self.assetJobsList.clear()

        self.selectedProject = ""
        self.selectedEpisode = ""
        self.selectedShot = ""
        self.selectedJob = ""


        # Get selected project
        self.selectedProject = item.text()

        # EPISODES
        # Fill episodes and sort them
        episodes = cerebroRead.GetEpisodes(self.selectedProject, self.db)
        episodes = filters.FilterScenes(episodes)
        episodes.sort()

        # Fill  List widget
        for episode in episodes:
            self.listEpisodes.addItem(episode)

        # ASSETS
        # Fill assets and sort them
        assets = cerebroRead.GetRootAssets(self.selectedProject, self.db)
        assets.sort()

        self.assetsTreeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.model.setHorizontalHeaderLabels(["Name", "Type", "URL"])
        self.assetsTreeView.setModel(self.model)
        self.assetsTreeView.setColumnWidth(0, 200)
        self.assetsTreeView.setColumnWidth(1, 130)
        self.assetJobsList.clear()

        for asset in assets:
            assetItemName = QtGui.QStandardItem(asset)
            assetItemType = QtGui.QStandardItem("Asset")
            assetItemURL = QtGui.QStandardItem(self.selectedProject + "/assets/" + asset)
            self.model.appendRow([assetItemName, assetItemType, assetItemURL])

        self.statusBar.showMessage("Select Episode or Asset:")

    def EpisodeClicked(self, item):
        # Clear
        self.listShots.clear()
        self.listJobs.clear()
        self.assetJobsList.clear()

        # Clear all asset selection
        self.assetsTreeView.clearSelection()
        self.assetJobsList.clearSelection()

        self.selectedEpisode = ""
        self.selectedShot = ""
        self.selectedJob = ""

        # Get Selected Episode
        self.selectedEpisode = item.text()

        # Fill shots and sort
        shots = cerebroRead.GetShots(self.selectedProject, self.selectedEpisode, self.db)
        shots = filters.FilterShots(shots)
        shots.sort()

        for shot in shots:
            self.listShots.addItem(shot)

        self.statusBar.showMessage("Select Shot:")

    def ShotClicked(self, item):
        # Clear
        self.listJobs.clear()
        self.assetJobsList.clear()

        # Clear all asset selection
        self.assetsTreeView.clearSelection()
        self.assetJobsList.clearSelection()

        self.selectedShot = ""

        # Get Selected shot
        self.selectedShot = item.text()

        # Fill jobs
        jobs = cerebroRead.GetJobs(self.selectedProject, self.selectedEpisode, self.selectedShot, self.db)
        #jobs = filters.FilterShotJobs(jobs)
        jobs.sort()

        for job in jobs:
            self.listJobs.addItem(job)
        self.statusBar.showMessage("Select Job:")

        self.selectedJob = ""


    def JobClicked(self, item):
        # Clear
        self.selectedJob = item.text()


    def AssetClicked(self, item):
        # Clear Selections
        self.listEpisodes.clearSelection()
        self.listShots.clearSelection()
        self.listJobs.clearSelection()

        # Clear lists
        self.listShots.clear()
        self.listJobs.clear()
        self.assetJobsList.clear()

        self.selectedShot = ""
        self.selectedJob = ""

        self.selectedEpisode = "assets"
        try:
            treeItem = self.model.itemFromIndex(item)
            self.selectedShot = treeItem.text()
        except IndexError:
            print ""

        # Fill Asset Jobs list
        assetJobs = cerebroRead.GetAssetJobs(self.selectedProject, self.selectedShot, self.db)
        assetJobs.sort()

        for job in assetJobs:
            self.assetJobsList.addItem(job)


    def AssetJobClicked(self, item):
        #Clear Selections
        self.listEpisodes.clearSelection()
        self.listShots.clearSelection()
        self.listJobs.clearSelection()

        # Clear lists
        self.listShots.clear()
        self.listJobs.clear()

        self.selectedJob = item.text()



    def StartHoudini(self):
        import random
        import time
        random.seed(int(time.time()))
        color = self.bgColors[random.randrange(len(self.bgColors))]

        # Check if project selected
        if (self.selectedProject != ""):
            # Check if assets or episides selected
            if(self.selectedEpisode == "assets"):
                # Check if asset and asset job are selected
                if(self.selectedShot != ""):
                    if(self.selectedJob != ""):
                        # Check for jobs inappropriate for Houdini assets
                        if(self.selectedJob not in "comp concept"):
                            print "Starting Houdini for asset"
                            windowTitle = self.selectedProject.lower() + "_" + self.selectedEpisode + "_" + self.selectedShot + "_" + self.selectedJob + "_ASSET"
                            args = self.selectedProject.lower() + " " + self.selectedEpisode + " " + self.selectedShot + " " + self.selectedJob
                            subprocess.Popen("xterm -xrm 'XTerm*selectToClipboard: true' -geometry 170x55+120+120 -fa 'Monospace' -fs 8 -T " + windowTitle + " -bg " + color + " -sb -sl 100000 -e /fd/lib/python/projectManager/HoudiniStart.py " + args, shell=True)
                        else:
                            self.statusBar.showMessage("Select other job: " + self.selectedJob + " is inappropriate for Houdini")
                    else:
                        self.statusBar.showMessage("Select Asset Job:")
                else:
                    self.statusBar.showMessage("Select Asset:")
            elif(self.selectedEpisode != ""):
                # Assume that episode selected
                # Check if shot and job are selected
                if (self.selectedShot != ""):
                    if (self.selectedJob != ""):
                        # Check for jobs inappropriate for Houdini shots
                        if (self.selectedJob not in "comp tracking"):
                            print "Starting Houdini for shot"
                            windowTitle = self.selectedProject.lower() + "_" + self.selectedEpisode + "_" + self.selectedShot + "_" + self.selectedJob + "_SHOT"
                            args = self.selectedProject.lower() + " " + self.selectedEpisode + " " + self.selectedShot + " " + self.selectedJob
                            subprocess.Popen("xterm -xrm 'XTerm*selectToClipboard: true' -geometry 170x55+120+120 -fa 'Monospace' -fs 8 -T " + windowTitle + " -bg " + color + " -sb -sl 100000 -e /fd/lib/python/projectManager/HoudiniStart.py " + args, shell=True)
                        else:
                            self.statusBar.showMessage("Select other job: " + self.selectedJob + " is inappropriate for Houdini")
                    else:
                        self.statusBar.showMessage("Select Job:")
                else:
                    self.statusBar.showMessage("Select Shot:")
            else:
                self.statusBar.showMessage("Select Episode or Asset:")

    def StartMaya(self):
        import random
        import time
        random.seed(int(time.time()))
        color = self.bgColors[random.randrange(len(self.bgColors))]

        # Check if project selected
        if (self.selectedProject != ""):
            # Check if assets or episides selected
            if (self.selectedEpisode == "assets"):
                # Check if asset and asset job are selected
                if (self.selectedShot != ""):
                    if (self.selectedJob != ""):
                        # Check for jobs appropriate for Houdini assets
                        if (self.selectedJob in "animation modeling tracking layout"):
                            print "Starting Maya for asset"
                            windowTitle = self.selectedProject.lower() + "_" + self.selectedEpisode + "_" + self.selectedShot + "_" + self.selectedJob + "_ASSET"
                            args = self.selectedProject.lower() + " " + self.selectedEpisode + " " + self.selectedShot + " " + self.selectedJob
                            subprocess.Popen(
                                "xterm -xrm 'XTerm*selectToClipboard: true' -geometry 170x55+120+120 -fa 'Monospace' -fs 8 -T " + windowTitle + " -bg " + color + " -sb -sl 100000 -e /fd/lib/python/projectManager/MayaStart.py " + args,
                                shell=True)
                        else:
                            self.statusBar.showMessage(
                                "Select other job: " + self.selectedJob + " is inappropriate for Maya")
                    else:
                        self.statusBar.showMessage("Select Asset Job:")
                else:
                    self.statusBar.showMessage("Select Asset:")
            elif (self.selectedEpisode != ""):
                # Assume that episode selected
                # Check if shot and job are selected
                if (self.selectedShot != ""):
                    if (self.selectedJob != ""):
                        # Check for jobs appropriate for Houdini shots
                        if (self.selectedJob in "animation modeling tracking layout"):
                            print "Starting Maya for shot"
                            windowTitle = self.selectedProject.lower() + "_" + self.selectedEpisode + "_" + self.selectedShot + "_" + self.selectedJob + "_SHOT"
                            args = self.selectedProject.lower() + " " + self.selectedEpisode + " " + self.selectedShot + " " + self.selectedJob
                            subprocess.Popen(
                                "xterm -xrm 'XTerm*selectToClipboard: true' -geometry 170x55+120+120 -fa 'Monospace' -fs 8 -T " + windowTitle + " -bg " + color + " -sb -sl 100000 -e /fd/lib/python/projectManager/MayaStart.py " + args,
                                shell=True)
                        else:
                            self.statusBar.showMessage(
                                "Select othe job: " + self.selectedJob + " is inappropriate for Maya")
                    else:
                        self.statusBar.showMessage("Select Job:")
                else:
                    self.statusBar.showMessage("Select Shot:")
            else:
                self.statusBar.showMessage("Select Episode or Asset:")

    def ShotFilterClicked(self):
        if (self.filterUsed == False):
            # delete custom text
            self.filterUsed == True
            # get list of shots
            self.listShotsToFilter = cerebroRead.GetShots(self.selectedProject, self.selectedEpisode, self.db)
            self.listShotsToFilter = filters.FilterShots(self.listShotsToFilter)
            self.listShotsToFilter.sort()
            # Setup font
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
            font = QtGui.QFont()
            font.setItalic(False)
            self.lineInputShotFilter.setPalette(palette)
            self.lineInputShotFilter.setFont(font)
            self.lineInputShotFilter.setText("")
        else:
            self.listShotsToFilter = cerebroRead.GetShots(self.selectedProject, self.selectedEpisode, self.db)
            self.listShotsToFilter = filters.FilterShots(self.listShotsToFilter)
            self.listShotsToFilter.sort()


    def FilterShots(self):
        # Clear
        self.listJobs.clear()
        self.assetJobsList.clear()

        # Clear all asset selection
        self.assetsTreeView.clearSelection()
        self.assetJobsList.clearSelection()

        self.selectedShot = ""
        self.selectedJob = ""

        self.listShots.clear()

        filterText = self.lineInputShotFilter.text()

        for shot in self.listShotsToFilter:
            if (filterText in shot):
                self.listShots.addItem(shot)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.setStyle("motif")
    frame = FdstarterGUI()
    frame.show()
    app.exec_()