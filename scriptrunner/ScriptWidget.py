from PyQt5.QtWidgets import QDesktopWidget, QWidget, QLabel, QVBoxLayout

class ScriptWidget(QWidget):

    def __init__(self, base, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.base = base

    def setBackgroundColor(self, widget, color):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), color)
        widget.setPalette(palette)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class TextboxWidget(QWidget):

    def __init__(self, label, boxClass):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        self.box = boxClass()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.box)
        self.setLayout(self.layout)
    
    def getValue(self):
        return self.box.text()

    def setValue(self, value):
        self.box.setText(value)

    def isEmpty(self):
        return len(self.box.text()) == 0