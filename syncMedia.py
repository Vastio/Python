# -------------------------------------------------------------------------------
# Name:        modulo1
# Purpose:
#
# Author:      s.catalano
#
# Created:     11/11/2017
# Copyright:   (c) s.catalano 2017
# Licence:     <GPLv3>
# -------------------------------------------------------------------------------

import sys
import subprocess

#########
# VARS  #
#########
srcMediaFolder = "./Media"
(dstFilmFolder, dstTvSerieFolder) = ("./Film", "./TvSeries")
fileExt = ("avi", "mkv", "mp4")
matchlist = ("\dx\d", "s\dx\d", "s0\dx\d", "\de\d", "s\de\d", "s0\de\d")


# Mount remote folder
def mountRemoteFolder():
    srcFolder = "//192.168.0.100/p2p"
    dstFolder = "/mnt/share"
    opts = "username=p2p,password=Claeseby@197,vers=3.0"

    try:
        subprocess.check_call(['mount.cifs', srcFolder, dstFolder, '-o', opts])
    except subprocess.CalledProcessError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s!\n" % err)
        return 0
    except OSError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s\n" % err)
        return 0
###


# MAIN
def main():

    if not mountRemoteFolder():
        sys.exit(1)

    # Listing source folder
###########


###########
if __name__ == '__main__':
    main()
