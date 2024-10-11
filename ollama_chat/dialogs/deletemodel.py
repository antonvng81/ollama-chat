from typing import Callable
import ollama
import flet
from ollama_chat.ai import ollama_get_models
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme

class ChatDeleteModel(flet.AlertDialog):
        
    def __init__(self, delete_result:Callable) -> None:

        
        self.progress_msg = flet.Text("", style= flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=12)) # type: ignore
        self.not_working = True
        
        self.result_msg = ChatResultMessage("Model not deleted.", False)

        self.delete_result = delete_result
        self.model_list = ollama_get_models()

        # controls  

        actions = [
            flet.ElevatedButton(text="Delete", on_click=self.delete_click),
            flet.ElevatedButton(text="Cancel", on_click=self.cancel_click)
            ]

        self.model_textfield = flet.TextField(
            hint_text="Enter model name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14),#type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14),#type: ignore
            autofocus=True, 
            on_change=self.model_textfield_changed,           
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            )

        # Selector for model

        model_options = []

        for model in self.model_list:
            model_options.append(flet.dropdown.Option(model))

        self.model_options = flet.Dropdown(
            border_radius=8,
            content_padding=flet.Padding(top=2,bottom=2, left=10, right=0),
            options=model_options,
            on_change=self.model_options_changed,
            value = self.model_list[0],
            border_color= ChatTheme.appbar_border_color,
            focused_border_color= ChatTheme.appbar_focused_border_color,
            border_width= ChatTheme.border_width,
            text_style=flet.TextStyle(color=ChatTheme.appbar_border_color, weight="bold", size=14),#type: ignore
        )

        # init

        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Delete",color = ChatTheme.dialog_color),
            content=flet.Column([self.model_options, self.model_textfield, self.progress_msg], 
                tight=True,
                ),
            actions=actions, #type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )        
        
    # methods
        
    def delete_click(self, e):

        self.not_working = False

        self.model_textfield.read_only = True
        self.model_options.disabled = True

        model = self.model_textfield.value

        if not model:
            
            # Provide a valid string

            self.progress_msg.color = flet.colors.RED            
            self.progress_msg.value = "Error: empty name."

            self.model_textfield.read_only = False
            self.model_options.disabled = False

            self.not_working = True

            e.page.update()

        else:

            # Perform ollama delete model

            try:
                result = ollama.delete(model)
            except:
                self.progress_msg.color = flet.colors.RED            
                self.progress_msg.value = "Error: ollama except."

            else:
                if result["status"] == "success":
                    self.progress_msg.color = flet.colors.GREEN            
                    self.progress_msg.value = f"Model {model} deleted."

                    self.result_msg = ChatResultMessage(f"Model '{model}' deleted.", True)
                else:
                    self.progress_msg.color = flet.colors.RED            
                    self.progress_msg.value = "Error: ollama not successful."

            self.model_textfield.read_only = False
            self.model_options.disabled = False

            self.not_working = True

            # once model is deleted menu is changed to one button dialog

            self.actions = [
                flet.ElevatedButton(text="Close", on_click=self.submit_click)
            ]      

            e.page.update()

    def submit_click(self,e):

        # all work done
        self.delete_result(e, self.result_msg)

    def cancel_click(self,e):
        # this if prevents dialog closing in the midle of deleting process
        if self.not_working is True:        
            self.delete_result(e, ChatResultMessage(f"Model delete cancelled.", False))

    def model_textfield_changed(self,e):
        
        if self.model_textfield.value in self.model_list:
            self.model_options.value = self.model_textfield.value

        e.page.update()            

    def model_options_changed(self,e):

        self.model_textfield.value = self.model_options.value        

        e.page.update()                  