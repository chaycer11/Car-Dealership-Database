from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, role, user_type):
        # The 'id' here will be a string like 'emp_1' or 'cust_4'
        # This allows us to use one LoginManager for two different tables.
        self.id = id           
        self.name = name       
        self.role = role       
        self.user_type = user_type