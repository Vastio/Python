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
import time
import subprocess
import re
import shutil

#########
# VARS  #
#########
srcMediaFolder = "/mnt/share"
dstFilmFolder = "/mnt/media/video/Films/"
dstTvSerieFolder = "/mnt/media/video/TvSeries"
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


# Verifica sel il file is una serie tv
def isTvSerie(file):

    for match in matchlist:
        regex = re.compile(match, re.IGNORECASE)
        if regex.search(file):
            return True

    return False
###


# Sposte il film nella directory destinazione
def handleFilm(src_file, file_name):

    # File destinazione
    dst_file = os.path.join(dstFilmFolder, file_name)

    if os.path.exists(dst_file):
        now = time.time() - (6 * 86400)

        if os.stat(src_file).st_ctime < now:
            print("Remove file: " + src_file)
            # os.remove(src_file)
    else:
        try:
            print(src_file + " -> " + dst_file)
            shutil.copyfile(src_file, dst_file)
        except IOError as err:
            sys.stderr.write(" [!] IOError: %s\n" % err)
            sys.exit(1)
###


# Listing source dir
def listSrcFolder(src_path):

    serie_list = []

    for f_name in os.listdir(src_path):

        if f_name != '#recycle':
            # Join della dir con il file_name
            full_path = os.path.join(src_path, f_name)

            # Verifica se file
            if os.path.isfile(full_path):
                # Verfica estensione del file
                if os.path.splitext(full_path)[1] in fileExt:
                    if isTvSerie(f_name):
                        serie_list.append(full_path)
                    else:
                        handleFilm(full_path, f_name)
            # Recursiva se directory
            if os.path.isdir(full_path):
                ret_list = listSrcFolder(full_path)
                serie_list.extend(ret_list)

    return serie_list
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
