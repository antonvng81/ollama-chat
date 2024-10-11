import os
from typing import Union, cast

import flet

from ollama_chat.account import ChatAccount
from ollama_chat.account.session import ChatAppSession
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai import ChatAI, ollama_get_models
from ollama_chat.appbar import ChatAppBar
from ollama_chat.ai.savechat import save_chat
from ollama_chat.mainview import ChatMainView
from ollama_chat.other.resultmessage import ChatResultMessage
from ollama_chat.sidebar import ChatSideBar
import ollama_chat.other.theme as ChatTheme
from ollama_chat.appcontrols.interface import ChatAppControlsInterface

class ChatAppControls(ChatAppControlsInterface):

    def __init__(self,
                 account:Union[ChatAccount,None]=None,
                 chatAI:Union[ChatAI,None]=None,
                 chatMainView:Union[ChatMainView,None]=None,
                 chatAppBar:Union[ChatAppBar,None]=None,
                 chatSideBar:Union[ChatSideBar,None]=None)->None:

        self.account = account
        self.chatAI = chatAI
        self.chatAppBar = chatAppBar
        self.chatMainView = chatMainView
        self.chatSideBar = chatSideBar


    # Chech build is not executed yet

    def empty(self)->bool:
        return  (self.account is None) or \
                (self.chatAI is None) or \
                (self.chatMainView is None) or \
                (self.chatAppBar is None) or \
                (self.chatSideBar is None)

    # Create default controls

    def create_controls_default(self,
                                account:ChatAccount,                                
                                page:flet.Page,                                
                                chat_name:str,  
                                model:str)->ChatResultMessage:

        # create default chat

        session = [ {
            "role": "system", 
            "content": f"You chat with {account.user_name}.",
            "_index":0}] 
        
        chatAI = ChatAI(chat_name, account.user_name, model, session)

        # build controls

        chatMainView = ChatMainView(page, chatAI)        
        chatAppBar = ChatAppBar(page, account, chatMainView, chatAI)
        chatSideBar = ChatSideBar(page, account, chatAI, chatMainView, chatAppBar)

        # append controls  to page

        page.padding = 0
        
        page.add(chatAppBar)
        page.add(
                flet.Row([chatMainView,
                          flet.VerticalDivider(color=ChatTheme.appbar_dropdown_color),chatSideBar], 
                          expand=True)
        )
        
        page.on_disconnect = self.page_close

        self.account = account
        self.chatAI = chatAI
        self.chatMainView = chatMainView
        self.chatAppBar = chatAppBar
        self.chatSideBar = chatSideBar

        return ChatResultMessage(f"New chat '{chatAI.name}' created", True)


    # Update to default controls

    def update_controls_default(self,
                                account:ChatAccount,      
                                page:flet.Page,                          
                                chat_name:str,  
                                model:str,
                                )->ChatResultMessage:
        
        # clear memory of chatAI
                
        chatAI = cast(ChatAI, self.chatAI)
        chatAI.dettach_files()

        # create default chat

        session = [ {
            "role": "system", 
            "content": f"You chat with {account.user_name}.",
            "_index":0}] 
        
        chatAI = ChatAI(chat_name, account.user_name, model, session)
        self.chatAI = chatAI

        # update controls
        self.account = account
        page.on_disconnect = self.page_close

        chatMainView = cast(ChatMainView, self.chatMainView)
        chatAppBar = cast(ChatAppBar, self.chatAppBar)
        chatSideBar = cast(ChatSideBar, self.chatSideBar)

        chatMainView.update_controls(chatAI)
        chatAppBar.update_controls(chatAI) 
        chatSideBar.update_controls(chatAI)

        page.update()

        return ChatResultMessage(f"New chat '{chatAI.name}' created", True)

    # Update to a loaded ChatAI

    def update_controls_load(self, page: flet.Page, file_name:str)->ChatResultMessage:
        
        chatAI = ChatAI()
        chatAI.load_chat_file(file_name)

        if chatAI.model not in ollama_get_models():
            return ChatResultMessage(f"Model '{chatAI.model}' not found.", False)        

        self.chatAI = chatAI

        page.on_disconnect = self.page_close

        # update to loaded session
        chatMainView = cast(ChatMainView, self.chatMainView)
        chatAppBar = cast(ChatAppBar, self.chatAppBar)
        chatSideBar = cast(ChatSideBar, self.chatSideBar)

        chatMainView.update_controls(self.chatAI)
        chatAppBar.update_controls(self.chatAI) 
        chatSideBar.update_controls(self.chatAI)
        
        # build session messages

        return ChatResultMessage(f"Chat '{self.chatAI.name}' loaded.",True)

        
    # Create to a loaded ChatAI

    def create_controls_load(self, account:ChatAccount, page:flet.Page, last_chat:str)->ChatResultMessage:
        
        # load chat

        chatAI = ChatAI()        
        chatAI.load_chat_file(last_chat)

        # check model

        if chatAI.model not in ollama_get_models():
            return ChatResultMessage(f"Model '{chatAI.model}' not found.", False)        

        # build controls

        chatMainView = ChatMainView(page, chatAI)        
        chatAppBar = ChatAppBar(page, account, chatMainView, chatAI)
        chatSideBar = ChatSideBar(page, account, chatAI, chatMainView, chatAppBar)

        # append controls  to page

        page.padding = 0
        page.add(chatAppBar)
        page.add(
                flet.Row([chatMainView,
                        flet.VerticalDivider(color=ChatTheme.appbar_dropdown_color),
                        chatSideBar], 
                        expand=True)
                )
            
        
        page.on_disconnect = self.page_close

        self.account = account
        self.chatAI = chatAI
        self.chatMainView = chatMainView
        self.chatAppBar = chatAppBar
        self.chatSideBar = chatSideBar

        # update to loaded session
        chatMainView = cast(ChatMainView, self.chatMainView)
        chatAppBar = cast(ChatAppBar, self.chatAppBar)
        chatSideBar = cast(ChatSideBar, self.chatSideBar)

        chatMainView.update_controls(self.chatAI)
        chatAppBar.update_controls(self.chatAI) 
        chatSideBar.update_controls(self.chatAI)
        
        # build session messages
        
        return ChatResultMessage(f"Chat '{self.chatAI.name}' loaded.", True)


    # Disconnect event

    def page_close(self, e)->None:
        
        chatAI = cast(ChatAI, self.chatAI)
        chatAI.dettach_files()

        # Save the chat

        chatSideBar = cast(ChatSideBar, self.chatSideBar)
        file_name = None

        chat_name = cast(str, chatAI.name)

        if str_codify(chat_name) in chatSideBar.chat_files.keys():

            account = cast(ChatAccount, self.account)
            file_name = save_chat(account, chatAI)

        elif chatSideBar.chat_files.values():
            file_name = next(iter(chatSideBar.chat_files.values()))
            
        # Save session (only if session open)

        if ChatAppSession.CHAT_APP_SESSION is not None:
            
            session = cast(ChatAppSession, ChatAppSession.CHAT_APP_SESSION)
            session.last_chat = file_name
            session.save_app_session()

