
from typing import List

import flet 
from ollama_chat.appbar.submenu import ChatSubMenu


class ChatPanelMenu(flet.ExpansionPanelList):
    
    def __init__(self, submenu_list:List[ChatSubMenu]):

        panel_controls = []

        for submenu in submenu_list:

            menu_controls = []
            for item in submenu.item_list:
            
                menu_controls.append(
                    flet.Row([
                        flet.Container(                                
                            content=item.content, 
                            on_click=item.on_click,
                            margin=10
                        )                        
                    ])
                )

            panel_controls.append(
                flet.ExpansionPanel(
                    header=flet.Container(content=submenu.content,margin=5),
                    content=flet.Column(menu_controls)
                )
            )

        super().__init__(panel_controls)

