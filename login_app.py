import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class MainWindow(qtw.QWidget):

  authenticated = qtc.pyqtSignal(str)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # 代码开始
    self.username_input = qtw.QLineEdit()
    self.password_input = qtw.QLineEdit()
    self.password_input.setEchoMode(qtw.QLineEdit.Password)

    self.cancel_button = qtw.QPushButton('取消')
    self.submit_button = qtw.QPushButton('登录')

    layout = qtw.QFormLayout()
    layout.addRow('用户名', self.username_input)
    layout.addRow('密码', self.password_input)

    button_widget = qtw.QWidget()
    button_widget.setLayout(qtw.QHBoxLayout())
    button_widget.layout().addWidget(self.cancel_button)
    button_widget.layout().addWidget(self.submit_button)
    layout.addRow(button_widget)
    self.setLayout(layout)

    self.cancel_button.clicked.connect(self.close)
    self.submit_button.clicked.connect(self.authenticate)

    self.username_input.textChanged.connect(self.set_button_text)
    self.authenticated.connect(self.user_logged_in)
    # 代码结束
    self.show()

  @qtc.pyqtSlot(str)
  def set_button_text(self, text):
    if text:
      self.submit_button.setText(f'登录 {text}')
    else:
      self.submit_button.setText('登录...')

  @qtc.pyqtSlot()
  def authenticate(self):
    username = self.username_input.text()
    password = self.password_input.text()

    if username == 'user' and password == 'pass':
      qtw.QMessageBox.information(self, '登录成功', '您已登录成功')

      self.authenticated.emit(username)
    else:
      qtw.QMessageBox.critical(self, '失败', '用户名或密码错误')

  @qtc.pyqtSlot(str)
  def user_logged_in(self, username):
    qtw.QMessageBox.information(self, '已登录', f'{username} 已成功登录')


if __name__ == '__main__':
  app = qtw.QApplication(sys.argv)
  w = MainWindow()
  sys.exit(app.exec_())
