from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QMessageBox, QLabel
from .NewServerWidget import NewServerWidget
from .NewScriptWidget import NewScriptWidget
import copy

class SettingsTab(QWidget):

    def __init__(self, base):
        QWidget.__init__(self)
        self.base = base

        self.layout = QHBoxLayout()

        self.serverWidget = QWidget()
        self.serverLayout = QVBoxLayout()

        self.serverBox = QComboBox()
        
        self.serverLabel = QLabel('Servers')
        self.serverLabel.setFont(QFont('SansSerif', 10, weight=QFont.Bold))
        self.editButton = QPushButton('Edit server', self)
        self.editButton.clicked.connect(self.editServer)
        self.cloneButton = QPushButton('Clone server', self)
        self.cloneButton.clicked.connect(self.cloneServer)
        self.removeButton = QPushButton('Remove server', self)
        self.removeButton.clicked.connect(self.removeServer)
        self.addButton = QPushButton('Add new server', self)
        self.addButton.clicked.connect(self.addServer)

        self.serverLayout.addWidget(self.serverLabel, 0, Qt.AlignCenter)
        self.serverLayout.addWidget(self.serverBox)
        self.serverLayout.addWidget(self.editButton)
        self.serverLayout.addWidget(self.cloneButton)
        self.serverLayout.addWidget(self.removeButton)
        self.serverLayout.addWidget(self.addButton)
        self.serverWidget.setLayout(self.serverLayout)

        self.scriptWidget = QWidget()
        self.scriptLayout = QVBoxLayout()

        self.scriptBox = QComboBox()
        
        self.scriptLabel = QLabel('Scripts')
        self.scriptLabel.setFont(QFont('SansSerif', 10, weight=QFont.Bold))
        self.scriptEditButton = QPushButton('Edit script', self)
        self.scriptEditButton.clicked.connect(self.editScript)
        self.scriptRemoveButton = QPushButton('Remove script', self)
        self.scriptRemoveButton.clicked.connect(self.removeScript)
        self.scriptAddButton = QPushButton('Add new script', self)
        self.scriptAddButton.clicked.connect(self.addScript)
        self.scriptRunButton = QPushButton('Run script', self)
        self.scriptRunButton.clicked.connect(self.runScript)

        self.scriptLayout.addWidget(self.scriptLabel, 0, Qt.AlignCenter)
        self.scriptLayout.addWidget(self.scriptBox)
        self.scriptLayout.addWidget(self.scriptEditButton)
        self.scriptLayout.addWidget(self.scriptRemoveButton)
        self.scriptLayout.addWidget(self.scriptAddButton)
        self.scriptLayout.addWidget(self.scriptRunButton)
        self.scriptWidget.setLayout(self.scriptLayout)

        self.layout.addWidget(self.serverWidget, 0, Qt.AlignTop)
        self.layout.addWidget(self.scriptWidget, 0, Qt.AlignTop)
        self.setLayout(self.layout)

        self.reloadServers()
        self.reloadScripts()

        self.newServerWidget = None
        self.newScriptWidget = None

        self.setFixedSize(self.sizeHint())

    def reloadServers(self):
        self.serverBox.clear()

        for server in self.base.getServers():
            self.serverBox.addItem(server['name'])

        enabled = self.serverBox.count() > 0
        self.editButton.setEnabled(enabled)
        self.cloneButton.setEnabled(enabled)
        self.removeButton.setEnabled(enabled)

    def reloadScripts(self):
        self.scriptBox.clear()

        for scriptName in self.base.getScripts().keys():
            self.scriptBox.addItem(scriptName)
        
        enabled = self.scriptBox.count() > 0
        self.scriptEditButton.setEnabled(enabled)
        self.scriptRemoveButton.setEnabled(enabled)
        self.scriptRunButton.setEnabled(enabled)

    def editServer(self, *args):
        index = self.serverBox.currentIndex()
        server = self.base.getServerByIndex(index)
        self.newServerWidget = NewServerWidget(self.base, server)

    def removeServer(self, *args):
        index = self.serverBox.currentIndex()
        servers = self.base.getServers()
        server = servers[index]

        if QMessageBox.question(self, 'Server Configuration', "Are you sure you want to delete {0}?".format(server['name']), QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return

        del servers[index]
        self.base.setServers(servers)

    def cloneServer(self, *args):
        index = self.serverBox.currentIndex()
        servers = self.base.getServers()
        server = servers[index]

        if QMessageBox.question(self, 'Server Configuration', "Are you sure you want to clone {0}?".format(server['name']), QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return

        originalName = server['name']
        name = originalName
        index = 1
        
        while self.base.isServer(name):
            name = '{0} ({1})'.format(originalName, index)
            index += 1
        
        server = copy.deepcopy(server)
        server['name'] = name
        servers.append(server)
        self.base.setServers(servers)

    def addServer(self, *args):
        self.newServerWidget = NewServerWidget(self.base, None)
    
    def editScript(self, *args):
        self.newScriptWidget = NewScriptWidget(self.base, self.scriptBox.currentText())
    
    def removeScript(self, *args):
        name = self.scriptBox.currentText()

        if QMessageBox.question(self, 'Scripts', "Are you sure you want to delete the script '{0}'?".format(name), QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        
        scripts = self.base.getScripts()
        del scripts[name]
        self.base.setScripts(scripts)

    def addScript(self, *args):
        self.newScriptWidget = NewScriptWidget(self.base, None)
    
    def runScript(self, *args):
        self.base.main.createServerTabs()