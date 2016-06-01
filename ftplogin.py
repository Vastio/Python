#!/usr/bin/env python

import sys
import time
from ftplib import FTP


####
def loginOK(ip) :

	ftp = FTP()
			
	try :
		ftp.connect(ip, timeout=15)
		ftp.login()
	except Exception :
		ftp.close()
		return False
	
	ftp.close()
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
	i = 1
	for ip in ip_list :
		sys.stdout.write("\r => Scanning %d of %d -> %s" % (i, len(ip_list), ip))
		if loginOK(ip) : 
			#print "\n\n[***] Anonymous login OK: %s [***]\n" % ip
			sys.stdout.write("\r [***] Anonymous login OK: %s [***]\n" % ip) 	
		sys.stdout.flush()
		time.sleep(0.2)
		i += 1
		
	print "\n\n Scanned %d hosts in %d seconds" % (len(ip_list), (time.time() - start_time))

###########
if __name__ == '__main__':
    main()


