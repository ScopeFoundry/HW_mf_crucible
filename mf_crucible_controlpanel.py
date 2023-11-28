from ScopeFoundry.measurement import Measurement

class MFCrucibleControlPanel(Measurement):
    
    name = "mf_crucible_control"
    
    def setup(self):
        #self.user_info = self.app.hardware['mf_crucible']
        pass
    
    def setup_figure(self):
        #self.user_info.settings.orcid.textChanged.connect(self.on_enter_orcid_id)
        
        self.ui = self.app.hardware['mf_crucible'].settings.New_UI()
        self.ui.orcid2.textChanged.connect(self.on_enter_orcid_id)      
        self.ui.hardware_treeWidget.orcid3.textChanged.connect(self.on_enter_orcid_id)      
        
        self.ui.email.returnPressed.connect(self.x_up)

    def x_up(self):
        print("pushed the xup button")