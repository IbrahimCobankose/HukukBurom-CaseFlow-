
import os
import shutil
import json
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QFileDialog, QInputDialog, QMessageBox, QPushButton, QMenu, 
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout
)
from forms.petitionsFormUi import Ui_FormPetitions
from views.MenuBase import MenuBase

class formPetitions(QtWidgets.QWidget, MenuBase):
    def __init__(self, current_user_id=None):
        super(formPetitions, self).__init__()
        
        self.ui = Ui_FormPetitions()
        
        container_layout = QtWidgets.QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.ui)
        
        self.current_user_id = current_user_id
        
        self.samples_folder = "Petition Samples"
        self.data_file = "petitions_data.json"
        
        if not os.path.exists(self.samples_folder):
            os.makedirs(self.samples_folder)

        self.setup_menu(self.ui)
        
        self.setup_dynamic_ui()
        
        self.petition_list = self.load_data()
        self.refresh_petition_list()

    def setup_dynamic_ui(self):
        
        if hasattr(self.ui, 'buttons_container'):
            while self.ui.buttons_container.count():
                item = self.ui.buttons_container.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
        
        self.btn_add_ref = self.ui.btnAddPetition
        self.btn_add_ref.setParent(None) 
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(100, 10, 100, 10)
        
        self.scroll_area.setWidget(self.scroll_content)
        
        self.ui.right_layout.insertWidget(0, self.btn_add_ref)
        self.ui.right_layout.insertWidget(1, self.scroll_area)
        
        try: self.btn_add_ref.clicked.disconnect()
        except: pass
        self.btn_add_ref.clicked.connect(self.add_new_petition)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self.get_default_petitions()
        else:
            defaults = self.get_default_petitions()
            self.save_data(defaults)
            return defaults

    def save_data(self, data):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri kaydedilemedi: {e}")

    def get_default_petitions(self):
        return [
            {"name": "Anlaşmalı Boşanma Dilekçesi", "file": "anlasmali-bosanma-dilekcesi.doc"},
            {"name": "Arsa Payının Düzeltilmesi", "file": "arsa-payinin-duzeltilmesi.doc"},
            {"name": "Çek İptali Dilekçesi", "file": "cek-iptali.doc"},
        ]

    def refresh_petition_list(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for item in self.petition_list:
            self.create_petition_row(item["name"], item["file"])

    def create_petition_row(self, display_name, filename):
        
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)
        

        btn_download = QPushButton(display_name)
        btn_download.setMinimumHeight(50)
        btn_download.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        btn_download.setStyleSheet("""
            QPushButton {
                background-color: #a4632d;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                font-size: 16px;
                border: 1px solid #8b5a2b;
            }
            QPushButton:hover { background-color: #cd853f; }
            QPushButton:pressed { background-color: #a0522d; }
        """)
        
      
        btn_download.clicked.connect(lambda checked, f=filename: self.download_petition(f))
        
        btn_delete = QPushButton("SİL")
        btn_delete.setFixedSize(80, 50)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #8b0000;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                font-size: 14px;
                border: 1px solid #500000;
            }
            QPushButton:hover { background-color: #ff4444; }
            QPushButton:pressed { background-color: #500000; }
        """)
        
        btn_delete.clicked.connect(lambda checked, f=filename, n=display_name: self.delete_petition(f, n))
        
        row_layout.addWidget(btn_download)
        row_layout.addWidget(btn_delete)
        
        self.scroll_layout.addWidget(row_widget)

    def add_new_petition(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Yüklenecek Dilekçe Dosyasını Seçin", "", 
            "Word/PDF Files (*.doc *.docx *.pdf *.txt);;All Files (*)", options=options
        )
        
        if not file_path: return 

        text, ok = QInputDialog.getText(self, 'Dilekçe Adı', 'Buton üzerinde görünecek ismi giriniz:')
        if not ok or not text: return 

        try:
            original_filename = os.path.basename(file_path)
            

            unique_filename = f"{int(time.time())}_{original_filename}"
            
            destination_path = os.path.join(self.samples_folder, unique_filename)
            
            shutil.copy(file_path, destination_path)
            
            new_item = {"name": text, "file": unique_filename}
            self.petition_list.append(new_item)
            self.save_data(self.petition_list)
            
            self.refresh_petition_list()
            
            QMessageBox.information(self, "Başarılı", "Dilekçe başarıyla eklendi!")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kopyalanırken hata oluştu: {e}")

    def delete_petition(self, filename, display_name):

        reply = QMessageBox.question(
            self, 'Silme Onayı', 
            f"'{display_name}' adlı dilekçeyi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                file_path = os.path.join(self.samples_folder, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

                self.petition_list = [p for p in self.petition_list if p['file'] != filename]
                self.save_data(self.petition_list)
                

                self.refresh_petition_list()
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Silme işlemi sırasında hata oluştu: {e}")

    def download_petition(self, file_name):
        source_path = os.path.join(self.samples_folder, file_name)

        if not os.path.exists(source_path):
            QMessageBox.warning(self, "Hata", f"Kaynak dosya bulunamadı:\n{source_path}")
            return


        clean_name = file_name.split('_', 1)[-1] if '_' in file_name else file_name

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Dilekçeyi Farklı Kaydet", clean_name,
            "All Files (*)", options=options
        )

        if save_path:
            try:
                shutil.copy(source_path, save_path)
                QMessageBox.information(self, "Başarılı", f"Dilekçe kaydedildi:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaydetme hatası: {e}")

    def resizeEvent(self, event):
        if hasattr(self.ui, 'background'):
             self.ui.background.setGeometry(0, 0, self.width(), self.height())
        if hasattr(self.ui, 'menu_widget'):
             self.ui.menu_widget.setFixedWidth(int(self.width() * 0.2))    
        super().resizeEvent(event)