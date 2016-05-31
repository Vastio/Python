#!/usr/bin/env python

import sys
import time
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


#####
##### MAIN
def main() :
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

	start_time = time.time()
	for ip in ip_list :
		sys.stdout.write("\r Scanning %s" % ip)
		if loginOK(ip) : 
			print "[***] Anonymous login OK: %s [***]" % ip
		else : 
			sys.stdout.flush()
			time.sleep(0.2)
		
	print "\n Scanned %d hosts in %d seconds" % (len(ip_list), (time.time() - start_time))

###########
if __name__ == '__main__':
    main()
