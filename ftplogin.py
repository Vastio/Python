#!/usr/bin/env python

import sys
from ftplib import FTP


####
def loginOK(ip) :
	try :
		ftp = FTP(ip)
		ftp.login()
	except Exception :
		return False

	return True
#####


try :
	filename = sys.argv[1]
except IndexError :
	print "\n Usage:  " + sys.argv[0] + " masscan_file\n"
	sys.exit(1)

ip_list = []

try :
	fh = open(filename, 'r')
	
	for line in fh :
		ip = line[12:-11]
		ip_list.append(ip)	
	fh.close()
except IOError :
	print "IO error to open " + filename
	sys.exit(1)

for ip in ip_list :
	if loginOK(ip) : print "[***] Anonymous login OK: %s [***]" % ip
