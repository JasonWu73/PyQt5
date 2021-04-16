import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class DialogWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.message_a_edit = qtw.QLineEdit()
        self.message_b_edit = qtw.QLineEdit()
        self.cancel_button = qtw.QPushButton('取消')
        self.submit_button = qtw.QPushButton('提交')

        self.setLayout(qtw.QFormLayout())
        self.layout().addRow('消息 A', self.message_a_edit)
        self.layout().addRow('消息 B', self.message_b_edit)
        buttons = qtw.QWidget()
        buttons.setLayout(qtw.QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow(buttons)

        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)

    def set_messages(self, message_a, message_b):
        self.message_a_edit.setText(message_a)
        self.message_b_edit.setText(message_b)

    @qtc.pyqtSlot()
    def on_submit(self):
        self.submitted.emit(self.message_a_edit.text(),
                            self.message_b_edit.text())
        self.close()


class MainWindow(qtw.QWidget):
    dialog = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(640, 480)
        self.message_a = 'Hello'
        self.message_b = '你是在找我吗?'

        self.message_a_display = qtw.QLabel(self.message_a)
        self.message_a_display.setFont(qtg.QFont('Monaco', 20))
        self.message_b_display = qtw.QLabel(self.message_b)
        self.message_b_display.setFont(qtg.QFont('Monaco', 20))

        self.edit_button = qtw.QPushButton('编辑')
        self.edit_button.clicked.connect(self.edit_messages)

        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.message_a_display)
        self.layout().addWidget(self.message_b_display)
        self.layout().addWidget(self.edit_button)

        self.show()

    @qtc.pyqtSlot(str, str)
    def update_messages(self, message_a, message_b):
        self.message_a = message_a
        self.message_b = message_b
        self.message_a_display.setText(self.message_a)
        self.message_b_display.setText(self.message_b)

    @qtc.pyqtSlot()
    def edit_messages(self):
        self.dialog = DialogWindow()
        self.dialog.set_messages(self.message_a, self.message_b)
        self.dialog.submitted.connect(self.update_messages)
        self.dialog.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
