from typing import List

import flet
import ollama_chat.other.theme as ChatTheme
from ollama_chat.appbar.menuitem import ChatMenuItem

class ChatSubMenu:

    STYLE = dict(color=ChatTheme.menu_text_color, weight="bold", size=ChatTheme.menu_text_size)

    def __init__(self, name:str, item_list:List[ChatMenuItem],icon:flet.Icon):
        self.name = name
        self.content = flet.Row([icon, flet.Text(name,**ChatSubMenu.STYLE)]) # type: ignore
        self.item_list = item_list
