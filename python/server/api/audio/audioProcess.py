# -*- coding: UTF-8 -*-
'''
@Project ：youtube_highlight_extract 
@File ：audioProcess.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-02-09 오후 6:37 
'''

import os
import numpy
import ffmpeg


SAMPLERATE = 11025
GETPICK_PERSEC = 2

def audioProcess(url_id):
    # print("########################################################")
    # print('audio ' + url_id)
    # print("########################################################")
    """"""

    folder = os.getcwd()
    target = ''
    for filename in os.listdir(folder+'/'):
        if url_id in filename:
            target = filename

    out, err = (
        ffmpeg
            .input(folder+'/'+target)
            .output('-', format='f32le', acodec='pcm_f32le', ac=1, ar=str(SAMPLERATE))
            .run(capture_stdout=True)
    )

    amplitudes = numpy.frombuffer(out, numpy.float32)

    AudioPick_7200perHOUR = []

    persec = SAMPLERATE // GETPICK_PERSEC
    pick, dirr = 0, 1
    for i in range(1, len(amplitudes)) :
        if not i %persec :
            AudioPick_7200perHOUR.append(int(1000 *pick) *dirr)
            pick = 0
            dirr = -dirr
        pick = max(pick, abs(amplitudes[i]))

    return AudioPick_7200perHOUR

    """"""