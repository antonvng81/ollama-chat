
from typing import List

import flet 
from ollama_chat.appbar.submenu import ChatSubMenu
import ollama_chat.other.theme as ChatTheme

class ChatBarMenu(flet.MenuBar):
    
    def __init__(self, submenu_list:List[ChatSubMenu]):

        bar_controls = []

        for submenu in submenu_list:

            menu_controls = []
            for item in submenu.item_list:
            
                menu_controls.append(
                    flet.MenuItemButton(
                        content=item.content, 
                        on_click=item.on_click
                        )
                    )

            bar_controls.append(
                flet.SubmenuButton(                    
                    content=submenu.content,
                    controls=menu_controls
                )
            )

        super().__init__(
            expand=False,
            controls = bar_controls, 
            style=flet.MenuStyle(
                elevation=0,
                bgcolor=ChatTheme.menu_bgcolor,
                alignment=flet.alignment.top_left))
