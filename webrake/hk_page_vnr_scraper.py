__author__ = 'toor'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the approprate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function

from pymongo import MongoClient
import bs4
import requests
import datetime

from logbook import Logger
from logbook import FileHandler

log_handler = FileHandler('hk_page.log')
log_handler.push_application()
log = Logger('hk_page_logger')

post = {}
s = requests.session()


def extract_data(page):
    data = []
    html = s.post(page)
    soup = bs4.BeautifulSoup(html.text)

    item = soup.findAll("div", {"class":"item"})
    for i, x in enumerate(item):
        post = {"store": "hagkaup",
                "title": x['title'],
                "_id": x['data-prid'],
                "price": get_numbers((x.b.string)),
                "tags": page.replace("http://www.hagkaup.is/vorur/", "").replace("/", " ").split(),
                "vnr":(get_numbers(x.a['href'])),
                "date": datetime.datetime.utcnow(),
                }
        print(post)
        data.append(post)

    return data

def get_numbers(path):
    true_vnr = ""
    for x in path:
        if(x.isdigit()):
            true_vnr = true_vnr + x
    return int(true_vnr)



def test():
    '''
    html_pages = ["http://www.hagkaup.is/vorur/matvara/drykkir/gosdrykkir",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/orkudrykkir",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/pilsner",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/safar",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/vatn",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/thykkni"]
                  STRIP FOR TEST
                  "http://www.hagkaup.is/vorur/matvara/snakk",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/gosdrykkir",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/orkudrykkir",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/pilsner",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/safar",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/vatn",
                  "http://www.hagkaup.is/vorur/matvara/drykkir/thykkni",
                  "http://www.hagkaup.is/vorur/matvara/avextir/ferskt",
                  "http://www.hagkaup.is/vorur/matvara/avextir/frosid",
                  "http://www.hagkaup.is/vorur/matvara/bakkelsi",
    '''
    html_pages = ["http://www.hagkaup.is/vorur/matvara/barnamatur/barnamauk",
                  "http://www.hagkaup.is/vorur/matvara/barnamatur/barnaolia",
                  "http://www.hagkaup.is/vorur/matvara/barnamatur/grautur",
                  "http://www.hagkaup.is/vorur/matvara/barnamatur/safi",
                  "http://www.hagkaup.is/vorur/matvara/barnamatur/thurrmjolk",
                  "http://www.hagkaup.is/vorur/matvara/braudmeti",
                  "http://www.hagkaup.is/vorur/matvara/graenmeti/ferskt",
                  "http://www.hagkaup.is/vorur/matvara/graenmeti/frosid",
                  "http://www.hagkaup.is/vorur/matvara/avextir/frosid",
                  "http://www.hagkaup.is/vorur/matvara/avextir/ferskt",
                  "http://www.hagkaup.is/vorur/matvara/alegg",
                  "http://www.hagkaup.is/vorur/matvara/grunnvorur",
                  "http://www.hagkaup.is/vorur/matvara/baetiefni-og-vitamin/baetiefni",
                  "http://www.hagkaup.is/vorur/matvara/baetiefni-og-vitamin/vitamin",
                  "http://www.hagkaup.is/vorur/matvara/kex-og-kokur/kokur",
                  "http://www.hagkaup.is/vorur/matvara/kex-og-kokur/kex",
                  "http://www.hagkaup.is/vorur/matvara/kaffi",
                  "http://www.hagkaup.is/vorur/matvara/hnetur-og-frae",
                  "http://www.hagkaup.is/vorur/matvara/kjotvorur",
                  "http://www.hagkaup.is/vorur/matvara/krydd",
                  "http://www.hagkaup.is/vorur/matvara/lifraent",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/jogurt",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/mjolk",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/ostur",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/rjomi",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/skyr",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/smjor-og-vidbit",
                  "http://www.hagkaup.is/vorur/matvara/mexikoskur-matur",
                  "http://www.hagkaup.is/vorur/matvara/morgunmatur",
                  "http://www.hagkaup.is/vorur/matvara/nudlur-og-hrisgrjon",
                  "http://www.hagkaup.is/vorur/matvara/oliur",
                  "http://www.hagkaup.is/vorur/matvara/pasta",
                  "http://www.hagkaup.is/vorur/matvara/nidursodid",
                  "http://www.hagkaup.is/vorur/matvara/sjavarfang",
                  "http://www.hagkaup.is/vorur/matvara/snakk",
                  "http://www.hagkaup.is/vorur/matvara/sosur-og-chutney",
                  "http://www.hagkaup.is/vorur/matvara/sultur",
                  "http://www.hagkaup.is/vorur/matvara/supur",
                  "http://www.hagkaup.is/vorur/matvara/te",
                  "http://www.hagkaup.is/vorur/matvara/thurrkadir-avextir",
                  "http://www.hagkaup.is/vorur/matvara/tilbunir-rettir",
                  "http://www.hagkaup.is/vorur/matvara/tilbunir-eftirrettir",
                  "http://www.hagkaup.is/vorur/matvara/tilbuin-salot",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/tyggjo",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/sukkuladi",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/lakkris",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/konfekt",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/karamellur",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/hlaup",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/brjostsykur",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/blandad"
                  ]
    '''


                  "http://www.hagkaup.is/vorur/matvara/hnetur-og-frae",

                  ,


                  "http://www.hagkaup.is/vorur/matvara/kaffi",
                  "http://www.hagkaup.is/vorur/matvara/italia",
                  "http://www.hagkaup.is/vorur/matvara/krydd",
                  "http://www.hagkaup.is/vorur/matvara/kjotvorur",
                  "http://www.hagkaup.is/vorur/matvara/kex-og-kokur/kex",
                  "http://www.hagkaup.is/vorur/matvara/kex-og-kokur/kokur",
                  "http://www.hagkaup.is/vorur/matvara/nidursodid",
                  "http://www.hagkaup.is/vorur/matvara/morgunmatur",
                  "http://www.hagkaup.is/vorur/matvara/mexikoskur-matur",
                  "http://www.hagkaup.is/vorur/matvara/lifraent",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/rjomi",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/skyr",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/smjor-og-vidbit",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/ostur",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/mjolk",
                  "http://www.hagkaup.is/vorur/matvara/mjolkurvorur/jogurt",
                  "http://www.hagkaup.is/vorur/matvara/nudlur-og-hrisgrjon",
                  "http://www.hagkaup.is/vorur/matvara/oliur",
                  "http://www.hagkaup.is/vorur/matvara/origami-sushi",
                  "http://www.hagkaup.is/vorur/matvara/pasta",
                  "http://www.hagkaup.is/vorur/matvara/sjavarfang",
                  "http://www.hagkaup.is/vorur/matvara/sosur-og-chutney",
                  "http://www.hagkaup.is/vorur/matvara/sultur",
                  "http://www.hagkaup.is/vorur/matvara/supur",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/lakkris",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/sukkuladi",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/tyggjo",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/konfekt",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/karamellur",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/hlaup",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/brjostsykur",
                  "http://www.hagkaup.is/vorur/matvara/saelgaeti/blandad",
                  "http://www.hagkaup.is/vorur/matvara/thurrkadir-avextir",
                  "http://www.hagkaup.is/vorur/matvara/tilbunir-rettir",
                  "http://www.hagkaup.is/vorur/matvara/tilbunir-eftirrettir",
                  "http://www.hagkaup.is/vorur/matvara/tilbuin-salot",
                  "http://www.hagkaup.is/vorur/matvara/te"]
                  '''

    for html_page in html_pages:
        s.get(html_page)
        data = extract_data(html_page)

        client = MongoClient('localhost', 27017)
        db = client['hagkaup']
        collection = db['scrape1']
        for x in data:
            try:
                collection.update({'_id': x["_id"]}, x, upsert=True)
                print(x)
            except:
                log.warn(("db fail", x))
                print("DOCUMENT ALREADY EXITS")
    '''assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWog")
    assert data["viewstate"].startswith("/wEPDwULLTE")
    '''

test()