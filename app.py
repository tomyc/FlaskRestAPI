from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'klucz' #jakis długi klucz
api = Api(app)

# @app.before_first_request # przeniesione do run.py
# def create_tables():
#     db.create_all()

jwt = JWT(app, authenticate, identity) #nowy endpoint: /auth - bedzie zwracany JWT token, który jest przesyłany do funkcji, która weryfikuje autoryzacje użytkownika

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__': #zabezpiecznie przed uruchomieniem aplikacji przy imporcie modułu app.py
    from db import db
    db.init_app(app)
    app.run(port=8000, debug=True)
