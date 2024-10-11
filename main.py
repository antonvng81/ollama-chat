import os
import flet
from ollama_chat.dialogs.login import ChatLogin

# Getting environament variables                    
upload_dir = os.environ.get('FLET_UPLOAD_DIR')
secret_key = os.environ.get('FLET_SECRET_KEY')

def main(page: flet.Page):

    page.title = "ollama chat"
    page.open(ChatLogin(page))

flet.app(target=main, view=flet.AppView.FLET_APP_WEB, upload_dir=upload_dir, assets_dir="assets")
