from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
from .ScriptWidget import ScriptWidget, TextboxWidget
import os

class AuthTypeWidget(TextboxWidget):

    def __init__(self, baseWidget, label):
        TextboxWidget.__init__(self, label, QComboBox)
        self.baseWidget = baseWidget
        self.box.addItem('Password')
        self.box.addItem('Private Key')
        self.box.currentIndexChanged.connect(self.enableCorrectWidget)
    
    def isPassword(self):
        return self.box.currentIndex() == 0
    
    def isPrivateKey(self):
        return self.box.currentIndex() == 1
    
    def setValue(self, value):
        self.box.setCurrentIndex(value)

    def enableCorrectWidget(self, *args):
        if self.isPassword():
            self.baseWidget.privateKeyWidget.hide()
            self.baseWidget.passwordWidget.show()
        else:
            self.baseWidget.privateKeyWidget.show()
            self.baseWidget.passwordWidget.hide()

        hint = self.baseWidget.sizeHint()
        hint.setWidth(300)
        self.baseWidget.setFixedSize(hint)

class PrivateKeyWidget(TextboxWidget):

    def __init__(self, label):
        TextboxWidget.__init__(self, label, QLineEdit)
        self.button = QPushButton('Choose')
        self.button.clicked.connect(self.choosePrivateKey)
        self.layout.addWidget(self.button)

    def choosePrivateKey(self, *args):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, 'Choose your private key!', "", "All Files (*);", options=options)

        if filename:
            self.box.setText(filename)

class NewServerWidget(ScriptWidget):

    def __init__(self, base, server=None):
        ScriptWidget.__init__(self, base)
        self.server = server
        
        self.setWindowTitle('Server Configuration')
        self.setBackgroundColor(self, Qt.white)

        self.layout = QVBoxLayout()

        self.nameWidget = TextboxWidget('Server Name:', QLineEdit)
        self.hostWidget = TextboxWidget('Server Hostname:', QLineEdit)
        self.usernameWidget = TextboxWidget('Username:', QLineEdit)
        self.authWidget = AuthTypeWidget(self, 'Authentication:')
        self.passwordWidget = TextboxWidget('Password:', QLineEdit)
        self.passwordWidget.box.setEchoMode(QLineEdit.Password)
        self.privateKeyWidget = PrivateKeyWidget('Private Key:')
        self.createButton = QPushButton('Save configuration')
        self.createButton.setFixedSize(100, 30)
        self.createButton.clicked.connect(self.saveServer)

        self.layout.addWidget(self.nameWidget)
        self.layout.addWidget(self.hostWidget)
        self.layout.addWidget(self.usernameWidget)
        self.layout.addWidget(self.authWidget)
        self.layout.addWidget(self.passwordWidget)
        self.layout.addWidget(self.privateKeyWidget)
        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.createButton, 0, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.fillServerDetails()

        self.authWidget.enableCorrectWidget()
        self.center()
        self.show()
    
    def isEdit(self):
        return self.server is not None

    def fillServerDetails(self):
        if not self.isEdit():
            return
        
        self.nameWidget.setValue(self.server['name'])
        self.hostWidget.setValue(self.server['hostname'])
        self.usernameWidget.setValue(self.server['username'])
        
        if 'password' in self.server:
            self.passwordWidget.setValue(self.server['password'])
            self.authWidget.setValue(0)
        elif 'privateKey' in self.server:
            self.privateKeyWidget.setValue(self.server['privateKey'])
            self.authWidget.setValue(1)

    def saveServer(self, *args):
        if self.nameWidget.isEmpty():
            QMessageBox.warning(self, 'Server Configuration', "The name of your server should not be empty!")
            return
        if self.hostWidget.isEmpty():
            QMessageBox.warning(self, 'Server Configuration', "The hostname of your server should not be empty!")
            return
        if self.usernameWidget.isEmpty():
            QMessageBox.warning(self, 'Server Configuration', "The username should not be empty!")
            return

        if self.authWidget.isPassword():
            if self.passwordWidget.isEmpty():
                QMessageBox.warning(self, 'Server Configuration', 'The password should not be empy!')
                return

        if self.authWidget.isPrivateKey():
            if self.privateKeyWidget.isEmpty():
                QMessageBox.warning(self, 'Server Configuration', 'Please choose your private key!')
                return
            if not os.path.exists(self.privateKeyWidget.getValue()):
                QMessageBox.warning(self, 'Server Configuration', 'That private key does not exist!')
                return

        servers = self.base.getServers()
        name = self.nameWidget.getValue()

        if self.base.isServer(name):
            if not self.isEdit() or self.server['name'] != name:
                QMessageBox.warning(self, 'Server Configuration', 'A server already exists with that name!')
                return

        newServer = {
            'name': name,
            'hostname': self.hostWidget.getValue(),
            'username': self.usernameWidget.getValue()
        }

        if self.authWidget.isPassword():
            newServer['password'] = self.passwordWidget.getValue()
        elif self.authWidget.isPrivateKey():
            newServer['privateKey'] = self.privateKeyWidget.getValue()
        
        if self.isEdit():
            server, i = self.base.getServer(self.server['name'])
            servers[i] = newServer
            text = "Server '{0}' has been edited!"
        else:
            servers.append(newServer)
            text = "New server '{0}' has been added!"
        
        self.base.setServers(servers)
        QMessageBox.information(self, 'Server Configuration', text.format(newServer['name']))
        self.close()