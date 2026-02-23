
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from forms.archiveFormUi import Ui_FormArchive
from database.connect_to_database import connect_to_database
from views.MenuBase import MenuBase


class formArchive(QtWidgets.QWidget, MenuBase):


    STATUS_MAP_FROM_DB = {
        "Preparation": "Hazırlık",
        "In Trial": "Duruşma Aşamasında",
        "Awaiting Decision": "Karar Aşamasında",
        "Closed": "Sonuçlandı"
    }


    def __init__(self, current_user_id=None):
        super(formArchive, self).__init__()
        
        self.ui = Ui_FormArchive()
        
        container_layout = QtWidgets.QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.ui)
        
        self.current_user_id = current_user_id
        
        self.load_archived_cases()
        
        # Ana içerik butonu
        self.ui.btnActive.clicked.connect(self.activate_selected_case)
        
        # Menü Butonları
        self.setup_menu(self.ui)

    def load_archived_cases(self):
        conn = connect_to_database()
        if conn is None:
            QMessageBox.critical(self, "Veritabanı Hatası", "Veritabanına bağlanılamadı!") # -> Türkçe
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
            WHERE {where_clause} AND c.is_active = FALSE;
            """
            
            cursor.execute(query, params)
            cases = cursor.fetchall()
            
            model = QStandardItemModel()
            self.ui.tableView.setModel(model)
            
            
            headers = ["Dava ID", "Dava Başlığı", "Dava Numarası", "Durum", "Oluşturulma Tarihi", 
                       "Avukat ID", "Avukat Adı", "Müvekkil Adı"]
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
                    QStandardItem(f"{row_data.get('lawyer_name', '')} {row_data.get('lawyer_surname', '')}"),
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
            self.ui.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Arşivlenmiş veriler yüklenirken bir hata oluştu: {str(e)}") # -> Türkçe
        finally:
            if conn:
                conn.close()

    def activate_selected_case(self):
        selected_indexes = self.ui.tableView.selectionModel().selectedRows()
        
        if not selected_indexes:
            # --- GÜNCELLEME 3: Mesajlar Türkçeleştirildi ---
            QMessageBox.warning(self, "Seçim Yapılmadı", "Lütfen aktif etmek için listeden bir dava seçin.")
            return
            
        selected_row = selected_indexes[0].row()
        case_id_item = self.ui.tableView.model().item(selected_row, 0)
        
        if not case_id_item: return 
            
        case_id = int(case_id_item.text())

        reply = QMessageBox.question(self, 'Aktif Etmeyi Onayla', 
                                     f"{case_id} ID'li davayı aktif etmek istediğinizden emin misiniz?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No: return

        conn = connect_to_database()
        if conn is None: return
        
        try:
            cursor = conn.cursor()
            update_query = "UPDATE cases SET is_active = TRUE WHERE case_id = %s"
            cursor.execute(update_query, (case_id,))
            conn.commit()
            
            QMessageBox.information(self, "Başarılı", f"Dava (ID: {case_id}) başarıyla aktifleştirildi.")
            
            self.load_archived_cases()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Veritabanı Hatası", f"Dava aktifleştirilirken bir hata oluştu: {str(e)}")
        finally:
            if conn: conn.close()