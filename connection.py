from flask import Flask
from flask_sqlalchemy import SQLAlchemy

CC = Flask("Cart Central")
CC.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<db_user>:<db_password>@localhost:<db_port>/cart_central'
db = SQLAlchemy(CC)
