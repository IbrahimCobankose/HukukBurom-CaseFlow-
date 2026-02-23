import os
import shutil
from forms.financialManagementFormUi import Ui_FinancialManagementForm
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from database.connect_to_database import connect_to_database
from decimal import Decimal, InvalidOperation 
from views.MenuBase import MenuBase

class formFinancialManagement(QtWidgets.QWidget, MenuBase):
    
    TRANSACTION_MAP_TO_DB = {
        "Ödeme Alındı (Müvekkil)": "Income",
        "Ödeme Alındı (Karşı Taraf)": "Income",
        "Diğer Gelir": "Income",
        "Masraf (Avukat)": "Expense",
        "Diğer Gider": "Expense"
    }
    
    TRANSACTION_MAP_FROM_DB = {
        "Income": "Ödeme Alındı (Müvekkil)",
        "Expense": "Masraf (Avukat)"
    }

    def __init__(self, current_user_id=None, case_id=None):
        super(formFinancialManagement, self).__init__()
        
        self.ui = Ui_FinancialManagementForm()
        
        container_layout = QtWidgets.QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.ui)

        self.current_user_id = current_user_id
        self.current_transaction_id = None
        
   
        self.receipts_folder = "Financial Receipts"
        if not os.path.exists(self.receipts_folder):
            os.makedirs(self.receipts_folder)
            
        
        self.current_receipt_path_db = None  # Veritabanından gelen yol
        self.pending_receipt_path = None     # Yeni seçilen (henüz kaydedilmemiş) dosya yolu

        # Sinyal Bağlantıları
        self.ui.saveButton.clicked.connect(self.save_button_clicked)
        self.ui.ClearButton.clicked.connect(self.clear_form_button_clicked)
        
    
        try:
            self.ui.btnAddReceipt.clicked.disconnect()
        except:
            pass
        self.ui.btnAddReceipt.clicked.connect(self.handle_receipt_button) 
        
        self.ui.caseComboBox.currentIndexChanged.connect(self.load_financial_data_for_case)

        self.setup_menu(self.ui)
        self.load_initial_data()

  

    def get_lawyer_ids_tuple(self):
        if isinstance(self.current_user_id, list):
            return tuple(self.current_user_id)
        elif self.current_user_id:
            return (self.current_user_id,)
        return ()

    def load_initial_data(self):
        self.load_cases()
        self.load_clients()
        self.load_opponents()
        self.ui.typeComboBox.clear()
        self.ui.typeComboBox.addItems(list(self.TRANSACTION_MAP_TO_DB.keys()))

    def load_cases(self):
        lawyer_ids = self.get_lawyer_ids_tuple()
        if not lawyer_ids: return
        conn = connect_to_database()
        if conn is None:
            QMessageBox.critical(self, "Hata", "Veritabanı bağlantısı yok.")
            return
        try:
            cursor = conn.cursor(dictionary=True)
            in_clause = ','.join(['%s'] * len(lawyer_ids))
            query = f"""
                SELECT c.case_id, c.case_title, c.case_number
                FROM cases c
                JOIN case_lawyers cl ON c.case_id = cl.case_id
                WHERE cl.lawyer_id IN ({in_clause}) AND c.is_active = TRUE
                ORDER BY c.case_title;
            """
            cursor.execute(query, lawyer_ids)
            cases = cursor.fetchall()

            self.ui.caseComboBox.clear()
            self.ui.caseComboBox.addItem("Dava Seçiniz...", None)
            for case in cases:
                display_text = f"{case['case_title']} ({case['case_number']})"
                self.ui.caseComboBox.addItem(display_text, case['case_id'])
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Davalar yüklenirken hata: {e}")
        finally:
            if conn: conn.close()
    
    def load_clients(self):
        lawyer_ids = self.get_lawyer_ids_tuple()
        if not lawyer_ids: return
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)
            in_clause = ','.join(['%s'] * len(lawyer_ids))
            query = f"SELECT DISTINCT c.client_id, c.fullname FROM clients c JOIN case_clients cc ON c.client_id = cc.client_id JOIN case_lawyers cl ON cc.case_id = cl.case_id WHERE cl.lawyer_id IN ({in_clause}) ORDER BY c.fullname;"
            cursor.execute(query, lawyer_ids)
            clients = cursor.fetchall()
            self.ui.clientComboBox.clear()
            self.ui.clientComboBox.addItem("Müvekkil Seçiniz...", None)
            for client in clients:
                self.ui.clientComboBox.addItem(client['fullname'], client['client_id'])
        except Exception as e:
            print(f"Hata: {e}")
        finally:
            if conn: conn.close()

    def load_opponents(self):
        lawyer_ids = self.get_lawyer_ids_tuple()
        if not lawyer_ids: return
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor(dictionary=True)
            in_clause = ','.join(['%s'] * len(lawyer_ids))
            query = f"SELECT DISTINCT o.opponent_id, o.name, o.surname FROM opponents o JOIN case_opponents co ON o.opponent_id = co.opponent_id JOIN case_lawyers cl ON co.case_id = cl.case_id WHERE cl.lawyer_id IN ({in_clause}) ORDER BY o.name;"
            cursor.execute(query, lawyer_ids)
            opponents = cursor.fetchall()
            self.ui.opponentComboBox.clear()
            self.ui.opponentComboBox.addItem("Karşı Taraf Seçiniz...", None)
            for opp in opponents:
                self.ui.opponentComboBox.addItem(f"{opp['name']} {opp['surname']}", opp['opponent_id'])
        except Exception as e:
            print(f"Hata: {e}")
        finally:
            if conn: conn.close()



    def load_financial_data_for_case(self):
        selected_case_id = self.ui.caseComboBox.currentData()

        if selected_case_id is None:
            self.clear_form(keep_case=False) 
            return

        conn = connect_to_database()
        if conn is None: return

        try:
            cursor = conn.cursor(dictionary=True)
 
            query = "SELECT * FROM financial_transactions WHERE case_id = %s LIMIT 1" 
            cursor.execute(query, (selected_case_id,))
            transaction = cursor.fetchone()

            if transaction:
                self.current_transaction_id = transaction['transaction_id']
                
                db_value = transaction['transaction_type']
                ui_value = self.TRANSACTION_MAP_FROM_DB.get(db_value, db_value)
                self.ui.typeComboBox.setCurrentText(ui_value) 
                
                self.ui.amountLineEdit.setText(str(transaction['amount']))
                self.ui.message_box.setPlainText(transaction['description'])

                if transaction.get('receipt_path') and transaction['receipt_path']:
                    self.current_receipt_path_db = transaction['receipt_path']
                    self.update_receipt_button_state(has_file=True)
                else:
                    self.current_receipt_path_db = None
                    self.update_receipt_button_state(has_file=False)
 

                client_id = transaction['client_id']
                if client_id:
                    index = self.ui.clientComboBox.findData(client_id)
                    if index != -1: self.ui.clientComboBox.setCurrentIndex(index)
                else:
                    self.ui.clientComboBox.setCurrentIndex(0) 

                opponent_id = transaction['opponent_id']
                if opponent_id:
                    index = self.ui.opponentComboBox.findData(opponent_id)
                    if index != -1: self.ui.opponentComboBox.setCurrentIndex(index)
                else:
                    self.ui.opponentComboBox.setCurrentIndex(0)
            
            else:
                self.clear_form(keep_case=True)
                # Varsayılanlar
                try:
                    q_c = "SELECT client_id FROM case_clients WHERE case_id = %s LIMIT 1"
                    cursor.execute(q_c, (selected_case_id,))
                    c = cursor.fetchone()
                    if c: 
                        idx = self.ui.clientComboBox.findData(c['client_id'])
                        if idx != -1: self.ui.clientComboBox.setCurrentIndex(idx)
                    
                    q_o = "SELECT opponent_id FROM case_opponents WHERE case_id = %s LIMIT 1"
                    cursor.execute(q_o, (selected_case_id,))
                    o = cursor.fetchone()
                    if o:
                        idx = self.ui.opponentComboBox.findData(o['opponent_id'])
                        if idx != -1: self.ui.opponentComboBox.setCurrentIndex(idx)

                    self.ui.typeComboBox.setCurrentIndex(0) 
                except: pass

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri yüklenirken hata: {e}")
            self.clear_form(keep_case=True)
        finally:
            if conn: conn.close()

    def clear_form(self, keep_case=False):
        self.current_transaction_id = None
        self.current_receipt_path_db = None
        self.pending_receipt_path = None
        
        self.update_receipt_button_state(has_file=False)

        if not keep_case:
            self.ui.caseComboBox.setCurrentIndex(0)
        self.ui.clientComboBox.setCurrentIndex(0)
        self.ui.opponentComboBox.setCurrentIndex(0)
        self.ui.typeComboBox.setCurrentIndex(0)
        self.ui.amountLineEdit.clear()
        self.ui.message_box.clear()

    def clear_form_button_clicked(self):
        self.clear_form(keep_case=False)

    # --- DOSYA BUTONU MANTIĞI ---

    def update_receipt_button_state(self, has_file):
        """Butonun görünümünü dosya durumuna göre günceller."""
        if has_file:
            self.ui.btnAddReceipt.setText("Belgeyi Görüntüle")
            self.ui.btnAddReceipt.setStyleSheet("""
                QPushButton {
                    background-color: #2e8b57; /* Yeşil */
                    color: white; font-weight: bold; border-radius: 10px; font-size: 16px;
                }
                QPushButton:hover { background-color: #3cb371; }
            """)
        else:
            self.ui.btnAddReceipt.setText("Fiş/Dekont Ekle")
            self.ui.btnAddReceipt.setStyleSheet("""
                QPushButton {
                    background-color: #a4632d; /* Standart Kahverengi */
                    color: white; font-weight: bold; border-radius: 10px; font-size: 16px;
                }
                QPushButton:hover { background-color: #cd853f; }
            """)

    def handle_receipt_button(self):
        """Butona basılınca: Dosya varsa açar, yoksa ekler."""
        
        # 1. Eğer halihazırda veritabanında kayıtlı bir dosya varsa
        if self.current_receipt_path_db:
            msg = QMessageBox()
            msg.setWindowTitle("Belge İşlemleri")
            msg.setText("Bu kayıt için bir belge mevcut.")
            btn_open = msg.addButton("Dosyayı Aç", QMessageBox.AcceptRole)
            btn_change = msg.addButton("Değiştir", QMessageBox.ActionRole)
            btn_cancel = msg.addButton("İptal", QMessageBox.RejectRole)
            msg.exec_()

            if msg.clickedButton() == btn_open:
                if os.path.exists(self.current_receipt_path_db):
                    os.startfile(self.current_receipt_path_db)
                else:
                    QMessageBox.warning(self, "Hata", "Dosya yerinde bulunamadı (Silinmiş veya taşınmış olabilir).")
            elif msg.clickedButton() == btn_change:
                self.select_new_file()

        # 2. Eğer henüz kaydedilmemiş ama yeni seçilmiş bir dosya varsa
        elif self.pending_receipt_path:
             QMessageBox.information(self, "Bilgi", f"Seçilen dosya:\n{self.pending_receipt_path}\n\nHenüz kaydedilmedi. 'Kaydet' butonuna basınca sisteme eklenecek.")
             
             self.select_new_file()
             
        # 3. Dosya yoksa, yeni seç
        else:
            self.select_new_file()

    def select_new_file(self):
        """Dosya seçme penceresini açar."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Belge Seç", "", "All Files (*)", options=options
        )
        if file_path:
            self.pending_receipt_path = file_path
            self.ui.btnAddReceipt.setText("Dosya Seçildi (Kaydet Bekleniyor)")
            self.ui.btnAddReceipt.setStyleSheet("""
                QPushButton {
                    background-color: #d2691e; /* Turuncu - Beklemede */
                    color: white; font-weight: bold; border-radius: 10px; font-size: 14px;
                }
            """)



    def save_button_clicked(self):
        if not self.validate_input(): return 
        try:
            case_id = self.ui.caseComboBox.currentData()
            client_id = self.ui.clientComboBox.currentData()
            opponent_id = self.ui.opponentComboBox.currentData()
            
            ui_transaction_type = self.ui.typeComboBox.currentText()
            db_transaction_type = self.TRANSACTION_MAP_TO_DB.get(ui_transaction_type)
            
            if db_transaction_type is None: return

            amount = Decimal(self.ui.amountLineEdit.text().replace(',', '.')) 
            description = self.ui.message_box.toPlainText()
            
            
            final_receipt_path = self.current_receipt_path_db 
            
            if self.pending_receipt_path:
                
                try:
                    filename = os.path.basename(self.pending_receipt_path)
                    destination = os.path.join(self.receipts_folder, filename)
                    
                    shutil.copy(self.pending_receipt_path, destination)
                    final_receipt_path = destination 
                except Exception as e:
                    QMessageBox.warning(self, "Dosya Hatası", f"Dosya kopyalanamadı: {e}")
                    return
            # ------------------------------

            if isinstance(self.current_user_id, list):
                lawyer_id_to_save = self.current_user_id[0]
            else:
                lawyer_id_to_save = self.current_user_id
            
            transaction_data = {
                "case_id": case_id,
                "client_id": client_id if client_id else None, 
                "opponent_id": opponent_id if opponent_id else None, 
                "transaction_type": db_transaction_type, 
                "amount": amount,
                "description": description,
                "lawyer_id": lawyer_id_to_save,
                "receipt_path": final_receipt_path 
            }
            self.save_transaction_to_db(transaction_data)
        except InvalidOperation:
            QMessageBox.warning(self, "Hata", "Miktar geçerli bir sayı olmalıdır.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata: {str(e)}")

    def validate_input(self):
        if self.ui.caseComboBox.currentData() is None:
            QMessageBox.warning(self, "Eksik", "Dava seçiniz.")
            return False
        if not self.ui.amountLineEdit.text():
            QMessageBox.warning(self, "Eksik", "Miktar giriniz.")
            return False
        return True

    def save_transaction_to_db(self, data):
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor()
            
            if self.current_transaction_id is not None:
                # UPDATE
                query = """
                    UPDATE financial_transactions SET
                        case_id = %s, client_id = %s, opponent_id = %s,
                        transaction_type = %s, amount = %s, description = %s,
                        lawyer_id = %s, receipt_path = %s, transaction_date = CURDATE()
                    WHERE transaction_id = %s;
                """
                params = (
                    data['case_id'], data['client_id'], data['opponent_id'],
                    data['transaction_type'], data['amount'], data['description'],
                    data['lawyer_id'], data['receipt_path'], self.current_transaction_id
                )
            else:
                # INSERT
                query = """
                    INSERT INTO financial_transactions
                        (case_id, client_id, opponent_id, transaction_type, 
                         amount, description, lawyer_id, receipt_path, transaction_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE());
                """
                params = (
                    data['case_id'], data['client_id'], data['opponent_id'],
                    data['transaction_type'], data['amount'], data['description'],
                    data['lawyer_id'], data['receipt_path']
                )
            cursor.execute(query, params)
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Finansal kayıt ve belge kaydedildi.")
            self.load_initial_data()
            self.clear_form(keep_case=False)
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")
        finally:
            if conn: conn.close()