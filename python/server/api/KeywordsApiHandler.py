from flask_restful import Api, Resource, reqparse

from api.HelperFunctions import _cut_time_and_messageset, AhoCorasick

def KeywordsSearch(URL_ID, KEYWORDS) : 
    ACtrie = AhoCorasick(KEYWORDS)
    chat_file = open('./chat_storage/'+URL_ID+'.txt', "r", encoding = 'UTF8')
    duration, _ = _cut_time_and_messageset(chat_file.readline().rstrip())
    target = chat_file.readline()
    Distribution = [0 for i in range(duration//60 +1)]
    i = 0
    while target : 
        t, messageset = _cut_time_and_messageset(target)
        if t >= duration : 
            break
        ans = ACtrie.search(messageset)
        Distribution[t //60] += len(ans)
        i += 1
        target = chat_file.readline()
    chat_file.close()
    return Distribution

class KeywordsApiHandler(Resource) :
    def get(self):
        return {
            'status' : '200',
            'message' : 'Success'
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        parser.add_argument('keywords', type=str)
        args = parser.parse_args()

        URL_ID = args['url'].split("=")[1]
        KEYWORDS = args['keywords'].split(', ')
        print('URL : ', URL_ID)
        print(*KEYWORDS)
        Distribution = KeywordsSearch(URL_ID, KEYWORDS)
       
        final_ret = {
            "type" : "POST",
            "status" : "Success search keywords",
            "result" : {'distribution' : Distribution}
        }
        
        return final_ret