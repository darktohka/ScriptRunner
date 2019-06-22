from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget
from .ScriptWidget import ScriptWidget
from .SettingsTab import SettingsTab
from .ServerTab import ServerTab

class MainWidget(ScriptWidget):

    def __init__(self, base):
        ScriptWidget.__init__(self, base)
        
        self.setWindowTitle('SSH Script Runner')
        self.setBackgroundColor(self, Qt.white)

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.settingsTab = SettingsTab(base)
        self.tabs.addTab(self.settingsTab, 'Settings')

        self.serverTabs = {}

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.updateSize()
        self.center()
        self.show()
    
    def updateSize(self):
        hint = self.sizeHint()
        hint.setWidth(500)

        if hint.height() < 400:
            hint.setHeight(400)

        self.setFixedSize(hint)
    
    def reloadServers(self):
        self.settingsTab.reloadServers()
    
    def reloadScripts(self):
        self.settingsTab.reloadScripts()
    
    def createServerTabs(self):
        for server in self.base.getServers():
            self.addServerTab(server)
    
    def addServerTab(self, server):
        name = server['name']

        if name in self.serverTabs:
            return

        tab = ServerTab(self.base, server)
        self.serverTabs[name] = tab
        tab.setIndex(self.tabs.addTab(tab, name))
        self.updateSize()

    def removeServerTab(self, name):
        if name not in self.serverTabs:
            return
        
        tab = self.serverTabs[name]
        self.tabs.removeTab(tab.getIndex())
        del self.serverTabs[name]
        self.updateSize()

    def runCommands(self, server, commands):
        self.addServerTab(server)
        self.serverTabs[server['name']].runCommands(commands)