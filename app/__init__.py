from flask import Flask
from urllib.parse import quote


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='ABSIKJDABFABJASCAS',
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:%s@localhost/e_commerce' % quote('Myca@1236'),
    SQLALCHEMY_TRACK_MODIFICATION=True,
)

# db = SQLAlchemy(app=app)
