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
import errno
import time
import argparse
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
matchlist = ("s\dx\d", "s0\dx\d", "\de\d", "s\de\d", "s0\de\d", "\dx\d")
DEBUG = False
INTERACT = False


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
            if DEBUG:
                print("[*] It's time to remove file: " + src_file)
            # os.remove(src_file)
    else:
        try:
            if DEBUG:
                print("[*] " + src_file + " -> " + dst_file)
            shutil.copyfile(src_file, dst_file)
        except IOError as err:
            sys.stderr.write(" [!] IOError: %s\n" % err)
            sys.exit(1)
###


# Listing source dir
def listSrcFolder(src_path):

    serie_list = {}

    for f_name in os.listdir(src_path):

        if f_name != '#recycle':
            # Join della dir con il file_name
            full_path = os.path.join(src_path, f_name)

            # Verifica se file
            if os.path.isfile(full_path):
                # Verfica estensione del file
                if os.path.splitext(full_path)[1] in fileExt:
                    if isTvSerie(f_name):
                        if DEBUG:
                            print("[*] Found TvSerie -> " + f_name)
                        serie_list[f_name] = full_path
                    else:
                        if DEBUG:
                            print("[*] Found Film -> " + f_name)
                        handleFilm(full_path, f_name)
            # Recursiva se directory
            if os.path.isdir(full_path):
                ret_list = listSrcFolder(full_path)
                serie_list.update(ret_list)

    return serie_list
###


# Define tv serie season
def getSeason(str_name):

    sep_list = ('x', 'X', 'e', 'E')

    season = 'Season '
    num = ''

    for char in str_name:
        if char.isdigit():
            num += char
        if char in sep_list:
            break

    return season + num
###


# Return th fullpath of destination
def returnDstFullPath(f_name):

    title = ''
    season = None
    split_name = f_name.split('.')
    for str_name in split_name:
        match_found = False
        for match in matchlist:
            regex = re.compile(match, re.IGNORECASE)
            if regex.match(str_name):
                match_found = True
                break
        if match_found is False:
            title += str_name + " "
        else:
            season = getSeason(str_name)
            break

    full_path = os.path.join(dstTvSerieFolder, title[:-1], season, f_name)
    return full_path
###


# Move Tv serie
def handleTvSerie(srcPath, dstPath):

    # Crea le directory se non esistono
    parent_dir = os.path.split(0)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(parent_dir):
                pass
            else:
                raise

    if not os.path.exists(dstPath):
        try:
            if DEBUG:
                print("[*] " + srcPath + " -> " + dstPath)
            # shutil.copyfile(srcPath, dstPath)
        except IOError as err:
            sys.stderr.write(" [!] IOError: %s\n" % err)
            sys.exit(1)
###


# MAIN
def main():

    parser = argparse.ArgumentParser(prog="syncMedia",
                                     description="Sync media in folder.")
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help="set debug ON.")
    parser.add_argument('-I', '--interactive',
                        action='store_true',
                        help="eanable interactive mode.")
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()

    # Set debug ON
    if args.debug:
        global DEBUG
        DEBUG = True

    # Set interactive mode ON
    if args.interactive:
        global INTERACT
        INTERACT = True

    if DEBUG:
        print("[*] Program starting...")

    if not mountRemoteFolder():
        sys.exit(1)

    if DEBUG:
        print("[*] Mounted smb source folder.")

    # Listing source folder
    file_list = listSrcFolder(srcMediaFolder)
    for f_name in file_list:
        dstPath = returnDstFullPath(f_name)
        handleTvSerie(file_list[f_name], dstPath)

    umountRemoteFolder()
###########


###########
if __name__ == '__main__':
    main()
