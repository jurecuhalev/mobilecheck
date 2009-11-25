#!/usr/bin/python

from xml.etree import ElementTree
import sys
import decimal
import datetime
import re

datum_re = re.compile('^(\d{2})\.(\d{2})\.$')
ura_re = re.compile('^(\d{2}):(\d{2})$')
trajanje_re = re.compile('^(?:(\d\d):(\d\d):(\d\d)|(\d+),(\d+)(K|M)B)$')
year_re = re.compile('^specifikacija_(\d\d)\d+_\d+.xml$')

kb = 0.0

class ParseError(Exception):
  pass

def per_peer(f, cost_per_peer):
  global kb
  #print '#' + '=' *40
  #print '#' + sys.argv[1]
  #print '#' + '-' *40
  
  #m = year_re.match(f)
  #if not m:
  #  raise ParseError("could not find year")
  #year = int('20' + m.group(1))
  year = 2009
  
  tree = ElementTree.parse(f)
  
  for x in tree.findall('.//Zapis'):
    datum = x.find('Datum').text
    ura = x.find('Ura').text
    opis = x.find('Opis').text
    cifra = x.find('Stevilka').text
    operater = x.find('Operater').text
    trajanje = x.find('Trajanje').text
    amount = decimal.Decimal(x.find('EUR').text)
    
    cur_sum, num = cost_per_peer.get((cifra, opis, operater), (decimal.Decimal(),0))
    cost_per_peer[(cifra, opis, operater)] = (cur_sum+amount, num+1)
    #print (datum, ura, opis, cifra, operater, trajanje, amount)
    event_date = map(int, datum_re.match(datum).groups())
    event_time = map(int, ura_re.match(ura).groups())
    
    timestamp = datetime.datetime(year, event_date[1],event_date[0], event_time[0], event_time[1])
    m = trajanje_re.match(trajanje)
    if m:
      t = m.groups()
      if t[3] != None:
        trajanje = float(t[3] + '.' + t[4])
        if t[5] == 'M':
          trajanje = trajanje * 1024
        kb += trajanje # XXX
      else:
        trajanje = datetime.timedelta(0, int(t[0])*3600 + int(t[1])*60 + int(t[2]))
    else:
      # should not get here
      raise ParseError(trajanje)
    
    print [timestamp, opis, cifra, operater, trajanje, amount]
  
  return cost_per_peer

def main():
  cost = {}
  for x in sys.argv[1:]:
    cost = per_peer(x, cost)
  costs = sorted([(v, k) for (k, v) in cost.iteritems()])
  total = sum([i[0] for i in cost.itervalues()])
  for entry in costs[-10:]:
    print '%.1f\t%s\t%s\t%s' % (entry[0][0]/total*100, entry[0][0], entry[0][1], entry[1])
  print '#' + '-' *40
  print 'KB', kb

if __name__ == "__main__":
  main()