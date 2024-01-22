from flask import Flask
from urllib.parse import quote

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = '21137affa59a4dd08b708dcf106c724f9'

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/e_commerce?charset=utf8mb4" % quote('Myca@1236')


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
