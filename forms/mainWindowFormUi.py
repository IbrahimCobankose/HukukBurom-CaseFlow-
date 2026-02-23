# forms/mainWindowFormUi.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton,
    QCalendarWidget, QTextEdit, QLabel
)
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wood Style Dashboard")
        self.resize(1200, 700)
        self.setObjectName("FormMainWindow")

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
        # === Ana düzen ===
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.main_layout)
        
        # === Menü çerçevesi ===
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
        self.buttons_layout.setSpacing(20)

        self.btnHome = self.create_button("Ana Sayfa")
        self.btnHome.setObjectName("btnHome")

        self.btnCases = self.create_button("Davalar")
        self.btnCases.setObjectName("btnCases")
        
        self.btnFinancialManag = self.create_button("Finansal Yönetim")
        self.btnFinancialManag.setObjectName("btnFinancialManag")
        
        self.btnLegislation = self.create_button("Mevzuat")
        self.btnLegislation.setObjectName("btnLegislation")
        
        self.btnPetitions = self.create_button("Dilekçe Örnekleri")
        self.btnPetitions.setObjectName("btnPetitions")
        
        self.btnArchive = self.create_button("Arşiv")
        self.btnArchive.setObjectName("btnArchive")

        self.btnAddLawyer = self.create_button("Bürom")
        self.btnAddLawyer.setObjectName("btnAddLawyer")
        
        self.btnExit = self.create_button("Çıkış")
        self.btnExit.setObjectName("btnExit")

        # --- Butonları sırayla ekle ---
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

        # === Sağ Alan ===
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(40, 40, 40, 40)
        self.right_layout.setSpacing(20)

        # Takvim
        self.calendarWidget = QCalendarWidget()
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: #e0c097;
                background-color: #f8e0b0;
                selection-background-color: #a0522d;
                color: #4b2e05;
                font-family: 'Palatino Linotype';
                font-size: 16px;
                border-radius: 10px;
                border: 2px solid #8b5a2b;
            }
            QCalendarWidget QAbstractItemView:enabled {
                selection-background-color: #a0522d;
                selection-color: white;
                background-color: #f2d7b6;
                color: #4b2e05;
                border: 1px solid #8b5a2b;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #b87333;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                background-color: #b87333;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #cd853f;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #8b5a2b;
            }
        """)
        self.right_layout.addWidget(self.calendarWidget, stretch=3)

        # Bilgilendirme Kutusu
        self.note_frame = QFrame()
        self.note_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(184, 115, 51, 60%);
                border-radius: 10px;
                border: 2px solid #8b5a2b;
            }
        """)
        info_layout = QVBoxLayout(self.note_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setSpacing(10)

        label = QLabel("Yaklaşan Davalar")
        label.setStyleSheet("font-family: 'Palatino Linotype'; color: white; font-weight: bold; font-size: 16px;")
        info_layout.addWidget(label)

        self.textDateNote = QTextEdit()
        self.textDateNote.setObjectName("textDateNote")
        self.textDateNote.setReadOnly(True)
        self.textDateNote.setStyleSheet("""
            QTextEdit {
                background-color: #f8e0b0;
                color: #4b2e05;
                font-family: 'Palatino Linotype';
                font-size: 18px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
            }
        """)
        self.textDateNote.setText(
            "📅 12 Kasım 2025 - Ankara 2. Asliye Hukuk Mahkemesi\n"
            "📅 14 Kasım 2025 - İstanbul Bölge Adliye Mahkemesi\n"
            "📅 20 Kasım 2025 - İzmir 1. İş Mahkemesi"
        )
        info_layout.addWidget(self.textDateNote, stretch=1)
        self.right_layout.addWidget(self.note_frame, stretch=1)

        # Arka plan Label'ı artık gerekli değil çünkü paintEvent kullanıyoruz
        # self.background kodu silindi

        # Yerleşim
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.right_widget, stretch=1)

    def create_button(self, text):
        """Dinamik boyutlu buton oluşturur."""
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
    
    def resizeEvent(self, event):
        """Dinamik ölçekleme"""
        width = self.width()
        height = self.height()

        # Menü genişliği toplam genişliğin %20'si olsun
        menu_width = int(width * 0.2)
        self.menu_widget.setFixedWidth(menu_width)

        # Buton boyutlarını da biraz orantılı ayarla
        button_height = max(40, int(self.height() * 0.06))
        for i in range(self.buttons_layout.count()):
            item = self.buttons_layout.itemAt(i).widget()
            if isinstance(item, QPushButton):
                item.setMinimumHeight(button_height)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormMainWindow()
    window.show()
    sys.exit(app.exec_())