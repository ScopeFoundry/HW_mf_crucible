from ScopeFoundry.measurement import Measurement

class MFCrucibleControlPanel(Measurement):
    
    name = "mf_crucible_control"
    
    def setup(self):
        #self.user_info = self.app.hardware['mf_crucible']
        pass
    
    def setup_figure(self):
        #self.user_info.settings.orcid.textChanged.connect(self.on_enter_orcid_id)
        
        #self.ui = self.user_info.settings.New_UI()
        #self.ui.email.returnPressed.connect(self.x_up)
        pass
    def x_up(self):
        print("pushed the xup button")