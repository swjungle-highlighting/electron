import os
import time
import json
import pytchat
import requests

from collections import defaultdict
exch =  defaultdict(lambda : 1)
exch['USD'] = 1200
exch['¥'] = 10
exch['EUR'] = 1350
exch['TWD'] = 45
exch['SGD'] = 900
exch['HKD'] = 150
exch['CAD'] = 950
exch['AUD'] = 850
exch['GBP'] = 1600
exch['RUB'] = 15

def _parse_elapsedTime(t) :
    if t[0] == '-' :
        return -1
    lent = len(t)
    if lent == 4 :
        hh = 0
        mm = int(t[0])
        ss = int(t[2:4])
    elif lent == 5 :
        hh = 0
        mm = int(t[0:2])
        ss = int(t[3:5])
    elif lent == 7 :
        hh = int(t[0])
        mm = int(t[2:4])
        ss = int(t[5:7])
    else :
        return -1
    return hh*3600 + mm*60 + ss

def _filter_message(message) :
    return message

def _calculate_superchat(currency, amount) :
    return int(exch[currency] * amount)

def _make_chatlog(url_id, duration, MessageSet, checkTime) : 
    if not os.path.exists('./resources/app/storage_chat/') : 
        os.chdir('./resources')
        os.chdir("./app")
        os.mkdir("./storage_chat")
        os.chdir('./../../')
    path = './resources/app/storage_chat/' + url_id + '.txt'
    chat_file = open(path, "w", encoding = 'UTF8')
    chat_file.writelines(str(duration) + ' duration(sec)' '\n')
    for i in checkTime :
        chat_file.writelines(str(i) + ' ' + str(MessageSet[i]) + '\n')
    chat_file.close()

def _make_barchart(duration, SuperchatAmount) : 
    SuperchatAmount_BarChart = [0 for i in range(duration)]
    for i in range(duration) : 
        if i %RANGE_SUPERCHAT : 
            SuperchatAmount_BarChart[i] = SuperchatAmount[i //RANGE_SUPERCHAT]
    return SuperchatAmount_BarChart


def YT_parse(url_id, duration) : 
    Distribution = [0 for i in range(duration //RANGE_DISTRIBUTION +1)]
    SuperchatAmount = [0 for i in range(duration //RANGE_SUPERCHAT +10)]
    MessageSet = {}
    checkTime = []

    chatset = pytchat.create(video_id=url_id, interruptable=False)

    while chatset.is_alive() :
        data = chatset.get()
        items = data.items
        for item in items :
            second = _parse_elapsedTime(item.elapsedTime)
            if second >= duration or second < 0 :
                continue
            Distribution[second //RANGE_DISTRIBUTION] += 1
            message = _filter_message(item.message)
            try :
                MessageSet[second].append(message)
            except :
                MessageSet[second] = [message]
                checkTime.append(second)
            if item.amountValue :
                SuperchatAmount[second //RANGE_SUPERCHAT] += _calculate_superchat(item.currency, item.amountValue)
                
    SuperchatAmount_BarChart = _make_barchart(duration, SuperchatAmount)
    _make_chatlog(url_id, duration, MessageSet, checkTime)

    return [Distribution, MessageSet, SuperchatAmount_BarChart]


def TW_parse(url_id, duration) :
    Distribution = [0 for i in range(duration //RANGE_DISTRIBUTION +1)]
    SuperchatAmount = [0 for i in range(duration //RANGE_SUPERCHAT +10)]
    MessageSet = {}
    checkTime = []

    header = {"Accept": "application/vnd.twitchtv.v5+json; charset=UTF-8"}
    params = {'client_id': "kimne78kx3ncx6brgo4mv6wki5h1ko"}

    i, next = 0, ''
    while True:
        if i == 0:
            url = f"https://api.twitch.tv/v5/videos/{url_id}/comments?content_offset_seconds=0"
            i += 1
        else:
            url = f"https://api.twitch.tv/v5/videos/{url_id}/comments?cursor={next}"

        try:
            response = requests.get(url, params=params, headers=header, timeout=10)
        except:
            time.sleep(1)
            continue
        j = json.loads(response.text)      
        for item in j["comments"]:
            second = int(item["content_offset_seconds"])
            if second >= duration or second < 0 : 
                continue
            message = _filter_message(item["message"]["body"])
            Distribution[second //RANGE_DISTRIBUTION] += 1
            try :
                MessageSet[second].append(message)
            except :
                MessageSet[second] = [message]
                checkTime.append(second)
        if '_next' not in j:
            break
        next = j["_next"]

    SuperchatAmount_BarChart = _make_barchart(duration, SuperchatAmount)
    _make_chatlog(url_id, duration, MessageSet, checkTime)

    return [Distribution, MessageSet, SuperchatAmount_BarChart]


RANGE_SUPERCHAT = 300
RANGE_DISTRIBUTION = 30
def chatProcess(url_id, duration, code) :
    ret = []
    if code == 1 : 
        ret = YT_parse(url_id, duration)
    elif code == 2 : 
        ret = TW_parse(url_id, duration)

    return ret