# forms/loginPageUi.py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormLoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("FormEmptyPage")
        self.resize(1920, 1080)
        self.setWindowTitle("Giriş Sayfası")

        # --- ARKA PLAN RESMİNİ YÜKLEME (Background 1) ---
        self.background = QtGui.QPixmap()
        
        # resources.py içinde 'background_img' varsa onu yükle
        if resources and hasattr(resources, 'background_img'):
             self.background.loadFromData(QByteArray.fromBase64(resources.background_img))
        # ------------------------------------------------

        self.original_width = 1920
        self.original_height = 1080

        self.original_font_sizes = {
            'button': 18,
            'lineedit': 20,
            'label': 30
        }

        self.min_font_sizes = {
            'button': 12,
            'lineedit': 14,
            'label': 24
        }
        
        self.max_font_sizes = {
            'button': 30,
            'lineedit': 32,
            'label': 60
        }
        
        self.font_button = QFont("Palatino Linotype", self.original_font_sizes['button'], QFont.Bold)
        self.font_LineEdit = QFont("Bodoni MT Condensed", self.original_font_sizes['lineedit'], QFont.Bold)
        self.font_label = QFont("Palatino Linotype", self.original_font_sizes['label'], QFont.Bold)
        
        # --- Sol Taraf (Avukat Girişi) ---
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(1050, 200, 350, 680))
        self.groupBox.setStyleSheet("color: #FFD4D4;background-color: #C6A560; padding:10px; border-radius: 20px")
        self.groupBox.setObjectName("groupBox")
        
        self.label = QLabel("AVUKAT",self)
        self.label.setObjectName("LawyerLabel")
        self.label.setFont(self.font_label)
        self.label.setStyleSheet("color: #50311F;padding:5px; border-radius: 10px")
        self.label.setGeometry(QtCore.QRect(1115, 250, 300, 80))

        self.label2 = QLabel("GİRİŞİ",self)
        self.label2.setObjectName("LoginLabel")
        self.label2.setFont(self.font_label)
        self.label2.setStyleSheet("color: #50311F;padding:5px; border-radius: 10px")
        self.label2.setGeometry(QtCore.QRect(1145, 330, 300, 80))
        
        self.LineEdit_1 = QLineEdit(self)
        self.LineEdit_1.setPlaceholderText("BARO ID")
        self.LineEdit_1.setObjectName("lineEdit")
        self.LineEdit_1.setFont(self.font_LineEdit)
        self.LineEdit_1.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.LineEdit_1.setGeometry(QtCore.QRect(1100, 450, 250, 80))
        self.LineEdit_1.setAlignment(Qt.AlignCenter)

        self.LineEdit_2 = QLineEdit(self)
        self.LineEdit_2.setPlaceholderText("PASSWORD")
        self.LineEdit_2.setObjectName("lineEdit_2")
        self.LineEdit_2.setFont(self.font_LineEdit)
        self.LineEdit_2.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.LineEdit_2.setGeometry(QtCore.QRect(1100, 550, 250, 80))
        self.LineEdit_2.setAlignment(Qt.AlignCenter)
        self.LineEdit_2.setEchoMode(QLineEdit.Password)

        self.btnLogin = QPushButton("GİRİŞ", self)
        self.btnLogin.setObjectName("LoginButton")
        self.btnLogin.setFont(self.font_button)
        self.btnLogin.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnLogin.setGeometry(QtCore.QRect(1100, 650, 250, 80))

        self.btnRegister = QPushButton("KAYIT", self)
        self.btnRegister.setObjectName("LoginButton")
        self.btnRegister.setFont(self.font_button)
        self.btnRegister.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnRegister.setGeometry(QtCore.QRect(1100, 750, 250, 80))


        # --- Sağ Taraf (Büro Girişi) ---
        self.groupBox2 = QtWidgets.QGroupBox(self)
        self.groupBox2.setGeometry(QtCore.QRect(1500, 200, 350, 680))
        self.groupBox2.setStyleSheet("color: #FFD4D4;background-color: #C6A560; padding:10px; border-radius: 20px")
        self.groupBox2.setObjectName("groupBox2")

        self.label3 = QLabel("  BÜRO",self)
        self.label3.setObjectName("label1")
        self.label3.setFont(self.font_label)
        self.label3.setStyleSheet("color: #50311F;padding:5px; border-radius: 10px")
        self.label3.setGeometry(QtCore.QRect(1575, 250, 300, 80))

        self.label4 = QLabel("GİRİŞİ",self)
        self.label4.setObjectName("label1")
        self.label4.setFont(self.font_label)
        self.label4.setStyleSheet("color: #50311F;padding:5px; border-radius: 10px")
        self.label4.setGeometry(QtCore.QRect(1595, 330, 300, 80))
        
        self.LineEdit_3 = QLineEdit(self)
        self.LineEdit_3.setPlaceholderText("BUREAU ID")
        self.LineEdit_3.setObjectName("lineEdit_3")
        self.LineEdit_3.setFont(self.font_LineEdit)
        self.LineEdit_3.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.LineEdit_3.setGeometry(QtCore.QRect(1550, 450, 250, 80))
        self.LineEdit_3.setAlignment(Qt.AlignCenter)

        self.LineEdit_4 = QLineEdit(self)
        self.LineEdit_4.setPlaceholderText("PASSWORD")
        self.LineEdit_4.setObjectName("lineEdit_4")
        self.LineEdit_4.setFont(self.font_LineEdit)
        self.LineEdit_4.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.LineEdit_4.setGeometry(QtCore.QRect(1550, 550, 250, 80))
        self.LineEdit_4.setAlignment(Qt.AlignCenter)
        self.LineEdit_4.setEchoMode(QLineEdit.Password)

        self.btnLogin_2 = QPushButton("GİRİŞ", self)
        self.btnLogin_2.setObjectName("LoginButton")
        self.btnLogin_2.setFont(self.font_button)
        self.btnLogin_2.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnLogin_2.setGeometry(QtCore.QRect(1550, 650, 250, 80))

        self.btnRegister_2 = QPushButton("KAYIT", self)
        self.btnRegister_2.setObjectName("LoginButton")
        self.btnRegister_2.setFont(self.font_button)
        self.btnRegister_2.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnRegister_2.setGeometry(QtCore.QRect(1550, 750, 250, 80))

        self.widgets = [
            (self.groupBox, 1050, 200, 350, 680),
            (self.label, 1115, 250, 300, 80),
            (self.label2, 1145, 330, 300, 80),
            (self.LineEdit_1, 1100, 450, 250, 80),
            (self.LineEdit_2, 1100, 550, 250, 80),
            (self.btnLogin, 1100, 650, 250, 80),
            (self.btnRegister, 1100, 750, 250, 80),
            (self.groupBox2, 1500, 200, 350, 680),
            (self.label3, 1575, 250, 300, 80),
            (self.label4, 1595, 330, 300, 80),
            (self.LineEdit_3, 1550, 450, 250, 80),
            (self.LineEdit_4, 1550, 550, 250, 80),
            (self.btnLogin_2, 1550, 650, 250, 80),
            (self.btnRegister_2, 1550, 750, 250, 80)
        ]

        self.label_widgets = [self.label, self.label2, self.label3, self.label4]
        self.lineedit_widgets = [self.LineEdit_1, self.LineEdit_2, self.LineEdit_3, self.LineEdit_4]
        self.button_widgets = [self.btnLogin, self.btnRegister, self.btnLogin_2, self.btnRegister_2]

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.setFocus()

    def resizeEvent(self, event):
        current_width = self.width()
        current_height = self.height()

        width_scale = current_width / self.original_width
        height_scale = current_height / self.original_height

        for widget, x, y, w, h in self.widgets:
            new_x = int(x * width_scale)
            new_y = int(y * height_scale)
            new_w = int(w * width_scale)
            new_h = int(h * height_scale)
            widget.setGeometry(QtCore.QRect(new_x, new_y, new_w, new_h))

        avg_scale = (width_scale + height_scale) / 2

        new_button_size = max(self.min_font_sizes['button'], 
                             min(self.max_font_sizes['button'], 
                                 self.original_font_sizes['button'] * avg_scale))
        
        new_lineedit_size = max(self.min_font_sizes['lineedit'], 
                               min(self.max_font_sizes['lineedit'], 
                                   self.original_font_sizes['lineedit'] * avg_scale))
        
        new_label_size = max(self.min_font_sizes['label'], 
                            min(self.max_font_sizes['label'], 
                                self.original_font_sizes['label'] * avg_scale))
        

        self.font_button.setPointSizeF(new_button_size)
        self.font_LineEdit.setPointSizeF(new_lineedit_size)
        self.font_label.setPointSizeF(new_label_size)

        for widget in self.label_widgets:
            widget.setFont(self.font_label)
        
        for widget in self.lineedit_widgets:
            widget.setFont(self.font_LineEdit)
        
        for widget in self.button_widgets:
            widget.setFont(self.font_button)
        
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.background.isNull():
            scaled = self.background.scaled(
                self.width(), self.height(),
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormLoginPage()
    window.show()
    sys.exit(app.exec_())