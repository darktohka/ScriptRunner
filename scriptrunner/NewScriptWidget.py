from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QPlainTextEdit
from .ScriptWidget import ScriptWidget, TextboxWidget

class NewScriptWidget(ScriptWidget):

    def __init__(self, base, script=None):
        ScriptWidget.__init__(self, base)
        self.script = script
        
        self.setWindowTitle('Script Configuration')
        self.setBackgroundColor(self, Qt.white)

        self.layout = QVBoxLayout()

        self.nameWidget = TextboxWidget('Script Name:', QLineEdit)
        self.commandWidget = TextboxWidget('Script Commands:', QPlainTextEdit)
        self.createButton = QPushButton('Save script')
        self.createButton.setFixedSize(100, 30)
        self.createButton.clicked.connect(self.saveScript)

        self.layout.addWidget(self.nameWidget)
        self.layout.addWidget(self.commandWidget)
        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.createButton, 0, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.fillScriptDetails()

        hint = self.sizeHint()
        hint.setWidth(300)
        self.setFixedSize(hint)
        self.center()
        self.show()

    def isEdit(self):
        return self.script is not None

    def fillScriptDetails(self):
        if not self.isEdit():
            return
        
        self.nameWidget.setValue(self.script)
        self.commandWidget.box.setPlainText(self.base.getScript(self.script))

    def saveScript(self, *args):
        script = self.commandWidget.box.toPlainText().replace('\r', '')

        if self.nameWidget.isEmpty():
            QMessageBox.warning(self, 'Script Configuration', "The name of your script should not be empty!")
            return
        if not script:
            QMessageBox.warning(self, 'Script Configuration', "Your script should not be empty!")
            return

        scripts = self.base.getScripts()
        name = self.nameWidget.getValue()

        if name in scripts:
            if not self.isEdit() or name != self.script:
                QMessageBox.warning(self, 'Script Configuration', 'A script with that name already exists!')
                return

        if self.script:
            del scripts[self.script]
        
        scripts[name] = script

        if self.isEdit():
            text = "Script '{0}' has been edited!"
        else:
            text = "New script '{0}' has been added!"
        
        self.base.setScripts(scripts)
        QMessageBox.information(self, 'Script Configuration', text.format(name))
        self.close()