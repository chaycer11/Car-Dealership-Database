from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, role, user_type):
        self.id = id           
        self.name = name       
        self.role = role       
        self.user_type = user_type