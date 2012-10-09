#! /usr/bin/env python

""" Stock Tool """

import urllib2, optparse
from threading import Thread

try:
  from bs4 import BeautifulSoup
except ImportError:
  print ("Could not import BeautifulSoup. "+
        "Try sourcing your bash_profile for the correct python executable")
  exit()

__version__ = '0.0.1'
DEBUG = False

BASE_URL = "http://www.google.com/finance?q="

class Stock(Thread):
  def __init__(self, symbol):
    Thread.__init__(self)
    self.symbol     = symbol
    self.price      = ""
    self.change     = ""
    self.change_pct = ""

  def run(self):
    url = BASE_URL+self.symbol
    try:
      soup = BeautifulSoup(urllib2.urlopen(url))
    except urllib2.URLError:
      self.price      = "--"
      self.change     = "--"
      self.change_pct = "--"
      return

    self.price = soup.find("span", {"class":"pr"}).get_text().strip()

    changes = soup.find("span", {"class":"ch"}).find_all("span")
    self.change = changes[0].get_text().strip()
    self.change_pct = changes[1].get_text().strip()

  def __str__(self):
    return "%6s %10s %9s %9s" % (
        self.symbol.ljust(6),
        self.price.rjust(10),
        self.change.rjust(9), 
        self.change_pct.rjust(9)
      )


class Portfolio():
  def __init__(self, filename):
    self.filename = filename
    self.stocks = []

    self.initializeFromFile()
    self.fetchAll()
    self.printAll()

  def initializeFromFile(self):
    f = open(self.filename)
    lines = f.readlines()
    f.close()

    for line in lines:
      self.stocks.append(Stock(line.strip()))

  def fetchAll(self):
    for stock in self.stocks:
      stock.start()

  def printAll(self):
    for stock in self.stocks:
      stock.join()
    for stock in self.stocks:
      print stock

def main():

  usage = "usage: %prog [options] tickerfile"
  parser = optparse.OptionParser(usage=usage, version="%prog "+__version__)

  parser.add_option("-d", "--debug", action="store_true", dest="debug",
                    default=False, help="debug mode")

  (options, args) = parser.parse_args()

  if len(args) < 1:
    parser.error("missing tickerfile")

  tickerfile = args[0]
  DEBUG = options.debug

  Portfolio(tickerfile)

if __name__ == '__main__':
  main()
