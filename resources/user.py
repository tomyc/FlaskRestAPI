import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Nazwa użytkownika musi być podana"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Hasło użytkownika musi być podana"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user is None:
            user = UserModel(data['username'], data['password']) # = zapisowi poniżej
            user = UserModel(**data)
            user.save_to_db()
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            #
            # query = "INSERT INTO users VALUES (NULL, ?, ?)"
            # cursor.execute(query, (data['username'], data['password'],))
            #
            # connection.commit()
            # connection.close()

            return {'message': "Dane o użytkowniku '{}' zapisane do bazy".format(data['username'])}, 201

        else:
            return {'message': "Użytkownik o nazwie '{}' istnieje już w bazie".format(data['username'])}, 400
