#!/usr/bin/python
from PySide import QtCore, QtGui
import sys

import cerebroRead
import filters

# --------------- GUI class description --------------------------------------------------------------------------------

class FdProjectManagerGUI (QtGui.QWidget):

    def __init__(self):
        super(FdProjectManagerGUI, self).__init__()
        self.setupUI()
        host = 'fs.dkfx.lan'
        port = '5432'
        self.db = cerebroRead.database.Database(host, port)
        self.cerebroProject = cerebroRead.CrProject()
        self.model = QtGui.QStandardItemModel()



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
        self.buttonLogin    = QtGui.QPushButton("Login to Cerebro/Get Projects List")
        iconLogin = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/login.png'))
        self.buttonLogin.setIcon(iconLogin)

        self.buttonGenerateProject = QtGui.QPushButton("Load Selected Project Data:")
        iconLoad = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/loadData.png'))
        self.buttonGenerateProject.setIcon(iconLoad)

        self.buttonCreateFolderStructure = QtGui.QPushButton("Create Folder structure:")
        iconCreate = QtGui.QIcon(QtGui.QPixmap('/fd/lib/icons/createFolders.png'))
        self.buttonCreateFolderStructure.setIcon(iconCreate)

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
        loginColumnLayout.addWidget(self.buttonGenerateProject, 3)
        loginColumnLayout.addWidget(self.buttonCreateFolderStructure, 5)

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
        # Episotes List
        labelEpisodes = QtGui.QLabel("Episodes: ")
        self.listEpisodes = QtGui.QListWidget()
        labelShots = QtGui.QLabel("Shots: ")
        self.listShots = QtGui.QListWidget()
        labelJobs = QtGui.QLabel("Jobs: ")
        self.listJobs = QtGui.QListWidget()

        scenesColumnLayout = QtGui.QVBoxLayout()
        scenesColumnLayout.addWidget(labelEpisodes, 0)
        scenesColumnLayout.addWidget(self.listEpisodes, 1)

        shotsColumnLayout = QtGui.QVBoxLayout()
        shotsColumnLayout.addWidget(labelShots, 0)
        shotsColumnLayout.addWidget(self.listShots, 1)

        jobsColumnLayout = QtGui.QVBoxLayout()
        jobsColumnLayout.addWidget(labelJobs, 0)
        jobsColumnLayout.addWidget(self.listJobs, 1)

        episodesGlobalLayout = QtGui.QHBoxLayout()
        episodesGlobalLayout.addItem(scenesColumnLayout)
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

        # Tab for Error List
        errorsTab = QtGui.QWidget()
        errorsTab.setAutoFillBackground(True)


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
        self.listEpisodes.itemClicked.connect(self.GetShotsFromSelectedEpisode)
        self.listShots.itemClicked.connect(self.GetJobsFromSelectedShot)
        self.listShots.itemEntered.connect(self.GetJobsFromSelectedShot)
        self.buttonGenerateProject.clicked.connect(self.GenerateProject)
        self.buttonCreateFolderStructure.clicked.connect(self.GenerateFolderStructure)
        #self.assetsTreeView.clicked.connect(self.GetJobsFromSelectedAsset)
        #self.buttonCheckFolderStructure.clicked.connect(self.CheckProject)

        #general window setup---------------------------------
        self.setLayout(StatusLayout)
        self.setGeometry(900, 300, 1200, 600)
        self.setWindowTitle("FD Project Manager")
        self.show()

    def LoginToCerebro(self):
        #login to cerebro with pass and login
        user = 'asknarin'
        password = 'evv250584'

        # Generate list of projects to select from
        self.listProjects.clear()

        # login
        if self.db.connect_from_cerebro_client() != 0:
            self.db.connect(user, password)

        projectsList = cerebroRead.GetRootProjects(self.db)
        filteredProjectsList = filters.FilterProjects(projectsList)
        filteredProjectsList.sort()

        i = 0
        for project in filteredProjectsList:
            self.listProjects.addItem(project)
            self.listProjects.item(i).setIcon(self.iconGreen)
            i = i + 1

        # print status message
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
        self.statusBar.setPalette(palette)
        self.statusBar.showMessage("Projects Loaded. Select scene.")



    def GenerateProject(self):
        # Show Loading Dialog

        if(len(self.listProjects.selectedItems()) == 0):
            # None of projects Selected
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 0, 0))
            self.statusBar.setPalette(palette)
            self.statusBar.showMessage("Select project !!!")
        else:
            # Display Selected Project name
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
            self.statusBar.setPalette(palette)
            self.statusBar.showMessage(self.listProjects.selectedItems()[0].text())

            # Setup the project
            self.cerebroProject.name = self.listProjects.selectedItems()[0].text()
            self.cerebroProject.fullURL = "/" + self.listProjects.selectedItems()[0].text()
            self.cerebroProject.taskID  = self.db.task_by_url(self.cerebroProject.fullURL)

            # Show Loading
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 255))
            self.statusBar.setPalette(palette)
            self.statusBar.showMessage("Loading Project Data.........")
            QtCore.QCoreApplication.processEvents()


            self.cerebroProject.Clear()
            self.cerebroProject.LoadScenes(self.db)
            self.cerebroProject.LoadAssets(self.db)


            self.listEpisodes.clearSelection()
            self.listEpisodes.clear()
            self.listShots.clearSelection()
            self.listShots.clear()
            self.listJobs.clearSelection()
            self.listJobs.clear()

            # LOAD EPISODES LIST
            for episode in self.cerebroProject.episodes:
                self.listEpisodes.addItem(episode.name)

            # LOAD ASSETS TREE

            self.assetsTreeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Name", "Type", "URL"])
            self.assetsTreeView.setModel(self.model)
            self.assetsTreeView.setColumnWidth(0, 200)
            self.assetsTreeView.setColumnWidth(1, 130)
            self.assetJobsList.clear()



            for asset in self.cerebroProject.assets:
                assetItemName = QtGui.QStandardItem(asset.name)
                assetItemType = QtGui.QStandardItem("Asset")
                assetItemURL  = QtGui.QStandardItem(asset.fullURL)
                self.model.appendRow([assetItemName, assetItemType, assetItemURL])


            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
            self.statusBar.setPalette(palette)
            self.statusBar.showMessage("Project " + self.cerebroProject.name + " Loaded.")


    def GetShotsFromSelectedEpisode(self, item):
        selectedScene = item.text()

        self.listShots.clear()
        self.listJobs.clear()

        shotsList = []

        for episode in self.cerebroProject.episodes:
            if(selectedScene in episode.name):
                if(len(selectedScene) == len(episode.name)):
                    for shot in episode.shots:
                        shotsList.append(shot.name)

        shotsList.sort()

        # Fill Shots Items
        for shot in shotsList:
            self.listShots.addItem(shot)

    def GetJobsFromSelectedShot(self, item):
        selectedShot = item.text()
        selectedEpisode = self.listEpisodes.selectedItems()[0].text()

        self.listJobs.clear()

        jobsList = []

        for episodeObj in self.cerebroProject.episodes:
            if(selectedEpisode in episodeObj.name):
                if (len(selectedEpisode) == len(episodeObj.name)):
                    for shotObj in episodeObj.shots:
                        if(selectedShot in shotObj.name):
                            if (len(selectedShot) == len(shotObj.name)):
                                for job in shotObj.jobs:
                                    jobsList.append(job)

        jobsList.sort()

        for job in jobsList:
            self.listJobs.addItem(job)

    def GenerateFolderStructure(self):
        self.cerebroProject.CreateFolderStrusture()




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.setStyle("motif")
    frame = FdProjectManagerGUI()
    frame.show()
    app.exec_()

