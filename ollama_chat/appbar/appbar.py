from typing import Callable, Union, cast
import flet
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme

from ollama_chat.account import ChatAccount

from ollama_chat.ai.filetypemap import FILE_TYPE_MAP
from ollama_chat.ai.attachedfiles import ChatAttachedFiles
from ollama_chat.ai import ChatAI, ollama_get_models
from ollama_chat.ai.log import ChatLog

from ollama_chat.mainview.message import ChatMessage
from ollama_chat.mainview import ChatMainView

from ollama_chat.appbar.menuitem import ChatMenuItem
from ollama_chat.appbar.submenu import ChatSubMenu
from ollama_chat.appbar.buttoncol import ChatButtonMenuCollapse
from ollama_chat.appbar.barmenu import ChatBarMenu
from ollama_chat.appbar.panelmenu import ChatPanelMenu

from ollama_chat.dialogs.pullmodel import ChatPullModel
from ollama_chat.dialogs.deletemodel import ChatDeleteModel
from ollama_chat.dialogs.selectmodel import ChatSelectModel
from ollama_chat.dialogs.savechat import ChatSaveChat
from ollama_chat.dialogs.deletechat import ChatDeleteChat
from ollama_chat.dialogs.newchat import ChatNewChat


class ChatAppBar(flet.Container):

    def __init__(self, page:flet.Page, account:ChatAccount, chatMainView: ChatMainView, chatAI: ChatAI) -> None:   

        self.page = page
        self.account = account
        self.chatAI = chatAI
        self.chatMainView = chatMainView
        self.chatSideBar = None
        self.page.on_resized = self.on_resized       
        
        # Dialogs

        self.attach_files_dialog = flet.FilePicker(on_result=self.attach_files_result)
        self.new_chat_dialog = None
        self.load_chat_dialog = None
        self.save_chat_dialog = None
        self.delete_chat_dialog = None
        self.pull_model_dialog = None
        self.delete_model_dialog = None
        self.select_model_dialog = None

        # Menu items (labels)

        submenu_list = [
            ChatSubMenu(    
                name="Chat",
                item_list=[
                    ChatMenuItem(name="New", icon=flet.icons.ACCOUNT_CIRCLE, on_click=self.new_chat_click),
                    ChatMenuItem(name="Load", icon=flet.icons.FOLDER_OPEN, on_click=self.load_chat_click),
                    ChatMenuItem(name="Save", icon=flet.icons.SAVE, on_click=self.save_chat_click),
                    ChatMenuItem(name="Delete", icon=flet.icons.DELETE, on_click=self.delete_chat_click),

                ],
                icon=flet.Icon(flet.icons.ACCOUNT_CIRCLE, color=ChatTheme.appbar_border_color)
            ),
            ChatSubMenu(    
                name="Model",
                item_list=[
                    ChatMenuItem(name="Select", icon=flet.icons.SEARCH, on_click=self.select_model_click),
                    ChatMenuItem(name="Pull", icon=flet.icons.ANDROID, on_click=self.pull_model_click),
                    ChatMenuItem(name="Delete", icon=flet.icons.DELETE, on_click=self.delete_model_click),
                ],
                icon=flet.Icon(flet.icons.ANDROID,color=ChatTheme.appbar_border_color,)
            ),
            self.build_attach_files_menu()
        ]

        # Panels and menubars
        
        self.panel = ChatPanelMenu(submenu_list)
        self.menubar = ChatBarMenu(submenu_list)

        # Panel menu
        
        self.button_menu_collapse = ChatButtonMenuCollapse( self.panel, self.menubar)

        self.check_collapsible()

        ## Current model

        model_list = ollama_get_models()
        model_options = []

        for model in model_list:
            model_options.append(flet.dropdown.Option(model))

        self.select_model_options = flet.Dropdown(
            height=50,
            width=200,
            alignment=flet.alignment.center_left,
            options=model_options,
            on_change=self.select_model_options_changed,
            value = self.chatAI.model,
            border_radius=8,
            border_width=ChatTheme.border_width,
            border_color= ChatTheme.appbar_dropdown_color,
            bgcolor=ChatTheme.appbar_dropdown_bgcolor,            
            text_style=flet.TextStyle(
                weight="bold", #type: ignore
                size=ChatTheme.appbar_dropdown_text_size,
                color=ChatTheme.appbar_dropdown_text_color),
        )

        # Chat side bar

        window_width = cast(int, self.page.width)

        if window_width < 576:
            sidebar_icon = flet.icons.ARROW_BACK_IOS
        else:
            sidebar_icon = flet.icons.ARROW_FORWARD_IOS

        self.sidebar_button = flet.IconButton(
            icon=sidebar_icon,
            icon_size=ChatTheme.icon_small_size,
            icon_color=ChatTheme.icon_color,
            on_click=self.chat_selection_click)        

        ## Init

        super().__init__(
            bgcolor=ChatTheme.appbar_bgcolor,
            content= flet.Column([
                flet.Row([
                            self.button_menu_collapse,                
                            self.menubar,
                            self.select_model_options,
                            flet.Container(expand=True),
                            self.sidebar_button                            
                ]),
                self.panel,
            ]),padding=6)

        
        
    ## Methods
        
    def did_mount(self)->None:
        
        page = cast(flet.Page, self.page)

        page.overlay.append(self.attach_files_dialog)        
        page.update()


    # On change model
        
    def select_model_options_changed(self,e)->None:

        if self.select_model_options.value is not None:

            log = self.chatAI.change_model(self.select_model_options.value)
            
            message = ChatMessage(text=log.last(), type=ChatMessage.LOG)                    
            self.chatMainView.chatMessageView.chat(message)
        
    # On new chat click

    def new_chat_click(self,e)->None:
        
        from ollama_chat.appcontrols import ChatAppControls

        self.new_chat_dialog = ChatNewChat(self.account, 
                        self.new_chat_result, 
                        ChatAppControls(self.account,
                                       self.chatAI, 
                                       self.chatMainView, 
                                       self, 
                                       self.chatSideBar))
        
        e.page.open(self.new_chat_dialog)

        
        
    def new_chat_result(self, e, result_msg:ChatResultMessage)->None:

        e.page.close(self.new_chat_dialog)
        self.new_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)                


    # On load file click
        
    def load_chat_click(self,e)->None:

        from ollama_chat.sidebar import ChatSideBar
        from ollama_chat.dialogs.loadchat import ChatLoadChat

        chatSideBar = cast(ChatSideBar, self.chatSideBar)
        
        self.load_chat_dialog = ChatLoadChat(self.account, 
                         self.chatAI, 
                         self.chatMainView, 
                         self, 
                         chatSideBar, 
                         self.load_chat_result)              

        e.page.open(self.load_chat_dialog)


    def load_chat_result(self, e, result_msg:ChatResultMessage)->None:
        
        e.page.close(self.load_chat_dialog)
        self.load_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)           
        self.chatMainView.chatMessageView.chat(message)
        
    # On save file click     
                  
    def save_chat_click(self,e)->None:
        self.save_chat_dialog = ChatSaveChat(self.account, self.chatAI, self.save_chat_result)
        e.page.open(self.save_chat_dialog)               

    def save_chat_result(self, e, chat_name, result_msg:ChatResultMessage)->None:

        from ollama_chat.sidebar import ChatSideBar

        if chat_name is not None:

            chatSideBar = cast(ChatSideBar, self.chatSideBar)

            self.chatAI.name = chat_name
            chatSideBar.update_listview(e)

        e.page.close(self.save_chat_dialog)
        self.save_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)

    # On delete chat
        
    def delete_chat_click(self,e):        
        self.delete_chat_dialog = ChatDeleteChat(self.account, self.chatAI, self.delete_chat_result)
        e.page.open(self.delete_chat_dialog)               

    def delete_chat_result(self, e, result_msg:ChatResultMessage)->None:

        from ollama_chat.sidebar import ChatSideBar

        if result_msg.success:

            chatSideBar = cast(ChatSideBar, self.chatSideBar)
            chatSideBar.update_listview(e)
                   
        e.page.close(self.delete_chat_dialog)
        self.delete_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)                

    # On pull model
        
    def pull_model_click(self, e)->None:
        self.pull_model_dialog = ChatPullModel(False, self.pull_model_result)
        e.page.open(self.pull_model_dialog)               

    def pull_model_result(self, e, model_list, result_msg:ChatResultMessage)->None:

        e.page.close(self.pull_model_dialog)
        self.pull_model_dialog = None

        model_options = []

        for model in model_list:
            model_options.append(flet.dropdown.Option(model))

        self.select_model_options.options = model_options

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)

    # Menu check collapsible

    def check_collapsible(self)->None:
        
        page = cast(flet.Page, self.page)
        window_width = cast(int, page.width)

        if window_width >= 576:
            self.button_menu_collapse.menubar.visible = True            
            self.button_menu_collapse.content.visible = False # type: ignore
            self.button_menu_collapse.panel.visible = False
           
        else:
            self.button_menu_collapse.content.visible = True # type: ignore
            self.button_menu_collapse.panel.visible = False
            self.button_menu_collapse.menubar.visible = False            

    def on_resized(self,e)->None:
        self.check_collapsible()
        self.update()

    # On delete model
        
    def delete_model_click(self,e):

        self.delete_model_dialog = ChatDeleteModel(self.delete_result)
        e.page.open(self.delete_model_dialog)

    def delete_result(self, e, result_msg:ChatResultMessage)->None:

        if not result_msg.success:
            
            e.page.close(self.delete_model_dialog)
            self.delete_model_dialog = None

        else:
            model_list = ollama_get_models()

            if not model_list:
                self.select_model_options.value = None

            elif self.chatAI.model not in model_list:
                self.chatAI.model = model_list[0]
                self.select_model_options.value = self.chatAI.model

            e.page.close(self.delete_model_dialog)
            self.delete_model_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message) 
                    
    # On files atached
   
    def get_attach_files_click_function(self, name:str, extensions:list)->Callable:
        def attach_files_click(e):
            self.attach_files_dialog.pick_files("Attach " + name + " ...", 
                                            allow_multiple=True,
                                            allowed_extensions=extensions)
        return attach_files_click

    def build_attach_files_menu(self)->ChatSubMenu:
        
        item_list = []
        for type_name, file_type in FILE_TYPE_MAP.items():
            item_list.append(
                ChatMenuItem(
                    name="Attach " + type_name, 
                    icon=flet.icons.FOLDER_OPEN,                     
                    on_click=self.get_attach_files_click_function(type_name, file_type["extensions"])
                    )
            )
        return ChatSubMenu(    
            name="File",
            item_list=item_list,
            icon=flet.Icon(flet.icons.FOLDER_OPEN,color=ChatTheme.appbar_border_color)

        )

    def attach_files_result(self, e: flet.FilePickerResultEvent)->None:

        if e.files:

            path = f"{self.account.user_dir}/{self.chatAI.name}/attached"
            attached_files = ChatAttachedFiles(path, self.attach_files_dialog)                        
            log =  self.chatAI.attach_files(attached_files)

            message = ChatMessage(text=log.last(), type=ChatMessage.LOG)    
            self.chatMainView.chatMessageView.chat(message)        
        else:
            message = ChatMessage(text="No files attached.", type=ChatMessage.LOG)     
            self.chatMainView.chatMessageView.chat(message)        
     
     # On model selection
                   
    def select_model_click(self,e)->None:
               
        self.select_model_dialog = ChatSelectModel(self.chatAI, self.select_model_result)
        e.page.open(self.select_model_dialog)
        
    def select_model_result(self, e, result_msg:ChatResultMessage)->None:
        
        e.page.close(self.select_model_dialog)
        self.select_model_dialog = None
        
        if result_msg.success:
            self.update_controls(self.chatAI)

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)


    # update controls on change AI model

    def update_controls(self, chatAI:ChatAI) -> None:
        self.select_model_options.value = chatAI.model
        self.chatAI = chatAI
        

    # update side bar

    def chat_selection_click(self, e)->None:

        from ollama_chat.sidebar import ChatSideBar

        chatSideBar = cast(ChatSideBar, self.chatSideBar)
        chatSideBar.collapse_click(e)