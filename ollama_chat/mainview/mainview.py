from typing import cast
import flet
from ollama import ResponseError


import ollama_chat.other.theme as ChatTheme
from ollama_chat.ai import ChatAI
from ollama_chat.mainview.message import ChatMessage
from ollama_chat.mainview.view import ChatMessageView

# Main view of the chat application

class ChatMainView(flet.Container):

    def __init__(self, page:flet.Page, chatAI: ChatAI) -> None:       

        self.page = page
        self.chatAI = chatAI
        
        # bottom controls

        self.user_textfield = flet.TextField(
            hint_text="Write a message...",
            autofocus=True,
            min_lines=1,
            filled=True,
            bgcolor=ChatTheme.text_entry_bgcolor,
            color=ChatTheme.text_entry_color,
            border_width=0,
            border_radius=8,
            shift_enter=False,
            multiline=True,
            expand=True,) # expanded

        self.user_mode = flet.RadioGroup(
            content=flet.Column([
                flet.Radio(value="user", label="user",),
                flet.Radio(value="system", label="system") 
            ]),
            value="user",
            on_change=self.on_change_role
        )

        self.user_mode_menu = flet.PopupMenuButton(       
            items=[
                flet.PopupMenuItem(
                    content=self.user_mode
                )
            ],
            content =flet.Icon(
                name = flet.icons.ACCOUNT_CIRCLE, 
                color=ChatTheme.icon_color, 
                size=ChatTheme.icon_size,
            ),
            tooltip="Choose role",
        )

        self.bottom_controls = flet.Row([
                    self.user_mode_menu,
                    self.user_textfield, # expanded
                    flet.IconButton(
                        icon=flet.icons.SEND,
                        tooltip="Send message",
                        on_click=self.send_click,
                        icon_color=ChatTheme.icon_color,
                        icon_size=ChatTheme.icon_size)])


        # midle messages

        self.chatMessageView = ChatMessageView(self.page,self.chatAI) # expanded
        self.chatMessageView.update_controls()

        self.midle_message_list = flet.Container(
                    content=self.chatMessageView,
                    border=flet.border.all(0, flet.colors.BACKGROUND),
                    padding=flet.Padding(left=13, right=13, top=0, bottom=0),
                    expand=True)
        
        # wrapping all

        content = flet.Column([self.midle_message_list, # expanded in a column
                               self.bottom_controls], 
                               expand = True)


        # init

        super().__init__(content, 
                         expand = True, # expand in controls
                         padding=flet.Padding(left=10, right=10, top=0, bottom=10))


    # methods
        
    # On send text to ollama

    def send_click(self, e):

        if self.user_textfield.value == "":
            return

        try:
            user_name = cast(str, self.chatAI.user_name)
            text = cast(str, self.user_textfield.value)

            if self.user_mode.value == "user":
                self.chatMessageView.chat(
                    ChatMessage(
                        user_name=user_name,
                        text=text, 
                        type=ChatMessage.QUERY))
                
            elif self.user_mode.value == "system":
                self.chatMessageView.chat(
                    ChatMessage(
                        user_name="system",
                        text=text, 
                        type=ChatMessage.SYSTEM))
                
        except ResponseError as err:
            
            self.chatMessageView.chat(ChatMessage(text=err.error, type=ChatMessage.LOG))


        self.user_textfield.value = ""
        e.page.update()

    # Update role
        
    def update_role(self):
        
        if self.user_mode.value == "system": 
            self.user_mode_menu.content = flet.Icon(
                    name = flet.icons.MANAGE_ACCOUNTS, 
                    color=ChatTheme.icon_color, 
                    size=ChatTheme.icon_size
                )
            
        elif self.user_mode.value == "user":     
            self.user_mode_menu.content = flet.Icon(
                    name = flet.icons.ACCOUNT_CIRCLE, 
                    color=ChatTheme.icon_color, 
                    size=ChatTheme.icon_size
                )

    # On change role

    def on_change_role(self, e):

        self.update_role()

        e.page.update()
        
    # update controls at AI session change

    def update_controls(self, chatAI:ChatAI):
        
        self.chatAI = chatAI
        self.chatMessageView.update_controls(chatAI)
        
        self.user_textfield.value = ""

        self.user_mode.value = "user"        
        self.update_role()


