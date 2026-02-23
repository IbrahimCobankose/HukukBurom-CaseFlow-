
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QMessageBox, QDialog, QVBoxLayout, QFormLayout, 
    QLineEdit, QTextEdit, QComboBox, QPushButton, QHBoxLayout, QLabel, QFileDialog
)
from PyQt5.QtGui import QPixmap
from database.connect_to_database import connect_to_database
from forms.singleCaseFormUi import Ui_FormSingleCase
from views.MenuBase import MenuBase 

class formSingleCase(QtWidgets.QWidget, MenuBase):


    STATUS_MAP_TO_DB = {
        "Hazırlık": "Preparation",
        "Duruşma Aşamasında": "In Trial",
        "Karar Aşamasında": "Awaiting Decision",
        "Sonuçlandı": "Closed"
    }
    STATUS_MAP_FROM_DB = {
        "Preparation": "Hazırlık",
        "In Trial": "Duruşma Aşamasında",
        "Awaiting Decision": "Karar Aşamasında",
        "Closed": "Sonuçlandı"
    }
 

    def __init__(self, current_user_id=None, case_id=None):
        super(formSingleCase, self).__init__()
        
        self.ui = Ui_FormSingleCase()
        
        container_layout = QtWidgets.QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.ui)
        
        self.current_user_id = current_user_id
        self.case_id = case_id
        self.document_path = None

        try:
            self.ui.labelDocument1.installEventFilter(self)
        except Exception as e:
            print(f"Event filter yüklenirken hata: {e}")
    
        self.ui.btnUpdate.clicked.connect(self.update_button_clicked)
        self.ui.btnAdd.clicked.connect(self.add_document_button_clicked)
        
        
        self.setup_menu(self.ui)
        
        if self.case_id:
            self.load_case_data()

    
        if isinstance(self.current_user_id, list):
            self.ui.btnUpdate.setEnabled(False)
            self.ui.btnUpdate.setToolTip("Dava detayları sadece bireysel avukat girişi ile güncellenebilir.")
            self.ui.btnAdd.setEnabled(False)
            self.ui.btnAdd.setToolTip("Doküman sadece bireysel avukat girişi ile eklenebilir.")

    def eventFilter(self, obj, event):
        if obj == self.ui.labelDocument1:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.open_document()
                return True 
                
        return super(formSingleCase, self).eventFilter(obj, event)

    def load_case_data(self):
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)
            
            case_query = "SELECT * FROM cases WHERE case_id = %s;"
            cursor.execute(case_query, (self.case_id,))
            case = cursor.fetchone()
            if case:
                self.ui.lineTitle.setText(case.get('case_title', ''))
                self.ui.lineNumber.setText(case.get('case_number', ''))
                
                eng_status = case.get('case_status', '')
                tr_status = self.STATUS_MAP_FROM_DB.get(eng_status, eng_status)
                self.ui.lineStatus.setText(tr_status)
                
                self.ui.textDescription.setText(case.get('case_description', ''))

            lawyer_query = "SELECT l.name, l.surname FROM lawyers l JOIN case_lawyers cl ON l.lawyer_id = cl.lawyer_id WHERE cl.case_id = %s;"
            cursor.execute(lawyer_query, (self.case_id,))
            lawyers = cursor.fetchall()
            lawyer_names = ", ".join([f"{l['name']} {l['surname']}" for l in lawyers])
            self.ui.lineLawyers.setText(lawyer_names)

            client_query = "SELECT cl.fullname FROM clients cl JOIN case_clients cc ON cl.client_id = cc.client_id WHERE cc.case_id = %s;"
            cursor.execute(client_query, (self.case_id, ))
            clients = cursor.fetchall()
            client_names = ", ".join([c['fullname'] for c in clients])
            self.ui.lineClients.setText(client_names)
            
            opponent_query = "SELECT o.name, o.surname FROM opponents o JOIN case_opponents co ON o.opponent_id = co.opponent_id WHERE co.case_id = %s;"
            cursor.execute(opponent_query, (self.case_id, ))
            opponents = cursor.fetchall()
            opponent_names = ", ".join([f"{o['name']} {o['surname']}" for o in opponents])
            self.ui.lineOpponents.setText(opponent_names)

            note_query = "SELECT note_content FROM case_notes WHERE case_id = %s ORDER BY created_at DESC LIMIT 1;"
            cursor.execute(note_query, (self.case_id,))
            note = cursor.fetchone()
            if note:
                self.ui.textNote.setText(note.get('note_content', ''))

            doc_query = "SELECT file_path, document_name FROM documents WHERE case_id = %s ORDER BY uploaded_at DESC LIMIT 1;"
            cursor.execute(doc_query, (self.case_id,))
            document = cursor.fetchone()
            if document and document.get('file_path'):
                self.document_path = document['file_path']
                document_name = document.get('document_name', 'Tıklayın')
                
           
                self.ui.labelDocument1.setToolTip(f"{document_name}\nYol: {self.document_path}")
                self.ui.labelDocument1.setCursor(QtCore.Qt.PointingHandCursor)
            else:
                self.ui.labelDocument1.setText("Doküman Yok")
                self.ui.labelDocument1.setStyleSheet("color: white; font-size: 14px;")
                self.ui.labelDocument1.setCursor(QtCore.Qt.ArrowCursor) # İmleci normale çevir
                self.document_path = None
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dava verileri yüklenirken hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()

    def add_document_button_clicked(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Doküman Dosyası Seç", "", 
                                                  "Tüm Dosyalar (*);;PDF (*.pdf);;Word (*.doc *.docx)", 
                                                  options=options)
        
        if not filePath:
            return

        conn = connect_to_database()
        if conn is None: return

        try:
            cursor = conn.cursor()
            file_name = os.path.basename(filePath)
            
            query = """
            INSERT INTO documents (case_id, lawyer_id, document_name, file_path)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.case_id, self.current_user_id, file_name, filePath))
            conn.commit()
            
            QMessageBox.information(self, "Başarılı", f"'{file_name}' dokümanı davaya başarıyla eklendi.")
            
            self.load_case_data()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Veritabanı Hatası", f"Doküman eklenirken hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()

    def update_button_clicked(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dava Bilgilerini Güncelle")
        dialog.setGeometry(200, 200, 500, 450)

        main_layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        lineTitle = QLineEdit()
        lineNumber = QLineEdit()
        comboStatus = QComboBox()
        textDescription = QTextEdit()
        textNoteUpdate = QTextEdit()
        checkIsActive = QtWidgets.QCheckBox("Bu dava aktif (Arşivlenmemiş)")

        comboStatus.addItems(list(self.STATUS_MAP_TO_DB.keys()))

        btnSave = QPushButton("Kaydet")
        btnExit = QPushButton("İptal")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btnSave)
        btn_layout.addWidget(btnExit)

        self.load_case_data_for_dialog(lineTitle, lineNumber, comboStatus, textDescription, checkIsActive, textNoteUpdate)

        form_layout.addRow("Dava Başlığı:", lineTitle)
        form_layout.addRow("Dava Numarası:", lineNumber)
        form_layout.addRow("Dava Durumu:", comboStatus)
        form_layout.addRow("Açıklama:", textDescription)
        form_layout.addRow("Yeni Not Ekle:", textNoteUpdate)
        form_layout.addRow(checkIsActive)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        btnSave.clicked.connect(lambda: self.save_updated_case(
            dialog, lineTitle.text(), lineNumber.text(), comboStatus.currentText(), 
            textDescription.toPlainText(), checkIsActive.isChecked(), textNoteUpdate.toPlainText()
        ))
        btnExit.clicked.connect(dialog.reject)

        dialog.exec_()

    def load_case_data_for_dialog(self, line_title, line_number, combo_status, text_description, check_is_active, text_note_update):
        conn = connect_to_database()
        if conn is None: return

        try:
            cursor = conn.cursor(dictionary=True)
            case_query = "SELECT case_title, case_number, case_status, case_description, is_active FROM cases WHERE case_id = %s;"
            cursor.execute(case_query, (self.case_id,))
            case_data = cursor.fetchone()
            if case_data:
                line_title.setText(case_data['case_title'])
                line_number.setText(case_data['case_number'])
                
                eng_status = case_data['case_status']
                tr_status = self.STATUS_MAP_FROM_DB.get(eng_status, eng_status)
                combo_status.setCurrentText(tr_status)
                
                text_description.setText(case_data['case_description'])
                check_is_active.setChecked(bool(case_data['is_active']))

            note_query = "SELECT note_content FROM case_notes WHERE case_id = %s ORDER BY created_at DESC LIMIT 1;"
            cursor.execute(note_query, (self.case_id,))
            note_data = cursor.fetchone()
            if note_data:
                text_note_update.setPlaceholderText(f"Önceki not:\n{note_data['note_content']}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Diyalog verileri yüklenirken hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()

    def save_updated_case(self, dialog, case_title, case_number, tr_status, case_description, is_active, note_content):
        """Dava bilgilerini günceller ve YENİ bir not kaydı oluşturur."""
        if not case_title or not case_number:
            QMessageBox.warning(dialog, "Eksik Bilgi", "Dava Başlığı ve Dava Numarası boş bırakılamaz!")
            return

        db_status = self.STATUS_MAP_TO_DB.get(tr_status)
        if not db_status:
            QMessageBox.warning(dialog, "Hata", f"Geçersiz statü değeri: {tr_status}")
            return

        conn = connect_to_database()
        if conn is None: return

        try:
            cursor = conn.cursor()
            update_query = "UPDATE cases SET case_title = %s, case_number = %s, case_status = %s, case_description = %s, is_active = %s WHERE case_id = %s;"
            cursor.execute(update_query, (case_title, case_number, db_status, case_description, is_active, self.case_id))

            if note_content.strip(): 
                note_query = "INSERT INTO case_notes (case_id, lawyer_id, note_content) VALUES (%s, %s, %s)"
                cursor.execute(note_query, (self.case_id, self.current_user_id, note_content))
            
            conn.commit()
            QMessageBox.information(dialog, "Başarılı", "Dava bilgileri başarıyla güncellendi!")
            self.load_case_data()
            dialog.accept()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(dialog, "Hata", f"Dava güncellenirken hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()

    def open_document(self):
        if self.document_path and os.path.exists(self.document_path):
            try: 
                normalized_path = os.path.normpath(self.document_path)
                os.startfile(normalized_path)
            except Exception as e: 
                QMessageBox.critical(self, "Hata", f"Dosya açılamadı: {str(e)}")
        elif self.document_path:
            QMessageBox.warning(self, "Dosya Bulunamadı", f"Dosya şu yolda bulunamadı: {self.document_path}")
        else:
            QMessageBox.information(self, "Doküman Yok", "Açılacak bir doküman bulunmuyor.")
    


    def exit_button_clicked(self):
        self.cases_button_clicked()