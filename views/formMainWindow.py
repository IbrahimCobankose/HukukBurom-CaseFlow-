
from forms.mainWindowFormUi import Ui_FormMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from database.connect_to_database import connect_to_database
from PyQt5.QtCore import QDate
from datetime import datetime
import locale 
from views.formMyBureau import formMyBureau

from views.MenuBase import MenuBase


class formMainWindow(QtWidgets.QWidget, MenuBase):
    def __init__(self, current_user_id=None):
        super(formMainWindow, self).__init__()
        
        self.ui = Ui_FormMainWindow()
        
        container_layout = QtWidgets.QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.ui)
        

        self.turkish_months = [
            "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        ]

        
        self.current_user_id = current_user_id
        
        self.setup_menu(self.ui)
        
        try:
            self.ui.btnAddLawyer.clicked.disconnect() 
        except:
            pass 

        self.ui.btnAddLawyer.clicked.connect(self.open_my_bureau)
        
        self.calendar_data = {}
        self.load_calendar_data()
        self.highlight_dates()
        self.ui.calendarWidget.clicked.connect(self.show_event_info)
        
        self.load_upcoming_event_note()

    def load_upcoming_event_note(self):
        event_translation = {
            'Hearing': 'Duruşma', 'Meeting': 'Toplantı',
            'Discovery': 'Keşif', 'Other': 'Diğer'
        }
        
        conn = connect_to_database()
        if conn is None:
            self.ui.textDateNote.setText("Veritabanı bağlantı hatası.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            
            if isinstance(self.current_user_id, list):
                lawyer_ids_tuple = tuple(self.current_user_id)
            else:
                lawyer_ids_tuple = (self.current_user_id,)

            if not lawyer_ids_tuple:
                self.ui.textDateNote.setText("İlişkili avukat bulunamadı.")
                return

            in_clause = ','.join(['%s'] * len(lawyer_ids_tuple))
            query_event = f"""
                SELECT ce.event_type, ce.event_date, ce.case_id, c.case_title
                FROM calendar_events ce
                JOIN cases c ON ce.case_id = c.case_id
                WHERE ce.lawyer_id IN ({in_clause}) AND ce.event_date >= NOW()
                ORDER BY ce.event_date ASC LIMIT 1;
            """
            
            cursor.execute(query_event, lawyer_ids_tuple)
            event = cursor.fetchone()

            if event:
                case_id = event['case_id']
                event_type_tr = event_translation.get(event['event_type'], event['event_type'])
                case_title = event['case_title']
                
 
                event_dt = event['event_date']
                tr_month = self.turkish_months[event_dt.month]
                event_date_tr = f"{event_dt.day} {tr_month} {event_dt.year}, {event_dt.strftime('%H:%M')}"


                query_note = "SELECT note_content FROM case_notes WHERE case_id = %s ORDER BY created_at DESC LIMIT 1;"
                cursor.execute(query_note, (case_id,))
                note = cursor.fetchone()
                
                note_content = "Dava notu bulunmamaktadır."
                if note:
                    note_content = note['note_content']

                display_text = (
                    f"YAKLAŞAN ETKİNLİK: {event_type_tr}\n"
                    f"Tarih: {event_date_tr}\n\n"
                    f"İlgili Dava: {case_title}\n"
                    f"---------------------------------\n"
                    f"Son Dava Notu:\n{note_content}"
                )
                self.ui.textDateNote.setText(display_text)
            else:
                self.ui.textDateNote.setText("Yaklaşan bir etkinlik bulunmamaktadır.")
        except Exception as e:
            self.ui.textDateNote.setText(f"Etkinlik yüklenirken hata oluştu: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Yaklaşan etkinlik yüklenemedi: {str(e)}")
        finally:
            if conn: conn.close()

    def load_calendar_data(self):
        conn = connect_to_database()
        if conn is None:
            QMessageBox.critical(self, "Database Error", "Could not connect to the database!")
            return
        try:
            cursor = conn.cursor(dictionary=True)
            if isinstance(self.current_user_id, list):
                lawyer_ids_tuple = tuple(self.current_user_id)
            else:
                lawyer_ids_tuple = (self.current_user_id,)
            if not lawyer_ids_tuple: return 
            
            in_clause = ','.join(['%s'] * len(lawyer_ids_tuple))
            query = f"""
                (SELECT c.case_id, c.case_title, c.case_number, c.created_at AS date, 'Dava Oluşturma Tarihi' AS type
                 FROM cases c JOIN case_lawyers cl ON c.case_id = cl.case_id
                 WHERE cl.lawyer_id IN ({in_clause}) AND c.created_at IS NOT NULL)
                UNION
                (SELECT c.case_id, c.case_title, c.case_number, c.file_date AS date, 'Dosya Tarihi' AS type
                 FROM cases c JOIN case_lawyers cl ON c.case_id = cl.case_id
                 WHERE cl.lawyer_id IN ({in_clause}) AND c.file_date IS NOT NULL)
                UNION
                (SELECT c.case_id, c.case_title, c.case_number, c.last_hearing_date AS date, 'Son Duruşma Tarihi' AS type
                 FROM cases c JOIN case_lawyers cl ON c.case_id = cl.case_id
                 WHERE cl.lawyer_id IN ({in_clause}) AND c.last_hearing_date IS NOT NULL)
                UNION
                (SELECT c.case_id, c.case_title, c.case_number, c.next_hearing_date AS date, 'Bir Sonraki Duruşma Tarihi' AS type
                 FROM cases c JOIN case_lawyers cl ON c.case_id = cl.case_id
                 WHERE cl.lawyer_id IN ({in_clause}) AND c.next_hearing_date IS NOT NULL)
                UNION
                (SELECT c.case_id, c.case_title, c.case_number, c.decision_date AS date, 'Karar Tarihi' AS type
                 FROM cases c JOIN case_lawyers cl ON c.case_id = cl.case_id
                 WHERE cl.lawyer_id IN ({in_clause}) AND c.decision_date IS NOT NULL)
                UNION
                (SELECT ce.case_id, c.case_title, c.case_number, ce.event_date AS date, ce.event_type AS type
                 FROM calendar_events ce LEFT JOIN cases c ON ce.case_id = c.case_id
                 WHERE ce.lawyer_id IN ({in_clause}) AND ce.event_date IS NOT NULL);
            """
            params = lawyer_ids_tuple * 6
            cursor.execute(query, params)
            dates = cursor.fetchall()
            
            for row in dates:
                date_obj = row['date']
                if date_obj:
                    date_str = date_obj.strftime('%Y-%m-%d')
                    if date_str not in self.calendar_data:
                        self.calendar_data[date_str] = []
                    self.calendar_data[date_str].append({
                        'title': row.get('case_title'), 'number': row.get('case_number'),
                        'date_full': date_obj, 'type': row.get('type')
                    })
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while loading calendar data: {str(e)}")
        finally:
            if conn: conn.close()

    def highlight_dates(self):
        important_date_format = QtGui.QTextCharFormat()
        important_date_format.setBackground(QtGui.QColor("#e0e0e0"))
        important_date_format.setFontWeight(QtGui.QFont.Bold)

        for date_str in self.calendar_data.keys():
            q_date = QDate.fromString(date_str, 'yyyy-MM-dd')
            self.ui.calendarWidget.setDateTextFormat(q_date, important_date_format)

    def show_event_info(self, date):
   
        date_str = date.toString('yyyy-MM-dd')
        
        if date_str in self.calendar_data:
            events = self.calendar_data[date_str]
            
   
            tr_month = self.turkish_months[date.month()]
            date_header = f"{date.day()} {tr_month} {date.year()}"
            message = f"{date_header} Tarihindeki Etkinlikler\n\n"

            for event in events:
                time_str = event['date_full'].strftime('%H:%M') if isinstance(event['date_full'], datetime) else "N/A"
                message += f"Dava: {event.get('title', 'N/A')} ({event.get('number', 'N/A')})\n"
                message += f"Etkinlik Türü: {event.get('type', 'N/A')}\n"
                if time_str != "N/A":
                     message += f"Saat: {time_str}\n"
                message += "\n"
            QMessageBox.information(self, "Takvim Etkinlikleri", message)
        else:

            tr_month = self.turkish_months[date.month()]
            date_header = f"{date.day()} {tr_month} {date.year()}"
            message = f"{date_header} tarihinde herhangi bir dava veya etkinlik bulunmamaktadır."
     
            QMessageBox.information(self, "Takvim Etkinlikleri", message)


    def open_my_bureau(self):
        """Bürom sayfasını açar."""
        self.bureau_form = formMyBureau(current_user_id=self.current_user_id)
        self.bureau_form.setGeometry(self.geometry())
        self.bureau_form.show()
        self.close()
  
    def exit_button_clicked(self):
        """Giriş ekranına döner (MenuBase'i ezer)."""
        from views.formLogin import formLogin
        self.login_form = formLogin()
        self.login_form.setGeometry(self.geometry())
        self.login_form.show()
        self.close()