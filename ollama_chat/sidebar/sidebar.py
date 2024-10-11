from typing import cast
import flet
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_decodify, str_codify
from ollama_chat.ai.savechat import save_chat
from ollama_chat.ai.deletechat import delete_chat
from ollama_chat.ai.getchatfiles import get_chat_files
from ollama_chat.ai import ChatAI
from ollama_chat.dialogs.rename import ChatRenameChat
from ollama_chat.mainview.message import ChatMessage
from ollama_chat.other.resultmessage import ChatResultMessage
from ollama_chat.sidebar.sidebaritem import ChatSideBarItem
from ollama_chat.mainview import ChatMainView
import ollama_chat.other.theme as ChatTheme


class ChatSideBar(flet.Container):

    def __init__(self, 
                 page:flet.Page, 
                 account:ChatAccount, 
                 chatAI:ChatAI, 
                 chatMainView:ChatMainView, 
                 chatAppBar:'ChatAppBar')->None:# type: ignore

        user_dir = cast(str, account.user_dir)

        self.account = account
        self.chatAI = chatAI
        self.chat_files = get_chat_files(user_dir)
        self.chatMainView = chatMainView
        self.chatAppBar = chatAppBar
        self.chatAppBar.chatSideBar = self 
        self.page = page

        self.new_chat_dialog = None
        self.rename_chat_dialog = None

        # Collapsed sidebar state

        window_width = cast(int, self.page.width)
        
        if window_width < 576:
           self.state = False
        else:
           self.state = True

        # Header controls

        self.title_label = flet.Text(
                            "CHATS", 
                            selectable = False, 
                            color = ChatTheme.sidebar_title_color,
                            size = ChatTheme.sidebar_title_size,
                            weight = flet.FontWeight.BOLD,
                            text_align = flet.TextAlign.CENTER,
                            width = 256)
        
        self.new_chat_button = flet.IconButton(
            icon=flet.icons.ADD,
            icon_size=ChatTheme.icon_small_size,
            on_click=self.new_chat_click)   
        
        self.chat_textfield = flet.TextField(
            hint_text="Enter chat name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=ChatTheme.sidebar_item_size), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=ChatTheme.sidebar_item_size), # type: ignore
            autofocus=True, 
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.appbar_dropdown_color,
            focused_border_color=ChatTheme.appbar_dropdown_color,
            border_radius=8,
            value="",
            on_change=self.change_search
            ) 

        self.header = flet.Column([
            flet.Row([self.new_chat_button, self.title_label]),
            self.chat_textfield])

        # List view of chats

        self.list_view = flet.ListView(self.create_listview_controls(), width=300, spacing=5)


        super().__init__(content=flet.Column([
            self.header,self.list_view]),visible=self.state)

    # Generate the main view
        
    def load_chat(self, e, chatSideBarItem:ChatSideBarItem):
               
        from ollama_chat.appcontrols import ChatAppControls

        chat_dir_name = str_codify(chatSideBarItem.chat_name)

        # Save current chat
        
        if chatSideBarItem.chat_name != self.chatAI.name:

            chat_name = cast(str, self.chatAI.name)

            # Does not save if current chat is removed

            if str_codify(chat_name) in self.chat_files:
                
                save_chat(self.account, self.chatAI)

        # Load selected chat

        chatAppControls = ChatAppControls(self.account, self.chatAI, self.chatMainView, self.chatAppBar, self)                    
        result_msg = chatAppControls.update_controls_load(e.page, self.chat_files[chat_dir_name])

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message) 

    # Delete a chat

    def delete_chat(self, e, chat_name:str):
                    
        if delete_chat(self.account, chat_name):
            
            self.update_listview(e)
            
            message = ChatMessage(text=f"Chat '{chat_name}' deleted.", type=ChatMessage.LOG)                        
            self.chatMainView.chatMessageView.chat(message) 
        else:
            message = ChatMessage(text=f"Chat not deleted.", type=ChatMessage.LOG)                        
            self.chatMainView.chatMessageView.chat(message) 

    # Rename a chat

    def rename_chat(self, e, old_chat_name:str):
        
        # check self.chatAI is the same
        
        self.rename_chat_dialog = ChatRenameChat(self.account, 
                                                 self.chatAI, 
                                                 self.chat_files, 
                                                 old_chat_name, 
                                                 self.rename_result)
        e.page.open(self.rename_chat_dialog)


    def rename_result(self, e, result_msg:ChatResultMessage):
        
        e.page.close(self.rename_chat_dialog)
        self.rename_chat_dialog = None

        if result_msg.success:
            self.update_listview(e)

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message) 

    # Update event

    def update_controls(self, chatAI:ChatAI):
        self.chatAI = chatAI

    # Update listview event

    def update_listview(self, e):
        
        user_dir = cast(str, self.account.user_dir)

        self.chat_files = get_chat_files(user_dir)

        self.content=flet.Column([
            self.header,
            flet.ListView(self.create_listview_controls(), width=300, spacing=5)])
        
        e.page.update()

    def create_listview_controls(self):        

        item_list = []

        for (chat_dir_name, file_name) in self.chat_files.items():
            
            empty = False
            matching = False

            name = str_decodify(chat_dir_name)   
            search_name = cast(str, self.chat_textfield.value)

            if self.chat_textfield.value == "":
                empty = True
            
            if name[0:len(search_name)] == search_name:
                matching = True

            if empty or matching:    
                item_list.append(
                    ChatSideBarItem(
                        name, 
                        self.load_chat,
                        self.delete_chat,
                        self.rename_chat))
                
        return item_list

    # Update chat search control event

    def change_search(self, e):

        self.content=flet.Column([
            self.header,
            flet.ListView(self.create_listview_controls(), width=300, spacing=5)])
        
        e.page.update()

        self.chat_textfield.focus()

    # Setting collapse button state

    def collapse_click(self, e):
        if self.state is True:
            self.visible=False
            self.state = False
            self.chatAppBar.sidebar_button.icon=flet.icons.ARROW_BACK_IOS
            self.chatMainView.visible = True
        else:
            self.visible=True
            self.state = True
            self.chatAppBar.sidebar_button.icon=flet.icons.ARROW_FORWARD_IOS
            if e.page.width < 576:
                self.chatMainView.visible = False        

        e.page.update()

    # Create new chat from sidebar
    
    def new_chat_click(self, e):
                
        from ollama_chat.appcontrols import ChatAppControls
        from ollama_chat.dialogs.newchat import ChatNewChat

        
        self.new_chat_dialog = ChatNewChat(self.account, 
                        self.new_chat_result, 
                        ChatAppControls(self.account,
                                       self.chatAI, 
                                       self.chatMainView, 
                                       self.chatAppBar, 
                                       self))
        e.page.open(self.new_chat_dialog)

    def new_chat_result(self, e, result_msg:ChatResultMessage):
        e.page.close(self.new_chat_dialog)
        self.new_chat_dialog = None

        message = ChatMessage(text=result_msg.message, type=ChatMessage.LOG)                        
        self.chatMainView.chatMessageView.chat(message)                
