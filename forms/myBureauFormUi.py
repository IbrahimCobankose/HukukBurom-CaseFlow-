# forms/myBureauFormUi.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton,
    QCalendarWidget, QTextEdit, QLabel,
)
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormMyBureau(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FormMyBureau")
        self.setObjectName("FormMyBureau")
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

    def initUI(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # QLabel ile arka plan yükleme kısmı SİLİNDİ (paintEvent kullanılıyor)
        
        self.menu_widget = QtWidgets.QFrame()
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))
        self.menu_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(120, 70, 30, 150); /* yarı saydam kahverengi */
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }
        """)

        self.buttons_layout = QVBoxLayout(self.menu_widget)
        self.buttons_layout.setContentsMargins(20, 40, 20, 40)
        self.buttons_layout.setSpacing(15)  # Daha az boşluk

        self.btnHome = self.create_button("Ana Sayfa")
        self.btnHome.setObjectName("btnHome")
        self.buttons_layout.addWidget(self.btnHome)

        self.btnCases = self.create_button("Davalar")
        self.btnCases.setObjectName("btnCases")
        self.buttons_layout.addWidget(self.btnCases)
        
        self.btnFinancialManag = self.create_button("Finansal Yönetim")
        self.btnFinancialManag.setObjectName("btnFinancialManag")
        self.buttons_layout.addWidget(self.btnFinancialManag)
        
        self.btnLegislation = self.create_button("Mevzuat")
        self.btnLegislation.setObjectName("btnLegislation")
        self.buttons_layout.addWidget(self.btnLegislation)
        
        self.btnPetitions = self.create_button("Dilekçe Örnekleri")
        self.btnPetitions.setObjectName("btnPetitions")
        self.buttons_layout.addWidget(self.btnPetitions)
        
        self.btnArchive = self.create_button("Arşiv")
        self.btnArchive.setObjectName("btnArchive")
        self.buttons_layout.addWidget(self.btnArchive)

        self.btnAddLawyer = self.create_button("Bürom")
        self.btnAddLawyer.setObjectName("btnAddLawyer")
        self.buttons_layout.addWidget(self.btnAddLawyer)
        
        self.btnExit = self.create_button("Çıkış")
        self.btnExit.setObjectName("btnExit")
        self.buttons_layout.addWidget(self.btnExit)

        self.buttons_layout.addStretch()

        # === Ana içerik alanı ===
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(40, 100, 40, 40)
        self.content_layout.setSpacing(40)
        
        # --- Label ---
        self.main_label = QLabel("BÜROM")
        self.main_label.setStyleSheet("""
            QLabel {
                font-family: Palatino Linotype;
                font-size: 60px;
                font-weight: bold;
                color: white;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
            }
        """)
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setFixedHeight(90)
        self.content_layout.addWidget(self.main_label)
        
        # --- Satır buton alanı ---
        self.rows_widget = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_widget)
        self.rows_layout.setSpacing(15)
        self.rows_layout.setContentsMargins(100, 10, 100, 10)
        
        # 5 satır oluştur
        self.row_1_widget = QWidget()
        self.row_1_layout = QHBoxLayout(self.row_1_widget)
        self.row_1_layout.setContentsMargins(0, 0, 0, 0)
        self.row_1_layout.setSpacing(15)
        
        self.pushButton = self.create_button2("Avukat 1")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumHeight(50)
        self.pushButton.setMinimumWidth(200)
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.btnDelete1 = self.create_button2("SİL")
        self.btnDelete1.setObjectName("btnDelete1")
        self.btnDelete1.setMinimumHeight(50)
        self.btnDelete1.setMaximumWidth(100)
        self.btnDelete1.setMinimumWidth(60)
        self.btnDelete1.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.row_1_layout.addWidget(self.pushButton, 4)
        self.row_1_layout.addWidget(self.btnDelete1)
        self.rows_layout.addWidget(self.row_1_widget)
        
        # 2. satır
        self.row_2_widget = QWidget()
        self.row_2_layout = QHBoxLayout(self.row_2_widget)
        self.row_2_layout.setContentsMargins(0, 0, 0, 0)
        self.row_2_layout.setSpacing(15)
        
        self.pushButton_2 = self.create_button2("Avukat 2")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumHeight(50)
        self.pushButton_2.setMinimumWidth(200)
        self.pushButton_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.btnDelete2 = self.create_button2("SİL")
        self.btnDelete2.setObjectName("btnDelete2")
        self.btnDelete2.setMinimumHeight(50)
        self.btnDelete2.setMaximumWidth(100)
        self.btnDelete2.setMinimumWidth(60)
        self.btnDelete2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.row_2_layout.addWidget(self.pushButton_2, 4)
        self.row_2_layout.addWidget(self.btnDelete2)
        self.rows_layout.addWidget(self.row_2_widget)
        
        # 3. satır
        self.row_3_widget = QWidget()
        self.row_3_layout = QHBoxLayout(self.row_3_widget)
        self.row_3_layout.setContentsMargins(0, 0, 0, 0)
        self.row_3_layout.setSpacing(15)
        
        self.pushButton_3 = self.create_button2("Avukat 3")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setMinimumHeight(50)
        self.pushButton_3.setMinimumWidth(200)
        self.pushButton_3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.btnDelete3 = self.create_button2("SİL")
        self.btnDelete3.setObjectName("btnDelete3")
        self.btnDelete3.setMinimumHeight(50)
        self.btnDelete3.setMaximumWidth(100)
        self.btnDelete3.setMinimumWidth(60)
        self.btnDelete3.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.row_3_layout.addWidget(self.pushButton_3, 4)
        self.row_3_layout.addWidget(self.btnDelete3)
        self.rows_layout.addWidget(self.row_3_widget)
        
        # 4. satır
        self.row_4_widget = QWidget()
        self.row_4_layout = QHBoxLayout(self.row_4_widget)
        self.row_4_layout.setContentsMargins(0, 0, 0, 0)
        self.row_4_layout.setSpacing(15)
        
        self.pushButton_4 = self.create_button2("Avukat 4")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setMinimumHeight(50)
        self.pushButton_4.setMinimumWidth(200)
        self.pushButton_4.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.btnDelete4 = self.create_button2("SİL")
        self.btnDelete4.setObjectName("btnDelete4")
        self.btnDelete4.setMinimumHeight(50)
        self.btnDelete4.setMaximumWidth(100)
        self.btnDelete4.setMinimumWidth(60)
        self.btnDelete4.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.row_4_layout.addWidget(self.pushButton_4, 4)
        self.row_4_layout.addWidget(self.btnDelete4)
        self.rows_layout.addWidget(self.row_4_widget)
        
        # 5. satır
        self.row_5_widget = QWidget()
        self.row_5_layout = QHBoxLayout(self.row_5_widget)
        self.row_5_layout.setContentsMargins(0, 0, 0, 0)
        self.row_5_layout.setSpacing(15)
        
        self.pushButton_5 = self.create_button2("Avukat 5")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setMinimumHeight(50)
        self.pushButton_5.setMinimumWidth(200)
        self.pushButton_5.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.btnDelete5 = self.create_button2("SİL")
        self.btnDelete5.setObjectName("btnDelete5")
        self.btnDelete5.setMinimumHeight(50)
        self.btnDelete5.setMaximumWidth(100)
        self.btnDelete5.setMinimumWidth(60)
        self.btnDelete5.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.row_5_layout.addWidget(self.pushButton_5, 4)
        self.row_5_layout.addWidget(self.btnDelete5)
        self.rows_layout.addWidget(self.row_5_widget)
        
        self.content_layout.addWidget(self.rows_widget)
        self.content_layout.addStretch()
        
        # --- Sağ alt köşe butonu ---
        self.bottom_right_widget = QWidget()
        self.bottom_right_layout = QHBoxLayout(self.bottom_right_widget)
        self.bottom_right_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_right_layout.addStretch()
        
        self.btnAddLawyer = self.create_button3("Avukat Ekle")
        self.btnAddLawyer.setObjectName("btnAddLawyer")
        self.btnAddLawyer.setFixedSize(120, 35)
        self.bottom_right_layout.addWidget(self.btnAddLawyer)
        
        self.content_layout.addWidget(self.bottom_right_widget)

        # --- Menü ve ana alanı düzenle ---
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.content_widget)
        self.main_layout.setStretchFactor(self.content_widget, 1)

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
    
    def create_button2(self, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(50)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn.setStyleSheet("""
            QPushButton {
                font-family: Palatino Linotype;
                background-color: #a0652c;
                color: white;
                font-size: 20px;
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
    
    def create_button3(self, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(50)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        btn.setStyleSheet("""
            QPushButton {
                font-family: Palatino Linotype;
                background-color: #a0652c;
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

    def resizeEvent(self, event):
        """Dinamik ölçekleme"""
        width = self.width()
        height = self.height()

        # Menü genişliği toplam genişliğin %20'si olsun
        menu_width = int(width * 0.2)
        self.menu_widget.setFixedWidth(menu_width)

        # Buton boyutlarını da biraz orantılı ayarla
        button_height = max(35, int(self.height() * 0.05))
        
        # Tüm menü butonlarını tek tek güncelle
        menu_buttons = [
            self.btnHome, self.btnCases, self.btnFinancialManag, 
            self.btnLegislation,  self.btnPetitions,
            self.btnArchive, self.btnAddLawyer, self.btnExit
        ]
        
        for btn in menu_buttons:
            btn.setMinimumHeight(button_height)

        # Satır butonlarının yüksekliğini dinamik ayarla
        row_button_height = max(45, int(self.height() * 0.07))
        
        # Tüm satır butonlarını tek tek güncelle
        row_long_buttons = [
            self.pushButton, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5
        ]
        
        row_small_buttons = [
            self.btnDelete1, self.btnDelete2, self.btnDelete3,
            self.btnDelete4, self.btnDelete5
        ]
        
        for btn in row_long_buttons:
            btn.setMinimumHeight(row_button_height)
            
        for btn in row_small_buttons:
            btn.setMinimumHeight(row_button_height)

        # background.setGeometry artık gerekli değil çünkü paintEvent kullanıyoruz

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormMyBureau()
    window.show()
    sys.exit(app.exec_())