#-------------------------------------------------------------------------------
# Name:        modulo1
# Purpose:
#
# Author:      s.catalano
#
# Created:     18/09/2015
# Copyright:   (c) s.catalano 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys, os
import re
import string


#########
# VARS  #
#########
__version__ = "v0.1"
__program__ = "syncMedia"
srcMediaFolder = "./Media"
(dstFilmFolder, dstTvSerieFolder) = ("./Film", "./TvSeries")
fileExt = ("avi", "mkv", "mp4")
matchlist = ("\dx\d", "s\dx\d", "s0\dx\d", "\de\d", "s\de\d", "s0\de\d")


#
## Move TvSeries
def handleTvSerie(file) :
    # Split file
    name = version = ""
    for part in string.split(file, '.', -1) :
        for match in matchlist :
            regex = re.compile(match, re.IGNORECASE)
            if regex.match(part) :
                reg = re.compile('(s|x|e)', re.IGNORECASE)
                print reg.split(part)
                #version = part
                break
        if version : break
        else :
            if name : name += " " + part
            else : name = part

    # Create TvSeries Folder if not exist
    #if not os.path.isdir(dstFilmFolder + "/" + name) :
    #    os.mkdir(dstTvSerieFolder + "/" + name)
###



#
## Return true if file is a TvSeries
def isTvSerie(file) :
    for match in matchlist :
        regex = re.compile(match, re.IGNORECASE)
        if regex.search(file) :
            return True
    return False
###


#
## Return true if file is a Film
def isFilm(file) :
    if isTvSerie(file) : return False
    else : return True
###


#
## MAIN
def main():
    print __program__ + " starting..."

    # Scanning src media folder
    if not os.path.isdir(srcMediaFolder) :
        print "Unable to open source folder"
        sys.exit(1)
    filelist = os.listdir(srcMediaFolder)
    for file in filelist :
        if isTvSerie(file) :
            handleTvSerie(file)
        elif isFilm(file) :
            print "Film: " + file
###########


###########
if __name__ == '__main__':
    main()
