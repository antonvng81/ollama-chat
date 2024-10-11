
from typing import Tuple, Union, cast
import flet

from ollama_chat.mainview.message import ChatMessage
from ollama_chat.mainview.viewitem import ChatMessageViewItem
from ollama_chat.ai import ChatAI

class ChatMessageView(flet.ListView):

    def __init__(self, page:flet.Page , chatAI:ChatAI) -> None:
        super().__init__(expand=True, spacing=10, auto_scroll=True)

        self.chatAI = chatAI
        self.page = page

        self.message_call_list = [
            self.query,
            self.system,
            self.log,
        ]

    # Show a message
    
    def append_message(self, index:int, chatMessage: ChatMessage, update: bool=True):
        self.controls.append(ChatMessageViewItem(self, index, chatMessage))
        if update:
            page = cast(flet.Page, self.page)
            page.update()

    # actions

    def query(self, chatMessage: ChatMessage, update: bool=True):
        
        message, message_answer = self.chatAI.query(chatMessage.text)

        self.append_message(message["_index"], chatMessage, update)
        self.append_message(message_answer["_index"],
                  ChatMessage("assistant",
                              message_answer["content"],
                              ChatMessage.LOAD), update)
        
        self.chatAI.dettach_files()

    def system(self, chatMessage: ChatMessage, update: bool=True):

        message = self.chatAI.system(chatMessage.text)
        self.append_message(message["_index"], chatMessage, update)

        self.chatAI.dettach_files()

    def log(self, chatMessage: ChatMessage, update: bool=True):
        self.controls.append(flet.Text(chatMessage.text,italic=True, size=13, color=flet.colors.GREY))
        if update:
            page = cast(flet.Page, self.page)
            page.update()        

    # (chat with model and) show message in the view

    def chat(self, chatMessage: ChatMessage, update:bool=True):
        self.message_call_list[chatMessage.message_type](chatMessage, update)

    # parse a raw message
        
    def parse_session_message(self, message:dict) -> Tuple[dict,ChatMessage]:
        
        if message["role"] == "system":
            user_name = "system"
        elif message["role"] == "assistant":    
            user_name = "assistant"
        else:
            user_name = cast(str, self.chatAI.user_name)
        
        text = ""

        if "_facade" in message:
            text = message["_facade"]
        else:
            text = message["content"]

        return message["_index"], ChatMessage(user_name=user_name, text=text, type=ChatMessage.LOAD) 
        
    # parse a log message injected in session

    def parse_log_message(self, message:dict) ->Union[ChatMessage,None]:

        if "_log" in message:

            log = message["_log"]

            if log != "":
                user_name = cast(str, self.chatAI.user_name)
                return ChatMessage(
                        user_name=user_name,
                        text=log,
                        type=ChatMessage.LOG)

        return  None

    #               | -> ChatMessageViewItem -> ChatMessageView
    # ChatMessage --|
    #               | -> ChatAI 

    def update_controls(self, chatAI:Union[ChatAI,None]=None):

        if chatAI is not None:
            self.chatAI = chatAI
        # else use the previous chatAI setted at constructor

        

        self.controls=[]
        
        page = cast(flet.Page, self.page)
        page.update()       

        user_name = cast(str, self.chatAI.user_name)
        self.chat(
            ChatMessage(
                user_name=user_name, 
                text=f"'{self.chatAI.user_name}' has joined the chat '{self.chatAI.name}'", 
                type=ChatMessage.LOG))
        
        for message in self.chatAI.session:

            # Log session changes
            if (chatMessage := self.parse_log_message(message)) is not None:
                self.chat(chatMessage, update=False)

            # Show the message
            index, chatMessage = self.parse_session_message(message)

            index = cast(int, index)
            self.append_message(index, chatMessage, update=False)
             
    # remove a message from ai and view
            
    def remove_message(self, index:int):

        self.chatAI.remove_message(index)

        for control in self.controls:
            if type(control) is ChatMessageViewItem:
                if control.index == index:
                    self.controls.remove(control)
                    break

        page = cast(flet.Page, self.page)
        page.update()