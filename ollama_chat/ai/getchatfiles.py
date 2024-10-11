
import os


def get_chat_files(path:str) -> dict:

    upload_dir = os.environ.get('FLET_UPLOAD_DIR')
    full_path = f"{upload_dir}/{path}"

    table = {}

    if os.path.exists(full_path):
        for entry in os.scandir(full_path):
            if entry.is_dir():
                
                name = entry.name
                file_name = f"{full_path}/{name}/{name}.json"

                table[name] = file_name
    
    return table
        
