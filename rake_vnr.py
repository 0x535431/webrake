#!/usr/bin/env python

__author__ = 'toor'

from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import datetime

post = {}
s = requests.session()



# hk_vnr_price_checker.
def vnr_price(vnr):
    print("hello")




def extract_data(page):
    data = []
    html = s.post(page)
    soup = BeautifulSoup(html.text)

    item = soup.findAll("div", {"class":"item"})
    for i, x in enumerate(item):
        post = {"store": "hagkaup",
                "title": x['title'],
                "_id": x['data-prid'],
                "price": (x.b.string),
                "tags": page.replace("http://www.hagkaup.is/vorur/", "").replace("/", " ").split(),
                "vnr":(x.a['href']),
                "date": datetime.datetime.utcnow(),
                }
        #print post
        data.append(post)

    return data


def test():
    html_pages = ["http://www.hagkaup.is/vorur/matvara/barnamatur"]

    for html_page in html_pages:
        s.get(html_page)
        data = extract_data(html_page)

        client = MongoClient('localhost', 27017)
        db = client['hagkaup']
        collection = db['gosdrykkir']
        for x in data:
            try:
                collection.insert_one(x)
                #print x
            except:
                collection.update({'_id':x["_id"]},x)
                print("DOCUMENT ALREADY EXITS")
    '''assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWog")
    assert data["viewstate"].startswith("/wEPDwULLTE")
    '''
