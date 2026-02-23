# forms/casesFormUi.py

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QFont
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
import sys

# Resimlerin olduğu dosyayı içe aktarıyoruz
try:
    import resources
except ImportError:
    resources = None

class Ui_FormCases(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("FormCases")
        self.setWindowTitle("Wood Theme - Transparent Table")
        self.resize(1900, 1000)

        # --- ARKA PLAN RESMİNİ YÜKLEME (Background 2) ---
        self.background = QtGui.QPixmap()
        
        # resources.py içinde 'background_img2' varsa onu yükle
        if resources and hasattr(resources, 'background_img2'):
             self.background.loadFromData(QByteArray.fromBase64(resources.background_img2))
        # Yedek olarak background_img varsa onu dene
        elif resources and hasattr(resources, 'background_img'):
             self.background.loadFromData(QByteArray.fromBase64(resources.background_img))
        # ------------------------------------------------
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setupUI()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.background.isNull():
            scaled = self.background.scaled(
                self.size(),
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)

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

    def setupUI(self):

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

        # Butonları ekle
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

        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(10)

        font_label = QFont("Bodoni MT Condensed", 40, QFont.Bold)

        self.label = QtWidgets.QLabel("Aktif Davalar")
        self.label.setObjectName("LawyerLabel")
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: #F5F5DC; padding:5px; border-radius: 10px")
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.tableView = QtWidgets.QTableView()
        self.tableView.setObjectName("tableView")
        
        self.tableView.setStyleSheet("""
            QTableView {
                border: 1px solid rgba(139,94,60,180);
                gridline-color: #C89F77;
                color: #2D1E12;
                font-family: 'Palatino Linotype';
                font-size: 10pt;
                selection-background-color: rgba(200,159,119,180);
                selection-color: white;
            }

            QHeaderView::section {
                background-color: rgba(139,94,60,220);
                color: #F5F1E3;
                font-weight: bold;
                border: none;
                padding: 6px;
                border-right: 1px solid #C89F77;
            }

            QTableView::item:hover {
                background-color: rgba(220,199,170,150);
            }

            QTableCornerButton::section {
                background-color: rgba(139,94,60,220);
                border: none;
            }
        """)

        self.btnAction = QtWidgets.QPushButton("Yeni Dava Ekle")
        self.btnAction.setObjectName("btnAction")
        self.btnAction.setFixedWidth(300)
        self.btnAction.setFixedHeight(60)
        self.btnAction.setStyleSheet("""
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

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.btnAction)
        self.button_layout.addStretch()
        
        self.tableView.setMinimumHeight(700)

        self.content_layout.addWidget(self.label)
        self.content_layout.addWidget(self.tableView)
        self.content_layout.addLayout(self.button_layout)
        self.content_layout.addStretch()

        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addWidget(self.content_widget)

        # Örnek Veriler (Gerçek uygulamada burası veritabanından dolacak)
        headers = [
            "CaseID", "CaseTitle", "CaseNumber", "Status",
            "CreationDate", "LawyerId", "LawyerName", "ClientFullname"
        ]
        model = QStandardItemModel(0, len(headers))
        model.setHorizontalHeaderLabels(headers)

        cases = [
            (1001, "Property Dispute", "P-2024-11", "Active", "2024-10-05", 201, "Ahmet Yılmaz", "Ali Demir"),
            (1002, "Contract Breach", "C-2024-02", "Closed", "2024-09-12", 202, "Mehmet Kaya", "Elif Öztürk"),
            (1003, "Divorce Case", "D-2024-15", "Active", "2024-07-21", 203, "Selin Arslan", "Ayşe Kara"),
            (1004, "Criminal Defense", "CR-2024-07", "Closed", "2024-05-30", 204, "Baran Çelik", "Fatih Yıldız"),
            # ... diğer örnek veriler ...
        ]

        for row, case in enumerate(cases):
            for col, value in enumerate(case):
                item = QStandardItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                if row % 2 == 0:
                    item.setBackground(QColor(("#F5F5DC"))) # krem
                else:
                    item.setBackground(QColor(237, 227, 207, 245))  # açık odun tonu

                model.setItem(row, col, item)

        self.tableView.setModel(model)

        header = self.tableView.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def resizeEvent(self, event):
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))

        button_height = max(40, int(self.height() * 0.06))
        for i in range(self.buttons_layout.count()):
            item = self.buttons_layout.itemAt(i).widget()
            if isinstance(item, QPushButton):
                item.setMinimumHeight(button_height)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormCases()
    window.show()
    sys.exit(app.exec_())