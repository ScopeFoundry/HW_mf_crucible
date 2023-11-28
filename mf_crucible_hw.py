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
        patt = re.compile("[0-9]*")
        orcid_format = "-".join(string[i:i+4] for i in range(0,len(string),4))
        print(orcid_format)
        #full_text = "-".join([orcid[0:4], orcid[4:8], orcid[8:12], orcid[12:16]])
        if all([len(orcid)==16, re.compile("[0-9]*").match(orcid)]):
            user_info = get_proposals_using_orcid(orcid_format)
            
            # update proposal dropdown options
            proposal_list = user_proposal_info['proposals']
            self.settings.get_lq('proposal').change_choice_list(proposal_list.append("InternalResearch"))
            self.settings.get_lq('proposal').update_value("InternalResearch")
            
            # update user email
            email = user_info['lbl_email'] if user_info['lbl_email'] is not None else user_info['email']
            self.settings.get_lq('email').update_value(email)
            

            
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
