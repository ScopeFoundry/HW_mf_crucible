from ScopeFoundry.measurement import Measurement
from datetime import datetime
from qtpy.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import QTimer, QTime

class MFCrucibleControlPanel(Measurement):
    
    name = "user_login_mf_crucible"
    
    
    def setup(self):
        #self.user_info = self.app.hardware['mf_crucible']
        pass
    
    def setup_figure(self):
        self.ui = self.app.hardware['mf_crucible'].settings.New_UI()
        self.hw_name = "mf_crucible"
        self.mf_crucible = self.app.hardware[self.hw_name]

        save_push_button = QPushButton('Login')
        logout_push_button = QPushButton('Log Out')

        self.ui.layout().addWidget(save_push_button)
        self.ui.layout().addWidget(logout_push_button)
        
        save_push_button.clicked.connect(self.save_info)
        logout_push_button.clicked.connect(self.clear_userinfo)

        # self.timer = QTimer(self)
        #self.timer.timeout.connect(self.clear_userinfo_at_time)
        #self.timer.start(4e6)  # Update every hour

    
    def update_time(self):
        # Get the current time and set it on the label
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(f"Current Time: {current_time}")
        
    def save_info(self):
        if self.mf_crucible.settings['proposal'] == []:
            try:
                self.on_enter_email()
            except:
                self.on_enter_orcid_id()
        
    
    def clear_userinfo(self):
        print(self.mf_crucible.settings.proposal)
        self.mf_crucible.settings['user_name'] = ""
        self.mf_crucible.settings['orcid'] = "XXXX-XXXX-XXXX-XXXX"
        self.mf_crucible.settings['email'] = "user-email@lbl.gov"
        self.mf_crucible.settings['session_name'] = "enter a session name to group datasets by (optional)"
        self.mf_crucible.settings['tags'] = "enter a comma separated list of keywords to tag your dataset with (optional)"
        prop_lq = self.mf_crucible.settings.get_lq('proposal')
        prop_lq.change_choice_list([])
        prop_lq.update_value("")


    # def clear_userinfo_at_time(self):
    #     if int(datetime.strftime(datetime.now(), "%H")) >= 23:
    #         self.clear_userinfo()













