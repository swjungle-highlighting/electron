# -*- encoding: utf-8 -*-
import sys
import os
import json

sys.stderr = sys.stdout

digit = ['0','1','2','3','4','5','6','7','8','9']
def _cut_time_and_messageset(line) :
    i = 0
    elapsetime = ''
    while line[i] in digit :
        elapsetime += line[i]
        i += 1
    ret = ''
    i += 1
    while i < len(line) :  
        ret += line[i]
        i += 1
    return int(elapsetime), ret

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

def cut_video(input_file, index, start, end, memo) : 
    ext = input_file.split('.')[-1]
    output_file = f'HIGHLIGHT_{str(index)}_{memo}.{ext}'
    input_path = '"' + input_file + '"'
    output_path = '"' + os.getcwd() + '/컷 보관함/' + output_file + '"'
    ffmpeg_call = ["ffmpeg -ss", _sec_to_str(start), "-to", _sec_to_str(end),  "-i", input_path, "-c copy", output_path]
    os.chdir(os.getcwd() + '/resources/app/python/')
    os.system(" ".join(ffmpeg_call))
    os.chdir(os.getcwd() + '/../../../')

if __name__ == '__main__':
    input_file = sys.argv[1]
    cuts = sys.argv[2].split('[cut]')[1:]

    if not os.path.exists('./컷 보관함') : 
        os.mkdir('./컷 보관함')

    index = 0
    for cut in cuts : 
        index += 1
        start, next = _cut_time_and_messageset(cut)
        end, memo = _cut_time_and_messageset(next)
        print(start, end, memo)
        cut_video(input_file, index, int(start), int(end), memo)

    ret = {
            "result" : "success"
        }
    print(json.dumps(ret))