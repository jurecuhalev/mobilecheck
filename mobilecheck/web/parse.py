from BeautifulSoup import BeautifulSoup


def main():  
  soup = BeautifulSoup(open('../../samples/sample1.xls', 'rb').read())
  for i in soup.findAll('td'):
    print i.encode('utf8')
  
  

if __name__ == '__main__':
  main()