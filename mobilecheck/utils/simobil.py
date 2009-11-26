# -*- coding: utf-8 -*-
#!/usr/bin/python

from xml.etree import ElementTree
import sys
import decimal
import datetime
import re

datum_re = re.compile('^(\d{2})\.(\d{2})\.$')
ura_re = re.compile('^(\d{2}):(\d{2})$')
trajanje_re = re.compile('^(?:(\d\d):(\d\d):(\d\d)|(\d+),(\d+)(K|M)B)$')

class ParseError(Exception):
  pass

def xmlparse(f):
  tree = ElementTree.parse(f)
  year = 2009
  entries = list()
  
  for x in tree.findall('.//Zapis'):
    kb = 0.0
    datum = x.find('Datum').text
    ura = x.find('Ura').text
    opis = x.find('Opis').text
    cifra = x.find('Stevilka').text
    operater = x.find('Operater').text
    trajanje = x.find('Trajanje').text
    amount = decimal.Decimal(x.find('EUR').text)
    
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
        
    #print [timestamp, opis, cifra, operater, trajanje, amount]
    
    e = {'timestamp':timestamp, 
         'description': opis, 
         'number': cifra, 
         'provider': operater, 
         'length': trajanje,
         'datakb': kb,
         'amount': amount}
    
    entries.append(e)
  return entries

def get_sms_count(entries):
  sms_counter = 0
  for e in entries:
    if e.get('description') == u'SMS sporo\u010dilo':
      sms_counter += 1
      
  return sms_counter

def get_data(entries):
  data_kb = 0
  for e in entries:
    if e.get('datakb') > 0:
      data_kb += e.get('datakb')
      
  return data_kb
  
def get_klici_stacionarno(entries):
  calls_length = datetime.timedelta(0)
  for e in entries:
    if e.get('description') == 'Klic v stacionarno omr.':
      calls_length = calls_length + e.get('length')
  return calls_length
  
  
def get_klici_simobil(entries):
  calls_length = datetime.timedelta(0)
  for e in entries:
    if e.get('description') == u'Klic v omre\u017eje Si.mobil':
      calls_length = calls_length + e.get('length')
  return calls_length

def get_klici_drugomobilno(entries):
  calls_length = datetime.timedelta(0)
  for e in entries:
    if e.get('description') == 'Klic v drugo mobilno omr.':
      calls_length = calls_length + e.get('length')
  return calls_length

def process(f):
  print f
  entries = xmlparse(f)
  summary = [
  
    {'description': u'Klici v omre\u017eje Si.mobil',
     'value': get_klici_simobil(entries)
    },
  
    {'description': u'Klici v druga mobilna omrežja',
     'value': get_klici_drugomobilno(entries)
    },

    {'description': u'Klici v stacionarna omrežja',
     'value': get_klici_stacionarno(entries)
    },
  
    {'description' : u'Število SMS sporočil',
     'value': get_sms_count(entries)},
    {'description': 'Prenos podatkov (v kb)',
     'value': get_data(entries)}]
  
  
  return summary
  
def main():
  entries = xmlparse(sys.argv[1])
  
  sms_count = get_sms_count(entries)
  data = get_data(entries)
  print "SMS count", sms_count
  print "Data transfer", get_data(entries), 'kb'
  print "Klici other", get_klici_drugo(entries)
  
if __name__ == "__main__":
  main()