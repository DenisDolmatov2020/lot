import datetime
import requests
import pytz
from rest_framework.utils import json

from lots.models import Lot
from number.models import Number


def choose_winners(lot):
    data_ = [1]
    if lot.players > 1:
        url = 'https://api.random.org/json-rpc/2/invoke'
        json_ = {
            "jsonrpc": "2.0",
            "method": "generateIntegers",
            "params": {
                "apiKey": "fc702e8a-53f0-4dc1-83f2-63c07fb0e835",
                "n": lot.winners,
                "min": 1,
                "max": lot.players,
                "replacement": False
            },
            "id": lot.id
        }
        r = requests.post(url, json=json_)
        json_ = json.loads(r.text)
        print(json_)
        print(json_['result']['random']['completionTime'])
        lot.winners_complete = json_['result']['random']['completionTime']
        data_ = json_['result']['random']['data']

    wins = Number.objects.filter(lot=lot, num__in=data_).update(won=True)
    lot.active = False
    lot.save()
    return wins
