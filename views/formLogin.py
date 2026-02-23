
from forms.loginPageUi import Ui_FormLoginPage
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from database.connect_to_database import connect_to_database
from views.formRegister import formRegister

class formLogin(QtWidgets.QWidget):
    def __init__(self):
        super(formLogin, self).__init__()
        self.resize(1600, 900)
        
        self.ui = Ui_FormLoginPage()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        
      
        self.ui.btnLogin.clicked.connect(self.lawyer_login_clicked)
        self.ui.btnLogin_2.clicked.connect(self.bureau_login_clicked)
        

        self.ui.btnRegister.clicked.connect(lambda: self.open_register_page("lawyer"))
        

        self.ui.btnRegister_2.clicked.connect(lambda: self.open_register_page("bureau"))
        # ------------------------------------

    def open_register_page(self, mode):
        """Kayıt formunu seçilen modda açar."""
        try:

            self.register_form = formRegister(current_user_id=None, register_mode=mode)
            self.register_form.setGeometry(self.geometry())
            self.register_form.show()
            self.close() 
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt sayfası açılamadı: {str(e)}")

    def lawyer_login_clicked(self):
        baro_id = self.ui.LineEdit_1.text()
        password = self.ui.LineEdit_2.text()
        login_id = self.check_lawyer_login(baro_id, password)
        if login_id is not None:
            self.open_main_window(login_id)
            self.close()

    def bureau_login_clicked(self):
        firm_name = self.ui.LineEdit_3.text()
        password = self.ui.LineEdit_4.text()
        login_id_list = self.check_law_firm_login(firm_name, password)
        if login_id_list is not None:
            self.open_main_window(login_id_list)
            self.close()

    def check_lawyer_login(self, baro_id, password):
        if not baro_id or not password:
            QMessageBox.warning(self, "Eksik Bilgi", "Baro Numarası ve şifre boş bırakılamaz!")
            return None
        conn = connect_to_database()
        if conn is None: return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT lawyer_id, password FROM lawyers WHERE bar_number = %s"
            cursor.execute(query, (baro_id,))
            user = cursor.fetchone()
            if user and password == user['password']:
                return user['lawyer_id']
            else:
                QMessageBox.warning(self, "Hata", "Hatalı giriş bilgileri!")
                return None
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
            return None
        finally:
            if conn: conn.close()

    def check_law_firm_login(self, firm_name, password):
        if not firm_name or not password:
            QMessageBox.warning(self, "Eksik Bilgi", "Büro Adı ve şifre boş bırakılamaz!")
            return None
        conn = connect_to_database()
        if conn is None: return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT law_firm_id FROM law_firms WHERE firm_name = %s AND password = %s"
            cursor.execute(query, (firm_name, password))
            firm = cursor.fetchone()
            if firm:
                firm_id = firm['law_firm_id']
                lawyers_query = "SELECT lawyer_id FROM lawyers WHERE law_firm_id = %s"
                cursor.execute(lawyers_query, (firm_id,))
                lawyer_ids = [row['lawyer_id'] for row in cursor.fetchall()]
                if not lawyer_ids:

                    QMessageBox.information(self, "Bilgi", "Bu büroya kayıtlı avukat yok.")

                    return [] 
                return lawyer_ids
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz büro bilgileri!")
                return None
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
            return None
        finally:
            if conn: conn.close()

    def open_main_window(self, user_id_data):
        from views.formMainWindow import formMainWindow
        self.main_form = formMainWindow(current_user_id=user_id_data)
        self.main_form.showMaximized() 
        self.close()