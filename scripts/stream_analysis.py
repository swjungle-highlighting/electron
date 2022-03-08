# -*- encoding: utf-8 -*-

from api.extract.streamExtract import streamProcess
import sys
import json

sys.stderr = sys.stdout

if __name__ == '__main__':
    print('run')
    result = streamProcess(sys.argv[1])
    print(json.dumps(result))