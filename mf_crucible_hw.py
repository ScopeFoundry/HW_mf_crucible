from ScopeFoundry import HardwareComponent
import re
import yaml
import requests
class MFCrucibleHW(HardwareComponent):
    
    name = 'mf_crucible'
    
    def setup(self):
        
        self.settings.New("orcid", initial="0000-0000-0000-0000", dtype=str)
        self.settings.New("proposal", initial="MFP0000", choices=(['MFP0000']), dtype=str)
        self.settings.New("email", initial="nobody@lbl.gov",dtype=str)
        
        self.settings.orcid.add_listener(self.on_enter_orcid_id, argtype = str)
        
        self.add_operation("User Login", self.login_opfunc)

    def login_opfunc(self):
        print("user login operation running")
        
    def on_enter_orcid_id(self):
        orcid = self.settings.orcid.value.replace("-", "")
        orcid_format = "-".join(orcid[i:i+4] for i in range(0,len(orcid),4))
        if all([len(orcid)==16, re.compile("[0-9]*").match(orcid), orcid != "0000000000000000"]):
            user_info = get_proposals_using_orcid(orcid_format)
            # update proposal dropdown options
            proposal_list = user_info['proposals']
            proposal_list.append("InternalResearch")
            prop_lq = self.settings.get_lq('proposal')
            prop_lq.change_choice_list(proposal_list)
            prop_lq.update_value("InternalResearch")
            
            # update user email
            email = user_info['lbl_email'] if user_info['lbl_email'] is not None else user_info['email']
            email_lq = self.settings.get_lq('email')
            email_lq.update_value(email)
            

            
def get_proposals_using_orcid(orcid_id):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f)
    f.close()
    apikey = secrets["apikey"]
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/sciCat-GetUser.aspx?key={apikey}&orcid={orcid_id}")
    if response.text != '' and response.status_code == 200:
        return(response.json())
    else:
        return(f"user with orcid ID {orcid_id} not found in user database")
