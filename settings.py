from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\Fun_N_Games\Course\project2\database2.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

