import flet
from ollama_chat.appbar.barmenu import ChatBarMenu
from ollama_chat.appbar.panelmenu import ChatPanelMenu


class ChatButtonMenuCollapse(flet.Container):
        
    def __init__(self, panel:ChatPanelMenu,menubar:ChatBarMenu)->None:

        self.panel = panel
        self.menubar = menubar

        super().__init__(
            content=flet.Icon(name=flet.icons.MENU), 
            on_click=self.menu_button_on_click,
            )

    def menu_button_on_click(self, e):
        if self.panel.visible == False:
            self.panel.visible = True
        else:
            self.panel.visible = False
        
        e.page.update()