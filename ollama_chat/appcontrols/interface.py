import flet

from ollama_chat.account import ChatAccount
from ollama_chat.other.resultmessage import ChatResultMessage

class ChatAppControlsInterface:
        
    def create_controls_default(
        self,
        account:ChatAccount,        
        page:flet.Page, 
        chat_name:str, 
        model:str)->ChatResultMessage: # type: ignore
        pass

    def update_controls_default(
        self,
        account:ChatAccount,        
        page:flet.Page,
        chat_name:str, 
        model:str,)->ChatResultMessage: # type: ignore
        pass

    def update_controls_load(self, e, file_name:str)->ChatResultMessage: # type: ignore
        pass

    def empty(self)->bool:
        return True
    
