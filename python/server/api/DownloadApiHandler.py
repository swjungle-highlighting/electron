from flask_restful import Api, Resource, reqparse

from api.download_logic.do_logic import create_cutTool, delete_cutTool
from api.HelperFunctions import _parse_bookmarker

class DownloadApiHandler(Resource) :
    def __init__(self) :
        self.downloadcount = 0
    
    def get(self):
        delete_cutTool()
        return {
            'status' : '200',
            'message' : 'Success'
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bookmarks', type=str)
        args = parser.parse_args()
        print(args['bookmarks'])
        bookmarks = _parse_bookmarker(args['bookmarks'])
        self.downloadcount += 1
        print(self.downloadcount)
        create_cutTool(bookmarks)
            
        final_ret = {
            "type" : "POST",
            "status" : "success"
        }
        return final_ret
