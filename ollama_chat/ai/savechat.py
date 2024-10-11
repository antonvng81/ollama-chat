
# Save a chat file

import os
from typing import cast
from ollama_chat.account import ChatAccount
from ollama_chat.account.strcodify import str_codify
from ollama_chat.ai import ChatAI


def save_chat(account:ChatAccount, chatAI:ChatAI) -> str:

    # Save the chat

    chat_name = cast(str, chatAI.name)

    upload_dir = os.environ.get('FLET_UPLOAD_DIR')
    
    chat_name_dir = str_codify(chat_name)

    file_path = f"{upload_dir}/{account.user_dir}/{chat_name_dir}"
    file_name = f"{file_path}/{chat_name_dir}.json"

    os.makedirs(file_path, exist_ok=True)

    chatAI.save_chat_file(file_name)

    return file_name