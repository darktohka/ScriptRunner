from PyQt5.QtWidgets import QApplication, QMessageBox
from .Settings import Settings
from .MainWidget import MainWidget
import sys

class ScriptRunner(object):

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loadSettings()
        self.main = None

    def loadSettings(self):
        try:
            self.settings = Settings('settings.json')
        except:
            QMessageBox.about(None, "Corrupt data", "It looks like your ScriptRunner data has become corrupted. Please restore an earlier backup to resolve this issue.")
            sys.exit()

    def getServers(self):
        return self.settings.get('servers', [])
    
    def setServers(self, servers):
        self.settings['servers'] = servers

        if self.main:
            self.main.reloadServers()

    def getServer(self, name):
        for i, server in enumerate(self.getServers()):
            if server['name'] == name:
                return server, i
        
        return None, None

    def getServerByIndex(self, index):
        return self.getServers()[index]

    def isServer(self, name):
        for server in self.getServers():
            if server['name'] == name:
                return True

        return False
    
    def getScripts(self):
        return self.settings.get('scripts', {})
    
    def setScripts(self, scripts):
        self.settings['scripts'] = scripts
        
        if self.main:
            self.main.reloadScripts()

    def getScript(self, script):
        return self.getScripts().get(script, '')

    def startMain(self):
        self.stopMain()
        self.main = MainWidget(self)

    def stopMain(self):
        if self.main:
            self.main.close()

        self.main = None

    def mainLoop(self):
        self.app.exec_()
