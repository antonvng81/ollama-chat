import json
import os
from ollama_chat.account.account import ChatAccount

class ChatAppSession:

    CHAT_APP_SESSION = None

    def __init__(self, account:ChatAccount) -> None:
        
        self.last_chat = None
        self.account = account

        ChatAppSession.CHAT_APP_SESSION = self


    # Save the app session

    def save_app_session(self)-> None:

        upload_dir = os.environ.get('FLET_UPLOAD_DIR')

        file_path = f"{upload_dir}/{self.account.user_dir}"
        file_name = f"{file_path}/session.json"

        with open(file_name, 'w') as file:
            json.dump({
                "user_name":self.account.user_name,
                "last_chat":self.last_chat},
                file) 



    # Load the app session

    def load_app_session(self) -> bool:

        upload_dir = os.environ.get('FLET_UPLOAD_DIR')

        file_path = f"{upload_dir}/{self.account.user_dir}"
        file_name = f"{file_path}/session.json"

        if not os.path.exists(file_name):
            return False
    
        with open(file_name, 'r') as file:            
            data = json.load(file)
            
        self.last_chat = data["last_chat"]            
        self.user_name = data["user_name"]
        
        return True



