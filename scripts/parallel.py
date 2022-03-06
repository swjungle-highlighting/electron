# -*- coding: UTF-8 -*-
'''
@Project ：password.py 
@File ：parallel.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-03-05 오후 7:52 
'''

import imp
import sys, os

sys.stderr = sys.stdout

import multiprocessing
import os

import yt_dlp
import ffmpeg
import numpy
import pytchat
from collections import defaultdict
import time

# audio
SAMPLERATE = 11025
GETPICK_PERSEC = 2


def audioProcess(url_id):
    global audio_start, audio_finish
    print("########################################################")
    print('audio ' + url_id)
    print("########################################################")
    """"""
    audio_start = time.perf_counter()

    folder = os.getcwd()
    print('folder', folder)
    print('url_id', url_id)
    target = ''
    for filename in os.listdir(folder + '/'):
        print('filename', filename)
        if url_id in filename:
            target = filename
    print('target',target)
    out, err = (
        ffmpeg
            .input(folder + '/' + target)
            .output('-', format='f32le', acodec='pcm_f32le', ac=1, ar=str(SAMPLERATE))
            .run(capture_stdout=True)
    )

    amplitudes = numpy.frombuffer(out, numpy.float32)

    AudioPick_7200perHOUR = []


    persec = SAMPLERATE // GETPICK_PERSEC
    pick, dirr = 0, 1
    for i in range(1, len(amplitudes)):
        if not i % persec:
            AudioPick_7200perHOUR.append(int(1000 * pick) * dirr)
            pick = 0
            dirr = -dirr
        pick = max(pick, abs(amplitudes[i]))
    audio_finish = time.perf_counter()

    return AudioPick_7200perHOUR

    """"""


# video
W, H = 128, 72
FPS = 10
DIFF_CUTLINE = 5000000


def videoProcess(url_id):
    global video_start, video_finish
    print("########################################################")
    print('video ' + url_id)
    print("########################################################")
    """"""
    video_start = time.perf_counter()

    folder = os.getcwd()
    target = ''
    for filename in os.listdir(folder + '/'):
        if url_id in filename:
            target = filename

    out, err = (
        ffmpeg
            .input(folder + '/' + target)
            .filter('fps', fps=FPS, round='up')
            .filter('scale', w=W, h=H)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
    )
    frames = (
        numpy
            .frombuffer(out, numpy.uint8)
            .reshape([-1, H, W, 3])
    )

    VideoDATA_3600perHOUR = []
    summ, before = 0, numpy.array([])
    for i in range(1, len(frames)):
        if not i % FPS:
            VideoDATA_3600perHOUR.append(min(summ, DIFF_CUTLINE))
            summ = 0
        now = frames[i]
        summ += abs(int(now.sum()) - int(before.sum()))
        before = now

    VideoDATA_3600perHOUR[0] = 0

    video_finish = time.perf_counter()

    return VideoDATA_3600perHOUR

    """"""


# chat
exch = defaultdict(lambda: 1)
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


def _parse_elapsedTime(t):
    if t[0] == '-':
        return -1
    lent = len(t)
    if lent == 4:
        hh = 0
        mm = int(t[0])
        ss = int(t[2:4])
    elif lent == 5:
        hh = 0
        mm = int(t[0:2])
        ss = int(t[3:5])
    elif lent == 7:
        hh = int(t[0])
        mm = int(t[2:4])
        ss = int(t[5:7])
    else:
        hh, mm, ss = 0, 0, -1
    return hh * 3600 + mm * 60 + ss


def _filter_message(message):
    return message


def _calculate_superchat(currency, amount):
    return int(exch[currency] * amount)


RANGE_SUPERCHAT = 300
RANGE_DISTRIBUTION = 10


def chatProcess(url_id, duration, chat_start, chat_finish):
    print("########################################################")
    print('chat ' + url_id)
    print("########################################################")

    chat_start = time.perf_counter()

    Distribution = [0 for i in range(duration // RANGE_DISTRIBUTION + 1)]
    SuperchatAmount = [0 for i in range(duration // RANGE_SUPERCHAT + 1)]
    MessageSet = {}
    checkTime = []
    chatset = pytchat.create(video_id=url_id, interruptable=False)

    while chatset.is_alive():
        data = chatset.get()
        items = data.items
        for item in items:
            second = _parse_elapsedTime(item.elapsedTime)
            if second >= duration or second < 0:
                continue
            Distribution[second // RANGE_DISTRIBUTION] += 1
            message = _filter_message(item.message)
            try:
                MessageSet[second].append(message)
            except:
                MessageSet[second] = [message]
                checkTime.append(second)
            if item.amountValue:
                SuperchatAmount[second // RANGE_SUPERCHAT] += _calculate_superchat(item.currency, item.amountValue)

    path = './chat_storage/' + url_id + '.txt'
    chat_file = open(path, "w", encoding='UTF8')
    for i in checkTime:
        chat_file.writelines(str(i) + ' ' + str(MessageSet[i]) + '\n')
    chat_file.close()

    chat_finish = time.perf_counter()

    return [Distribution, MessageSet, SuperchatAmount]


# extract
def _sec_to_str(sec):
    t = []
    t.append(sec % 60)
    t.append((sec % 3600 - t[0]) // 60)
    t.append(sec // 3600)
    for i in range(3):
        if t[i] < 10:
            t[i] = '0' + str(t[i])
        else:
            t[i] = str(t[i])
    return t[2] + ':' + t[1] + ':' + t[0]


CUT_RANGE = 600


def _do_subprocess(input_file, duration, index, audio, video):
    output_file = str(index) + input_file
    start = index * CUT_RANGE
    end = min(duration, (index + 1) * CUT_RANGE)
    ffmpeg_call = ["ffmpeg -ss", _sec_to_str(start), "-to", _sec_to_str(end), "-i", input_file, "-c copy", output_file]
    os.system(" ".join(ffmpeg_call))
    audio += audioProcess(output_file)
    video += videoProcess(output_file)
    os.remove(os.getcwd() + "/" + output_file)

def mulitProcessing(input_file, duration, index, audio, video ,CUT_RANGE):
    print('input', input_file)
    while index <= duration // CUT_RANGE:
        _do_subprocess(input_file, duration, index, audio, video)
        index += 1


opts = {
    'ignoreerrors': True,
    'nooverwrites': True,
    'format': 'worst',
    'outtmpl': './%(id)s.mp4',
}


def streamProcess(url):
    global extract_start, extract_finish
    print('::stream::')
    extract_start = time.perf_counter()
    url_id = url.split("=")[1]

    if len(url_id) != 11:
        return False

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        duration = info_dict.get('duration', None)
        title = info_dict.get('title')
        thumbnail = info_dict.get('thumbnail')

    extract_finish = time.perf_counter()

    ### parallel processing
    audio = []
    video = []
    input_file = url_id + '.mp4'
    index = 0

    pool = multiprocessing.Pool(processes=1)
    chat = pool.starmap_async(chatProcess, [(url_id, duration, chat_start, chat_finish)])
    mulitProcessing(input_file, duration,index,audio,video,CUT_RANGE)

    # chat = chatProcess(url_id, duration)
    # print(chat.get()[0])
    chat = chat.get()[0]
    pool.close()
    pool.join()
    ###

    folder = os.getcwd()
    target = ''
    for filename in os.listdir(folder + '/'):
        if url_id in filename:
            target = filename

    os.remove(folder + '/' + target)
    print('delete stream target!!')

    return {
        'audio': audio,
        'video': video,
        'chat': chat,
        'title': title,
        'thumbnail': thumbnail,
        'duration': duration
    }


if __name__ == "__main__":
    extract_start = 0
    extract_finish = 0
    audio_start = 0
    audio_finish = 0
    video_start = 0
    video_finish = 0
    chat_start = 0
    chat_finish = 0

    start = time.perf_counter()
    streamProcess('https://www.youtube.com/watch?v=gdZLi9oWNZg')
    finish = time.perf_counter()

    print(f'Extract Finished in {round(extract_finish - extract_start, 2)} second(s)')
    print(f'Audio Finished in {round(audio_finish - audio_start, 2)} second(s)')
    print(f'Video Finished in {round(video_finish - video_start, 2)} second(s)')
    print(f'Chat Finished in {round(chat_finish - chat_start, 2)} second(s)')
    print('audio start time : ', audio_start, ",  chat start time : ", chat_start)
    print(f'Finished in {round(finish - start, 2)} second(s)')
