import requests
import json
from random import choice
import random


class CatFact(object):
    def __init__(self, app_id, rest_key, class_name):
        self.class_name = class_name
        self.post_headers = {
                        "X-Parse-Application-Id": app_id,
                        "X-Parse-REST-API-Key": rest_key,
                        "Content-Type": "application/json" }
        self.get_headers = {
                        "X-Parse-Application-Id": app_id,
                        "X-Parse-REST-API-Key": rest_key }
        self.url = "https://api.parse.com/1/classes/%s" % self.class_name
        self.inc_url = "https://api.parse.com/1/classes/counterclass"
        self.phone_url = "https://api.parse.com/1/classes/phoneclass"

    def add_fact(self, content):
        headers = self.post_headers
        data = {"content": content}
        r = requests.post(self.url, data=json.dumps(data), headers=headers)
        return json.loads(r.content)

    def del_fact(self, factid):
        pass

    def get_fact(self, factid):
        headers = self.get_headers
        url = self.url + '/%s' % factid
        r = requests.get(url, headers=headers)
        return json.loads(r.content)
        
    def increment(self):
        headers = self.post_headers
        url = self.inc_url
        data = {"numfacts": {"__op": "Increment", "amount": 1}}
        r = requests.put(url, data=json.dumps(data), headers=headers)
        return r.status_code

    def get_random(self):
        headers = self.get_headers
        r = requests.get(self.url, headers=headers)
        crap = json.loads(r.content)['results']
        poo = random.choice(crap)
        pooId = poo['objectId']
        content = self.get_fact(pooId)
        return content

    def add_number(self, number):
        headers = self.post_headers
        url = self.phone_url
        data = {"number": number}
        r = requests.put(url, data=json.dumps(data), headers=headers)
        return json.loads(r.content)

    def get_numbers(self):
        headers = self.get_headers
        url = self.phone_url
        nums = []
        r = requests.get(url, headers=headers)
        for n in json.loads(r.content)['response']:
            nums.append(n['number'])
        return nums


if __name__ == '__main__':
    app_id = 'jz5Wqcm027Rm4be5WSivaUwKXOGeUJhdSR5DRZ1Y'
    rest_key = '0VhiHy7cNeN2H83LhapPo6ELBKleBzUPNx97Nun2'
    class_name = 'catfacts'
    cat = CatFact(app_id, rest_key, class_name)
    print cat.get_random()
