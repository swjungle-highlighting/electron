# -*- encoding: utf-8 -*-
from api.HelperFunctions import _cut_time_and_messageset, AhoCorasick
import sys
import json

sys.stderr = sys.stdout

def KeywordsSearch(URL_ID, KEYWORDS) : 
    ACtrie = AhoCorasick(KEYWORDS)
    chat_file = open('./resources/app/storage_chat/'+URL_ID+'.txt', "r", encoding = 'UTF8')
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

if __name__ == '__main__':
    url = sys.argv[1]
    keywords = sys.argv[2]

    URL_ID = url.split("=")[1]
    KEYWORDS = keywords.split(', ')
    Distribution = KeywordsSearch(URL_ID, KEYWORDS)

    ret = {
            "result" : {'distribution' : Distribution}
        }
    print(json.dumps(ret))