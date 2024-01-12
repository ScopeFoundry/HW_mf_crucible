from ScopeFoundry.measurement import Measurement
from qtpy.QtWidgets import QPushButton, QLabel

class MFCrucibleControlPanel(Measurement):
    
    name = "user_login_mf_crucible"
    
    
    def setup(self):
        #self.user_info = self.app.hardware['mf_crucible']
        pass
    
    def setup_figure(self):
        self.ui = self.app.hardware['mf_crucible'].settings.New_UI()
        self.hw_name = "mf_crucible"
        self.mf_crucible = self.app.hardware[self.hw_name]
        
        logout_push_button = QPushButton('Log Out')
        self.ui.layout().addWidget(logout_push_button)
        logout_push_button.clicked.connect(self.clear_userinfo)

    def clear_userinfo(self):
        print("ya clicked")
        print(self.mf_crucible.settings.proposal)
        self.mf_crucible.settings['user_name'] = ""
        self.mf_crucible.settings['orcid'] = "XXXX-XXXX-XXXX-XXXX"
        self.mf_crucible.settings['email'] = "user-email@lbl.gov"
        prop_lq = self.mf_crucible.settings.get_lq('proposal')
        prop_lq.change_choice_list([])
        prop_lq.update_value("")