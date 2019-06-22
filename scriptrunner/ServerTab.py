from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QSizePolicy, QMessageBox
from .ServerThread import ServerThread

class ServerTab(QWidget):

    def __init__(self, base, server):
        QWidget.__init__(self)
        self.base = base
        self.server = server
        self.index = -1
        self.layout = QVBoxLayout()

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.output)
        self.setLayout(self.layout)

        self.serverThread = None
    
    def setIndex(self, index):
        self.index = index
    
    def getIndex(self):
        return self.index
    
    def getName(self):
        return self.server['name']

    def runCommands(self, commands):
        if self.serverThread:
            QMessageBox.warning(self, 'Error!', 'Server {0} is already running a command!'.format(self.getName()))
            return

        self.serverThread = ServerThread(self.server, commands)
        self.serverThread.start()