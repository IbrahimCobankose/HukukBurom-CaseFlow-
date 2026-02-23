from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class formUYAP(QtWidgets.QWidget):
    def __init__(self, current_user_id=None):
        super(formUYAP, self).__init__()
        
        self.current_user_id = current_user_id
        
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://avukatbeta.uyap.gov.tr/giris"))
        
        self.btnExit = QtWidgets.QPushButton("Exit")
        self.btnExit.clicked.connect(self.exit_button_clicked)
        
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        layout.addWidget(self.btnExit)
        
        self.setLayout(layout)

    def exit_button_clicked(self):
        from views.formMainWindow import formMainWindow
        self.main_form = formMainWindow(current_user_id=self.current_user_id)
        self.main_form.setGeometry(self.geometry())
        self.main_form.show()
        self.close()