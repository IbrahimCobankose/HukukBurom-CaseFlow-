# forms/registerPageUi.py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormRegisterPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("FormEmptyPage")
        self.resize(1920, 1080)
        self.setWindowTitle("Boş Sayfa (1920x1080)")

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
            'label': 40
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

        self.font_LineEdit = QFont("Bodoni MT Condensed", self.original_font_sizes['lineedit'], QFont.Bold)
        self.font_button = QFont("Palatino Linotype", self.original_font_sizes['button'], QFont.Bold)
        self.font_label = QFont("Palatino Linotype", self.original_font_sizes['label'], QFont.Bold)


        self.labelTitle = QLabel("REGISTRATION", self)
        self.labelTitle.setFont(QFont("Palatino Linotype", 60, QFont.Bold))
        self.labelTitle.setStyleSheet("color: #50311F;")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setGeometry(QtCore.QRect(1000, 40, 900, 80))

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(1050, 150, 350, 780))
        self.groupBox.setStyleSheet("color: #FFD4D4;background-color: #C6A560; padding:10px; border-radius: 20px")

        self.lineName = QLineEdit(self)
        self.lineName.setPlaceholderText("NAME")
        self.lineName.setObjectName("lineName")
        self.lineName.setFont(self.font_LineEdit)
        self.lineName.setGeometry(QtCore.QRect(1100, 170, 250, 60))
        self.lineName.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineName.setAlignment(Qt.AlignCenter)

        self.lineSurname = QLineEdit(self)
        self.lineSurname.setPlaceholderText("SURNAME")
        self.lineSurname.setObjectName("lineSurname")
        self.lineSurname.setFont(self.font_LineEdit)
        self.lineSurname.setGeometry(QtCore.QRect(1100, 250, 250, 60))
        self.lineSurname.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineSurname.setAlignment(Qt.AlignCenter)

        self.lineEmail = QLineEdit(self)
        self.lineEmail.setPlaceholderText("EMAIL")
        self.lineEmail.setObjectName("lineEmail")
        self.lineEmail.setFont(self.font_LineEdit)
        self.lineEmail.setGeometry(QtCore.QRect(1100, 330, 250, 60))
        self.lineEmail.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineEmail.setAlignment(Qt.AlignCenter)
        
        self.linePassword = QLineEdit(self)
        self.linePassword.setPlaceholderText("PASSWORD")
        self.linePassword.setObjectName("linePassword")
        self.linePassword.setFont(self.font_LineEdit)
        self.linePassword.setGeometry(QtCore.QRect(1100, 410, 250, 60))
        self.linePassword.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.linePassword.setAlignment(Qt.AlignCenter)

        self.linePhone = QLineEdit(self)
        self.linePhone.setPlaceholderText("PHONE NUMBER")
        self.linePhone.setObjectName("linePhone")
        self.linePhone.setFont(self.font_LineEdit)
        self.linePhone.setGeometry(QtCore.QRect(1100, 490, 250, 60))
        self.linePhone.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.linePhone.setAlignment(Qt.AlignCenter)

        self.lineBaroId = QLineEdit(self)
        self.lineBaroId.setPlaceholderText("BARO ID")
        self.lineBaroId.setObjectName("lineBaroId")
        self.lineBaroId.setFont(self.font_LineEdit)
        self.lineBaroId.setGeometry(QtCore.QRect(1100, 570, 250, 60))
        self.lineBaroId.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBaroId.setAlignment(Qt.AlignCenter)

        self.lineBaroNumber = QLineEdit(self)
        self.lineBaroNumber.setPlaceholderText("BARO NUMBER")
        self.lineBaroNumber.setObjectName("lineBaroNumber")
        self.lineBaroNumber.setFont(self.font_LineEdit)
        self.lineBaroNumber.setGeometry(QtCore.QRect(1100, 650, 250, 60))
        self.lineBaroNumber.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBaroNumber.setAlignment(Qt.AlignCenter)

        self.btnSave = QPushButton("KAYDET", self)
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setFont(self.font_button)
        self.btnSave.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnSave.setGeometry(QtCore.QRect(1100, 770, 250, 60))

        self.btnCancel = QPushButton("ÇIKIŞ", self)
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setFont(self.font_button)
        self.btnCancel.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnCancel.setGeometry(QtCore.QRect(1100, 850, 250, 60))


        self.groupBox2 = QtWidgets.QGroupBox(self)
        self.groupBox2.setGeometry(QtCore.QRect(1500, 150, 350, 780))
        self.groupBox2.setStyleSheet("color: #FFD4D4;background-color: #C6A560; padding:10px; border-radius: 20px")

        self.lineBureauName = QLineEdit(self)
        self.lineBureauName.setPlaceholderText("BUREAU NAME")
        self.lineBureauName.setObjectName("lineBureauName")
        self.lineBureauName.setFont(self.font_LineEdit)
        self.lineBureauName.setGeometry(QtCore.QRect(1550,170,250,60))
        self.lineBureauName.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBureauName.setAlignment(Qt.AlignCenter)

        self.lineBureauPassword = QLineEdit(self)
        self.lineBureauPassword.setPlaceholderText("PASSWORD")
        self.lineBureauPassword.setObjectName("lineBureauPassword")
        self.lineBureauPassword.setFont(self.font_LineEdit)
        self.lineBureauPassword.setGeometry(QtCore.QRect(1550,250,250,60))
        self.lineBureauPassword.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBureauPassword.setAlignment(Qt.AlignCenter)

        self.lineBureauAddress = QLineEdit(self)
        self.lineBureauAddress.setPlaceholderText("ADDRESS")
        self.lineBureauAddress.setObjectName("lineBureauAddress")
        self.lineBureauAddress.setFont(self.font_LineEdit)
        self.lineBureauAddress.setGeometry(QtCore.QRect(1550,330,250,60))
        self.lineBureauAddress.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBureauAddress.setAlignment(Qt.AlignCenter)
        
        self.lineBureauPhone = QLineEdit(self)
        self.lineBureauPhone.setPlaceholderText("PHONE NUMBER")
        self.lineBureauPhone.setObjectName("lineBureauPhone")
        self.lineBureauPhone.setFont(self.font_LineEdit)
        self.lineBureauPhone.setGeometry(QtCore.QRect(1550,410,250,60))
        self.lineBureauPhone.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBureauPhone.setAlignment(Qt.AlignCenter)

        self.lineBureauEmail = QLineEdit(self)
        self.lineBureauEmail.setPlaceholderText("BUREAU EMAIL")
        self.lineBureauEmail.setObjectName("lineBureauEmail")
        self.lineBureauEmail.setFont(self.font_LineEdit)
        self.lineBureauEmail.setGeometry(QtCore.QRect(1550,490,250,60))
        self.lineBureauEmail.setStyleSheet("color: #50311F;background-color: #D7D3CA; padding:5px; border-radius: 10px")
        self.lineBureauEmail.setAlignment(Qt.AlignCenter)

        self.btnBureauSave = QPushButton("KAYDET", self)
        self.btnBureauSave.setObjectName("btnBureauSave")
        self.btnBureauSave.setFont(self.font_button)
        self.btnBureauSave.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnBureauSave.setGeometry(QtCore.QRect(1550,770,250,60))

        self.btnBureauCancel = QPushButton("ÇIKIŞ", self)
        self.btnBureauCancel.setObjectName("btnBureauCancel")
        self.btnBureauCancel.setFont(self.font_button)
        self.btnBureauCancel.setStyleSheet("color: #50311F; background-color: #B19158; padding:5px; border-radius: 10px")
        self.btnBureauCancel.setGeometry(QtCore.QRect(1550,850,250,60))


        self.widgets = [
            (self.groupBox, 1050, 150, 350, 780),
            (self.lineName, 1100, 170, 250, 60),
            (self.lineSurname, 1100, 250, 250, 60),
            (self.lineEmail, 1100, 330, 250, 60),
            (self.linePassword, 1100, 410, 250, 60),
            (self.linePhone, 1100, 490, 250, 60),
            (self.lineBaroId, 1100, 570, 250, 60),
            (self.lineBaroNumber, 1100, 650, 250, 60),
            (self.btnSave, 1100, 770, 250, 60),
            (self.btnCancel, 1100, 850, 250, 60),

            (self.groupBox2, 1500, 150, 350, 780),
            (self.lineBureauName, 1550, 170, 250, 60),
            (self.lineBureauPassword, 1550, 250, 250, 60),
            (self.lineBureauAddress, 1550, 330, 250, 60),
            (self.lineBureauPhone, 1550, 410, 250, 60),
            (self.lineBureauEmail, 1550, 490, 250, 60),
            (self.btnBureauSave, 1550, 770, 250, 60),
            (self.btnBureauCancel, 1550, 850, 250, 60),

            (self.labelTitle, 1000, 40, 900, 80),
        ]

        self.lineedit_widgets = [
            self.lineName, self.lineSurname, self.lineEmail, self.linePassword,
            self.linePhone, self.lineBaroId, self.lineBaroNumber,
            self.lineBureauName, self.lineBureauPassword, self.lineBureauAddress,
            self.lineBureauPhone, self.lineBureauEmail
        ]


        self.button_widgets = [
            self.btnSave, self.btnCancel, self.btnBureauSave, self.btnBureauCancel
        ]
        self.group_lawyer_widgets = [
            self.groupBox,
            self.lineName, 
            self.lineSurname, 
            self.lineEmail, 
            self.linePassword,
            self.linePhone, 
            self.lineBaroId, 
            self.lineBaroNumber,
            self.btnSave, 
            self.btnCancel
        ]

        # BÜRO TARAFI WIDGETLARI LISTESI
        self.group_bureau_widgets = [
            self.groupBox2,
            self.lineBureauName, 
            self.lineBureauPassword, 
            self.lineBureauAddress,
            self.lineBureauPhone, 
            self.lineBureauEmail,
            self.btnBureauSave, 
            self.btnBureauCancel
        ]
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
            widget.setGeometry(new_x, new_y, new_w, new_h)

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

        self.font_label.setPointSizeF(new_label_size)   
        self.labelTitle.setFont(self.font_label)

        

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
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormRegisterPage()
    window.show()
    sys.exit(app.exec_())