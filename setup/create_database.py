import os
import mysql.connector

MYSQL_ROOT_KEY = os.environ.get('MYSQL_ROOT_KEY')

def create_mysql_database():

    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_ROOT_KEY)
    
    cursor = mysql_db.cursor()
    cursor.execute("CREATE DATABASE ollama_chat")

    mysql_db.close()

def create_mysql_table():

    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_ROOT_KEY,
        database="ollama_chat")
    
    cursor = mysql_db.cursor()
    cursor.execute("""
        CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(100) UNIQUE,
        hash_password VARCHAR(100)
        )""")
    
    mysql_db.close()

def main():

    create_mysql_database()
    create_mysql_table()


if __name__ == "__main__":
    main()