from typing import Self, cast

import flet 
import os
import shutil

from ollama_chat.ai.filetypemap import FILE_TYPE_MAP

class ChatAttachedFiles:

    def __init__(self, path:str, file_picker:flet.FilePicker)->None:

        file_picker_result = cast(flet.FilePickerResultEvent, file_picker.result)
        page = cast(flet.Page, file_picker.page)

        if not file_picker_result.files:
            return
        
        self.upload_dir = os.environ.get('FLET_UPLOAD_DIR')

        self.dest = {}
        self.src = {}
        self.path = path
        

        upload_list = []

        for picker_file in file_picker_result.files:
                
            file_name, file_extension = os.path.splitext(picker_file.name)

            for file_type_key, file_type_value in FILE_TYPE_MAP.items():            
            
                # check extensions
                if file_extension[1:] in file_type_value["extensions"]:

                    # create list for this key
                    if file_type_key not in self.dest:
                        self.dest[file_type_key] = []
                        self.src[file_type_key] = []

                    src_file_name = picker_file.path

                    #  create a path for this file
                    dest_file_name = f"{path}/{file_type_key}/{picker_file.name}"

                    # append file name                        
                    self.dest[file_type_key].append(f"{self.upload_dir}/{dest_file_name}") 
                    self.src[file_type_key].append(src_file_name) 

                    # append uploader object           
                    upload_list.append(
                        flet.FilePickerUploadFile(
                            picker_file.name,
                            upload_url=page.get_upload_url(dest_file_name,600)))
                    
                    break
        
        # perform the upload of files
                
        file_picker.upload(upload_list)

    
    # extend one object inside other
            
    def extend_table(self, other:Self):
            
        for file_type_key, file_list in other.dest.items():

            if file_type_key not in self.dest:
                self.dest[file_type_key] = []

            self.dest[file_type_key].extend(file_list)

        for file_type_key, file_list in other.src.items():

            if file_type_key not in self.src:
                self.src[file_type_key] = []

            self.src[file_type_key].extend(file_list)

                
    # log in text parsing

    def get_log(self):
        
        text  = ""

        for file_type_key, file_list in self.src.items():
            for file_name in file_list:
                if file_name is not None:
                    text = text + "File attached: " + file_name + "\n"

        return text.rstrip()
        
    def remove_files(self):
        shutil.rmtree(f"{self.upload_dir}/{self.path}")




