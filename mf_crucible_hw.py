from ScopeFoundry import HardwareComponent

class MFCrucibleHW(HardwareComponent):
    
    name = 'mf_crucible'
    
    def setup(self):
        
        self.settings.New("orcid", initial="0000-0000-0000-0000", dtype=str)
        self.settings.New("proposal", initial="MFP0000", choices=(['MFP0000']), dtype=str)
        self.settings.New("email", initial="nobody@lbl.gov",dtype=str)
    
    