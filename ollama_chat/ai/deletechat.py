# Save a chat file

import os
import shutil
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_codify


def delete_chat(account:ChatAccount, chat_name:str):

    upload_dir = os.environ.get('FLET_UPLOAD_DIR')

    file_path = f"{upload_dir}/{account.user_dir}/{str_codify(chat_name)}"

    if os.path.exists(file_path):
        shutil.rmtree(file_path)
        return True
    
    return False