import sys
import os
import time
import json
import sqlite3
import urllib2
from bs4 import BeautifulSoup
import telepot


configFile = "./config.json"


# Retrieve extracted numbers from website
def getExtractNumbers(url):

    numbers = []

    # Get page from url
    try:
        resp = urllib2.urlopen(url)
    except urllib2.URLErrro, err:
        sys.stderr.write("URLError " + str(err.reason) + "\n")
        sys.exit(1)

    soup = BeautifulSoup(resp, 'html.parser')

    # print soup.prettify() # For debug

    # Estrae la data
    date = soup.find('input', {'id': 'datepicker'}).get('value')
    todate = time.strftime("%d/%m/%Y")

    if date != todate:
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


# Load json config file
def loadJson():
    with open(configFile) as json_file:
        jsonData = json.load(json_file)
    return jsonData
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


# send message to junabot
def sendMessage(bot_token, usr_id, message):
    try:
        bot = telepot.Bot(bot_token)
        bot.sendMessage(usr_id, message)
    except telepot.exception.TelegramError as ex:
        print("Error: " + ex[0])
###


# create db
def createDB(db):

    # QUERY
    query = """
        CREATE TABLE IF NOT EXISTS nums(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        data    TIMESTAMP   NOT NULL,
        num1    INT NOT NULL,
        num2    INT NOT NULL,
        num3    INT NOT NULL,
        num4    INT NOT NULL,
        num5    INT NOT NULL,
        num6    INT NOT NULL,
        num7    INT NOT NULL,
        num8    INT NOT NULL,
        num9    INT NOT NULL,
        num10    INT NOT NULL,
        num11    INT NOT NULL,
        num12    INT NOT NULL,
        num13    INT NOT NULL,
        num14    INT NOT NULL,
        num15    INT NOT NULL,
        num16    INT NOT NULL,
        num17    INT NOT NULL,
        num18    INT NOT NULL,
        num19    INT NOT NULL,
        num20    INT NOT NULL
        );
    """

    try:
        db_conn = sqlite3.connect(db)
        db_cur = db_conn.cursor()
        db_cur.execute(query)
        db_conn.commit()
        db_conn.close()
    except sqlite3.Error as sql_err:
            print "Error exec query: %s" % (sql_err)
###


# insert nums in db
def insertNumsDB(numbers, db):

    # query
    query = """
    INSERT INTO nums (data,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11,num12,num13,num14,num15,num16,num17,num18,num19,num20)
    VALUES (date('now'),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    """

    
###


# main
def main():
    json = loadJson()

    extractNums = getExtractNumbers(json['url'])
    playedNums = json['numbers']

    # Create db if not exists
    if not os.path.isfile(json['database']):
        createDB(json['database'])

    if extractNums is not None:
        (numbers, goldNum) = compareNumbers(extractNums, playedNums)

        # Costruzione del messaggio
        message = "\nNumeri estratti: " + str(extractNums) + "\n"
        message += "Numeri giocati: " + str(playedNums) + "\n"
        message += "=======================================\n"
        message += "<*> Numeri individuati: " + str(numbers) + "\n"
        message += "<*> Numero oro: " + str(goldNum) + "\n"
        message += "=======================================\n"

        sendMessage(json['bot_token'], json['seba_id'], message)
#####
if __name__ == '__main__':
    main()
