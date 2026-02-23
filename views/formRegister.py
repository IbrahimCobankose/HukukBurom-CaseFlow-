
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout
from datetime import datetime
import re

try:
    from forms.registerPageUi import Ui_FormRegisterPage
except ImportError:
    print("Hata: registerPageUi.py bulunamadı.")

try:
    from database.connect_to_database import connect_to_database
except ImportError:
    print("Hata: Veritabanı bağlantı fonksiyonu (connect_to_database) bulunamadı.")


class formRegister(QtWidgets.QWidget):
    def __init__(self, current_user_id=None, register_mode="both"):
        """
        register_mode: "lawyer" (Sadece Avukat), "bureau" (Sadece Büro) veya "both" (İkisi de)
        """
        super().__init__()
        
        self.current_user_id = current_user_id
        

        if isinstance(self.current_user_id, list) and self.current_user_id:
            self.register_mode = "lawyer"
        else:
            self.register_mode = register_mode

        self.law_firm_id_to_assign = None

        try:
            self.ui = Ui_FormRegisterPage()
            
            container_layout = QVBoxLayout(self)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addWidget(self.ui)
            
            self.ui.btnCancel.clicked.connect(self.return_to_previous_window)
            self.ui.btnSave.clicked.connect(self.save_lawyer)
            
            self.ui.btnBureauCancel.clicked.connect(self.return_to_previous_window)
            self.ui.btnBureauSave.clicked.connect(self.save_bureau)
            
            self.ui.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.lineBureauPassword.setEchoMode(QtWidgets.QLineEdit.Password)
            
            if isinstance(self.current_user_id, list) and self.current_user_id:
                self.fetch_law_firm_id()
            
            self.setup_ui_for_role()

        except AttributeError as e:
            QMessageBox.critical(self, "UI Hatası", f"UI bileşenleri yüklenemedi: {e}")
        except Exception as e:
            print(f"Bilinmeyen UI Hatası: {e}")

    def setup_ui_for_role(self):
        
        # === MOD 1: Sadece Avukat Kaydı ("lawyer") ===
        if self.register_mode == "lawyer":
            # Büro widget'larını gizle
            if hasattr(self.ui, 'group_bureau_widgets'):
                for widget in self.ui.group_bureau_widgets:
                    widget.setVisible(False)
            
            # Avukat widget'larını göster
            if hasattr(self.ui, 'group_lawyer_widgets'):
                for widget in self.ui.group_lawyer_widgets:
                    widget.setVisible(True)
                
            if hasattr(self.ui, 'labelTitle'):
                self.ui.labelTitle.setText("YENİ AVUKAT KAYDI")
  

        elif self.register_mode == "bureau":
            if hasattr(self.ui, 'group_lawyer_widgets'):
                for widget in self.ui.group_lawyer_widgets:
                    widget.setVisible(False)
            
            if hasattr(self.ui, 'group_bureau_widgets'):
                for widget in self.ui.group_bureau_widgets:
                    widget.setVisible(True)
            
            if hasattr(self.ui, 'labelTitle'):
                self.ui.labelTitle.setText("YENİ BÜRO KAYDI")


        else:
 
            if hasattr(self.ui, 'group_lawyer_widgets'):
                for widget in self.ui.group_lawyer_widgets:
                    widget.setVisible(True)
            
            if hasattr(self.ui, 'group_bureau_widgets'):
                for widget in self.ui.group_bureau_widgets:
                    widget.setVisible(True)

            if hasattr(self.ui, 'labelTitle'):
                self.ui.labelTitle.setText("KAYIT EKRANI")


    def fetch_law_firm_id(self):
        if not isinstance(self.current_user_id, list) or not self.current_user_id:
            return

        first_lawyer_id_in_firm = self.current_user_id[0]
        conn = connect_to_database()
        if conn is None: return
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT law_firm_id FROM lawyers WHERE lawyer_id = %s"
            cursor.execute(query, (first_lawyer_id_in_firm,))
            result = cursor.fetchone()
            
            if result and result['law_firm_id']:
                self.law_firm_id_to_assign = result['law_firm_id']
        except Exception as e:
            print(f"Büro ID hatası: {str(e)}")
        finally:
            if conn: conn.close()

    def validate_inputs(self):
        self.name = self.ui.lineName.text().strip()
        self.surname = self.ui.lineSurname.text().strip()
        self.email = self.ui.lineEmail.text().strip()
        self.password = self.ui.linePassword.text()
        self.phone = self.ui.linePhone.text().strip() or None
        self.baro_id_str = self.ui.lineBaroId.text().strip()
        self.baro_number = self.ui.lineBaroNumber.text().strip() or None

        if not self.name or not self.surname or not self.email or not self.password:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad, Soyad, Email ve Şifre zorunludur.")
            return False
        
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.email):
            QMessageBox.warning(self, "Geçersiz Format", "Geçerli bir email girin.")
            return False
            
        try:
            if self.baro_id_str: self.baro_id = int(self.baro_id_str)
            else: self.baro_id = None
        except ValueError:
             QMessageBox.warning(self, "Geçersiz Format", "Baro ID sayı olmalıdır.")
             return False
        return True

    def save_lawyer(self):
        if not self.validate_inputs(): return
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO lawyers (name, surname, email, password, phone_number, baro_id, bar_number, law_firm_id, is_admin, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (self.name, self.surname, self.email, self.password, self.phone, self.baro_id, self.baro_number, self.law_firm_id_to_assign, False, datetime.now())
            cursor.execute(query, values)
            conn.commit()
            QMessageBox.information(self, "Başarılı", f"Avukat '{self.name} {self.surname}' kaydedildi.")
            self.return_to_previous_window()
        except Exception as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                QMessageBox.warning(self, "Hata", "Bu email veya Baro ID zaten kayıtlı.")
            else:
                QMessageBox.critical(self, "Hata", f"Kayıt başarısız: {str(e)}")
        finally:
            if conn: conn.close()
    
    def validate_bureau_inputs(self):
        self.bureau_name = self.ui.lineBureauName.text().strip()
        self.bureau_password = self.ui.lineBureauPassword.text()
        self.bureau_address = self.ui.lineBureauAddress.text().strip() or None
        self.bureau_phone = self.ui.lineBureauPhone.text().strip() or None
        self.bureau_email = self.ui.lineBureauEmail.text().strip() or None
        
        if not self.bureau_name or not self.bureau_password:
            QMessageBox.warning(self, "Eksik Bilgi", "Büro Adı ve Şifre zorunludur.")
            return False
        return True

    def save_bureau(self):
        if not self.validate_bureau_inputs(): return
        conn = connect_to_database()
        if conn is None: return
        try:
            cursor = conn.cursor()
            query = "INSERT INTO law_firms (firm_name, password, address, phone_number, email) VALUES (%s, %s, %s, %s, %s)"
            values = (self.bureau_name, self.bureau_password, self.bureau_address, self.bureau_phone, self.bureau_email)
            cursor.execute(query, values)
            conn.commit()
            QMessageBox.information(self, "Başarılı", f"Hukuk Bürosu '{self.bureau_name}' kaydedildi.")
            self.return_to_previous_window()
        except Exception as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                QMessageBox.warning(self, "Hata", "Bu Büro Adı zaten kayıtlı.")
            else:
                QMessageBox.critical(self, "Hata", f"Kayıt başarısız: {str(e)}")
        finally:
            if conn: conn.close()

    def return_to_previous_window(self):
 
        if isinstance(self.current_user_id, list) and self.current_user_id:
            try:
                from views.formMainWindow import formMainWindow 
                self.prev_form = formMainWindow(current_user_id=self.current_user_id)
                self.prev_form.setGeometry(self.geometry())
                self.prev_form.show()
            except Exception as e:
                print(f"Ana sayfaya dönüş hatası: {e}")

    
        else:
            try:
                from views.formLogin import formLogin
                self.prev_form = formLogin()
                self.prev_form.setGeometry(self.geometry())
                self.prev_form.show()
            except Exception as e:
                print(f"Login sayfasına dönüş hatası: {e}")
        

        self.close()