import os
import sys
sys.stderr = sys.stdout

def call(url_id) : 
    print(os.getcwd())
    dl_call = ["twitch-dl", f"download -q 160p30 {url_id} --output {url_id}.mp4"]
    os.chdir(os.getcwd() + '/python/Scripts/')
    os.system(" ".join(dl_call))
    os.chdir(os.getcwd() + '/../../')

if __name__ == '__main__':
    print(11111111112)
    url_id = '1416989028'
    call(url_id)
    print(1111111111)