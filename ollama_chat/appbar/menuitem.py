from typing import Callable
import flet
import ollama_chat.other.theme as ChatTheme

class ChatMenuItem:

    STYLE = dict(color=ChatTheme.menu_text_color, weight="bold", size=ChatTheme.menu_text_size)

    def __init__(self, name:str, icon:str, on_click:Callable)->None:
        
        self.on_click = on_click
        self.name = name
        self.icon = icon
    
        self.content = flet.Row([
            flet.Icon(name=icon,
                      color=ChatTheme.icon_color,
                      size=ChatTheme.icon_small_size), 
            flet.Text(name, **ChatMenuItem.STYLE)]) # type: ignore
