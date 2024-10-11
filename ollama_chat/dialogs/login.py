import flet

from ollama_chat.account import ChatAccount
from ollama_chat.account.session import ChatAppSession
from ollama_chat.appcontrols.appcontrols import ChatAppControls
from ollama_chat.dialogs.register import ChatRegister
from ollama_chat.dialogs.newchat import ChatNewChat
from ollama_chat.mainview.message import ChatMessage
from ollama_chat.mainview.view import ChatMessageView
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from typing import cast

# Login dialog

class ChatLogin(flet.AlertDialog):

    def __init__(self, page:flet.Page) -> None:

        self.account = ChatAccount()
        self.chatAppControls = None

        ## controls

        self.new_chat_dialog = None

        self.username_textfield = flet.TextField(
            hint_text="Enter your name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14),# type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14),# type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            on_submit=self.login_click,
            shift_enter=True
            )
        
        self.password_textfield = flet.TextField(
            hint_text="Enter your password",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14),# type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14),# type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            on_submit=self.login_click,
            shift_enter=True,
            password=True,
            can_reveal_password=True
            )        

        # actions

        actions = [
            flet.ElevatedButton(text="Register account", on_click=self.register_click),
            flet.ElevatedButton(text="Login chat", on_click=self.login_click),
            ]
            
        # create empty page
            
        page.horizontal_alignment = "stretch" # type: ignore
        page.add(flet.Container())
        page.update()

        # init
                    
        super().__init__(      
            modal=True,
            open=True,
            title=flet.Text("Welcome!",color = ChatTheme.dialog_color),
            content=flet.Column([
                self.username_textfield, 
                self.password_textfield], 
                tight=True,),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,)
        
    # methods

    def login_click(self, e):

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

            if self.account.login(user_name, password):

                app_session = ChatAppSession(self.account)                
                session_ok = False

                if app_session.load_app_session():
                    if app_session.last_chat is not None:
                    
                        e.page.close(self)

                        last_chat = cast(str, app_session.last_chat)

                        self.chatAppControls = ChatAppControls()                        
                        result_msg = self.chatAppControls.create_controls_load(self.account, e.page, last_chat)

                        if result_msg.success:
                            
                            message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                            
                            self.chatAppControls.chatMainView.chatMessageView.chat(message) #type:ignore

                        session_ok = result_msg.success

                if not session_ok:

                    # create an empty chat if session failed
                    e.page.close(self)

                    self.chatAppControls = ChatAppControls()                        
                    self.new_chat_dialog = ChatNewChat(self.account, self.new_chat_result, self.chatAppControls)
                    e.page.open(self.new_chat_dialog) 


            else:
                self.username_textfield.error_text = "Login autentication failed!"
                self.password_textfield.error_text = "Login autentication failed!"


    def new_chat_result(self, e, result_msg:ChatResultMessage):

        e.page.close(self.new_chat_dialog)
        self.new_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                            
        self.chatAppControls.chatMainView.chatMessageView.chat(message) #type:ignore

    def register_click(self, e):
        e.page.close(self)
        e.page.open(ChatRegister(e.page)) 

