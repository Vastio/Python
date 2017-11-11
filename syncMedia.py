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
import os
import subprocess
import re

#########
# VARS  #
#########
srcMediaFolder = "/mnt/share"
(dstFilmFolder, dstTvSerieFolder) = ("./Film", "./TvSeries")
fileExt = (".avi", ".mkv", ".mp4")
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

    return 1
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

    file_list = []

    for f_name in os.listdir(src_path):

        # Join della dir con il file_name
        full_path = os.path.join(src_path, f_name)

        # Verifica se file
        if os.path.isfile(full_path):
            # Verfica estensione del file
            if os.path.splitext(full_path)[1] in fileExt:
                file_list.append(full_path)
        # Recursiva se directory
        if os.path.isdir(full_path):
            file_list = listSrcFolder(full_path)

    return file_list
###


# MAIN
def main():

    if not mountRemoteFolder():
        sys.exit(1)

    # Listing source folder
    file_list = listSrcFolder(srcMediaFolder)

    umountRemoteFolder()
###########


###########
if __name__ == '__main__':
    main()
