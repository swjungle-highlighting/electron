# -*- coding: UTF-8 -*-
'''
@Project ：youtube_highlight_extract 
@File ：streamExtract.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-02-09 오후 12:30 
'''
import multiprocessing
import os
import subprocess
import locale
import yt_dlp
import time

from api.audio.audioProcess import audioProcess
from api.video.videoProcess import videoProcess
from api.chat.chatProcess import chatProcess

from api.extract.spriteExtract import make_sprite

def _sec_to_str(sec) :
    t = []
    t.append(sec %60)
    t.append((sec %3600 -t[0])//60)
    t.append(sec //3600)
    for i in range(3) :
        if t[i] < 10 :
            t[i] = '0'+str(t[i])
        else :
            t[i] = str(t[i])
    return t[2]+':'+t[1]+':'+t[0]

digit = ['0','1','2','3','4','5','6','7','8','9']
def _cut_time_and_messageset(line) :
    i = 0
    elapsetime = ''
    while line[i] in digit :
        elapsetime += line[i]
        i += 1
    return int(elapsetime), line[i+1:]

CUT_RANGE = 600
def _do_subprocess(input_file, duration, index, audio, video) :
    output_file = str(index) + input_file
    start = index * CUT_RANGE
    end = min(duration, (index+1) * CUT_RANGE)
    ffmpeg_call = ["ffmpeg -ss", _sec_to_str(start), "-to", _sec_to_str(end),  "-i", input_file, "-c copy", output_file]
    subprocess.check_output(" ".join(ffmpeg_call), stderr=subprocess.STDOUT)
    audio += audioProcess(output_file)
    video += videoProcess(output_file)
    os.remove(os.getcwd() + "/" + output_file)

def _check_platform(url) : 
    if url[:32] == "https://www.youtube.com/watch?v=" : 
        return 1, url[32:]
    if url[:29] == "https://www.twitch.tv/videos/" : 
        return 2, url[29:]
    return 0, None


def mulitProcessing(input_file, duration, index, audio, video ,CUT_RANGE):
    while index <= duration // CUT_RANGE:
        _do_subprocess(input_file, duration, index, audio, video)
        index += 1

opts = {
    'ignoreerrors' : True,
    'nooverwrites' : True,
    'format' : 'worstvideo[height<=144]+worstaudio/worst[height<=144]/worst',
    'outtmpl' : './%(id)s.%(ext)s',
}
err = {
    'message' : 'error'
}

def streamProcess(url) :
    code, url_id = _check_platform(url)
    if not url_id : 
        return err
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        duration = info_dict.get('duration', None)
        title = info_dict.get('title')
        thumbnail = info_dict.get('thumbnail')

    audio = []
    video = []
    input_file = url_id + '.mp4'
    if code == 2 : 
        input_file = 'v' + input_file
    index = 0

    pool = multiprocessing.Pool(processes=1)
    chat = pool.starmap_async(chatProcess, [(url_id, duration, code)])
    mulitProcessing(input_file, duration, index, audio, video, CUT_RANGE)
    make_sprite(input_file)

    chat = chat.get()[0]
    pool.close()
    pool.join()


    folder = os.getcwd()
    target = ''
    for filename in os.listdir(folder + '/'):
        if url_id in filename:
            target = filename

    os.remove(folder + '/' + target)

    return {
            'audio' : audio,
            'video' : video,
            'chat' : chat,
            'title' : title,
            'thumbnail' : thumbnail,
            'duration' : duration
            }