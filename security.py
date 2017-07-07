from models.user import UserModel
from werkzeug.security import safe_str_cmp

# users=[
#     User(1, 'tom', 'asdf')
# ]
#
#
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    #if user and user.password == password: # w przypadku porównywania łańcuchów mogą pojawić sie problemy z róznymi systemami
    if user and safe_str_cmp(user.password, password): # w przypadku porównywania łańcuchów mogą pojawić sie problemy z róznymi systemami
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
