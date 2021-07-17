#coding=utf-8

import sys
import os
import os.path
##class methodinfo:
##    def __init__(self,filename):
##        
def readInfo(filename):
    f=open(filename,'r')
    dic={}
    dic['input']=[]
    dic['output']=[]
    strline=f.readline()
    while(strline):
        strline=strline.replace('\n','')
        strline=strline.replace('\r','')
        strline=strline.replace(' ','')
        strline=strline.replace('"','')
        if(strline==''):
            strline=f.readline()
            continue
        if(strline[0]=='#'):
            strline=strline[1:len(strline)].split(':')
            if(strline[0]=='methodtype'):
               dic['methodtype']=strline[1]
            if(strline[0]=='mainfile'):
               dic['mainfile']=strline[1]
            if(strline[0]=='mainmethod'):
               dic['mainmethod']=strline[1]
            if(strline[0]=='icon'):
               dic['icon']=strline[1]
            if(strline[0]=='input'):
               strinput=strline[1]
               strinput=strinput.split(',')
               inputpar={}
               for str1 in strinput:
                   str1=str1.split('=')
                   inputpar[str1[0]]=str1[1]
               dic['input'].append(inputpar)
            if(strline[0]=='output'):
               strinput=strline[1]
               strinput=strinput.split(',')
               inputpar={}
               for str1 in strinput:
                   str1=str1.split('=')
                   inputpar[str1[0]]=str1[1]
               dic['output'].append(inputpar)
        strline=f.readline()
    return dic        
    f.close()
dic=readInfo('methodinfo')
