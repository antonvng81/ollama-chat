#!/bin/bash

curl -fsSL https://ollama.com/install.sh | sh

sudo apt-get install mysql-server

python3 -m venv venv
source venv/bin/activate

pip install flet
pip install mysql-connector-python
pip install bcrypt
pip install ollama

mkdir uploads
mkdir secret

read -p "write mysql root pasword:" sql_password
read -p "write a secret key for flet:" flet_password
read -p "write a directory name for uploads:" uploads_dir
 
touch secret/SECRET_KEY
echo "export FLET_UPLOAD_DIR='${uploads_dir}'"       >> secret/SECRET_KEY
echo "export FLET_SECRET_KEY='${flet_password}'"     >> secret/SECRET_KEY
echo "export MYSQL_ROOT_KEY='${sql_password}'"       >> secret/SECRET_KEY

source secret/SECRET_KEY

mysql --user=root --password=$sql_password

python3 setup/create_database.py