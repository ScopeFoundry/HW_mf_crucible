from ScopeFoundry import HardwareComponent

class MFCrucibleHW(HardwareComponent):
    
    name = 'mf_crucible'
    
    def setup(self):
        
        self.settings.New("orcid1", initial="0000-0000-0000-0000", dtype=str)
        self.settings.New("orcid2", initial="0000-0000-0000-0000", dtype=str)
        self.settings.New("orcid3", initial="0000-0000-0000-0000", dtype=str)
        self.settings.New("proposal", initial="MFP0000", choices=(['MFP0000']), dtype=str)
        self.settings.New("email", initial="nobody@lbl.gov",dtype=str)
        
        self.orcid1.textChanged.connect(self.on_enter_orcid_id)      
        self.ui.orcid2.textChanged.connect(self.on_enter_orcid_id)      
        self.ui.hardware_treeWidget.orcid3.textChanged.connect(self.on_enter_orcid_id)      
        
    def on_enter_orcid_id(self, text):
        text_clean = text.replace("-", "")
        patt = re.compile("[0-9]*")
        full_text = "-".join([text_clean[0:4], text_clean[4:8], text_clean[8:12], text_clean[12:16]])
        print(full_text)
        if all([len(text_clean)==16, patt.match(text_clean)]):
            user_proposal_info = get_proposals_using_orcid(full_text)
            print(user_proposal_info)
            proposal_list = user_proposal_info['proposals']
            proposal_list.append("InternalResearch")
            proposal_list_lq = self.settings.get_lq('proposal')
            proposal_list_lq.change_choice_list(proposal_list)
            # self.ui.proposal_dropdown.clear()
            # self.ui.proposal_dropdown.addItems(proposal_list)

            
def get_proposals_using_orcid(orcid_id):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f, 'r')
    f.close()
    apikey = secrets["apikey"]
    print(f"https://foundry-admin.lbl.gov/api/json/sciCat-GetUser.aspx?key={apikey}&orcid={orcid_id}")
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/sciCat-GetUser.aspx?key={apikey}&orcid={orcid_id}")
    if response.text != '' and response.status_code == 200:
        return(response.json())
    else:
        return(f"user with orcid ID {orcid_id} not found in user database")
