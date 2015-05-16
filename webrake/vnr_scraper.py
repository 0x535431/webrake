
import urllib.request
import urllib.parse
import bs4
#from bs4 import BeautifulSoup
from setuptools.compat import unicode

__author__ = 'toor'


class Vnr(object):
    'A way of getting price info out of html data'

    version = '0.1'             # class variable

    def __init__(self, vnr):
        self.vnr = vnr


    def fuck(self):
        print("FUCK")

    def get_price(self):
        '''
        Used to get the price in the vnr.
        :return: price as int
        '''
        self.logger.info('Hi, bar')
        soup = gethtml(self.vnr)

        item = soup.find("div", {"class":"price"})
        #print(type(item), item)
        extracted_price = item.b.contents[0]

        extracted_price = extracted_price.encode("utf-8", "strict")
        extracted_price = extracted_price.decode("utf-8")

        # Converts the dirty string "1.234 kr." to clean price string. "1234"
        price_string = extracted_price.replace(".", "").replace("kr", "")
        print(price_string)
        return int(price_string)

def gethtml(vnr_url):
    # Builds the request from the weblink
    request = urllib.request.Request(vnr_url)

    # Adding charset parameter to the Content-Type header.
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    request.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0")

    # Performs the request and saves the BeautifulSoup-object
    soup = doRequest(request)

    return soup

def doRequest(request):
    requestResult = urllib.request.urlopen(request)
    soup = bs4.BeautifulSoup(requestResult, from_encoding='utf8')
    return soup

if __name__ == '__main__':

    bob = Vnr("http://www.hagkaup.is/vorur/vnr/13749")
    bob.get_price()
    shit = Vnr("http://www.hagkaup.is/vorur/vnr/74")
    shit.get_price()
    fuck = Vnr("http://www.hagkaup.is/vorur/vnr/24216")
    fuck.get_price()
