import flet

from ollama_chat.ai.ai import ollama_get_models
from ollama_chat.dialogs.newchat import ChatNewChat
from ollama_chat.dialogs.pullmodel import ChatPullModel
from ollama_chat.mainview.message import ChatMessage
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.account import ChatAccount
from ollama_chat.appcontrols.appcontrols import ChatAppControls

# Login dialog

class ChatRegister(flet.AlertDialog):

    def __init__(self, page:flet.Page) -> None:

        self.account = ChatAccount()

        ## controls

        self.pull_model_dialog = None
        self.new_chat_dialog = None

        self.username_textfield = flet.TextField(
            hint_text="Register your name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            on_submit=self.register_click,
            shift_enter=True
            )
        
        self.password_textfield = flet.TextField(
            hint_text="Register your password",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            on_submit=self.register_click,
            shift_enter=True,
            password=True,
            can_reveal_password=True            
            )        

        # actions

        actions = [
            flet.ElevatedButton(text="Register", on_click=self.register_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]
            
        # create empty page
            
        page.horizontal_alignment = "stretch" # type: ignore
        page.add(flet.Container())
        page.update()

        # init
                    
        super().__init__(      
            modal=True,
            open=True,
            title=flet.Text("Register a new account!",color = ChatTheme.dialog_color),
            content=flet.Column([
                self.username_textfield, 
                self.password_textfield], 
                tight=True,),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,)
        
    # methods

    def register_click(self, e):

        check_fields = True
        if not self.username_textfield.value:
            self.username_textfield.error_text = "User name can't be empty!"
            self.username_textfield.update()
            check_fields= False

        if not self.password_textfield.value:
            self.password_textfield.error_text = "User password can't be empty!"
            self.password_textfield.update()
            check_fields= False

        if check_fields:

            user_name = self.username_textfield.value.strip() # type: ignore
            password = self.password_textfield.value.strip() # type: ignore

            if self.account.register(user_name, password):

                e.page.close(self)

                if not ollama_get_models():

                    # This dialog only closes if exists a model

                    self.pull_model_dialog = ChatPullModel(True, self.pull_model_result)
                    e.page.open(self.pull_model_dialog)
                
                else:
                    
                    # This dialog does not have cancel button

                    self.new_chat_dialog = ChatNewChat(self.account, self.new_chat_result, ChatAppControls())
                    e.page.open(self.new_chat_dialog)

            else:
                self.username_textfield.error_text = "Register autentication failed, choose another name!"
                self.password_textfield.error_text = "Register autentication failed!"


    def new_chat_result(self, e, result_msg:ChatResultMessage):

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.new_chat_dialog.chatAppControls.chatMainView.chatMessageView.chat(message)    # type: ignore

        e.page.close(self.new_chat_dialog)
        self.new_chat_dialog = None

       
    def cancel_click(self, e):
        from ollama_chat.dialogs.login import ChatLogin

        e.page.close(self)
        e.page.open(ChatLogin(e.page)) 

    def pull_model_result(self, e, model_list:list, result_msg:ChatResultMessage):
       
        e.page.close(self.pull_model_dialog)
        self.pull_model_dialog = None

        # This dialog does not have cancel button

        self.new_chat_dialog = ChatNewChat(self.account, self.new_chat_result, ChatAppControls())
        e.page.open(self.new_chat_dialog)        