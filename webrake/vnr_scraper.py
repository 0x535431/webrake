from pymongo import MongoClient
import pymongo
import datetime

import urllib.parse
import bs4
from bs4 import Comment

import concurrent.futures
import urllib.request

from logbook import Logger
from logbook import FileHandler

log_handler = FileHandler('Vnr_scraper.log')
log_handler.push_application()
log = Logger('My Awesome Logger')

__author__ = 'toor'


class Vnr(object):
    'A way of getting price info out of html data'

    version = '0.1'  # class variable

    def __init__(self, vnr):
        self.vnr = bs4.BeautifulSoup(vnr, from_encoding='utf8')
        self.title = ""
        self.productVnr = 0
        self.productNo = 0
        self.price = 0
        self.productDescriptionShort = ""
        self.productImage = ""
        self.innkaupasvid = ""
        self.trademark = ""
        self.unit = 0
        # Extracting data.
        self.get_data()
        # kg or stk ?
        self.get_unit()

    def fuck(self):
        print("FUCK")

    def get_unit(self):
        '''
        Used to get the unit of the item.
        1 = Stk. 2 = kr / kg
        '''

        try:
            item = self.vnr.find("div", {"class": "price"})
            # print(type(item), item)
            extracted_price = item.b.contents[0]
            # Let's see if we can get info on the kg weight.
            if (len(item.b.contents) == 2):
                self.unit = 2
            else:
                self.unit = 1
                # extracted_price = extracted_price.encode("utf-8", "strict")
                # extracted_price = extracted_price.decode("utf-8")

                # Converts the dirty string "1.234 kr." to clean price string. "1234"
                # price_string = extracted_price.replace(".", "").replace("kr", "")
                # print(price_string)
        except:
            # We should not get here
            log.warn("get_unit fucked up somehow.")

    def get_data(self):
        '''
        Used to get all the data from a vnr lookup page.
        '''

        soup = self.vnr
        item = soup.find("div", {"class": "boxbody"})
        comments = item.findAll(text=lambda text: isinstance(text, Comment), limit=1)

        # ERROR HANDELING FOR BLANK ITEMS.
        if len(comments) == 0:
            log.warn("We got a blank Vnr")
            self.title = "blank"
            return

        product_str = str(comments[0]).split("\n")

        # Let's set the object variables!
        # Price=239 - > ["price", "123"] -> self.price = 123
        for line in product_str:
            line = line.strip()
            line = line.split("=")
            if line[0] in ["eplica-search-index-fields", "SearchType", "ProductType", "Innkaupasvid"]:
                continue

            if "title" == line[0]:
                self.title = line[1]
                continue
            if "ProductID" == line[0]:
                self.productVnr = int(line[1])
                continue
            if "ProductNo" == line[0]:
                self.productNo = int(line[1])
                continue
            if 'Price' == line[0]:
                self.price = int(line[1])
                continue
            if "ProductDescriptionShort" == line[0]:
                line[1] = line[1].replace("<p>", "").replace("</p>", "")
                self.productDescriptionShort = line[1]
                continue
            if line[0] == "ProductImage":
                self.productImage = line[1]
                continue
            if "Trademark" == line[0]:
                self.trademark = line[1]
                continue

            # We should not get here
            log.warn(("get_data(): No match. line:", line))


if __name__ == '__main__':

    def yrange():
        '''
        A generator for vnr numbers to check out.
        :return:
        '''
        client = MongoClient('localhost', 27017)
        db = client['hagkaup']
        collection = db['scrape1']
        result = collection.find({"store": "hagkaup"}, {"vnr": 1, "qty": 1, "_id": 0})
        assert isinstance(result, pymongo.cursor.Cursor)

        for x in result:
            assert isinstance(x, dict)
            x = x.popitem()
            assert isinstance(x, tuple)
            yield "http://www.hagkaup.is/vorur/vnr/" + str(x[1])
        result.close()

    # This is our generator !
    URLS = yrange()
    # FOR TESTING!
    #URLS = ["http://www.hagkaup.is/vorur/vnr/13749", "http://www.hagkaup.is/vorur/vnr/8"]
    url_list = []

    def load_url(url, timeout):
        return urllib.request.urlopen(url, timeout=timeout).read()

    def get_numbers(path):
        true_vnr = ""
        for x in path:
            if (x.isdigit()):
                true_vnr = true_vnr + x
        return int(true_vnr)

    my_client = MongoClient('localhost', 27017)
    database = my_client['hagkaup']
    coll = database['scrape1']

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = dict((executor.submit(load_url, url, 240), url)
                             for url in URLS)

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            if future.exception() is not None:
                print('%r generated an exception: %s' % (url,
                                                         future.exception()))
                log.warn(('%r generated an exception: %s' % (url,future.exception())))
            else:
                if len(future.result()) > 10500:
                    try:
                        #print('%r page is %d bytes' % (url, len(future.result())))
                        # url_list.append(Vnr(future.result()))
                        bob = Vnr(future.result())
                        #print(bob.title)
                        #print(bob.unit)
                        # TEST VERSION OF DB COMS.
                        post = {"store": "hagkaup",
                                "title": bob.title,
                                "_id": bob.productNo,
                                "price": bob.price,
                                "vnr": bob.productVnr,
                                "date": datetime.datetime.utcnow(),
                                "unit": bob.unit,
                                "trademark": bob.trademark}

                        try:
                            coll.update({'_id': post["_id"]}, post, upsert=True)
                            print(post)

                        except:
                            log.warn(("db fail", post))
                            print("Db fuckup!")

                    except:
                        log.warn("url_list.append fail.")
                        print(len(future.result()), "future fuckup.")
