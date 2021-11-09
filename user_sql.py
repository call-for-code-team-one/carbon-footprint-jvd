from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], username=user[1], password=user[2]
        )
        return user

    @staticmethod
    def create(id, username, password):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, username,password) "
            "VALUES (?, ?, ?, ?)",
            (id, username, password),
        )
        db.commit()
    @staticmethod
    def find_by_id(id):
        return User