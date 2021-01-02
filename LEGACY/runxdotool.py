#!/usr/bin/env python
#
#       runxdotool.py
#       
#       Copyright 2010 esbat <esbat@esbat-laptop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import gtk, subprocess, time, string
def AddCommandToRun(CommandPath):
    print CommandPath
    afile = open(CommandPath)
    ParamsForCommand = afile.read().split("\n")
    for s in ParamsForCommand:
        EachCommand = s.split(" ")
        if EachCommand[0] == 'move':
            subprocess.check_call(["xdotool","mousemove",EachCommand[3],EachCommand[4]])
        if EachCommand[0] == 'delay':
            time.sleep(string.atof(EachCommand[1]))
        if EachCommand[0] == 'click':
            if EachCommand[2] == 'left':
                for i in EachCommand[5]:
                    subprocess.check_call(["xdotool","click","1"])
                    time.sleep(string.atof(EachCommand[9]))
            if EachCommand[2] == 'middle':
                for i in EachCommand[5]:
                    subprocess.check_call(["xdotool","click","2"])
                    time.sleep(string.atof(EachCommand[9]))
            if EachCommand[2] == 'right':
                for i in EachCommand[5]:
                    subprocess.check_call(["xdotool","click","3"])
                    time.sleep(string.atof(EachCommand[9]))
        if EachCommand[0] == 'type':
            for i in EachCommand[5]:
                subprocess.check_call(["xdotool","key",EachCommand[3]])
                time.sleep(string.atof(EachCommand[9]))
    return 0


def main():
    
    return 0

if __name__ == '__main__': main()
