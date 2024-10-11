import flet

import ollama_chat.other.theme as ChatTheme
from ollama_chat.mainview.message import ChatMessage

class ChatMessageViewItem(flet.Container):

    def __init__(self, chatMessageView, index:int, chatMessage: ChatMessage)->None:
               

        self.index = index
        self.chatMessageView = chatMessageView

        self.chatMessage = chatMessage
        self.delete_button = flet.IconButton(
            icon=flet.icons.CLOSE,
            icon_size=ChatTheme.icon_small_size,
            on_click=self.on_remove_click)              
        self.delete_button.visible = False
        

        if self.chatMessage.user_name == "assistant":

            super().__init__(
                content = self.build_controls("assistant", 
                                               flet.icons.ANDROID, 
                                               chatMessage.text),
                on_hover=self.hover
            )
        
        elif self.chatMessage.user_name == "system":

            super().__init__(
                content = self.build_controls("system", 
                                               flet.icons.MANAGE_ACCOUNTS, 
                                               chatMessage.text),
                on_hover=self.hover                                               
            )
        else:
            super().__init__(
                content = self.build_controls(chatMessage.user_name, 
                                               flet.icons.ACCOUNT_CIRCLE, 
                                               chatMessage.text),
                on_hover=self.hover                                               
            )
        
    
    def build_controls(self, user_name:str, icon:str, text:str):

        return flet.Row([
            flet.Column([
                flet.Row([
                    flet.Icon(name=icon, size=ChatTheme.icon_small_size, color=ChatTheme.icon_color),
                    flet.Text(user_name + ":", 
                        selectable=False, 
                        color=ChatTheme.message_color,            
                        weight=flet.FontWeight.BOLD,
                        size=13),
                    flet.Container(expand=True),
                    self.delete_button,
                    ],height=ChatTheme.icon_small_size+5),                
                flet.Container(
                        flet.Markdown(text, 
                                      selectable=True,
                                      extension_set=flet.MarkdownExtensionSet.COMMON_MARK,
                                      on_tap_link=lambda e: self.chatMessageView.page.launch_url(e.data),
                                      ),
                        bgcolor=ChatTheme.message_bgcolor, 
                        border_radius=20,
                        padding=5,
                        margin=flet.margin.only(left=5,top=3,bottom=5),
                        ),
            ],
            tight=True,
            spacing=5,
            expand=True,
        ),],
        vertical_alignment="start", # type: ignore
        )

    
    def on_remove_click(self, e):
        self.chatMessageView.remove_message(self.index)

    def hover(self, e):

        if e.data=="true":
            self.delete_button.visible = True
        else:
            self.delete_button.visible = False

        e.page.update()
