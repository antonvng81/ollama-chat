
from typing import Any, List, Mapping, Union, Tuple,  cast
import ollama
import json

from ollama_chat.ai.log import ChatLog
from ollama_chat.ai.attachedfiles import ChatAttachedFiles
from ollama_chat.ai.filetypemap import FILE_TYPE_MAP


# Decorator to insert files in prompt

def file_parser(name, extensions:List[str]):                
    def decorator(function):
        FILE_TYPE_MAP[name] = { "extensions":extensions,"function":function}
        def wrapper(self, message:dict, file_list:list):
            return function(self, message, file_list)
        return wrapper
    return decorator


class ChatAI:

    def __init__(   self,                 
                    name: Union[str,None]=None, 
                    user_name: Union[str,None]=None,                                       
                    model: Union[str,None]=None,  
                    session: list=[]) -> None:
    
        self.name = name
        self.user_name = user_name

        self.session = session
        self.model = model
        self.index_count = 0

        self.log = ChatLog() # empty
        self.attached_files = None

    def increment_index_count(self):
        self.index_count +=1

    # change model
        
    def change_model(self, model:str)->ChatLog:
        
        self.model = model

        msglog = "Model changed: " + model

        self.log.add(msglog)

        return self.log

    # register attached files on ChatFileTable object

    def attach_files(self, attached_files:ChatAttachedFiles) -> ChatLog:

        if self.attached_files is None:
            self.attached_files = attached_files
        else:
            self.attached_files.extend_table(attached_files)

        attached_files_log = attached_files.get_log()

        self.log.add(attached_files_log)

        return self.log

    def dettach_files(self):
        if self.attached_files is not None:
            self.attached_files.remove_files()
            self.attached_files = None

    # parse methods 

    @file_parser("images",["jpg"])
    def images_parser(self, message:dict, file_list:list)->dict:

        # informative only
        message["_attached_images"] = file_list

        # model read these files
        message["images"] = file_list

        return message

    @file_parser("texts",["txt"])
    def texts_parser(self, message:dict, file_list:list)->dict:
        
        # informative only
        message["_attached_texts"] = file_list

        text = "Based on the following context:\n\n"
        
        for file_name in file_list:
            with open(file_name, 'r') as file:            
                file_text = file.read()
                text = text + f"File: {file_name}\n```\n{file_text}\n```\n"
        
        if "_facade" not in message:
            message["_facade"] = message["content"]                

        message["content"] = text + message["_facade"]
    
        return message
    
    # parse ChatFileTable object to a raw message

    def parse_attached_files(self, message:dict)->dict:

        if self.attached_files is not None:

            file_table = self.attached_files.dest

            for type_name, file_type in FILE_TYPE_MAP.items():
                if type_name in file_table:
                    message = file_type["function"](self, message, file_table[type_name])
    
        return message
    
    # perform actions to AI

    def query(self, user_query: str) -> Tuple[dict,dict]:

        message = {
            "role": "user", 
            "content": user_query,
            "stream":False,
            "_index":self.index_count
        }

        self.increment_index_count()

        if not self.log.empty():
            message["_log"] = self.log.text()
        
        self.log.clear()

        message = self.parse_attached_files(message)
        self.session.append(message)

        model = cast(str, self.model)
        
        response = ollama.chat(model=model, messages=self.session)        
        response = cast(Mapping[str,Any], response) # default output                     

        answer = response["message"]["content"]
        
        message_answer = {
            "role": "assistant", 
            "content": answer,
            "_index":self.index_count}

        self.increment_index_count()

        self.session.append(message_answer) 
        
        return message, message_answer

    def system(self, system_query: str) -> dict:

        message = {
            "role": "system", 
            "content": system_query,
            "_index": self.index_count
        }
        
        self.increment_index_count()

        if not self.log.empty():
            message["_log"] = self.log.text()
        
        self.log.clear()

        message = self.parse_attached_files(message)      
        
        self.session.append(message)

        return message

    # Load/Save chat sessions
        
    def save_chat_file(self, file_name:str)-> None:
                        
        with open(file_name, 'w') as file:
            json.dump({
                "name":self.name,
                "user_name":self.user_name,
                "model":self.model,
                "session": self.session,
                "index_count":self.index_count},file)           

    def load_chat_file(self, file_name:str) -> None:
   
        with open(file_name, 'r') as file:            
            data = json.load(file)
            
        self.name = data["name"]            
        self.user_name = data["user_name"]
        self.model = data["model"]
        self.session = data["session"]  
        self.index_count = data["index_count"]

    def clear_chat(self):
        self.name = ""
        self.user_name = ""
        self.model = ""
        self.session = []
        self.index_count = 0

    def remove_message(self, index:int):
        for message in self.session:
            if message["_index"] == index:
                self.session.remove(message)
                break


def ollama_get_models():
    model_list = [model["name"] for model in ollama.list()["models"]]
    return model_list


