from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Nie nazwy sklepu w bazie'},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Sklep o nazwie'{}', już istnieje w bazie".format(name)},400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Zapis sklepu nie powiódł się'},500

        return store.json(),201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Nazwa sklepu usunięta'},200

class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}, 200
