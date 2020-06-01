from app import db

class User(db.Model):
    __tablename__='users'

    def generate_auth_token(self,expiration=600):
        s=11;