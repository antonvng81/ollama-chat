import os
import bcrypt
import mysql.connector
from typing import  Tuple, cast
from ollama_chat.account.strcodify import str_codify

FLET_SECRET_KEY = os.environ.get('FLET_SECRET_KEY')
MYSQL_ROOT_KEY = os.environ.get('MYSQL_ROOT_KEY')

class ChatAccount:


    def __init__(self):

        self.mysql_db = mysql.connector.connect(host="localhost",
                            user="root",
                            password=MYSQL_ROOT_KEY,
                            database="ollama_chat")
        self.user_name = None       
        self.user_dir = None 

    def login(self, user_name:str, password:str):

        query = '''SELECT user_name, hash_password FROM users
                   WHERE user_name = %s'''
        
        mysql_cursor = self.mysql_db.cursor()
        mysql_cursor.execute(query,(user_name,))

        row = mysql_cursor.fetchone()

        if row:
            
            row = cast(Tuple, row)

            hash_password = row[1]
            self.user_name = row[0]
            self.user_dir = str_codify(self.user_name)

            return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))
        else:
            return False


    def register(self, user_name:str, password:str):

        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
       
        query = '''INSERT INTO users (user_name, hash_password) VALUES (%s,%s)'''

        mysql_cursor = self.mysql_db.cursor()       
        mysql_cursor.execute(query,(user_name, hash_password))

        self.mysql_db.commit()

        if mysql_cursor.rowcount == 1:
            self.user_name = user_name
            self.user_dir = str_codify(self.user_name)
            return True
        else:
            return False
    
