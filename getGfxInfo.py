#!/usr/bin/python
# ----------------------------------------------------------------------------------------------------------------------
# Name Of File:getGfxInfo.py                                                                                           #
# Author: Qi Huaping                                                                                                   #
# Purpose Of File: Script to monitor adb shell dumpsys gfxinfo on one app and return a average                         #
#                                                                                                                      #
# History:                                                                                                             #
# Date                   Author                  Changes                                                               #
# 2016.06.10             Qi Huaping              Inital                                                                #
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
import subprocess
import sys
import re
import getopt

"""
Device Graphic Monitor scripts
-------------------------------------

getGfxInfo.py -s <serial> -p <package name>

getGfxInfo.py --serial=<serial> --packageName <package name>

"""

device_id = None
packageName = None

def main():
    global packageName
    global device_id
    try:
        options, _ = getopt.getopt(sys.argv[1:], "hp:s:", ["help","package=","serial="])
    except getopt.GetoptError as err:
        print(err.msg)
        print(__doc__)
        sys.exit(1)

    for opt, arg in options:
        if opt in ('-s', '--serial'):
            device_id = arg
        elif opt in ('-p', '--package'):
            packageName = arg
        elif opt in ('-h', '--help'):
           usage()
           sys.exit(0)
    if packageName == None or device_id == None:
        usage()
        sys.exit(1)
    #print packageName, device_id
    print "GrapicTime:",get_graphic_time(device_id, packageName)

def usage():
    print """Usage:
    commmads like:
    getGfxInfo.py -s ec8fc2b3 -p com.android.launcher3

    getGfxInfo.py -s <serial> -p <package name>

    getGfxInfo.py --serial=<serial> --packageName <package name>

    """

# ----------------------------------------------------------------------------------------------------------------------
#   get_graphic_time
#
#   DESCRIPTION
#
#   Args
#   Arg. 2
#   device_id - adb serial id of the the Device under test (DUT}
#   packageName - package under monitor
#   return:
#         avarage time for per frame, it should be less than 16.67, otherwise, you may feel stuck on the screen
# ----------------------------------------------------------------------------------------------------------------------
def get_graphic_time(device_id, packageName):

    try:
        proc = subprocess.Popen(['adb', '-s', device_id, 'shell', 'dumpsys', 'gfxinfo', packageName], stdout=subprocess.PIPE)
        alllines = proc.stdout.read().rstrip()
        #print alllines
        regx = re.compile(r'(\s+\d+\.\d{2})(\s+\d+\.\d{2})(\s+\d+\.\d{2})(\s+\d+\.\d{2})',re.MULTILINE)
        #print regx.findall(alllines)
        num = 0.0
        total = 0
        for gfx in regx.findall(alllines):
            num += 1
            total1 = 0
            for data in gfx:
                total1 += float(data.replace(" ","").replace("\t","").strip())
            total += total1
        if num != 0:
            return total/num
        else:
            return None
        #print gfxData
    except Exception, e:
        print e


if __name__ == "__main__":

    main()
