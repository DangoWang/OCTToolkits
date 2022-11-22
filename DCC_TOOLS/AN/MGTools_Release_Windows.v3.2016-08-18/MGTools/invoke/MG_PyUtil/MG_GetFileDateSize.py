#==============================================================//
#                   MGtools - MGgetFileDateSize
#==============================================================//
#Author: Miguel (Wenfeng Gao) 
#website: http://mgland.com
#Feedback: http://mgland.com/works/mel.asp
#E-mail: mgtoolspro@gmail.com
#CopyRight Miguel @ mgland animation studio.

#from input string get size and date information
from os import stat
from time import localtime
from locale import setlocale,format,LC_NUMERIC
from math import ceil
def MGgetFileDateInt (eachFile):
    statInfo =stat(eachFile)
    return int (statInfo.st_mtime)

def MGgetFileSizeInt (eachFile):
    statInfo =stat(eachFile)
    sizeRaw = ceil (statInfo.st_size/1024.0)
    return sizeRaw

def MGgetFileDateSize (fileString):
    fileList = fileString.split (';')
    result=''
    for eachFile in fileList:
        statInfo =stat(eachFile)
        sizeRaw = ceil (statInfo.st_size/1024.0)
        setlocale (LC_NUMERIC,'')
        sizeString =format ('%.*f',(0,sizeRaw),True)+'KB;'
        result+=sizeString; 

        dateTopRow = int (statInfo.st_mtime)
        dateRaw =localtime (dateTopRow )
        dateString = str (dateRaw.tm_mon)+'/'+str (dateRaw.tm_mday)+'/'+str (dateRaw.tm_year)+' '+str (dateRaw.tm_hour)+':'+str (dateRaw.tm_min)+':'+str (dateRaw.tm_sec)#+';'
        result+=dateString;
        #result+=(str(sizeRaw)+";");
        #result+=(str(dateTopRow));

    return result
   
#if __name__ == '__main__':
#    MGgetFileDateSize ('E:/Data/Char/Conch_v1.5.ma;E:/Data/Char/Z-Mouse_v1.35.ma')    
