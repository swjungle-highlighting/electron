# -*- coding: UTF-8 -*-
'''
@Project ：youtube_highlight_extract 
@File ：videoProcess.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-02-09 오후 6:38 
'''

import os
import ffmpeg
import numpy


W, H = 128, 72
FPS = 10
DIFF_CUTLINE = 5000000


def videoProcess(url_id):
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

    return VideoDATA_3600perHOUR