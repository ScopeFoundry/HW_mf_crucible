from ScopeFoundry.measurement import Measurement

class MFCrucibleControlPanel(Measurement):
    
    name = "mf_crucible_control"
    
    def setup(self):
        #self.user_info = self.app.hardware['mf_crucible']
        pass
    
    def setup_figure(self):
        self.ui = self.app.hardware['mf_crucible'].settings.New_UI()
