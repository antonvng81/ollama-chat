# ollama-chat

A chat client for ollama.

Created with flet UI library.

# installation

- install ollama 

    curl -fsSL https://ollama.com/install.sh | sh

- install mysql

    sudo apt-get install mysql-server <br/>
    mysql -uroot -pYOUR_SQL_ROOT_PASSWORD <br/>

- create the venv environment: 
    
    sh create_venv.sh

- create database: 
    
    python3 create_database.py

- create the following dirs and file

    mkdir uploads <br/>
    mkdir secret <br/>
    touch secret/SECRET_KEY <br/>

- put this into SECRET_KEY file
    
    export FLET_UPLOAD_DIR='uploads' <br/>
    export FLET_SECRET_KEY='YOUR_CUSTOM_FLET_SECRET_KEY' <br/>  
    export MYSQL_ROOT_KEY='YOUR_SQL_ROOT_PASSWORD' <br/>

# run

- run with the following command

    sh run.sh
