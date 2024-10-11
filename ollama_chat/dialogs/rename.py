import flet 
from typing import Callable
from ollama_chat.account import ChatAccount
from ollama_chat.ai import ChatAI
from ollama_chat.ai.renamechat import rename_chat
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme

class ChatRenameChat(flet.AlertDialog):

    def __init__(self, account:ChatAccount, chatAI:ChatAI, chat_files:dict, old_chat_name:str, rename_result:Callable) -> None:

        self.rename_result = rename_result   
        self.old_chat_name = old_chat_name
        self.account = account
        self.chat_files = chat_files
        self.chatAI = chatAI

        self.result_msg = ChatResultMessage(f"Chat '{old_chat_name}' not renamed.", False)

        # controls

        self.chat_textfield = flet.TextField(
            hint_text="Enter new chat name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,  
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            value=self.old_chat_name
            )        

        # Selector for chat

        actions = [
            flet.ElevatedButton(text="Rename", on_click=self.submit_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Rename chat",color = ChatTheme.dialog_color),
            content=flet.Column([ self.chat_textfield], 
                tight=True,
            ),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )                        

    # Submit event

    def submit_click(self,e):

        self.chat_textfield.error_text = ""
        new_chat_name = self.chat_textfield.value

        if not new_chat_name:
            self.chat_textfield.error_text = "Please write chat's new name!"
            e.page.update()

        else:
            if self.old_chat_name != new_chat_name: 
                if rename_chat(self.account, self.chat_files, self.old_chat_name, new_chat_name):
                    
                    if self.old_chat_name == self.chatAI.name:
                        self.chatAI.name = new_chat_name

                    self.result_msg = ChatResultMessage(f"Chat renamed to '{new_chat_name}'.", True)

                    self.rename_result(e, self.result_msg)
                else:    
                    self.chat_textfield.error_text = "Chat name already exists!"
                    e.page.update()

            else:
                self.chat_textfield.error_text = "Chat names are equal!"
                e.page.update()


    def cancel_click(self,e):

        self.result_msg = ChatResultMessage("Chat rename cancelled.", False)
        self.rename_result(e, self.result_msg)




