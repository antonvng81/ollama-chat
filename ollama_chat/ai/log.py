class ChatLog:

    def __init__(self):
        self._text = ""
        self._last = ""

    def empty(self):
        return self.text == ""
    
    def text(self):
        return self._text
    
    def last(self):
        return self._last
    
    def add(self, msg:str):

        self._last = msg

        if not self.empty():
            self._text += "\n" + msg
        else:
            self._text = msg
    
        return self
    
    def clear(self):
        self._text = ""
        self._last = ""