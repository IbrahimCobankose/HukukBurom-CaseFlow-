
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel
from forms.myBureauFormUi import Ui_FormMyBureau
from database.connect_to_database import connect_to_database
from views.MenuBase import MenuBase
from views.formRegister import formRegister

class formMyBureau(QtWidgets.QWidget, MenuBase):
    def __init__(self, current_user_id=None):
        super(formMyBureau, self).__init__()
        
        self.ui = Ui_FormMyBureau()
        
        # Ana layout ayarı
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        
        self.current_user_id = current_user_id
        
        
        self.setup_menu(self.ui) 
        
 
        try:
            self.ui.btnAddLawyer.clicked.disconnect()
        except:
            pass
        self.ui.btnAddLawyer.clicked.connect(self.open_add_lawyer_form)


        self.setup_dynamic_list_area()
        

        self.load_bureau_lawyers()

    def setup_dynamic_list_area(self):

        if hasattr(self.ui, 'rows_widget'):
            self.ui.rows_widget.setParent(None) 


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
        

        self.ui.content_layout.insertWidget(1, self.scroll_area)

    def load_bureau_lawyers(self):
  
 
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not isinstance(self.current_user_id, list) or not self.current_user_id:
            return 

        conn = connect_to_database()
        if conn is None: return

        try:
            cursor = conn.cursor(dictionary=True)
            
 
            current_lawyer_id = self.current_user_id[0]
            query_firm = "SELECT law_firm_id FROM lawyers WHERE lawyer_id = %s"
            cursor.execute(query_firm, (current_lawyer_id,))
            firm_result = cursor.fetchone()
            
            if not firm_result: return
            firm_id = firm_result['law_firm_id']

            query_lawyers = """
                SELECT lawyer_id, name, surname, is_admin 
                FROM lawyers 
                WHERE law_firm_id = %s 
                ORDER BY name ASC
            """
            cursor.execute(query_lawyers, (firm_id,))
            lawyers = cursor.fetchall()
            
            # 3. Her avukat için dinamik bir satır oluştur
            for lawyer in lawyers:
                self.create_lawyer_row(lawyer)
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Avukatlar yüklenirken hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()

    def create_lawyer_row(self, lawyer_data):

        
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(15)
        
        full_name = f"{lawyer_data['name']} {lawyer_data['surname']}"
        if lawyer_data['lawyer_id'] == self.current_user_id[0]:
            full_name += " (Ben)"

   
        btn_name = QPushButton(full_name)
        btn_name.setMinimumHeight(50)
        btn_name.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
   
        btn_name.setStyleSheet("""
            QPushButton {
                font-family: Palatino Linotype;
                background-color: #a0652c;
                color: white;
                font-size: 20px;
                border-radius: 10px;
                border: 1px solid #8b5a2b;
            }
            QPushButton:hover { background-color: #cd853f; }
            QPushButton:pressed { background-color: #a0522d; }
        """)
        
        # --- Sil Butonu ---
        btn_delete = QPushButton("SİL")
        btn_delete.setFixedSize(100, 50)
        btn_delete.setStyleSheet("""
            QPushButton {
                font-family: Palatino Linotype;
                background-color: #8b0000; /* Koyu Kırmızı */
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid #500000;
            }
            QPushButton:hover { background-color: #ff4444; }
            QPushButton:pressed { background-color: #500000; }
        """)
        
        # Silme olayını bağla
        btn_delete.clicked.connect(lambda: self.delete_lawyer(lawyer_data['lawyer_id']))
        
        # Satıra ekle
        row_layout.addWidget(btn_name)
        row_layout.addWidget(btn_delete)
        
        # Ana listeye ekle
        self.scroll_layout.addWidget(row_widget)

    def open_add_lawyer_form(self):

        
        self.register_form = formRegister(current_user_id=self.current_user_id, register_mode="lawyer")
        self.register_form.setGeometry(self.geometry())
        self.register_form.show()
        self.close()

    def delete_lawyer(self, lawyer_id_to_delete):
        """Seçilen avukatı ve ona bağlı TÜM verileri siler."""
        
        if isinstance(self.current_user_id, list):
            current_id = self.current_user_id[0]
        else:
            current_id = self.current_user_id

        if lawyer_id_to_delete == current_id:
            QMessageBox.warning(self, "İşlem Engellendi", "Kendinizi silemezsiniz!")
            return


        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Kritik Silme İşlemi")
        msg.setText("Bu avukatı silmek üzeresiniz!")
        msg.setInformativeText(
            "DİKKAT: Bu avukatın üzerinde kayıtlı geçmiş davalar, duruşmalar ve finansal kayıtlar bulunmaktadır.\n\n"
            "Eğer silerseniz, BU AVUKATA AİT TÜM GEÇMİŞ VERİLER DE SİLİNECEKTİR.\n\n"
            "Yine de devam etmek istiyor musunuz?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            conn = connect_to_database()
            if conn is None: return
            
            try:
                cursor = conn.cursor()
                
                
                # 1. Dava Bağlantıları (Junction Table)
                cursor.execute("DELETE FROM case_lawyers WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                # 2. Takvim Etkinlikleri
                cursor.execute("DELETE FROM calendar_events WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                # 3. Dava Notları
                cursor.execute("DELETE FROM case_notes WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                # 4. Yüklenen Dokümanlar
                cursor.execute("DELETE FROM documents WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                # 5. Finansal İşlemler
                cursor.execute("DELETE FROM financial_transactions WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                # 6. VE SON OLARAK: Avukatın Kendisi
                cursor.execute("DELETE FROM lawyers WHERE lawyer_id = %s", (lawyer_id_to_delete,))
                
                conn.commit()
                
                QMessageBox.information(self, "Başarılı", "Avukat ve ilgili tüm verileri başarıyla silindi.")
                self.load_bureau_lawyers() # Listeyi yenile
                
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Hata", f"Silme işlemi sırasında hata oluştu:\n{str(e)}")
            finally:
                if conn: conn.close()