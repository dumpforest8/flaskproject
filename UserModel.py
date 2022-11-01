from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    token = db.Column(db.String(500))

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password,
            'token': self.token
        })

    def create_user(_username,_password,_token):
        new_user = User(username=_username,password=_password,token =_token)
        db.session.add(new_user)
        db.session.commit()

    def delete_user(user):
        is_successful = User.query.filter_by(username=user).delete()
        db.session.commit()
        return bool(is_successful)

    def get_all_users():
        return User.query.all()

    def get_user(user):
        return User.query.filter_by(username = user).first()

    def is_user_valid(user):
        is_user =  User.query.filter_by(username = user).first()
        if is_user is None:
            return False
        else:
            return True
        

    def user_password_match(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    def update_token(user, _token):
        user_to_update = User.query.filter_by(username=user).first()
        user_to_update.token = _token
        db.session.commit()
        

    






