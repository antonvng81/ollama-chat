import flet
from typing import Callable, cast
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai import ChatAI
from ollama_chat.ai.savechat import save_chat
from ollama_chat.ai.getchatfiles import get_chat_files
from ollama_chat.appbar import ChatAppBar
from ollama_chat.mainview import ChatMainView
from ollama_chat.appcontrols import ChatAppControls
from ollama_chat.other.resultmessage import ChatResultMessage
from ollama_chat.sidebar import ChatSideBar
import ollama_chat.other.theme as ChatTheme

class ChatLoadChat(flet.AlertDialog):

    def __init__(self, 
                 account:ChatAccount, 
                 chatAI:ChatAI, 
                 chatMainView:ChatMainView, 
                 chatAppBar:ChatAppBar, 
                 chatSideBar:ChatSideBar, 
                 close_result:Callable) -> None:

        self.account = account
        self.close_result = close_result   
        self.chatAI = chatAI
        self.chatMainView = chatMainView
        self.chatAppBar = chatAppBar
        self.chatSideBar = chatSideBar

        user_dir = cast(str, self.account.user_dir)
        self.chat_files = get_chat_files(user_dir)

        # controls

        self.chat_textfield = flet.TextField(
            hint_text="Enter chat name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,  
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            value=""
            )        

        # Selector for chat

        actions = [
            flet.ElevatedButton(text="Load", on_click=self.submit_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Load chat",color = ChatTheme.dialog_color),
            content=flet.Column([ self.chat_textfield], 
                tight=True,
            ),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )                        

    # Submit event

    def submit_click(self,e):

        self.chat_textfield.error_text = ""
        chat_name = self.chat_textfield.value

        if not chat_name:
            self.chat_textfield.error_text = "Empty chat name!"
            e.page.update()            

        else:

            chat_dir_name = str_codify(chat_name)

            if chat_dir_name not in self.chat_files:
                self.chat_textfield.error_text = "Please choose a saved chat!"
                e.page.update()
            else:

                # Save current chat
                
                if chat_name != self.chatAI.name: 

                    chat_name = cast(str, self.chatAI.name)
                    
                    # Does not save if current chat is removed

                    if str_codify(chat_name) in self.chat_files:

                        save_chat(self.account, self.chatAI)

                # Load selected chat

                chatAppControls = ChatAppControls(self.account, self.chatAI, self.chatMainView, self.chatAppBar, self.chatSideBar)                    
                result_msg = chatAppControls.update_controls_load(e.page, self.chat_files[chat_dir_name])

                self.close_result(e, result_msg)

    def cancel_click(self,e):
        self.close_result(e, ChatResultMessage("Chat load cancelled.", False))




