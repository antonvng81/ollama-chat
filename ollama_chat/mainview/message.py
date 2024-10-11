
class ChatMessage():
    
    QUERY = 0
    SYSTEM = 1
    LOG = 2
    LOAD = 3

    def __init__(self, user_name: str="", text: str="", type: int=LOG)->None:
        self.user_name = user_name
        self.text = text
        self.message_type = type
