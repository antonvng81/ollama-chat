from typing import Callable, cast

import flet
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai import ollama_get_models
from ollama_chat.ai.ai import ChatAI
from ollama_chat.ai.getchatfiles import get_chat_files
from ollama_chat.ai.savechat import save_chat
from ollama_chat.appcontrols.interface import ChatAppControlsInterface

from ollama_chat.mainview.message import ChatMessage
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.sidebar.sidebar import ChatSideBar


class ChatNewChat(flet.AlertDialog):

    def __init__(self, 
                 account:ChatAccount,
                 close_result:Callable, 
                 chatAppControls:ChatAppControlsInterface) -> None:

        self.account = account
        self.close_result = close_result
        self.chatAppControls = chatAppControls

        user_dir = cast(str, self.account.user_dir)
        self.chat_files = get_chat_files(user_dir)   

        ## controls

        self.chat_name_textfield = flet.TextField(
            hint_text="Enter chat name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            on_submit=self.new_chat_click,
            shift_enter=True
            )

        model_list = ollama_get_models()
        model_options = []

        for model in model_list:
            model_options.append(flet.dropdown.Option(model))

        self.select_model_options = flet.Dropdown(
            hint_text="Choose the ai model",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color,weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore           
            options=model_options,
            on_change =self.model_options_changed,
            color = ChatTheme.dialog_color,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_width= ChatTheme.border_width,            
            border_radius=8
        )


        if self.chatAppControls.empty():
            
            # dialog exits only if new chat is created

            actions = [
                flet.ElevatedButton(text="New chat", on_click=self.new_chat_click),
            ]
        else:
            actions = [
                flet.ElevatedButton(text="New chat", on_click=self.new_chat_click),
                flet.ElevatedButton(text="Cancel", on_click=self.cancel_click)
            ]

        # init
                    
        super().__init__(      
            modal=True,
            open=True,
            title=flet.Text("Create a new chat!",color = ChatTheme.dialog_color),
            content=flet.Column([
                self.chat_name_textfield, 
                self.select_model_options], 
                tight=True,
            ),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )        
        

    # New chat submit event

    def new_chat_click(self, e):

        from ollama_chat.appcontrols import ChatAppControls

        chatAppControls = cast(ChatAppControls, self.chatAppControls)

        # Check text entries

        new_chat_success = True
        if not self.chat_name_textfield.value:
            self.chat_name_textfield.error_text = "Chat name can't be empty!"
            self.chat_name_textfield.update()
            new_chat_success= False

        if self.select_model_options.value is None:
            self.select_model_options.error_text = "Please choose an ai model!"
            self.select_model_options.update()
            new_chat_success= False

        if new_chat_success:

            chat_name = cast(str, self.chat_name_textfield.value)
            model = cast(str, self.select_model_options.value)

            if chatAppControls.empty():
                
                # Create default controls

                self.result_msg = chatAppControls.create_controls_default(self.account, e.page, chat_name, model)
                
            else:

                chatAI = cast(ChatAI, chatAppControls.chatAI)

                if chat_name != chatAI.name: 

                    # Does not save if current chat is removed

                    current_chat_name = cast(str, chatAI.name)
                    
                    if str_codify(current_chat_name) in self.chat_files:

                        save_chat(self.account, chatAI)

                # Update to default controls

                self.result_msg = self.chatAppControls.update_controls_default(self.account, e.page, chat_name, model)
                

            # Save to default new chat

            chatAI = cast(ChatAI, chatAppControls.chatAI)
            save_chat(self.account, chatAI)

            chatSideBar = cast(ChatSideBar, chatAppControls.chatSideBar)
            chatSideBar.update_listview(e)

            self.close_result(e, self.result_msg)

    def cancel_click(self,e):
        self.result_msg = ChatResultMessage("New chat cancelled.", False)
        self.close_result(e, self.result_msg)

    def model_options_changed(self,e):
        pass