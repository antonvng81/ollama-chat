import flet 
from typing import Callable
from ollama_chat.account import ChatAccount
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.ai import ChatAI
from ollama_chat.ai.deletechat import delete_chat

class ChatDeleteChat(flet.AlertDialog):

    def __init__(self, account:ChatAccount, chatAI:ChatAI, close_result:Callable) -> None:

        self.close_result = close_result   
        self.chatAI = chatAI
        self.account = account

        # controls

        self.chat_textfield = flet.TextField(
            hint_text="Enter chat name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), #type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), #type: ignore
            autofocus=True,  
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            value=""
            )        

        # Selector for chat

        actions = [
            flet.ElevatedButton(text="Delete", on_click=self.submit_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Delete chat",color = ChatTheme.dialog_color),
            content=flet.Column([ self.chat_textfield], 
                tight=True,
            ),
            actions=actions, #type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )                        

    # Submit event
        
    def submit_click(self,e):

        self.chat_textfield.error_text = ""
        chat_name = self.chat_textfield.value

        if not chat_name:
            self.chat_textfield.error_text = "Please write chat's name to delete!"
            e.page.update()
        else:
            delete_chat(self.account, chat_name)
            self.close_result(e, ChatResultMessage(f"Chat '{chat_name}' deleted.", True))

    def cancel_click(self,e):
        self.close_result(e, ChatResultMessage("Chat delete cancelled.", False))




