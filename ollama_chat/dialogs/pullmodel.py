from typing import Callable, cast
import ollama

import flet
from ollama_chat.other.resultmessage import ChatResultMessage
import ollama_chat.other.theme as ChatTheme
from ollama_chat.ai import ollama_get_models

class ChatPullModel(flet.AlertDialog):
        
    def __init__(self, assert_model:bool, close_result:Callable) -> None:

        self.assert_model = assert_model
        self.close_result = close_result
        self.not_working = True
        self.result_msg = ChatResultMessage("Model not pulled.", False)


        self.model_textfield = flet.TextField(
            hint_text="Enter model name",
            hint_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=14), # type: ignore
            text_style=flet.TextStyle(color=ChatTheme.dialog_color, weight="bold", size=14), # type: ignore
            autofocus=True,            
            border_width=ChatTheme.border_width,
            border_color=ChatTheme.dialog_border_color,
            focused_border_color=ChatTheme.dialog_focused_border_color,
            border_radius=8,
            )
        
        self.progress_msg = flet.Text("", style= flet.TextStyle(color=ChatTheme.dialog_color, weight="normal", size=12)) # type: ignore
        self.progressbar = flet.ProgressBar(width=400,value=0, color=ChatTheme.dialog_border_color)

        actions = [
            flet.ElevatedButton(text="Pull", on_click=self.pull_click),
            flet.ElevatedButton(text="Close", on_click=self.submit_click)
            ]
        
        super().__init__(                
            modal=True,
            open=True,
            title=flet.Text("Pull",color = ChatTheme.dialog_color),
            content=flet.Column([self.model_textfield, self.progress_msg, self.progressbar], 
                tight=True,
                ),
            actions=actions, # type: ignore
            actions_alignment=flet.MainAxisAlignment.END,
            )

    # Pull event

    def pull_click(self, e):

        self.not_working = False    
        self.model_textfield.read_only = True
        self.progress_msg.color = ChatTheme.text_entry_color
        
        model = self.model_textfield.value


        if not model:

            self.model_textfield.error_text = "Model name can't be empty!"
            self.model_textfield.update()

        else:
            
            model = cast(str, model)

            try:

                current_digest, digest_set = '', {}
                for progress in ollama.pull(model, stream=True):

                    digest = progress.get('digest', '') # type: ignore
                    
                    if digest != current_digest and current_digest in digest_set:
                        digest_set[current_digest]['completed'] = digest_set[current_digest]['total']
                        self.progressbar.value = 1.0

                    if not digest:
                        continue

                    if digest not in digest_set and (total := progress.get('total')): # type: ignore
                        digest_set[digest] =  {'completed':0.0,'total':total}
                        self.progress_msg.value = f"pulling {digest[7:19]}"
                        self.progressbar.value = 0.0

                    if completed := progress.get('completed'): # type: ignore
                        digest_set[digest]['completed']=completed
                        self.progressbar.value = digest_set[digest]['completed'] / digest_set[digest]['total']

                    current_digest = digest
                    e.page.update()

            except:
                self.progress_msg.color = flet.colors.RED
                self.progress_msg.value = "Error: Model pull not successful"
                e.page.update()


            else:
                self.progress_msg.color = flet.colors.GREEN            
                self.progress_msg.value = "Model pull successful"
                e.page.update()

                self.result_msg = ChatResultMessage(f"Model '{model}' pulled.", True)
            
        self.not_working = True
        self.model_textfield.read_only = False


    def submit_click(self,e):

        if self.not_working: 

            model_list = ollama_get_models()

            if model_list:
                self.close_result(e, model_list, self.result_msg)
            else:
                self.progress_msg.color = flet.colors.RED            
                self.progress_msg.value = "Error: No models installed."
                e.page.update()            
                
                if not self.assert_model:
                    self.result_msg = ChatResultMessage("Error: No models pulled.", False)                
                    self.close_result(e, model_list, self.result_msg)








