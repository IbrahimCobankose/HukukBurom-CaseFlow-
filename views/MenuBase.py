# views/MenuBase.py

from PyQt5 import QtWidgets

class MenuBase:
  
    
    def setup_menu(self, ui):
  
        
        try:
            ui.btnHome.clicked.connect(self.home_button_clicked)
            ui.btnCases.clicked.connect(self.cases_button_clicked)
            ui.btnFinancialManag.clicked.connect(self.financial_button_clicked)
            ui.btnLegislation.clicked.connect(self.legislation_button_clicked)
            
            ui.btnPetitions.clicked.connect(self.petitions_button_clicked)
            ui.btnArchive.clicked.connect(self.archive_button_clicked)
            
            ui.btnAddLawyer.clicked.connect(self.addLawyer_button_clicked)
            
            ui.btnExit.clicked.connect(self.exit_button_clicked)
            
        except AttributeError as e:
            print(f"HATA: UI dosyanız (arayüz) MenuBase ile uyumsuz. Buton adı hatası: {e}")
            return

        if hasattr(self, 'current_user_id') and self.current_user_id:
            if isinstance(self.current_user_id, list):
                ui.btnAddLawyer.setVisible(True)
            else:
                ui.btnAddLawyer.setVisible(False)
        else:
             if hasattr(ui, 'btnAddLawyer'):
                ui.btnAddLawyer.setVisible(False) 


    def home_button_clicked(self):
        if type(self).__name__ == "formMainWindow":
            if hasattr(self, 'load_upcoming_event_note'):
                self.load_upcoming_event_note()
            return
            
        from views.formMainWindow import formMainWindow
        self.main_form = formMainWindow(current_user_id=self.current_user_id)
        self.main_form.setGeometry(self.geometry())
        self.main_form.show()
        self.close()

    def cases_button_clicked(self):
        if type(self).__name__ == "formCases":
            if hasattr(self, 'load_case_data'):
                self.load_case_data()
            return
            
        from views.formCases import formCases
        self.cases_form = formCases(current_user_id=self.current_user_id)
        self.cases_form.setGeometry(self.geometry())
        self.cases_form.show()
        self.close()
        
    def financial_button_clicked(self):
        if type(self).__name__ == "formFinancialManagement":
            if hasattr(self, 'load_initial_data'):
                self.load_initial_data()
            return
            
        from views.formFinancialManagement import formFinancialManagement
        self.financial_form = formFinancialManagement(current_user_id=self.current_user_id)
        self.financial_form.setGeometry(self.geometry())
        self.financial_form.show()
        self.close()
        
    def legislation_button_clicked(self):
        if type(self).__name__ == "formLegislation": return
        
        from views.formLegislation import formLegislation 
        self.legislation_form = formLegislation(current_user_id=self.current_user_id)
        self.legislation_form.setGeometry(self.geometry())
        self.legislation_form.show()
        self.close()
        

        
    def petitions_button_clicked(self):
        if type(self).__name__ == "formPetitions": return
            
        from views.formPetitions import formPetitions
        self.petitions_form = formPetitions(current_user_id=self.current_user_id)
        self.petitions_form.setGeometry(self.geometry())
        self.petitions_form.show()
        self.close()
        
    def archive_button_clicked(self):
        if type(self).__name__ == "formArchive":
            if hasattr(self, 'load_archived_cases'):
                self.load_archived_cases()
            return

        from views.formArchive import formArchive
        self.archive_form = formArchive(current_user_id=self.current_user_id)
        self.archive_form.setGeometry(self.geometry())
        self.archive_form.show()
        self.close()
        
    def addLawyer_button_clicked(self):
 
        if type(self).__name__ == "formMyBureau": 
            if hasattr(self, 'load_bureau_lawyers'):
                self.load_bureau_lawyers()
            return
            
        from views.formMyBureau import formMyBureau
        self.bureau_form = formMyBureau(current_user_id=self.current_user_id)
        self.bureau_form.setGeometry(self.geometry())
        self.bureau_form.show()
        self.close()

    def exit_button_clicked(self):
        self.home_button_clicked()