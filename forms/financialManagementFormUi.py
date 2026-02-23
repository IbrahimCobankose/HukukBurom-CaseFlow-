# forms/financialManagementFormUi.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QComboBox, QTextEdit, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QByteArray
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FinancialManagementForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FinancialManagementForm")
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

        # === MENÜ ALANI ===
        self.menu_widget = QtWidgets.QFrame()
        self.setObjectName("FinancialManagementForm")
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

        # === SAĞ İÇERİK ALANI ===
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 60, 0, 60)
        self.right_layout.setSpacing(30)
        self.right_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # --- Dava Başlığı ---
        row1 = QHBoxLayout()
        row1.addStretch(1)

        self.caseLabel = QLabel("Dava Başlığı:")
        self.caseLabel.setObjectName("caseLabel")
        self.caseLabel.setFixedWidth(120)
        self.caseLabel.setStyleSheet("font-family: 'Palatino Linotype';font-size: 16px; font-weight: bold; color: white;")

        self.caseComboBox = QComboBox()
        self.caseComboBox.setObjectName("caseComboBox")
        self.caseComboBox.addItems(["Seçenek 1-1", "Seçenek 1-2", "Seçenek 1-3"])
        self.caseComboBox.setMinimumWidth(300)
        self.caseComboBox.setStyleSheet("""
            QComboBox {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
            }
        """)

        row1.addWidget(self.caseLabel)
        row1.addWidget(self.caseComboBox)
        row1.addStretch(1)
        self.right_layout.addLayout(row1)

        # --- İşlem Türü ---
        row2 = QHBoxLayout()
        row2.addStretch(1)

        self.typeLabel = QLabel("İşlem Türü:")
        self.typeLabel.setObjectName("typeLabel")
        self.typeLabel.setFixedWidth(120)
        self.typeLabel.setStyleSheet("font-family: 'Palatino Linotype';font-size: 16px; font-weight: bold; color: white;")

        self.typeComboBox = QComboBox()
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItems(["Seçenek 2-1", "Seçenek 2-2", "Seçenek 2-3"])
        self.typeComboBox.setMinimumWidth(300)
        self.typeComboBox.setStyleSheet("""
            QComboBox {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
            }
        """)

        row2.addWidget(self.typeLabel)
        row2.addWidget(self.typeComboBox)
        row2.addStretch(1)
        self.right_layout.addLayout(row2)

        # --- Davacı ---
        row3 = QHBoxLayout()
        row3.addStretch(1)

        self.clientLabel = QLabel("Davacı:")
        self.clientLabel.setObjectName("clientLabel")
        self.clientLabel.setFixedWidth(120)
        self.clientLabel.setStyleSheet("font-family: 'Palatino Linotype';font-size: 16px; font-weight: bold; color: white;")

        self.clientComboBox = QComboBox()
        self.clientComboBox.setObjectName("clientComboBox")
        self.clientComboBox.addItems(["Seçenek 3-1", "Seçenek 3-2", "Seçenek 3-3"])
        self.clientComboBox.setMinimumWidth(300)
        self.clientComboBox.setStyleSheet("""
            QComboBox {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
            }
        """)

        row3.addWidget(self.clientLabel)
        row3.addWidget(self.clientComboBox)
        row3.addStretch(1)
        self.right_layout.addLayout(row3)

        # --- Karşı Taraf ---
        row4 = QHBoxLayout()
        row4.addStretch(1)

        self.defendantLabel = QLabel("Karşı Taraf:")
        self.defendantLabel.setObjectName("defendantLabel")
        self.defendantLabel.setFixedWidth(120)
        self.defendantLabel.setStyleSheet("font-family: 'Palatino Linotype';font-size: 16px; font-weight: bold; color: white;")

        self.opponentComboBox = QComboBox()
        self.opponentComboBox.setObjectName("opponentComboBox")
        self.opponentComboBox.addItems(["Seçenek 4-1", "Seçenek 4-2", "Seçenek 4-3"])
        self.opponentComboBox.setMinimumWidth(300)
        self.opponentComboBox.setStyleSheet("""
            QComboBox {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
            }
        """)

        row4.addWidget(self.defendantLabel)
        row4.addWidget(self.opponentComboBox)
        row4.addStretch(1)
        self.right_layout.addLayout(row4)

        # --- Miktar ---
        row5 = QHBoxLayout()
        row5.addStretch(1)

        self.amountLabel = QLabel("Miktar:")
        self.amountLabel.setObjectName("amountLabel")
        self.amountLabel.setFixedWidth(120)
        self.amountLabel.setStyleSheet("font-family: 'Palatino Linotype';font-size: 16px; font-weight: bold; color: white;")

        self.amountLineEdit = QLineEdit()
        self.amountLineEdit.setObjectName("amountLineEdit")
        self.amountLineEdit.setMinimumWidth(300)
        self.amountLineEdit.setStyleSheet("""
            QLineEdit {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
            }
        """)

        row5.addWidget(self.amountLabel)
        row5.addWidget(self.amountLineEdit)
        row5.addStretch(1)
        self.right_layout.addLayout(row5)

        # --- Mesaj Kutusu ---
        message_layout = QHBoxLayout()
        message_layout.addStretch(1)

        self.message_box = QTextEdit()
        self.message_box.setFixedHeight(160)
        self.message_box.setFixedWidth(600)
        self.message_box.setStyleSheet("""
            QTextEdit {
                font-family: 'Palatino Linotype';
                font-size: 20px;
                border-radius: 10px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;
                padding: 8px;
            }
        """)

        message_layout.addWidget(self.message_box)
        message_layout.addStretch(1)
        self.right_layout.addLayout(message_layout)

        # --- Butonlar ---
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.saveButton = QPushButton("Kaydet")
        self.ClearButton = QPushButton("Temizle")
        self.btnAddReceipt = QPushButton("Fiş/Dekont Al")

        for btn in [self.saveButton, self.ClearButton, self.btnAddReceipt]:
            btn.setMinimumHeight(50)
            btn.setMinimumWidth(130)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #a4632d;
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
            button_layout.addWidget(btn)

        button_layout.addStretch(1)
        self.right_layout.addLayout(button_layout)

        # --- Arka Plan Label'ı (Yedek) ---
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        # Ana Yerleşim
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addLayout(self.right_layout, stretch=1)

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
            QPushButton:hover { background-color: #cd853f; }
            QPushButton:pressed { background-color: #a0522d; }
        """)
        return btn

    def resizeEvent(self, event):
        # Menü genişliği pencere genişliğinin %20'si olsun
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))

        button_height = max(40, int(self.height() * 0.06))
        for i in range(self.buttons_layout.count()):
            item = self.buttons_layout.itemAt(i).widget()
            if isinstance(item, QPushButton):
                item.setMinimumHeight(button_height)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FinancialManagementForm()
    window.show()
    sys.exit(app.exec_())