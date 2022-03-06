import os

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
    output_file = 'HIGHLIGHT_' + str(index) + '_' + memo + input_file
    input_path = '"' + os.getcwd() + '/../' + input_file + '"'
    output_path = '"' + os.getcwd() + '/../' + output_file + '"'
    ffmpeg_call = ["ffmpeg -ss", _sec_to_str(start), "-to", _sec_to_str(end),  "-i", input_path, "-c copy", output_path]
    os.system(" ".join(ffmpeg_call))

input_file = input('분할할 영상파일의 이름을 입력하세요 : ')

chat_file = open('./user_query.txt', "r", encoding = 'UTF8')
target = chat_file.readline().rstrip()
index = 1
while target : 
    start, next = _cut_time_and_messageset(target)
    end, memo = _cut_time_and_messageset(next + '_')
    cut_video(input_file, index, int(start), int(end), memo)
    index += 1
    target = chat_file.readline().rstrip()
chat_file.close()