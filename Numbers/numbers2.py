import sys
import time
import json
import urllib2
from bs4 import BeautifulSoup


configFile = "./config.json"


# Load json config file
def loadJson():
    with open(configFile) as json_file:
        jsonData = json.load(json_file)
    return jsonData
###


# Recupera i numeri al sito specificato nel config.json file
def getExtractNumbers(url):

    numbers = []

    # Get page from url
    try:
        resp = urllib2.urlopen(url)
    except urllib2.URLErrro, err:
        sys.stderr.write("URLError " + str(err.reason) + "\n")
        sys.exit(1)

    soup = BeautifulSoup(resp, 'html.parser')

    # print(soup.prettify()) # For debug

    # Estrae la data
    date = soup.find('input', {'id': 'datepicker'}).get('value')
    todate = time.strftime("%d/%m/%Y")

    if date == todate:
        return None
    else:
        # Estrae i 20 numeri
        for num in soup.find_all('div', class_='ball'):
            numbers.append(int(num.string))

        # Estrae il numero oro
        num = soup.find('div', class_='value_goldnumber')
        if (num):
            numbers.append(int(num.string))

    return numbers
###


# MAIN
def main():

    json = loadJson()

    extractNums = getExtractNumbers(json['url'])
    print(extractNums)
###


if __name__ == '__main__':
    main()
