import json

from flask_restful import Api, Resource, reqparse

class BookMarkerApiHandler(Resource):
    def get(self):
        return {
            'status' : '200',
            'message' : 'This is get method'
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('markers', type=dict)
        parser.add_argument('url', type=str)

        args = parser.parse_args()
        request_markers = args['markers']['list']
        request_url = args['url']


        url_id = request_url.split("=")[1]
        path = './bookmarker_storage/'+url_id+'.json'

        with open(path, 'w', encoding="UTF-8") as f:
            json.dump(request_markers, f, ensure_ascii=False)

        return {
            'status': '200',
            'message': 'Save bookmarker',
            'markers' : request_markers,
        }