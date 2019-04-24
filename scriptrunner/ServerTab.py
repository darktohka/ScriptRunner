from PyQt5.QtWidgets import QWidget

class ServerTab(QWidget):

    def __init__(self, base, server):
        QWidget.__init__(self)
        self.base = base
        self.server = server
        self.index = -1

        self.setFixedSize(self.sizeHint())
    
    def setIndex(self, index):
        self.index = index
    
    def getIndex(self):
        return self.index