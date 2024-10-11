from typing import Callable
import flet
import ollama_chat.other.theme as ChatTheme

class ChatSideBarItem(flet.Container):

    def __init__(self, chat_name:str,
                 load_chat:Callable, 
                 delete_chat:Callable,
                 rename_chat:Callable):
        
        self.chat_name = chat_name
        self.load_chat = load_chat
        self.delete_chat = delete_chat
        self.rename_chat = rename_chat

        self.text_control = flet.Container(
            flet.Text(
                chat_name, 
                color=ChatTheme.sidebar_item_color,
                size=ChatTheme.sidebar_item_size,            
                weight=flet.FontWeight.BOLD,
                expand=True,                            
                ),
            expand=True,
            on_click=self.text_click,
        )


        self.delete_button = flet.IconButton(
            icon=flet.icons.CLOSE,
            icon_size=ChatTheme.icon_small_size,
            on_click=self.delete_click)  
        
        self.rename_button = flet.IconButton(
            icon=flet.icons.DRIVE_FILE_RENAME_OUTLINE,
            icon_size=ChatTheme.icon_small_size,
            on_click=self.rename_click)          
                    
        self.delete_button.visible = False
        self.rename_button.visible = False

        row = flet.Row([self.text_control, self.rename_button, self.delete_button])

        super().__init__(content = row, height=40, on_hover=self.hover)


    def text_click(self, e):
        self.load_chat(e, self)

    def delete_click(self, e):
        self.delete_chat(e, self.chat_name)

    def rename_click(self, e):
        self.rename_chat(e, self.chat_name)        

    def hover(self, e):

        if e.data=="true":
            self.delete_button.visible = True
            self.rename_button.visible = True

        else:
            self.delete_button.visible = False
            self.rename_button.visible = False

        e.page.update()