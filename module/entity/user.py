from flask_login import UserMixin
from module.app.extensions import login_manager


class User(UserMixin):
    def __init__(self, id1):
        self.id = id1


users_data = [
    {'id': 'remote', 'username': 'remote', 'password': 'zqh112233!'}
]


def query_user(user_id):
    for user in users_data:
        if user_id == user['id']:
            return user
    return None


def add_user(user_id, password="ha5rwa!@#rsada"):
    if query_user(user_id) is None:
        users_data.append({'id': user_id, 'username': user_id, 'password': password})


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User(user_id)
        return curr_user
