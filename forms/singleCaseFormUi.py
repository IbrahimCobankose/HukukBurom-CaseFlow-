# forms/singleCaseFormUi.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QByteArray
import sys


try:
    import resources
except ImportError:
    resources = None

class Ui_FormSingleCase(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dava Detay")
        self.setObjectName("FormSingleCase")
        self.resize(1600, 1000)

        # --- ARKA PLAN RESMİNİ YÜKLEME ---
        self.background_pixmap = QtGui.QPixmap()
        if resources and hasattr(resources, 'background_img2'):
            self.background_pixmap.loadFromData(QByteArray.fromBase64(resources.background_img2))
        
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

        # === SOL MENÜ ÇERÇEVESİ ===
        self.menu_widget = QtWidgets.QFrame()
        self.menu_widget.setObjectName("menuFrame") # ID çakışmasını önlemek için düzelttim
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

        # Butonlar
        self.btnHome = self.create_button("Ana Sayfa")
        self.btnCases = self.create_button("Davalar")
        self.btnFinancialManag = self.create_button("Finansal Yönetim")
        self.btnLegislation = self.create_button("Mevzuat")
        self.btnPetitions = self.create_button("Dilekçe Örnekleri")
        self.btnArchive = self.create_button("Arşiv")
        self.btnAddLawyer = self.create_button("Bürom")
        self.btnExit = self.create_button("Çıkış")

        # Butonları ekle (UYAP kaldırıldı)
        for btn in [self.btnHome, self.btnCases, self.btnFinancialManag, 
                    self.btnLegislation, self.btnPetitions, self.btnArchive, 
                    self.btnAddLawyer, self.btnExit]:
            self.buttons_layout.addWidget(btn)

        self.buttons_layout.addStretch()

        # === SAĞ İÇERİK ALANI ===
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(40, 100, 40, 60)
        self.right_layout.setSpacing(40)
        self.right_layout.setAlignment(Qt.AlignTop)

        self.form_container = QHBoxLayout()
        self.form_container.setSpacing(80)
        self.form_container.setAlignment(Qt.AlignTop)

        self.left_column = QVBoxLayout()
        self.left_column.setSpacing(30)

        self.right_column = QVBoxLayout()
        self.right_column.setSpacing(30)

        self.form_container.addLayout(self.left_column, 1)
        self.form_container.addLayout(self.right_column, 1)

        # Form elemanlarını oluştur
        self.create_form_elements()

        # Doküman ve Güncelle butonlarını içeren satırı buraya (initUI) veya create_form_elements'e ekleyebiliriz.
        # Sizin önceki yapınızda initUI'daydı, bütünlük açısından buraya ekliyorum:
        
        # --- SATIR 4 (Doküman ve Butonlar) ---
        row4_left = QHBoxLayout()
        self.c1 = QLabel("Doküman:")
        self.c1.setObjectName("c1")
        self.c1.setFont(QtGui.QFont("Palatino Linotype", 14))
        self.c1.setFixedWidth(160) # create_form_elements'te atanan değerle aynı olmalı

        # --- PDF İKONUNU YÜKLEME ---
        self.labelDocument1 = QLabel()
        self.labelDocument1.setObjectName("labelDocument1")
        self.labelDocument1.setAlignment(QtCore.Qt.AlignCenter)
        
        pixmap_pdf = QtGui.QPixmap()
        if resources and hasattr(resources, 'pdf_icon_img'):
             pixmap_pdf.loadFromData(QByteArray.fromBase64(resources.pdf_icon_img))
        
        if not pixmap_pdf.isNull():
            self.labelDocument1.setPixmap(pixmap_pdf)
            self.labelDocument1.setScaledContents(True)
        else:
            self.labelDocument1.setText("📄") # Resim yoksa emoji göster
            self.labelDocument1.setStyleSheet("font-size: 30px;")
            
        self.labelDocument1.setFixedSize(50, 50)

        self.btnAdd = QPushButton("Doküman Ekle")
        self.btnAdd.setObjectName("btnAdd")

        row4_left.addWidget(self.c1)
        row4_left.addWidget(self.labelDocument1)
        row4_left.addWidget(self.btnAdd)

        row4_right = QHBoxLayout()
        self.btnUpdate = QPushButton("Güncelle")
        self.btnUpdate.setObjectName("btnUpdate")
        
        # UYAP butonu kaldırıldı
        row4_right.addWidget(self.btnUpdate)

        self.left_column.addLayout(row4_left)
        self.right_column.addLayout(row4_right)
        
        # -------------------------------------

        self.right_layout.addLayout(self.form_container)

        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addLayout(self.right_layout, stretch=1)

    def create_form_elements(self):
        self.label_width = 160
        
        # Ortak Stil Tanımları
        input_style = """
            QLineEdit, QTextEdit {
                font-family: 'Palatino Linotype';
                font-size: 17px;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #8b5a2b;
                background-color: #fff8f0;                   
            }
        """
        
        # --- SATIR 1 ---
        row1_left = QHBoxLayout()
        self.labelTitle = QLabel("Dava Başlığı:")
        self.labelTitle.setFixedWidth(self.label_width)
        self.lineTitle = QLineEdit()
        self.lineTitle.setStyleSheet(input_style)
        row1_left.addWidget(self.labelTitle)
        row1_left.addWidget(self.lineTitle)

        row1_right = QHBoxLayout()
        self.labelNumber = QLabel("Dava Numarası:")
        self.labelNumber.setFixedWidth(self.label_width)
        self.lineNumber = QLineEdit()
        self.lineNumber.setStyleSheet(input_style)
        row1_right.addWidget(self.labelNumber)
        row1_right.addWidget(self.lineNumber)

        self.left_column.addLayout(row1_left)
        self.right_column.addLayout(row1_right)

        # --- SATIR 2 ---
        row2_left = QHBoxLayout()
        self.labelStatus = QLabel("Dava Durumu:")
        self.labelStatus.setFixedWidth(self.label_width)
        self.lineStatus = QLineEdit()
        self.lineStatus.setStyleSheet(input_style)
        row2_left.addWidget(self.labelStatus)
        row2_left.addWidget(self.lineStatus)

        row2_right = QHBoxLayout()
        self.labelLawyers = QLabel("Avukat:")
        self.labelLawyers.setFixedWidth(self.label_width)
        self.lineLawyers = QLineEdit()
        self.lineLawyers.setStyleSheet(input_style)
        row2_right.addWidget(self.labelLawyers)
        row2_right.addWidget(self.lineLawyers)

        self.left_column.addLayout(row2_left)
        self.right_column.addLayout(row2_right)

        # --- SATIR 3 ---
        row3_left = QHBoxLayout()
        self.labelClients = QLabel("Müvekkil:")
        self.labelClients.setFixedWidth(self.label_width)
        self.lineClients = QLineEdit()
        self.lineClients.setStyleSheet(input_style)
        row3_left.addWidget(self.labelClients)
        row3_left.addWidget(self.lineClients)

        row3_right = QHBoxLayout()
        self.labelOpponents = QLabel("Karşı Taraf:")
        self.labelOpponents.setFixedWidth(self.label_width)
        self.lineOpponents = QLineEdit()
        self.lineOpponents.setStyleSheet(input_style)
        row3_right.addWidget(self.labelOpponents)
        row3_right.addWidget(self.lineOpponents)

        self.left_column.addLayout(row3_left)
        self.right_column.addLayout(row3_right)

        # --- SATIR 5 (Açıklama ve Not) ---
        row5_left = QHBoxLayout()
        self.labelDescription = QLabel("Açıklama:")
        self.labelDescription.setFixedWidth(self.label_width)
        self.textDescription = QTextEdit()
        self.textDescription.setStyleSheet(input_style)
        self.textDescription.setFixedHeight(150)
        row5_left.addWidget(self.labelDescription)
        row5_left.addWidget(self.textDescription)

        row5_right = QHBoxLayout()
        self.labelNote = QLabel("Not:")
        self.labelNote.setFixedWidth(self.label_width)
        self.textNote = QTextEdit()
        self.textNote.setStyleSheet(input_style)
        self.textNote.setFixedHeight(150)
        row5_right.addWidget(self.labelNote)
        row5_right.addWidget(self.textNote)

        self.left_column.addLayout(row5_left)
        self.right_column.addLayout(row5_right)

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

    def resizeEvent(self, event):
        # Menü genişliği %20
        self.menu_widget.setFixedWidth(int(self.width() * 0.2))

        # Buton yüksekliği
        button_height = max(40, int(self.height() * 0.06))
        for i in range(self.buttons_layout.count()):
            item = self.buttons_layout.itemAt(i).widget()
            if isinstance(item, QPushButton):
                item.setMinimumHeight(button_height)

        self.adjust_form_elements()
        super().resizeEvent(event)

    def adjust_form_elements(self):
        # Dinamik boyutlandırma
        base_width = self.width()
        base_height = self.height()
        
        font_size = max(12, int(base_height * 0.018))
        label_style = f"color: white; font-size: {font_size}px; font-weight: bold; font-family: 'Palatino Linotype';"
        
        button_style = f"""
            QPushButton {{
                background-color: #a4632d;
                color: white;
                font-size: {font_size}px;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid #8b5a2b;
            }}
            QPushButton:hover {{ background-color: #cd853f; }}
            QPushButton:pressed {{ background-color: #a0522d; }}
        """
        
        self.label_width = max(120, int(base_width * 0.08))
        
        # Tüm label'ları güncelle
        labels = [
            self.labelTitle, self.labelNumber,
            self.labelStatus, self.labelLawyers,
            self.labelClients, self.labelOpponents,
            self.labelDescription, self.labelNote,
            self.c1
        ]
        
        for label in labels:
            label.setStyleSheet(label_style)
            label.setFixedWidth(self.label_width)
        
        # Doküman ikonu boyutu
        icon_size = max(40, int(min(base_width, base_height) * 0.025))
        self.labelDocument1.setFixedSize(icon_size, icon_size)

        # Form buton stilleri
        self.btnAdd.setStyleSheet(button_style)
        self.btnUpdate.setStyleSheet(button_style)
        
        # TextEdit ve LineEdit yükseklikleri
        textedit_height = max(100, int(base_height * 0.15))
        self.textDescription.setFixedHeight(textedit_height)
        self.textNote.setFixedHeight(textedit_height)
        
        input_height = max(30, int(base_height * 0.04))
        line_edits = [
            self.lineTitle, self.lineNumber,
            self.lineStatus, self.lineLawyers,
            self.lineClients, self.lineOpponents
        ]
        
        for line_edit in line_edits:
            line_edit.setMinimumHeight(input_height)
        
        button_height = max(35, int(base_height * 0.045))
        self.btnAdd.setMinimumHeight(button_height)
        self.btnUpdate.setMinimumHeight(button_height)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_FormSingleCase()
    window.show()
    sys.exit(app.exec_())