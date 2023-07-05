import datetime
import json
import os


def log(args: dict, result):
    path = 'datas\\log.json'
    # flatten
    result = list(map(lambda x: x[0], result))

    args.update(result=result, timestamp=datetime.datetime.today().__str__())
    with open(path, 'a') as f:
        json.dump(args, f, indent=4)
        f.write('\n')
