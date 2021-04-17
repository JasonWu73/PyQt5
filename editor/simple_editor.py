import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import resources


class SearchWidget(qtw.QWidget):
    submitted = qtc.pyqtSignal(str, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qtw.QFormLayout())
        self.term_input = qtw.QLineEdit()
        self.case_checkbox = qtw.QCheckBox('Case Sensitive?')
        self.search_button = qtw.QPushButton('Search')
        self.search_button.setObjectName('search_button')  # 用于样式表
        search_image = qtg.QPixmap(':/images/search.svg')
        gear_image = qtg.QPixmap(':/images/gear.svg')
        search_icon = qtg.QIcon(search_image)
        search_icon.addPixmap(gear_image, qtg.QIcon.Disabled)
        self.search_button.setEnabled(False)
        self.search_button.setIcon(search_icon)
        self.search_button.clicked.connect(self.on_submit)

        self.layout().addRow('Search Term', self.term_input)
        self.layout().addRow('', self.case_checkbox)
        self.layout().addRow('', self.search_button)

        self.term_input.textChanged.connect(self.check_term)

    @qtc.pyqtSlot(str)
    def check_term(self, term):
        if term:
            self.search_button.setEnabled(True)
        else:
            self.search_button.setEnabled(False)

    @qtc.pyqtSlot()
    def on_submit(self):
        term = self.term_input.text()
        case_sensitive = self.case_checkbox.checkState() == qtc.Qt.Checked
        self.submitted.emit(term, case_sensitive)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.text_edit = qtw.QTextEdit()
        self.setCentralWidget(self.text_edit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = file_menu.addAction('Open')
        save_action = file_menu.addAction('Save')
        file_menu.addSeparator()
        quit_action = file_menu.addAction('Quit')

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        quit_action.triggered.connect(self.close)

        self.statusBar().showMessage('Welcome to my editor', 2000)

        edit_toolbar = self.addToolBar('Edit')

        copy_icon = qtg.QIcon(qtg.QPixmap(':/images/copy.svg'))
        cut_icon = qtg.QIcon(qtg.QPixmap(':/images/cut.svg'))
        paste_icon = qtg.QIcon(qtg.QPixmap(':/images/paste.svg'))
        undo_icon = qtg.QIcon(qtg.QPixmap(':/images/undo.svg'))
        redo_icon = qtg.QIcon(qtg.QPixmap(':/images/redo.svg'))

        edit_toolbar.addAction(copy_icon, 'Copy', self.text_edit.copy)
        edit_toolbar.addAction(cut_icon, 'Cut', self.text_edit.cut)
        edit_toolbar.addAction(paste_icon, 'Paste', self.text_edit.paste)
        edit_toolbar.addAction(qtg.QIcon.fromTheme('edit-undo', undo_icon),
                               'Undo', self.text_edit.undo)
        edit_toolbar.addAction(redo_icon, 'Redo', self.text_edit.redo)

        search_dock = qtw.QDockWidget('Search')
        search_widget = SearchWidget()
        search_dock.setWidget(search_widget)
        search_widget.submitted.connect(self.search)

        self.addDockWidget(qtc.Qt.RightDockWidgetArea, search_dock)

        self.show()

    @qtc.pyqtSlot(str, bool)
    def search(self, term, case_sensitive=False):
        if case_sensitive:
            cur = self.text_edit.find(term,
                                      qtg.QTextDocument.FindCaseSensitively)
        else:
            cur = self.text_edit.find(term)

        if not cur:
            self.statusBar().showMessage('No matches Found', 2000)

    @qtc.pyqtSlot()
    def save_file(self):
        text = self.text_edit.toPlainText()
        filename, _ = qtw.QFileDialog.getSaveFileName()
        if filename:
            with open(filename, 'w') as handle:
                handle.write(text)
                self.statusBar().showMessage(f'Saved to {filename}')

    @qtc.pyqtSlot()
    def open_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as handle:
                text = handle.read()
            self.text_edit.clear()
            self.text_edit.insertPlainText(text)
            self.text_edit.moveCursor(qtg.QTextCursor.Start)
            self.statusBar().showMessage(f'Editing {filename}')


style_sheets = '''
QTextEdit {
    background-color: #2E3440;
    color: white;
    font-size: 16px;
}
'''

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(style_sheets)
    w = MainWindow()
    sys.exit(app.exec_())
