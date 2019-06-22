from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QCheckBox
from .ScriptWidget import ScriptWidget

class ChooseServerWidget(ScriptWidget):

    def __init__(self, base, script):
        ScriptWidget.__init__(self, base)
        self.script = script
        
        self.setWindowTitle('Run')
        self.setBackgroundColor(self, Qt.white)

        self.layout = QVBoxLayout()

        self.label = QLabel('Choose the servers to run the script on:')
        self.layout.addWidget(self.label)

        self.serverBoxes = {}

        for server in self.base.getServers():
            name = server['name']
            box = QCheckBox(name)
            box.setChecked(True)
            self.layout.addWidget(box)
            self.serverBoxes[name] = box

        self.createButton = QPushButton("Run '{0}'".format(script))
        self.createButton.setFixedSize(100, 30)
        self.createButton.clicked.connect(self.runScript)

        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.createButton, 0, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.setFixedSize(self.sizeHint())

        self.center()
        self.show()
    
    def runScript(self, *args):
        command = self.base.getScript(self.script)
        count = 0

        for server in self.base.getServers():
            name = server['name']

            if not self.serverBoxes[name].isChecked():
                continue
            
            self.base.main.runCommands(server, command)
            count += 1
        
        if not count:
            QMessageBox.information(self, 'Scripts', "Script '{0}' has been aborted.".format(self.script))
        else:
            QMessageBox.information(self, 'Scripts', "Running script '{0}' on {1} servers!".format(self.script, count))

        self.close()