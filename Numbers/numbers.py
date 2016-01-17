#-------------------------------------------------------------------------------
# Name:        numbers
# Purpose:
#
# Author:      s.catalano
#
# Created:     25/09/2015
# Copyright:   (c) s.catalano 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import sys, os, time
import json, urllib2, re
from bs4 import BeautifulSoup

configFile = "./config.json"



#
## Load json config file
def loadJson() :
    with open(configFile) as json_file :
        jsonData = json.load(json_file)
    return jsonData
###


#
## Retrieve extracted numbers from website
def getExtractNumbers(url) :

    numbers = []

    # Get page from url
    try :
        resp = urllib2.urlopen(url)
    except urllib2.URLErrro, err :
        sys.stderr.write("URLError " + str(err.reason) + "\n")
        sys.exit(1)

    soup = BeautifulSoup(resp, 'html.parser')

    #print soup.prettify() # For debug

    # Estrae la data
    date = soup.find('input', {'id': 'datepicker'}).get('value')
    todate = time.strftime("%d/%m/%Y")

    if date != todate :
        return None
    else :
        # Estrae i 20 numeri
        for num in soup.find_all('div', class_='ball') :
            numbers.append(int(num.string))

        # Estrae il numero oro
        num = soup.find('div', class_='value_goldnumber')
        if (num) : numbers.append(int(num.string))

        return numbers
###



#
## Compare numbers
def compareNumbers(extractNums, playedNums) :

    numbers = []

    for num in playedNums :
        if num in extractNums : numbers.append(num)

    # Numero oro
    if extractNums[-1] in playedNums : goldNum = extractNums[-1]
    else : goldNum = 0

    return (numbers, goldNum)
###



#
## MAIN
def main() :
    json = loadJson() # Carica i dati da json

    extractNums = getExtractNumbers(json['url'])
    if extractNums == None :
        sys.exit(0)

    playedNums = json['numbers']

    (numbers, goldNum) = compareNumbers(extractNums, playedNums)

    # Costruzione del messaggio
    message = "\nNumeri estratti: " + str(extractNums) + "\n";
    message += "Numeri giocati: " + str(playedNums) + "\n";
    message += "===========================================\n"
    message += "<*> Numeri individuati: " + str(numbers) + "\n";
    message += "<*> Numero oro: " + str(goldNum) + "\n";

    print message
###



#####
if __name__ == '__main__':
    main()
