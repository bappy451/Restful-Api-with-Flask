from flask_restful import Resource, reqparse
from models.paper import PaperModel


class Paper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('journalName',
                        type=str,
                        required=True,
                        help="Every Paper needs a journalName."
                        )
    parser.add_argument('area',
                        type=str,
                        required=True,
                        help="Every Papaer needs a area."
                        )
    parser.add_argument('abstract',
                        type=str,
                        required=True,
                        help="Every Papaer needs a abstract."
                        )
    parser.add_argument('fullPaper',
                        type=str,
                        required=True,
                        help="Every Paper needs a fullPaper."
                        )
    
    def get(self, name):
        paper = PaperModel.find_by_name(name)
        if paper:
            return paper.json()
        return {'message': 'Paper not found'}, 404

    def post(self, name):
        if PaperModel.find_by_name(name):
            return {'message': "A paper with name '{}' already exists.".format(name)}, 400

        data = Paper.parser.parse_args()
        paper = PaperModel(name, **data)
        try:
            paper.save_to_db()
        except:
            return {"message": "An error occurred creating the paper."}, 500

        return paper.json(), 201

    def delete(self, name):
        paper = PaperModel.find_by_name(name)
        if paper:
            paper.delete_from_db()

        return {'message': 'Paper deleted'}


class PaperList(Resource):
    def get(self):
        return {'papers': list(map(lambda x: x.json(), PaperModel.query.all()))}
