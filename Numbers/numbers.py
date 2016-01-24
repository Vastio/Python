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
import argparse, json, urllib2, re
import smtplib, imaplib, email.utils
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


#----------------
# Define Version
#----------------
__version__ = 'v0.3'



#------------
# Globa Vars
#------------
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
def extractNewNumbersFromMail(mailFrom) :

    new_numbers= []

    # server setting
    try :
        imap = imaplib.IMAP4_SSL(mailFrom['server'], 993)
        imap.login(mailFrom['username'], mailFrom['password'])

        # Select INBOX e setting readonly
        imap.select('INBOX')

        typ, msg_id = imap.search(None, '(SUBJECT "[New Numbers]")')

        if len(msg_id[0]) != 0 :
            part, msg_data = imap.fetch(msg_id[0], '(BODY.PEEK[TEXT])')

            # Sign the message to be deleted
            imap.store(msg_id[0], '+FLAGS', '\\Deleted')

            for response_part in msg_data:
                if isinstance(response_part, tuple):

                    # Estrae i numeri dalla stringa
                    for num in response_part[1].split(',') :
                        new_numbers.append(int(num))

            # Really delete the message.
            typ, response = imap.expunge()
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
## Aggiunge una nuova mail al file di configurazione
def addNewMail(new_mail) :

    mail_list = {'mailTo' : []}

    try :
        json_data = None
        # Apre il file config.json in lettura
        with open(config_file, 'r') as j_file :
            json_data = json.load(j_file)

            # Aggiunge la nuova mail se non esiste gia
            if not new_mail in json_data['mailTo'] :
                json_data['mailTo'].append(new_mail)

        # Apre il file in scrittura e scrive il dati cambiati
        with open(config_file, 'w') as j_file :
            j_file.write(json.dumps(json_data))

    except IOError, err :
        print "[!] Error to open config file: %s" % err
        exit(1)
    except ValueError, err :
		print "[!] Error in json file: %s" % err
		exit(1)
##



#
## Send result via mail
def send_mail(mess, mail) :

    message = MIMEText(mess)
    message['To'] = email.utils.formataddr(('Recipient', mail))
    message['From'] = email.utils.formataddr(('Author', 'number@gmail.com'))
    message['Subject'] = "[10 e lotto results]"

    try :
        server = smtplib.SMTP('127.0.0.1')
    except smtplib.SMTPConnectError, err :
        print "[!] Error SMTP connection: " + err

    try:
        server.sendmail('number@gmail.com', [mail], message.as_string())
    finally:
        server.quit()
##



#
## MAIN
def main() :

     # Command line arguments
    parser = argparse.ArgumentParser(description="Compare numbers")
    parser.add_argument('-N', '--numbers', action="store_true", help="extract new numbers from mail and exit.")
    parser.add_argument('-m', '--mail', help="add new mailTo to config file and exit.")
    parser.add_argument('-S', '--sendmail', action="store_true", help="send result via mail (specified in config mail).")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()

    json = loadJson() # Carica i dati da json

     # Aggiunge unsa nuova mail al file di configurazione
    if args.mail :
        addNewMail(args.mail)
        sys.exit(1)

    extractNewNumbersFromMail(json['mailFrom'])

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
    message += "===========================================\n"

    if args.sendmail :
        for mail in json['mailTo'] :
            send_mail(message, mail)
    else :
        print message
###



#####
if __name__ == '__main__':
    main()
