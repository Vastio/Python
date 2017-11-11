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
import re

#########
# VARS  #
#########
srcMediaFolder = "/mnt/share"
(dstFilmFolder, dstTvSerieFolder) = ("./Film", "./TvSeries")
fileExt = ("avi", "mkv", "mp4")
matchlist = ("\dx\d", "s\dx\d", "s0\dx\d", "\de\d", "s\de\d", "s0\de\d")


# Mount remote folder
def mountRemoteFolder():
    smb = "//192.168.0.100/p2p"
    opts = "username=p2p,password=Claeseby@1997,vers=3.0"

    try:
        subprocess.check_call(['mount.cifs', smb, srcMediaFolder, '-o', opts])
    except subprocess.CalledProcessError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s!\n" % err)
        return 0
    except OSError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s\n" % err)
        return 0
###


# Umount rmeote folder
def umountRemoteFolder():
    try:
        subprocess.check_call(['umount', srcMediaFolder])
    except subprocess.CalledProcessError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s!\n" % err)
        return 0
    except OSError as err:
        sys.stderr.write(" [!] Unable  to mount remote folder: %s\n" % err)
        return 0
###


# Listing source dir
def listSrcFolder(src_path):

    for f_name in os.listdir(src_path):
        path_name = os.path.join(src_path, f_name)
        if os.path.is_file(path_name):
            if
###


# MAIN
def main():

    if not mountRemoteFolder():
        sys.exit(1)

    # Listing source folder
    files = listSrcFolder(srcMediaFolder)
###########


###########
if __name__ == '__main__':
    main()
