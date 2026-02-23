
from forms.casesFormUi import Ui_FormCases
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from database.connect_to_database import connect_to_database
from views.MenuBase import MenuBase 
from views.formSingleCase import formSingleCase

class formCases(QtWidgets.QWidget, MenuBase):
    

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


    def __init__(self, current_user_id=None):
            super(formCases, self).__init__()
            
            self.ui = Ui_FormCases()
            
            container_layout = QtWidgets.QVBoxLayout(self)
            container_layout.setContentsMargins(0, 0, 0, 0) # Kenar boşluklarını sıfırla
            container_layout.addWidget(self.ui)
            
            self.current_user_id = current_user_id
            
            self.load_case_data()
            
            self.ui.tableView.doubleClicked.connect(self.open_single_case_form)
            self.ui.btnAction.clicked.connect(self.bring_action_button_clicked)
            
            self.setup_menu(self.ui)

    def load_case_data(self):
        """Fetches case data from the database and loads it into the QTableView."""
        conn = connect_to_database()
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Could not connect to the database!")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            
            if isinstance(self.current_user_id, list):
                lawyer_ids_tuple = tuple(self.current_user_id)
                where_clause = f"l.lawyer_id IN ({','.join(['%s'] * len(lawyer_ids_tuple))})"
                params = lawyer_ids_tuple
            else:
                where_clause = "l.lawyer_id = %s"
                params = (self.current_user_id,)
            
            query = f"""
            SELECT 
                c.case_id, c.case_title, c.case_number, c.case_status, c.created_at,
                cl.fullname AS client_fullname,
                l.lawyer_id, l.name AS lawyer_name, l.surname AS lawyer_surname
            FROM cases c
            LEFT JOIN case_clients cc ON c.case_id = cc.case_id
            LEFT JOIN clients cl ON cc.client_id = cl.client_id
            LEFT JOIN case_lawyers ca ON c.case_id = ca.case_id
            LEFT JOIN lawyers l ON ca.lawyer_id = l.lawyer_id
            WHERE {where_clause} AND c.is_active = TRUE;
            """
            
            cursor.execute(query, params)
            cases = cursor.fetchall()
            
            model = QStandardItemModel()
            self.ui.tableView.setModel(model)
            

            headers = [
                "Dava ID", "Dava Başlığı", "Dava Numarası", "Durum", 
                "Oluşturulma Tarihi", "Avukat ID", 
                "Avukat Adı", "Müvekkil Adı"
            ]
            model.setHorizontalHeaderLabels(headers)

            for i, row_data in enumerate(cases):
                
 
                eng_status = row_data.get('case_status', '')
                tr_status = self.STATUS_MAP_FROM_DB.get(eng_status, eng_status)
 
                
                row = [
                    QStandardItem(str(row_data.get('case_id', ''))),
                    QStandardItem(str(row_data.get('case_title', ''))),
                    QStandardItem(str(row_data.get('case_number', ''))),
                    QStandardItem(tr_status), 
                    QStandardItem(str(row_data.get('created_at', ''))),
                    QStandardItem(str(row_data.get('lawyer_id', ''))),
                    QStandardItem(str(f"{row_data.get('lawyer_name', '')} {row_data.get('lawyer_surname', '')}")),
                    QStandardItem(str(row_data.get('client_fullname', '')))
                ]
                for item in row:
                    item.setTextAlignment(QtCore.Qt.AlignCenter) 
                    if i % 2 == 0:
                        item.setBackground(QColor("#F5F5DC")) 
                    else:
                        item.setBackground(QColor(237, 227, 207, 245))
                model.appendRow(row)

            self.ui.tableView.resizeColumnsToContents()
            self.ui.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading data: {str(e)}")
        finally:
            if conn:
                conn.close()


    def bring_action_button_clicked(self):
        """Açılan diyalog penceresinde yeni bir dava oluşturma formunu gösterir."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Dava Oluştur") 
        dialog.setGeometry(200, 200, 500, 400)

        main_layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        lineTitle = QLineEdit()
        lineNumber = QLineEdit()
        comboStatus = QComboBox()
        textDescription = QTextEdit()
        
  
        comboStatus.addItems(list(self.STATUS_MAP_TO_DB.keys()))

        comboClients = QComboBox()
        comboOpponents = QComboBox()
        comboLawyers = QComboBox()

        self.load_related_data(comboClients, comboOpponents, comboLawyers)

      
        form_layout.addRow("Dava Başlığı:", lineTitle)
        form_layout.addRow("Dava Numarası:", lineNumber)
        form_layout.addRow("Dava Durumu:", comboStatus)
        form_layout.addRow("Açıklama:", textDescription)
        form_layout.addRow("Müvekkil:", comboClients)
        form_layout.addRow("Karşı Taraf:", comboOpponents)
        form_layout.addRow("Atanan Avukat:", comboLawyers)

        btnSave = QPushButton("Kaydet") 
        btnExit = QPushButton("İptal")  

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btnSave)
        btn_layout.addWidget(btnExit)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        btnSave.clicked.connect(lambda: self.save_new_case(
            dialog, lineTitle.text(), lineNumber.text(), comboStatus.currentText(), 
            textDescription.toPlainText(), comboClients.currentData(), 
            comboOpponents.currentData(), comboLawyers.currentData()
        ))
        btnExit.clicked.connect(dialog.reject)

        dialog.exec_()

    def load_related_data(self, combo_clients, combo_opponents, combo_lawyers):
        """Loads data for clients, opponents, and lawyers from the database."""
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT client_id, fullname FROM clients")
            clients = cursor.fetchall()
            combo_clients.addItem("Müvekkil Seçiniz...", -1) 
            for client in clients:
                combo_clients.addItem(client['fullname'], client['client_id'])

            cursor.execute("SELECT opponent_id, name, surname FROM opponents")
            opponents = cursor.fetchall()
            combo_opponents.addItem("Karşı Taraf Seçiniz...", -1) 
            for opponent in opponents:
                combo_opponents.addItem(f"{opponent['name']} {opponent['surname']}", opponent['opponent_id'])

            cursor.execute("SELECT lawyer_id, name, surname FROM lawyers")
            lawyers = cursor.fetchall()
            combo_lawyers.addItem("Avukat Seçiniz...", -1) 
            for lawyer in lawyers:
                combo_lawyers.addItem(f"{lawyer['name']} {lawyer['surname']}", lawyer['lawyer_id'])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading data: {str(e)}")
        finally:
            if conn: conn.close()

    def save_new_case(self, dialog, case_title, case_number, case_status, case_description, client_id, opponent_id, lawyer_id):
        """Saves the new case and related data to the database."""
        if not case_title or not case_number:
            QMessageBox.warning(dialog, "Uyarı", "Dava Başlığı ve Dava Numarası boş bırakılamaz!") # -> Türkçe
            return

        db_status = self.STATUS_MAP_TO_DB.get(case_status)
        
        if not db_status:
            QMessageBox.warning(dialog, "Hata", f"Geçersiz statü değeri: {case_status}")
            return


        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor()

            query_case = "INSERT INTO cases (case_title, case_number, case_status, case_description) VALUES (%s, %s, %s, %s)"
            # Çevrilmiş 'db_status'u kaydet
            cursor.execute(query_case, (case_title, case_number, db_status, case_description))
            new_case_id = cursor.lastrowid

            if lawyer_id and lawyer_id != -1:
                query_lawyer = "INSERT INTO case_lawyers (case_id, lawyer_id) VALUES (%s, %s)"
                cursor.execute(query_lawyer, (new_case_id, lawyer_id))

            if client_id and client_id != -1:
                query_client = "INSERT INTO case_clients (case_id, client_id) VALUES (%s, %s)"
                cursor.execute(query_client, (new_case_id, client_id))

            if opponent_id and opponent_id != -1:
                query_opponent = "INSERT INTO case_opponents (case_id, opponent_id) VALUES (%s, %s)"
                cursor.execute(query_opponent, (new_case_id, opponent_id))

            conn.commit()
            QMessageBox.information(dialog, "Başarılı", "Yeni dava başarıyla oluşturuldu!") 
            self.load_case_data() # Refresh the table view
            dialog.accept()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(dialog, "Hata", f"Dava kaydedilirken bir hata oluştu: {str(e)}") 
        finally:
            if conn: conn.close()

    def open_single_case_form(self, index):
        """Açılan forma çift tıklanan satırdaki dava ID'sini gönderir."""
        if not index.isValid():
            return
        
        case_id_item = self.ui.tableView.model().item(index.row(), 0)
        case_id = int(case_id_item.text())
        
        self.single_case_form = formSingleCase(
            current_user_id=self.current_user_id,
            case_id=case_id
        )
        self.single_case_form.setGeometry(self.geometry())
        self.single_case_form.show()
        self.close()