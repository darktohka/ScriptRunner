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

        self.setFixedSize(self.sizeHint())
        self.center()
        self.show()
    
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
        self.setFixedSize(self.sizeHint())

    def removeServerTab(self, name):
        if name not in self.serverTabs:
            return
        
        tab = self.serverTabs[name]
        self.tabs.removeTab(tab.getIndex())
        del self.serverTabs[name]
