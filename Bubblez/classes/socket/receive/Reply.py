import json, requests, traceback
from ...Color import Color
from ...Log import logTime


class Reply:
    def __init__(self, client, data) -> None:
        self.client = client
        self.replyid = int(data["replyid"])
        self._from = data['from']
        self.raw_data = data 
        if "reply" in data: self.message = data["reply"]
        elif "content" in data: self.message = data['content']
        if "username" in data: self.username = data['username']
        if "rnfsw" in data: self.nsfw = data["rnsfw"]
        if "edit_date" in data:  self.edited = data["edit_date"]
        if "edited" in data: self.edited = data["edited"] 
        if "reply_date" in data: self.reply_date = data["reply_date"]

    def delete(self):
        """
        Deleting to this reply!
        """
        url, data = self.client.live_url, {"token": self.client.token, "replyid": self.replyid, "confirm": "true"}
        if self.client.canary: url = self.client.canary_url
        url += "/reply/delete"
        response = requests.post(url=url, data=data)
        if response.ok:
            try:
                resp_js = response.json()
                if '200' in resp_js:
                    if resp_js['200'] == f'reply {self.replyid} has been deleted':
                        self.deleted = True
                        print(f"{Color.OKGREEN}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} Reply deleted! {Color.ENDC}")
                        return True 
                else:
                    print(f"{Color.WARNING}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} The reply has not been deleted,  Code: {response.status_code}", Color.ENDC)
                    print(f"{Color.WARNING}Reason: {response.content}", Color.ENDC)
                    return False 
            except:
                print(f"{Color.FAIL}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} There is a error acoured on reply/delete! Code: {response.status_code}", Color.ENDC)
                print(f"{Color.FAIL}Reason: {response.content}", Color.ENDC)
                traceback.print_exc()
                return False 
        else:      
            print(f"{Color.FAIL}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} There is a error acoured on reply/delete! Code: {response.status_code}", Color.ENDC)
            print(f"{Color.FAIL}Reason: {response.content}", Color.ENDC)
            traceback.print_exc()
            return False  

    def edit(self, message:str):
        """
        Editing this reply!

        message: `str` The message than will be displayed in the reply!
        """
        data, url = {"token": self.client.token, "reply": message, "replyid": self.replyid}, self.client.live_url
        url += "/reply/edit"
        response = requests.post(url=url, data=data)
        if response.ok:
            try:
                resp_js = response.json()
                if '200' in resp_js and resp_js['200'] == f'Reply {self.replyid} has been updated':
                    self.message = message
                    self.edited = True
                    print(f"{Color.OKGREEN}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} Reply edited! {Color.ENDC}")
                    return self
                else:
                    print(f"{Color.WARNING}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} Reply has not been edited! Code: {response.status_code}", Color.ENDC)
                    print(f"{Color.WARNING}Reason: {response.content}", Color.ENDC)
                    return False
            except:
                print(f"{Color.FAIL}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} There is a error acoured on reply/edit! Code: {response.status_code}", Color.ENDC)
                print(f"{Color.FAIL}Reason: {response.content}", Color.ENDC)
                traceback.print_exc()
                return False
        else:      
            print(f"{Color.FAIL}[Bubblez.py-websockets-{self.client.prefix_log}] {logTime()} There is a error acoured on reply/edit! Code: {response.status_code}", Color.ENDC)
            print(f"{Color.FAIL}Reason: {response.content}", Color.ENDC)
            traceback.print_exc()
            return False 

    def json(self):
        return self.raw_data