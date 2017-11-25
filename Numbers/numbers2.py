#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    except urllib2.URLErrro as err:
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


# Compare numbers
def compareNumbers(extractNums, playedNums):

    numbers = []

    for num in playedNums:
        if num in extractNums:
            numbers.append(num)

    # Numero oro
    if extractNums[-1] in playedNums:
        goldNum = extractNums[-1]
    else:
        goldNum = 0

    return (numbers, goldNum)
###


# MAIN
def main():

    json = loadJson()

    extractNums = getExtractNumbers(json['url'])
    playedNums = json['numbers']

    if extractNums is not None:
        (numbers, goldNum) = compareNumbers(extractNums, playedNums)

        # Costruzione del messaggio
        message = "\nNumeri estratti: " + str(extractNums) + "\n"
        message += "Numeri giocati: " + str(playedNums) + "\n"
        message += "=======================================\n"
        message += "<*> Numeri individuati: " + str(numbers) + "\n"
        message += "<*> Numero oro: " + str(goldNum) + "\n"
        message += "=======================================\n"

        print(message)
###


if __name__ == '__main__':
    main()
