from ScopeFoundry import HardwareComponent
import re
import yaml
import requests
class MFCrucibleHW(HardwareComponent):
    
    name = 'mf_crucible'
    
    def setup(self):
        self.settings.New("email", initial="user-email@lbl.gov",dtype=str)
        self.settings.New("user_name", initial = "", dtype = str)
        self.settings.New("orcid", initial="XXXX-XXXX-XXXX-XXXX", dtype=str)
        self.settings.New("proposal", initial="", choices=([]), dtype=str)
        self.settings.New("session_name", initial = "enter a session name to group datasets by", dtype = str)
        self.settings.New("tags", initial = "list,tags,separated,by,commas", dtype = str)
        
        self.settings.orcid.add_listener(self.on_enter_orcid_id, argtype = str)
        self.settings.email.add_listener(self.on_enter_email, argtype = str)
        #self.add_operation("User Login", self.login_opfunc)

    #def login_opfunc(self):
      #  print("user login operation running")
    def update_proposals(self, user_info):
        email = user_info['lbl_email'] if user_info['lbl_email'] is not None else user_info['email']
        
        internal_research_val = f"MFUSER_{email.split('@')[0]} (InternalResearch)"
        proposal_list = user_info['proposals']
        proposal_list.append(internal_research_val)
        prop_lq = self.settings.get_lq('proposal')
        prop_lq.change_choice_list(proposal_list)
        prop_lq.update_value(internal_research_val)

    def update_username(self, user_info):
        # update name
        user_name = f"{user_info['first_name']} {user_info['last_name']}"
        user_name_lq = self.settings.get_lq('user_name')
        user_name_lq.update_value(user_name)
        
    def on_enter_orcid_id(self):
        orcid = self.settings.orcid.value.replace("-", "")
        orcid_format = "-".join(orcid[i:i+4] for i in range(0,len(orcid),4))
        print(orcid_format)
        if all([len(orcid)==16, re.compile("[0-9]*").match(orcid), orcid != "0000000000000000"]):
            user_info = get_proposals_using_orcid(orcid_format)
            print(user_info)
            if user_info is not None:
                # update user email
                email = user_info['lbl_email'] if user_info['lbl_email'] is not None else user_info['email']
                email_lq = self.settings.get_lq('email')
                email_lq.update_value(email)

                # update proposal dropdown options
                self.update_proposals(user_info)
                
                # update user name
                self.update_username(user_info)

                
                
    def on_enter_email(self):
            email = self.settings.email.value.strip()
            user_info = get_proposals_using_email(email)
            print(user_info)
            if user_info is not None:
                # proposal dropdown options
                self.update_proposals(user_info)

                # update name
                self.update_username(user_info)

                # update orcid
                orcid = user_info['orcid']
                if orcid is not None:
                    orcid_lq = self.settings.get_lq('orcid')
                    orcid_lq.update_value(orcid)
                else:
                    print("user needs to add orcid to their user profile")
                
                
    




def get_proposals_using_email(email):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f)
    f.close()
    apikey = secrets["apikey"]
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/scicat/getuserbyemail.aspx?key={apikey}&email={email}")
    if response.text != '' and response.status_code == 200:
        return(response.json())
    else:
        return(None)


def get_proposals_using_orcid(orcid_id):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f)
    f.close()
    apikey = secrets["apikey"]
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/sciCat-GetUser.aspx?key={apikey}&orcid={orcid_id}")
    if response.text != '' and response.status_code == 200:
        return(response.json())
    else:
        return(None)
