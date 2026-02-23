# forms/petitionsFormUi.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormPetitions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dilekçeler")
        self.resize(1200, 700)

        # --- ARKA PLAN RESMİNİ YÜKLEME (Background 2) ---
        self.background_pixmap = QtGui.QPixmap()
        
        # resources.py içinde 'background_img2' varsa onu yükle
        if resources and hasattr(resources, 'background_img2'):
             self.background_pixmap.loadFromData(QByteArray.fromBase64(resources.background_img2))
        # Yedek olarak background_img varsa onu dene
        elif resources and hasattr(resources, 'background_img'):
             self.background_pixmap.loadFromData(QByteArray.fromBase64(resources.background_img))
        # ------------------------------------------------

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.initUI()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.background_pixmap.isNull():
            scaled = self.background_pixmap.scaled(
                self.size(),
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)
        super().paintEvent(event)
    
    def create_button(self, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(50)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #b87333;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid #8b5a2b;
            }
            QPushButton:hover {
                background-color: #cd853f;
            }
            QPushButton:pressed {
                background-color: #a0522d;
            }
        """)
        return btn

    def initUI(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.menu_widget = QtWidgets.QFrame()
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))
        self.menu_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(120, 70, 30, 150);
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }
        """)

        self.buttons_layout = QVBoxLayout(self.menu_widget)
        self.buttons_layout.setContentsMargins(20, 40, 20, 40)
        self.buttons_layout.setSpacing(20)


        self.btnHome = self.create_button("Ana Sayfa")
        self.btnCases = self.create_button("Davalar")
        self.btnFinancialManag = self.create_button("Finansal Yönetim")
        self.btnLegislation = self.create_button("Mevzuat")

        self.btnPetitions = self.create_button("Dilekçe Örnekleri")
        self.btnArchive = self.create_button("Arşiv")
        self.btnAddLawyer = self.create_button("Bürom")
        self.btnExit = self.create_button("Çıkış")

        for btn in [
            self.btnHome,
            self.btnCases,
            self.btnFinancialManag,
            self.btnLegislation,
            self.btnPetitions,
            self.btnArchive,
            self.btnAddLawyer,
            self.btnExit,
        ]:
            self.buttons_layout.addWidget(btn)

        self.buttons_layout.addStretch()

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(200, 0, 200, 0)
        self.right_layout.setSpacing(10)
        self.right_layout.setAlignment(Qt.AlignCenter)


        self.buttons_container = QVBoxLayout()
        self.buttons_container.setAlignment(Qt.AlignTop)
        self.buttons_container.setSpacing(12)

        self.button_style = """
            QPushButton {
                background-color: #a4632d;
                color: white;
                font-weight: bold;
                border-radius: 12px;
                font-size: 17px;
            }
            QPushButton:hover { background-color: #cd853f; }
            QPushButton:pressed { background-color: #a0522d; }
        """

        self.btnAddPetition = QPushButton("DİLEKÇE EKLE")
        self.btnAddPetition.setObjectName("btnAddPetition")

        self.pushButton_2 = QPushButton("Anlaşmalı Boşanma Dilekçesi")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QPushButton("Arsa Payının Düzeltilmesi Dilekçesi")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QPushButton("Ayrılık İstemli Dava Dilekçesi")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QPushButton("Çalışma İzni Talebi Dilekçesi")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QPushButton("Çek İptali Dilekçesi")
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QPushButton("Davadan Feragat Dilekçesi")
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QPushButton("Dava Dosyalarının Birleştirilmesi Dilekçesi")
        self.pushButton_8.setObjectName("pushButton_8")

        self.pushButton_9 = QPushButton("Evlenmeye İzin Talebi Dilekçesi")
        self.pushButton_9.setObjectName("pushButton_9")

        self.pushButton_10 = QPushButton("İdari Para Cezasına İtiraz Dilekçesi")
        self.pushButton_10.setObjectName("pushButton_10")

        self.pushButton_11 = QPushButton("İsim Değiştirilmesi Dilekçesi")
        self.pushButton_11.setObjectName("pushButton_11")


        self.all_buttons = [
            self.btnAddPetition, self.pushButton_2, self.pushButton_3, self.pushButton_4,
            self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8,
            self.pushButton_9, self.pushButton_10, self.pushButton_11
        ]

        for btn in self.all_buttons:
            btn.setStyleSheet(self.button_style)
            self.buttons_container.addWidget(btn)

        self.right_layout.addLayout(self.buttons_container)

        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addLayout(self.right_layout)

    def resizeEvent(self, event):
        # self.background.setGeometry kodu kaldırıldı (paintEvent kullanılıyor)
        
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))

        button_width = int(self.width() * 0.42)  # pencerenin %42'si

        button_height = max(35, int((self.height() * 0.75) / 16))  

        for btn in self.all_buttons:
            btn.setFixedWidth(button_width)
            btn.setFixedHeight(button_height)

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormPetitions()
    window.show()
    sys.exit(app.exec_())