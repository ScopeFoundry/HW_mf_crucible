from ScopeFoundry import HardwareComponent
import re
import yaml
from datetime import datetime
import requests

class MFCrucibleHW(HardwareComponent):
    
    name = 'mf_crucible'
    initial_orcid_value= "XXXX-XXXX-XXXX-XXXX"
    initial_email_value = "user-email@lbl.gov"
    
    def setup(self):
        self.settings.New("email", initial = self.initial_email_value, dtype = str)
        self.settings.New("user_name", initial = "", dtype = str)
        self.settings.New("orcid", initial = self.initial_orcid_value, dtype = str)
        self.settings.New("proposal", initial = "", choices = ([]), dtype = str)
        self.settings.New("session_name", initial = "(optional)", dtype = str)
        self.settings.New("comments", initial = "add any desired comments here (optional)", dtype = str)
        self.settings.New("tags", initial = "list,tags,separated,by,commas (optional)", dtype = str)
        #self.settings.New('metadata_file', dtype='file')
                          
        self.settings.orcid.add_listener(self.on_enter_orcid_id, argtype = str)
        self.settings.email.add_listener(self.on_enter_email, argtype = str)
        
    def connect(self):
        print("connected")

    
    def disconnect(self):
        print("disconnected")

    
    def update_proposals(self, proposal_list):
        print(proposal_list)
        prop_lq = self.settings.get_lq('proposal')
        prop_lq.change_choice_list(proposal_list)
        prop_lq.update_value(proposal_list[0])

    
    def update_username(self, user_name):
        # update name
        user_name_lq = self.settings.get_lq('user_name')
        user_name_lq.update_value(user_name)

    
    def on_enter_orcid_id(self):
        if self.settings.email.value.strip() == self.initial_email_value:
            orcid = self.settings.orcid.value
            if orcid != self.initial_orcid_value:
                print("validating orcid")
                orcid = orcid.replace("-", "")
                orcid_format = "-".join(orcid[i:i+4] for i in range(0,len(orcid),4))
            if all([len(orcid)==16, re.compile("[0-9]*").match(orcid), orcid != "0000000000000000"]):
                t = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} pulling user info from proposal database")
                all_user_accounts = get_proposals_using_orcid(orcid_format)
                
                if all_user_accounts is not None:
                    print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} user info received")
                    print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} parsing response")
                    # update user email
                    email = parse_email(all_user_accounts)
                    proposal_list = parse_proposals(all_user_accounts, email)
                    user_name = parse_username(all_user_accounts)
                    
                    print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} updating values")
                    email_lq = self.settings.get_lq('email')
                    email_lq.update_value(email)
                    self.update_proposals(proposal_list)
                    self.update_username(user_name)
                else:
                    print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} proposal database response failed, could be down or user with this orcid not found")
                
    def on_enter_email(self):
        provided_email = self.settings.email.value.strip()
        if provided_email != self.initial_email_value:
            print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} getting user info for email")
            user_info = get_user_using_email(provided_email)
            if user_info is not None:
                print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} user_info received from proposal database")
                all_user_accounts = collect_user_accounts(user_info)
                email = parse_email(all_user_accounts, provided_email)
                proposal_list = parse_proposals(all_user_accounts, email)
                user_name = parse_username(all_user_accounts)

                print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} parsing response and updating values")
                # proposal dropdown options
                self.update_proposals(proposal_list)

                # update name
                self.update_username(user_name)

                # update orcid
                orcid = user_info['orcid']
                if orcid is not None:
                    orcid_lq = self.settings.get_lq('orcid')
                    orcid_lq.update_value(orcid)
                else:
                    print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} user needs to add orcid to their user profile")
            else:
                print(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} proposal database response failed, could be down or user with this email not found")

def get_user_using_email(email):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f)
    f.close()
    apikey = secrets["apikey"]
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/scicat/getuserbyemail.aspx?key={apikey}&email={email}")
    if len(response.json()) > 0 and response.status_code == 200:
        return(response.json()) # single dictionary
    else:
        return(None)


def get_proposals_using_orcid(orcid_id):
    with open("secrets/proposaldb.yaml") as f:
        secrets= yaml.safe_load(f)
    f.close()
    apikey = secrets["apikey"]
    response = requests.request(method="get", url=f"https://foundry-admin.lbl.gov/api/json/sciCat-GetUser.aspx?key={apikey}&orcid={orcid_id}")
    if len(response.json())> 0 and response.status_code == 200:
        return(response.json()) # list
    else:
        return(None)


def parse_email(all_user_accounts, provided_email=""):
    emails = {acct["email"]:acct['lbl_email'].lower() for acct in all_user_accounts if acct['lbl_email'] is not None}
    num_lbl_emails = len(set(list(emails.values())))
    
    if num_lbl_emails == 1:
        use_this_email = list(emails.values())[0]
    elif num_lbl_emails > 1 and provided_email != "":
        use_this_email = emails[provided_email]
    elif num_lbl_emails > 1 and provided_email == "":
        use_this_email = list(emails.values())[0]
    else:
        use_this_email = provided_email
        
    return(use_this_email)


def collect_user_accounts(user_info):
    try:
        all_user_accounts = get_proposals_using_orcid(user_info['orcid'])
    except:
        all_user_accounts = [user_info]
    return(all_user_accounts)


def parse_proposals(all_user_accounts, email):
    internal_research_val = f"MFUSER_{email.split('@')[0]} (InternalResearch)"
    proposal_list = [internal_research_val]
    for acct in all_user_accounts:
        proposal_list += acct['proposals']
    return(proposal_list)
   


def parse_username(all_user_accounts):
    usernames = [f"{acct['first_name']} {acct['last_name']}" for acct in all_user_accounts if acct['last_name'] is not None]
    num_names = len(set(usernames))
    print(set(usernames))
    if num_names == 1:
        return(usernames[0])
    elif num_names > 1:
        return('multiple names found, please type your first and last name manually')
    else:
        return("no names found for this orcid")