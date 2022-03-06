# -*- coding: UTF-8 -*-
'''
@Project ：youtube_highlight_extract 
@File ：chatProcess.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-02-09 오후 6:38 
'''

import pytchat



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
        hh, mm, ss = 0, 0, -1
    return hh*3600 + mm*60 + ss

def _filter_message(message) :
    return message


def _calculate_superchat(currency, amount) :
    return int(exch[currency] * amount)

RANGE_SUPERCHAT = 300
RANGE_DISTRIBUTION = 10
def chatProcess(url_id, duration) :

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
                
    SuperchatAmount_BarChart = [0 for i in range(duration)]
    for i in range(duration) : 
        if i %RANGE_SUPERCHAT : 
            SuperchatAmount_BarChart[i] = SuperchatAmount[i //RANGE_SUPERCHAT]



    path = './chat_storage/' + url_id + '.txt'
    chat_file = open(path, "w", encoding = 'UTF8')
    chat_file.writelines(str(duration) + ' duration(sec)' '\n')
    for i in checkTime :
        chat_file.writelines(str(i) + ' ' + str(MessageSet[i]) + '\n')
    chat_file.close()

    return [Distribution, MessageSet, SuperchatAmount_BarChart]