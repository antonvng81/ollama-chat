import os
from typing import cast
from ollama_chat.account import ChatAccount
from ollama_chat.account.session import ChatAppSession
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai import ChatAI


def rename_chat(account:ChatAccount, chat_files:dict, old_chat_name:str, new_chat_name:str)->bool:

    new_chat_name_dir = str_codify(new_chat_name)

    if new_chat_name_dir in chat_files:
        return False

    # rename the chat

    upload_dir = os.environ.get('FLET_UPLOAD_DIR')
    
    old_chat_name_dir = str_codify(old_chat_name)
    old_file_path = f"{upload_dir}/{account.user_dir}/{old_chat_name_dir}"

    new_file_path = f"{upload_dir}/{account.user_dir}/{new_chat_name_dir}"

    os.rename(old_file_path, new_file_path)

    old_file_name = f"{new_file_path}/{old_chat_name_dir}.json"
    new_file_name = f"{new_file_path}/{new_chat_name_dir}.json"

    os.rename(old_file_name, new_file_name)

    # Rename json file contents

    chatAI = ChatAI()
    chatAI.load_chat_file(new_file_name)
    
    chatAI.name = new_chat_name
    chatAI.save_chat_file(new_file_name)

    return True
