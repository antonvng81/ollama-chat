import flet 
from typing import Callable
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai.savechat import save_chat
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.ai import ChatAI

class ChatSaveChat(flet.AlertDialog):

    def __init__(self, account:ChatAccount, chatAI:ChatAI, close_result:Callable) -> None:

        self.close_result = close_result   
        self.chatAI = chatAI
        self.account = account

        self.result_msg = ChatResultMessage(f"Chat '{chatAI.name}' not saved", False)

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
            value=self.chatAI.name
            )        

        # Selector for chat

        actions = [
            flet.ElevatedButton(text="Save", on_click=self.submit_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Save chat",color = ChatTheme.dialog_color),
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
            self.chat_textfield.error_text = "Please write chat's name to save!"
            e.page.update()
        else:
            self.chatAI.name = chat_name
            save_chat(self.account, self.chatAI)

            self.close_result(e, chat_name, ChatResultMessage(f"Chat '{chat_name}' saved.", True))

    def cancel_click(self,e):
        self.close_result(e, None, ChatResultMessage("Chat save cancelled.", False))



