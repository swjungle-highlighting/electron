# -*- coding: UTF-8 -*-
'''
@Project ：youtube_highlight_extract 
@File ：HelloApiHandler.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-02-07 오후 5:30 
'''
import json
import pymysql
from flask_restful import Api, Resource, reqparse

from api.extract.streamExtract import streamProcess
from api.HelperFunctions import return_MessageSet, _get_bookmarker
import time

from password import dbpw, dbip


class HelloApiHandler(Resource):
    def get(self):
        return {
            'status' : '200',
            'message' : 'Success'
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)

        args = parser.parse_args()
        print(args)

        request_url = args['url']
        url_id = request_url.split("=")[1]

        """
        check database
        """
        db = pymysql.connect(
            host=dbip,
            port=3306,
            user='root',
            password=dbpw,
            db='highlighting', charset='utf8', autocommit=True  # 실행결과확정
        )

        cursor = db.cursor()
        sql = 'SELECT result FROM youtube WHERE url="' + request_url + '";'
        cursor.execute(sql)

        data = cursor.fetchone()

        if data :
            # if url in db
            result = eval(data[0])
            chat = result['chat']
            chatSet = return_MessageSet(url_id)
            chat = [chat[0]] + [chatSet] + [chat[1]]
            result['chat'] =chat

            bookmarker = _get_bookmarker(url_id)

            final_ret = {
                "type": "POST",
                "status": "This is Database",
                "url": request_url,
                "result": result,
                "bookmarker" : bookmarker,
            }

            db.close()
            print("Success read DB")
            return final_ret

        """
        stream data fetch start
        """

        start = time.perf_counter()
        res = streamProcess(request_url)
        finish = time.perf_counter()
        print(f'Finished in {round(finish - start, 2)} second(s)')

        if res == False:
            return {
                "error" : "id is not valid"
            }

        """
        stream data fetch end
        """

        path = './bookmarker_storage/' + url_id + '.json'
        temp = []
        with open(path, 'w', encoding="UTF-8") as f:
            json.dump(temp, f, ensure_ascii=False)
        bookmarker = _get_bookmarker(url_id)


        final_ret = {
            "type" : "POST",
            "status" : "Success insert Database",
            "url" : request_url,
            "result" : res,
            "bookmarker": bookmarker,
        }

        """
        insert database
        """
        title = res['title']
        title = title.replace("'", "\\'")
        chat = res['chat']
        chat = [chat[0] ]+[chat[2]]
        json_str = '{"audio":'+str(res['audio'])+', "video":'+str(res['video'])+', "chat":'+str(chat)+', "title":'+str('"'+title+'"')+', "thumbnail":'+str('"'+res['thumbnail']+'"')+', "duration":'+str('"'+str(res['duration'])+'"')+'}'
        sql = "insert into youtube(url, result) values('"+request_url+"', '"+json_str+"');"
        cursor.execute(sql)
        print("Success insert DB")

        db.close()

        return final_ret