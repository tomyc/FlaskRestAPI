#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    #parse bedzie dostpna w każdej z metod
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Wartość musi być podana"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store ID musi być podana"
                        )

    @jwt_required() #metoda get bedzie wymagała wcześniejszej autoryzacji
    def get(self, name):
        # for item in items:
        #     if item['name']==name:
        #         return item
        # return {'message':'Brak elementu'}, 404
        # item = next(filter(lambda x:x['name']==name, items),None)
        # return {'item':item}, 200 if item else 404
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message':'Element nie znaleziony'}, 404

    def post(self, name):
        #if next(filter(lambda x:x['name']==name, items),None) is not None:
        #if next(filter(lambda x:x['name']==name, items),None): # rownoznaczne z poprzednim zapisem
        if ItemModel.find_by_name(name):
            return {'message':"Element '{}' jest już w bazie".format(name)}, 400


        data = Item.parser.parse_args()

        #data = request.get_json(silent=True)
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            #item.insert_item()
            item.save_to_db()
        except:
            return {'message':'Wystąpił błąd przy dodawaniu elementu do bazy'}, 500 #internal server error

        #items.append(item)
        return item.json(), 201

    def delete(self, name):
        # global items
        # items = list(filter(lambda x:x['name'] !=name, items))
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name = ?"
        #
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':"Element '{}' został usuniety".format(name)}

    def put(self, name):

        data = Item.parser.parse_args() #po zmianie lokalizacji definicji parsera należy dodać, że jest on cześcią klasy Item
        #data = request.get_json() #usunąc po zdefiniowaniu parsera

        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])

        if item is None:
            #item = ItemModel(name, data['price'], data['store_id']) # zgodne z zapisem poniżej
            item = ItemModel(name, data['price'], **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name':row[0], 'price':row[1]})
        #
        # connection.close()

        return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}, 200 # lub zapis poniżej
        #return {'items':[item.json() for item in ItemModel.query.all()]}, 200
