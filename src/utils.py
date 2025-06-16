import os
import json


def save_json(filedir, filename, jsondata):
    os.makedirs(filedir, exist_ok=True)
    with open(os.path.join(filedir, filename), "w", encoding="utf-8") as f:
        f.write(json.dumps(jsondata))
