# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1155, 683)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 730, 577))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.scroll, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockLabel = QtWidgets.QDockWidget(MainWindow)
        self.dockLabel.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockLabel.setObjectName("dockLabel")
        self.labelListContainer = QtWidgets.QWidget()
        self.labelListContainer.setObjectName("labelListContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.labelListContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listLayout = QtWidgets.QVBoxLayout()
        self.listLayout.setObjectName("listLayout")
        self.editButton = QtWidgets.QToolButton(self.labelListContainer)
        self.editButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.editButton.setObjectName("editButton")
        self.listLayout.addWidget(self.editButton)
        self.useDefaultLabelQHBoxLayout = QtWidgets.QHBoxLayout()
        self.useDefaultLabelQHBoxLayout.setObjectName("useDefaultLabelQHBoxLayout")
        self.useDefaultLabelCheckbox = QtWidgets.QCheckBox(self.labelListContainer)
        self.useDefaultLabelCheckbox.setObjectName("useDefaultLabelCheckbox")
        self.useDefaultLabelQHBoxLayout.addWidget(self.useDefaultLabelCheckbox)
        self.defaultLabelTextLine = QtWidgets.QLineEdit(self.labelListContainer)
        self.defaultLabelTextLine.setObjectName("defaultLabelTextLine")
        self.useDefaultLabelQHBoxLayout.addWidget(self.defaultLabelTextLine)
        self.listLayout.addLayout(self.useDefaultLabelQHBoxLayout)
        self.labelList = QtWidgets.QListWidget(self.labelListContainer)
        self.labelList.setObjectName("labelList")
        self.listLayout.addWidget(self.labelList)
        self.deleteAllLabels = QtWidgets.QPushButton(self.labelListContainer)
        self.deleteAllLabels.setObjectName("deleteAllLabels")
        self.listLayout.addWidget(self.deleteAllLabels)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.countLabel = QtWidgets.QLabel(self.labelListContainer)
        self.countLabel.setObjectName("countLabel")
        self.horizontalLayout_2.addWidget(self.countLabel)
        self.moreStats = QtWidgets.QPushButton(self.labelListContainer)
        self.moreStats.setObjectName("moreStats")
        self.horizontalLayout_2.addWidget(self.moreStats)
        self.listLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.listLayout, 0, 0, 1, 1)
        self.dockLabel.setWidget(self.labelListContainer)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockLabel)
        self.filedock = QtWidgets.QDockWidget(MainWindow)
        self.filedock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.filedock.setObjectName("filedock")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileTreeWidget = QtWidgets.QTreeWidget(self.dockWidgetContents_3)
        self.fileTreeWidget.setHeaderHidden(True)
        self.fileTreeWidget.setObjectName("fileTreeWidget")
        self.fileTreeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.fileTreeWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.prevImage = QtWidgets.QPushButton(self.dockWidgetContents_3)
        self.prevImage.setEnabled(False)
        self.prevImage.setObjectName("prevImage")
        self.horizontalLayout_3.addWidget(self.prevImage)
        self.nextImage = QtWidgets.QPushButton(self.dockWidgetContents_3)
        self.nextImage.setEnabled(False)
        self.nextImage.setObjectName("nextImage")
        self.horizontalLayout_3.addWidget(self.nextImage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.detectAll = QtWidgets.QPushButton(self.dockWidgetContents_3)
        self.detectAll.setEnabled(False)
        self.detectAll.setObjectName("detectAll")
        self.verticalLayout.addWidget(self.detectAll)
        self.detectAllProgressBar = QtWidgets.QProgressBar(self.dockWidgetContents_3)
        self.detectAllProgressBar.setEnabled(False)
        self.detectAllProgressBar.setProperty("value", 0)
        self.detectAllProgressBar.setObjectName("detectAllProgressBar")
        self.verticalLayout.addWidget(self.detectAllProgressBar)
        self.exportCSV = QtWidgets.QPushButton(self.dockWidgetContents_3)
        self.exportCSV.setEnabled(False)
        self.exportCSV.setObjectName("exportCSV")
        self.verticalLayout.addWidget(self.exportCSV)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.filedock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.filedock)
        self.toolbar_open = QtWidgets.QToolBar(MainWindow)
        self.toolbar_open.setEnabled(True)
        self.toolbar_open.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolbar_open.setObjectName("toolbar_open")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar_open)
        self.toolbar_zoom = QtWidgets.QToolBar(MainWindow)
        self.toolbar_zoom.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolbar_zoom.setObjectName("toolbar_zoom")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar_zoom)
        self.toolbar_edit = QtWidgets.QToolBar(MainWindow)
        self.toolbar_edit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolbar_edit.setObjectName("toolbar_edit")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar_edit)
        self.dockwidget_server = QtWidgets.QDockWidget(MainWindow)
        self.dockwidget_server.setEnabled(True)
        self.dockwidget_server.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockwidget_server.setObjectName("dockwidget_server")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.serverHost = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.serverHost.setObjectName("serverHost")
        self.verticalLayout_3.addWidget(self.serverHost)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.serverPort = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.serverPort.setMaximum(10000)
        self.serverPort.setProperty("value", 8000)
        self.serverPort.setObjectName("serverPort")
        self.verticalLayout_4.addWidget(self.serverPort)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.dockwidget_server.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockwidget_server)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1155, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu_file = QtWidgets.QMenu(self.menuBar)
        self.menu_file.setObjectName("menu_file")
        self.menu_Edit = QtWidgets.QMenu(self.menuBar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_View = QtWidgets.QMenu(self.menuBar)
        self.menu_View.setObjectName("menu_View")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menuBar)
        self.quit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/quit")
        self.quit.setIcon(icon)
        self.quit.setObjectName("quit")
        self.openProj = QtWidgets.QAction(MainWindow)
        self.openProj.setCheckable(False)
        self.openProj.setEnabled(True)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.openProj.setIcon(icon)
        self.openProj.setObjectName("openProj")
        self.createProject = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/add")
        self.createProject.setIcon(icon)
        self.createProject.setObjectName("createProject")
        self.openAnnotation = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.openAnnotation.setIcon(icon)
        self.openAnnotation.setObjectName("openAnnotation")
        self.openNextImgAction = QtWidgets.QAction(MainWindow)
        self.openNextImgAction.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/next")
        self.openNextImgAction.setIcon(icon)
        self.openNextImgAction.setObjectName("openNextImgAction")
        self.openPrevImgAction = QtWidgets.QAction(MainWindow)
        self.openPrevImgAction.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/prev")
        self.openPrevImgAction.setIcon(icon)
        self.openPrevImgAction.setObjectName("openPrevImgAction")
        self.verify = QtWidgets.QAction(MainWindow)
        self.verify.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/label_plus")
        self.verify.setIcon(icon)
        self.verify.setObjectName("verify")
        self.saveProj = QtWidgets.QAction(MainWindow)
        self.saveProj.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/save")
        self.saveProj.setIcon(icon)
        self.saveProj.setObjectName("saveProj")
        self.save_format = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/label_form")
        self.save_format.setIcon(icon)
        self.save_format.setObjectName("save_format")
        self.saveAs = QtWidgets.QAction(MainWindow)
        self.saveAs.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/save-as")
        self.saveAs.setIcon(icon)
        self.saveAs.setObjectName("saveAs")
        self.closeAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/close")
        self.closeAction.setIcon(icon)
        self.closeAction.setObjectName("closeAction")
        self.resetAllAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/resetall")
        self.resetAllAction.setIcon(icon)
        self.resetAllAction.setObjectName("resetAllAction")
        self.color1 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/color")
        self.color1.setIcon(icon)
        self.color1.setObjectName("color1")
        self.createMode = QtWidgets.QAction(MainWindow)
        self.createMode.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/new")
        self.createMode.setIcon(icon)
        self.createMode.setObjectName("createMode")
        self.editMode = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../../.designer/backup/resources/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editMode.setIcon(icon)
        self.editMode.setObjectName("editMode")
        self.create = QtWidgets.QAction(MainWindow)
        self.create.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/new_shape")
        self.create.setIcon(icon)
        self.create.setObjectName("create")
        self.deleteAction = QtWidgets.QAction(MainWindow)
        self.deleteAction.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/remove_shape")
        self.deleteAction.setIcon(icon)
        self.deleteAction.setObjectName("deleteAction")
        self.copy = QtWidgets.QAction(MainWindow)
        self.copy.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/edit_shape")
        self.copy.setIcon(icon)
        self.copy.setObjectName("copy")
        self.detect = QtWidgets.QAction(MainWindow)
        self.detect.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/shape_t")
        self.detect.setIcon(icon)
        self.detect.setObjectName("detect")
        self.advancedMode = QtWidgets.QAction(MainWindow)
        self.advancedMode.setCheckable(True)
        icon = QtGui.QIcon.fromTheme(":/expert")
        self.advancedMode.setIcon(icon)
        self.advancedMode.setObjectName("advancedMode")
        self.hideAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/hide")
        self.hideAll.setIcon(icon)
        self.hideAll.setObjectName("hideAll")
        self.showAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/hide")
        self.showAll.setIcon(icon)
        self.showAll.setObjectName("showAll")
        self.help = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/help")
        self.help.setIcon(icon)
        self.help.setObjectName("help")
        self.showInfo = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/help")
        self.showInfo.setIcon(icon)
        self.showInfo.setObjectName("showInfo")
        self.zoomIn = QtWidgets.QAction(MainWindow)
        self.zoomIn.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/zoom_in")
        self.zoomIn.setIcon(icon)
        self.zoomIn.setObjectName("zoomIn")
        self.zoomOut = QtWidgets.QAction(MainWindow)
        self.zoomOut.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/zoom_out")
        self.zoomOut.setIcon(icon)
        self.zoomOut.setObjectName("zoomOut")
        self.zoomOrg = QtWidgets.QAction(MainWindow)
        self.zoomOrg.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/original")
        self.zoomOrg.setIcon(icon)
        self.zoomOrg.setIconVisibleInMenu(True)
        self.zoomOrg.setProperty("shortcutVisibleInContextMenu", True)
        self.zoomOrg.setObjectName("zoomOrg")
        self.fitWindow = QtWidgets.QAction(MainWindow)
        self.fitWindow.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/fit")
        self.fitWindow.setIcon(icon)
        self.fitWindow.setShortcut("")
        self.fitWindow.setObjectName("fitWindow")
        self.fitWidth = QtWidgets.QAction(MainWindow)
        self.fitWidth.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/fit_width")
        self.fitWidth.setIcon(icon)
        self.fitWidth.setObjectName("fitWidth")
        self.edit = QtWidgets.QAction(MainWindow)
        self.edit.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/edit")
        self.edit.setIcon(icon)
        self.edit.setObjectName("edit")
        self.shapeLineColor = QtWidgets.QAction(MainWindow)
        self.shapeLineColor.setEnabled(False)
        self.shapeLineColor.setObjectName("shapeLineColor")
        self.shapeFillColor = QtWidgets.QAction(MainWindow)
        self.shapeFillColor.setEnabled(False)
        self.shapeFillColor.setObjectName("shapeFillColor")
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.autoSaving = QtWidgets.QAction(MainWindow)
        self.autoSaving.setCheckable(True)
        self.autoSaving.setObjectName("autoSaving")
        self.singleClassMode = QtWidgets.QAction(MainWindow)
        self.singleClassMode.setCheckable(True)
        self.singleClassMode.setObjectName("singleClassMode")
        self.displayLabelOption = QtWidgets.QAction(MainWindow)
        self.displayLabelOption.setCheckable(True)
        self.displayLabelOption.setObjectName("displayLabelOption")
        self.saveAnnot = QtWidgets.QAction(MainWindow)
        self.saveAnnot.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/upload")
        self.saveAnnot.setIcon(icon)
        self.saveAnnot.setObjectName("saveAnnot")
        self.update = QtWidgets.QAction(MainWindow)
        self.update.setObjectName("update")
        self.version = QtWidgets.QAction(MainWindow)
        self.version.setObjectName("version")
        self.showCurrentClass = QtWidgets.QAction(MainWindow)
        self.showCurrentClass.setObjectName("showCurrentClass")
        self.hideCurrentClass = QtWidgets.QAction(MainWindow)
        self.hideCurrentClass.setObjectName("hideCurrentClass")
        self.toolbar_open.addAction(self.openProj)
        self.toolbar_open.addAction(self.createProject)
        self.toolbar_open.addAction(self.saveProj)
        self.toolbar_open.addAction(self.verify)
        self.toolbar_open.addAction(self.saveAnnot)
        self.toolbar_open.addAction(self.save_format)
        self.toolbar_zoom.addAction(self.zoomOut)
        self.toolbar_zoom.addAction(self.zoomIn)
        self.toolbar_zoom.addAction(self.zoomOrg)
        self.toolbar_zoom.addAction(self.fitWindow)
        self.toolbar_zoom.addAction(self.fitWidth)
        self.toolbar_edit.addAction(self.create)
        self.toolbar_edit.addAction(self.detect)
        self.toolbar_edit.addAction(self.edit)
        self.toolbar_edit.addAction(self.copy)
        self.toolbar_edit.addAction(self.deleteAction)
        self.menu_file.addAction(self.openProj)
        self.menu_file.addAction(self.createProject)
        self.menu_file.addAction(self.saveProj)
        self.menu_file.addAction(self.saveAs)
        self.menu_file.addAction(self.save_format)
        self.menu_file.addAction(self.closeAction)
        self.menu_file.addAction(self.resetAllAction)
        self.menu_Edit.addAction(self.create)
        self.menu_Edit.addAction(self.deleteAction)
        self.menu_Edit.addAction(self.edit)
        self.menu_Edit.addAction(self.copy)
        self.menu_Edit.addAction(self.detect)
        self.menu_View.addAction(self.autoSaving)
        self.menu_View.addAction(self.singleClassMode)
        self.menu_View.addAction(self.displayLabelOption)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.hideAll)
        self.menu_View.addAction(self.showAll)
        self.menu_View.addAction(self.hideCurrentClass)
        self.menu_View.addAction(self.showCurrentClass)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.zoomIn)
        self.menu_View.addAction(self.zoomOut)
        self.menu_View.addAction(self.zoomOrg)
        self.menu_View.addAction(self.fitWindow)
        self.menu_View.addAction(self.fitWidth)
        self.menu_View.addSeparator()
        self.menu_Help.addAction(self.help)
        self.menu_Help.addAction(self.showInfo)
        self.menu_Help.addAction(self.update)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu_Edit.menuAction())
        self.menuBar.addAction(self.menu_View.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Active Image Labeler"))
        self.dockLabel.setWindowTitle(_translate("MainWindow", "Box Labels"))
        self.editButton.setText(_translate("MainWindow", "..."))
        self.useDefaultLabelCheckbox.setText(_translate("MainWindow", "Use default label"))
        self.deleteAllLabels.setText(_translate("MainWindow", "Remove All Boxes"))
        self.countLabel.setText(_translate("MainWindow", "TextLabel"))
        self.moreStats.setText(_translate("MainWindow", "More ..."))
        self.filedock.setWindowTitle(_translate("MainWindow", "File List                                          Score"))
        self.prevImage.setText(_translate("MainWindow", "Previous"))
        self.nextImage.setText(_translate("MainWindow", "Next"))
        self.detectAll.setText(_translate("MainWindow", "Detect on All images"))
        self.exportCSV.setText(_translate("MainWindow", "Export .csv"))
        self.toolbar_open.setWindowTitle(_translate("MainWindow", "Handle Image"))
        self.toolbar_zoom.setWindowTitle(_translate("MainWindow", "Zoom"))
        self.toolbar_edit.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockwidget_server.setWindowTitle(_translate("MainWindow", "Connection with Server"))
        self.label.setText(_translate("MainWindow", "Host:"))
        self.serverHost.setText(_translate("MainWindow", "localhost"))
        self.label_2.setText(_translate("MainWindow", "Port:"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_Edit.setTitle(_translate("MainWindow", "Edit"))
        self.menu_View.setTitle(_translate("MainWindow", "View"))
        self.menu_Help.setTitle(_translate("MainWindow", "Help"))
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.quit.setToolTip(_translate("MainWindow", "Quit application"))
        self.quit.setStatusTip(_translate("MainWindow", "Quit application"))
        self.quit.setWhatsThis(_translate("MainWindow", "Quit application"))
        self.quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.openProj.setText(_translate("MainWindow", "Open project"))
        self.openProj.setToolTip(_translate("MainWindow", "Open image or label file"))
        self.openProj.setStatusTip(_translate("MainWindow", "Open image or label file"))
        self.openProj.setWhatsThis(_translate("MainWindow", "Open image or label file"))
        self.openProj.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.createProject.setText(_translate("MainWindow", "Create Project"))
        self.createProject.setToolTip(_translate("MainWindow", "Open Directory"))
        self.createProject.setStatusTip(_translate("MainWindow", "Open Directory"))
        self.createProject.setWhatsThis(_translate("MainWindow", "Open Directory"))
        self.createProject.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.openAnnotation.setText(_translate("MainWindow", "Open Annotation"))
        self.openAnnotation.setToolTip(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setStatusTip(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setWhatsThis(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.openNextImgAction.setText(_translate("MainWindow", "Next Image"))
        self.openNextImgAction.setToolTip(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setStatusTip(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setWhatsThis(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setShortcut(_translate("MainWindow", "D"))
        self.openPrevImgAction.setText(_translate("MainWindow", "Previous Image"))
        self.openPrevImgAction.setToolTip(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setStatusTip(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setWhatsThis(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setShortcut(_translate("MainWindow", "A"))
        self.verify.setText(_translate("MainWindow", "Verify Image"))
        self.verify.setStatusTip(_translate("MainWindow", "Verify Image"))
        self.verify.setWhatsThis(_translate("MainWindow", "Verify Image"))
        self.verify.setShortcut(_translate("MainWindow", "Space"))
        self.saveProj.setText(_translate("MainWindow", "Save project"))
        self.saveProj.setStatusTip(_translate("MainWindow", "Save project"))
        self.saveProj.setWhatsThis(_translate("MainWindow", "Save project"))
        self.saveProj.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.save_format.setText(_translate("MainWindow", "Change save format"))
        self.save_format.setIconText(_translate("MainWindow", "PascalVOC"))
        self.save_format.setStatusTip(_translate("MainWindow", "Change save format"))
        self.save_format.setWhatsThis(_translate("MainWindow", "Change save format"))
        self.saveAs.setText(_translate("MainWindow", "Save As"))
        self.saveAs.setToolTip(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setStatusTip(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setWhatsThis(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.closeAction.setText(_translate("MainWindow", "Close"))
        self.closeAction.setToolTip(_translate("MainWindow", "Close the current file"))
        self.closeAction.setStatusTip(_translate("MainWindow", "Close the current file"))
        self.closeAction.setWhatsThis(_translate("MainWindow", "Close the current file"))
        self.closeAction.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.resetAllAction.setText(_translate("MainWindow", "Reset All"))
        self.resetAllAction.setStatusTip(_translate("MainWindow", "Reset All"))
        self.resetAllAction.setWhatsThis(_translate("MainWindow", "Reset All"))
        self.color1.setText(_translate("MainWindow", "Box Line Color"))
        self.color1.setToolTip(_translate("MainWindow", "Choose Box line color"))
        self.color1.setStatusTip(_translate("MainWindow", "Choose Box line color"))
        self.color1.setWhatsThis(_translate("MainWindow", "Choose Box line color"))
        self.createMode.setText(_translate("MainWindow", "Create\\nRectBox"))
        self.createMode.setIconText(_translate("MainWindow", "Create\n"
"RectBox"))
        self.createMode.setToolTip(_translate("MainWindow", "Draw a new box"))
        self.createMode.setStatusTip(_translate("MainWindow", "Draw a new box"))
        self.createMode.setWhatsThis(_translate("MainWindow", "Draw a new box"))
        self.createMode.setShortcut(_translate("MainWindow", "W"))
        self.editMode.setText(_translate("MainWindow", "Edit Label"))
        self.editMode.setToolTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setStatusTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setWhatsThis(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setShortcut(_translate("MainWindow", "Ctrl+J"))
        self.create.setText(_translate("MainWindow", "Create RectBox"))
        self.create.setToolTip(_translate("MainWindow", "Draw a new box"))
        self.create.setStatusTip(_translate("MainWindow", "Draw a new box"))
        self.create.setWhatsThis(_translate("MainWindow", "Draw a new box"))
        self.create.setShortcut(_translate("MainWindow", "W"))
        self.deleteAction.setText(_translate("MainWindow", "Delete RectBox"))
        self.deleteAction.setToolTip(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setStatusTip(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setWhatsThis(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setShortcut(_translate("MainWindow", "Del"))
        self.copy.setText(_translate("MainWindow", "Copy RectBox"))
        self.copy.setToolTip(_translate("MainWindow", "Copy the current box"))
        self.copy.setStatusTip(_translate("MainWindow", "Copy the current box"))
        self.copy.setWhatsThis(_translate("MainWindow", "Copy the current box"))
        self.copy.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.detect.setText(_translate("MainWindow", "Detect RectBox"))
        self.detect.setToolTip(_translate("MainWindow", "Detect all boxes"))
        self.detect.setStatusTip(_translate("MainWindow", "Detect all boxes"))
        self.detect.setWhatsThis(_translate("MainWindow", "Detect all boxes"))
        self.detect.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
        self.advancedMode.setText(_translate("MainWindow", "Advanced Mode"))
        self.advancedMode.setIconText(_translate("MainWindow", "Advanced Mode"))
        self.advancedMode.setToolTip(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setStatusTip(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setWhatsThis(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.hideAll.setText(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setIconText(_translate("MainWindow", "Hide all\n"
"bounding boxes"))
        self.hideAll.setToolTip(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setStatusTip(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setWhatsThis(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.showAll.setText(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setIconText(_translate("MainWindow", "Show all\n"
"bounding boxes"))
        self.showAll.setToolTip(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setStatusTip(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setWhatsThis(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.help.setText(_translate("MainWindow", "Tutorial"))
        self.help.setToolTip(_translate("MainWindow", "Show demo"))
        self.help.setStatusTip(_translate("MainWindow", "Show demo"))
        self.help.setWhatsThis(_translate("MainWindow", "Show demo"))
        self.showInfo.setText(_translate("MainWindow", "Information"))
        self.showInfo.setStatusTip(_translate("MainWindow", "Information"))
        self.showInfo.setWhatsThis(_translate("MainWindow", "Information"))
        self.zoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.zoomIn.setToolTip(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setStatusTip(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setWhatsThis(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.zoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.zoomOut.setToolTip(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setStatusTip(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setWhatsThis(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.zoomOrg.setText(_translate("MainWindow", "Original size"))
        self.zoomOrg.setToolTip(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setStatusTip(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setWhatsThis(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setShortcut(_translate("MainWindow", "Ctrl+*"))
        self.fitWindow.setText(_translate("MainWindow", "Fit Window"))
        self.fitWindow.setToolTip(_translate("MainWindow", "Zoom follows window size"))
        self.fitWindow.setStatusTip(_translate("MainWindow", "Zoom follows window size"))
        self.fitWindow.setWhatsThis(_translate("MainWindow", "Zoom follows window size"))
        self.fitWidth.setText(_translate("MainWindow", "Fit Width"))
        self.fitWidth.setToolTip(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setStatusTip(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setWhatsThis(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setShortcut(_translate("MainWindow", "Ctrl+Shift+F"))
        self.edit.setText(_translate("MainWindow", "Edit RectBox"))
        self.edit.setToolTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setStatusTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setWhatsThis(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.shapeLineColor.setText(_translate("MainWindow", "Shape Line Color"))
        self.shapeLineColor.setToolTip(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeLineColor.setStatusTip(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeLineColor.setWhatsThis(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeFillColor.setText(_translate("MainWindow", "Shape Fill Color"))
        self.shapeFillColor.setToolTip(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.shapeFillColor.setStatusTip(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.shapeFillColor.setWhatsThis(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.actiontest.setText(_translate("MainWindow", "test"))
        self.autoSaving.setText(_translate("MainWindow", "Auto Save mode"))
        self.singleClassMode.setText(_translate("MainWindow", "Single Class Mode"))
        self.singleClassMode.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.displayLabelOption.setText(_translate("MainWindow", "Display Labels"))
        self.displayLabelOption.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.saveAnnot.setText(_translate("MainWindow", "Save annotation"))
        self.saveAnnot.setToolTip(_translate("MainWindow", "Save annotation file"))
        self.saveAnnot.setStatusTip(_translate("MainWindow", "Save the labels to a file"))
        self.saveAnnot.setWhatsThis(_translate("MainWindow", "Save the labels to a file"))
        self.update.setText(_translate("MainWindow", "Update"))
        self.version.setText(_translate("MainWindow", "Version"))
        self.showCurrentClass.setText(_translate("MainWindow", "Show similar bounding box"))
        self.showCurrentClass.setToolTip(_translate("MainWindow", "Show similar bounding box"))
        self.showCurrentClass.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.hideCurrentClass.setText(_translate("MainWindow", "Hide similar bounding box"))
        self.hideCurrentClass.setToolTip(_translate("MainWindow", "Hide similar bounding box"))
        self.hideCurrentClass.setShortcut(_translate("MainWindow", "Ctrl+Shift+H"))
