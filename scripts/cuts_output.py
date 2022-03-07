# -*- encoding: utf-8 -*-
import sys
import json

sys.stderr = sys.stdout


if __name__ == '__main__':
    file = sys.argv[1]
    cuts = sys.argv[2]


    ret = {
            "result" : "success"
        }
    print(json.dumps(ret))