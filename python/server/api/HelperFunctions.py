from collections import deque
import os
import zipfile
import json

##################################################################################
## parse elapsetime and chatdata from /chat_storage textfile
digit = ['0','1','2','3','4','5','6','7','8','9']
def _cut_time_and_messageset(line) :
    i = 0
    elapsetime = ''
    while line[i] in digit :
        elapsetime += line[i]
        i += 1
    return int(elapsetime), line[i+1:]

##################################################################################
## return dict(JSON) type MessageSet for front from /chat_storage textfile
def return_MessageSet(URL_ID) : 
    MessageSet = {}
    chat_file = open('./chat_storage/'+URL_ID+'.txt', "r", encoding = 'UTF8')
    _1, _2 = _cut_time_and_messageset(chat_file.readline().rstrip())
    target = chat_file.readline().rstrip()
    i = 0
    while target : 
        second, message = _cut_time_and_messageset(target)
        MessageSet[second] = _str_to_list(message)
        i += 1
        target = chat_file.readline().rstrip()
    chat_file.close()
    return MessageSet

def _str_to_list(message) :
    return message[2:len(message)-2].split("', '")

##################################################################################
## aho-corasick class for keywords seach
class NODE(dict) :
    
        def __init__(self) :
            self.final = False
            self.out = set()
            self.fail = None
            
        def addout(self, out) :
            if type(out) is set :
                self.out = self.out.union(out)
            else  :
                self.out.add(out)
        
        def addchild(self, alphabet, node = None) :
            self[alphabet] = NODE() if node is None else node

class AhoCorasick() :      
    def __init__(self, PATTERN_LIST) :
        self.PATTERN_LIST = PATTERN_LIST
        self.head = NODE()      
        self.makeTrie()
        self.makeFailure()
        
    def search(self, TARGET) :
        now = self.head
        ret = []
        for letter in TARGET  :
            while now is not self.head and letter not in now :
                now = now.fail
            if letter in now :
                now = now[letter]           
            if now.final :
                ret.extend(list(now.out))
        return ret
    
    def makeTrie(self) :
        for pattern in self.PATTERN_LIST :
            now = self.head
            for letter in pattern  :
                if letter not in now :
                    now.addchild(letter)
                now = now[letter]
            now.final = True
            now.addout(pattern)
            
    def makeFailure(self) :
        que = deque()
        self.head.fail = self.head
        que.append(self.head)
        while que :
            now = que.popleft()
            for next in now :
                child = now[next]
                
                if now is self.head :
                    child.fail = self.head
                else  :
                    f = now.fail
                    while f is not self.head and next not in f :
                        f = f.fail
                    if next in f :
                        f = f[next]
                    child.fail = f                
                child.addout(child.fail.out)
                child.final |= child.fail.final     
                que.append(child)

##################################################################################
## make textfile and zipfile for download cutting tool
def _make_textfile(bookmarks, count) : 
    path = f'./api/download_logic/user_query{count}.txt'
    chat_file = open(path, "w", encoding = 'UTF8')
    for start, end, memo in bookmarks :
        chat_file.writelines(str(start) + ' ' + str(end) + ' ' + memo + '\n')
    chat_file.close()

def _make_zipfile() : 
    root = os.getcwd()
    target = root + '/build/exe.win-amd64-3.7'
    os.chdir(target)
    zip_file = zipfile.ZipFile('../../HIGHLIGHTING.zip', 'w')
    for (path, dir, files) in os.walk(target) : 
        for file in files : 
            zip_file.write(os.path.join(os.path.relpath(path, target), file), compress_type = zipfile.ZIP_DEFLATED)
    zip_file.close()
    os.chdir(root)

##################################################################################
## return dict(JSON) type Bookmarks from /bookmarker_storage JSONfile
def _get_bookmarker(URL_ID):
    path = './bookmarker_storage/' + URL_ID + '.json'
    with open(path, 'r', encoding="UTF-8") as fp:
        return json.load(fp)

##################################################################################
## parse memo, start, end from bookmark json
def _get_memo_and_timePointer(bookmark) : 
    left = bookmark.split("'text': '")[1]
    memo, i = '', 0 
    while left[i] != "'" : 
        memo += left[i]
        i += 1
    startPointer, left = _cut_time_and_messageset(left.split("startPointer': ")[1])
    endPointer, left = _cut_time_and_messageset(left.split("endPointer': ")[1])
    return memo, startPointer, endPointer

def _parse_bookmarker(bookmarks_str) : 
    bookmarks = bookmarks_str[2:len(bookmarks_str)-2].split('}, {')
    ret = []
    for b in bookmarks : 
        memo, startPointer, endPointer = _get_memo_and_timePointer(b)
        ret.append([startPointer, endPointer, memo])
    return ret