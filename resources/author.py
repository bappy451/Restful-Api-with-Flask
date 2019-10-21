from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.author import AuthorModel


class Author(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('paper_id',
                        type=int,
                        required=True,
                        help="Every Author needs a paer_id."
                        )
    parser.add_argument('institutin_name',
                        type=str,
                        required=True,
                        help="Every Author needs a institutin_name."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="Every Author needs a email."
                        )
    parser.add_argument('designation',
                        type=str,
                        required=True,
                        help="Every Author needs a designation."
                        )

    @jwt_required()
    def get(self, name):
        author = AuthorModel.find_by_name(name)
        if author:
            return author.json()
        return {'message': 'author not found'}, 404

    def post(self, name):
        if AuthorModel.find_by_name(name):
            return {'message': "An author with name '{}' already exists.".format(name)}, 400

        data = Author.parser.parse_args()

        author = AuthorModel(name, **data)

        try:
            author.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return author.json(), 201

    def delete(self, name):
        author = AuthorModel.find_by_name(name)
        if author:
            author.delete_from_db()
            return {'message': 'author deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Author.parser.parse_args()

        author = AuthorModel.find_by_name(name)

        if author:
            author.institutin_name = data['institutin_name']
        else:
            author = AuthorModel(name, **data)

        author.save_to_db()

        return author.json()


class AuthorList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), AuthorModel.query.all()))}
