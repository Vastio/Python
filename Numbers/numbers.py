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
import smtplib, imaplib, email.utils
from email.mime.text import MIMEText
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

    if date == todate :
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
## Estrae i nuovi numeri giocati
## e li salva nel file di configurazione
def extractNewNumbersFromMail(mailFrom, debug) :

    new_numbers= []

    # server setting
    try :
        imap = imaplib.IMAP4_SSL(mailFrom['server'], 993)
        imap.login(mailFrom['username'], mailFrom['password'])

        # Select INBOX e setting readonly
        imap.select('INBOX')

        typ, msg_id = imap.search(None, '(SUBJECT "[New Numbers]")')

        if debug : print typ, msg_id

        if len(msg_id[0]) != 0 :
            part, msg_data = imap.fetch(msg_id[0], '(BODY.PEEK[TEXT])')

            # Sign the message to be deleted
            imap.store(msg_id[0], '+FLAGS', '\\Deleted')

            for response_part in msg_data:
                if isinstance(response_part, tuple):

                    # Estrae i numeri dalla stringa
                    for num in response_part[1].split(',') :
                        new_numbers.append(int(num))

                    if debug : print "New numbers: ", new_numbers
            # Really delete the message.
            typ, response = imap.expunge()
            if debug : print typ, 'Message deleted: ', response
        else :
            if debug : print "No new numbers found in mailbox"
    except imaplib.IMAP4.error, err :
        print "Imap error: " + str(err)

    imap.logout()

    # Append numbers in config.json file
    if new_numbers :
        dict_num = {'numbers' : new_numbers}
        with open('config.json') as f:
            data = json.load(f)

        data.update(dict_num)

        with open('config.json', 'w') as f:
            json.dump(data, f)
##



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
