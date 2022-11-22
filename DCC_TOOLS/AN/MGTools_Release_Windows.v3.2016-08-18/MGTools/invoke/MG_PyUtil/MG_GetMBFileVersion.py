#==============================================================//
#                   MGtools - MGreadMBVersionInfo
#==============================================================//
#Author: Miguel (Wenfeng Gao) 
#website: http://mgland.com
#Feedback: http://mgland.com
#E-mail: mgtoolspro@gmail.com
#CopyRight Miguel @ mgland animation studio.
import os

def MGreadMAVersionInfo (fileName):
    if not os.path.isfile(fileName):
        return 'Unknown'
    if not fileName.endswith('.ma'):
        return 'Unknown'
    theLine = ''
    try:
        f = open(fileName,'r')
        theLine = f.readline().strip()
    finally:
        f.close()
    if not len(theLine):
        return 'Unknown'
    temp = theLine.split(' ')
    return temp[2]

def MGreadMBVersionInfo (fileName):
    '''Get the Maya version string return via given File argument'''
    handle=open (fileName,'r')
    rawString=handle.read(500)
    handle.close()
    rawString= repr(rawString)
    if not 'Maya ' in rawString:
        return 'Unknown'
    first=rawString.find('Maya ')
    if len(rawString) < (first+30):
        return 'Unknown'    
    midString=rawString[first:(first+30)]
    if not len(midString):
        return 'Unknown'
    digit='.0123456789'
    near=midString.split() [-1]
    result=''
    if not len(near):
        return 'Unknown'
    for c  in near:
        if c in digit:
            result+=c
        else:
            break;
    
    if len(result):
        return result
    else:
        return 'Unknown'

#if __name__ == '__main__':
#    print (MGreadMBVersionInfo ('C:/Users/miguel/Documents/maya/projects/default/scenes/untitled.001.mb'))


