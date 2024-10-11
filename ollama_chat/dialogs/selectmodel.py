import flet 
from typing import Callable, cast
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.ai import ollama_get_models, ChatAI

class ChatSelectModel(flet.AlertDialog):

    def __init__(self, chatAI:ChatAI, close_result:Callable) -> None:

        self.close_result = close_result        
        self.chatAI = chatAI
        self.model_list = ollama_get_models()
        self.prev_model = chatAI.model

        # controls

        self.model_textfield = flet.TextField(
            hint_text="Enter model name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,  
            on_change=self.textview_changed,          
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            value=self.chatAI.model
            )        
        
        # Selector for model

        model_options = []

        for model in self.model_list:
            model_options.append(flet.dropdown.Option(model))

        self.model_options = flet.Dropdown(
            border_radius=8,
            content_padding=flet.Padding(top=2,bottom=2, left=10, right=0),
            options=model_options,
            on_change=self.options_changed,
            value = self.chatAI.model,
            border_color= ChatTheme.appbar_border_color,
            focused_border_color= ChatTheme.appbar_focused_border_color,
            border_width= ChatTheme.border_width,
            text_style=flet.TextStyle(color=ChatTheme.appbar_border_color, weight="bold", size=14), # type: ignore
        )

        actions = [
            flet.ElevatedButton(text="Submit", on_click=self.submit_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click),
            ]

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Select",color = ChatTheme.dialog_color),
            content=flet.Column([self.model_options, self.model_textfield], 
                tight=True,
            ),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )                        

    # Submit event

    def submit_click(self,e):

        self.model_textfield.error_text = ""
        model = self.model_textfield.value
        
        if model == self.prev_model:
            self.close_result(e, ChatResultMessage("Model is the same.", False))

        elif model not in self.model_list:
            self.model_textfield.error_text = "Please choose an installed model!"
            e.page.update()

        else:
            model = cast(str, model)
            log = self.chatAI.change_model(model)

            if log is not None:
                self.close_result(e, ChatResultMessage("Model changed.", True))
            else:
                self.close_result(e, ChatResultMessage("Model not changed.", False))

    def cancel_click(self,e):
        self.close_result(e, ChatResultMessage("Model change cancelled.", False))


    def options_changed(self,e):
        self.model_textfield.error_text = ""
        self.model_textfield.value = self.model_options.value        
        e.page.update()

    def textview_changed(self,e):
        
        if self.model_textfield.value not in self.model_list:
            self.model_textfield.error_text = "Please choose an installed model!"
            e.page.update()
        else:
            self.model_textfield.error_text = ""
            self.model_options.value =self.model_textfield.value
            e.page.update()



