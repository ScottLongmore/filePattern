# Stock modules
import sys
import os
import re
import datetime
import operator
import collections
import json
import logging
import types

# Local modules
import error_codes
from setup_logging import setup_logging
import dirRE


DTGfrmts=collections.OrderedDict(
         {
         'Y':'%Y',
         'y':'%y',
         'j':'%j',
         'm':'%m',
         'd':'%d',
         'H':'%H',
         'M':'%M'
         }
         )

# Logging
LOG = logging.getLogger(__file__) #create the logger for this file
logging_setup = "utils"
setup_logging(logging_setup)

def ddhh2pack(day,hour):

    if hour==0:
        pcode='X'
        pday=day
    elif hour==6:
        pcode='Y'
        pday=day
    elif hour==12:
        pcode='X'
        pday=day+50
    elif hour==18:
        pcode='Y'
        pday=day+50
    else:
        msg="Hour: {} is not a synoptic time (0,6,12,18)".format(hour)
        error(LOG,msg,error_codes.EX_IOERR)
 
    return(pcode,pday)
     
def pack2hhdd(pcode,pday):
    
    if pcode == 'X' and pday < 50:
       hour=0 
    elif pcode == 'Y' and pday < 50:
       hour=6
    elif pcode == 'X' and pday > 50:
       hour=12
       day=pday-50
    elif pcode == 'Y' and pday > 50:
       hour=18
       day=pday-50
    else:
        msg="Pack code: {} /day: {} not valid".format(pcode,pday)
        error(LOG,msg,error_codes.EX_IOERR)

    return(day,hour)

def dateTimeStrings(DTG):
    
    DTGstrs={}
    try:
        for DTGfrmtKey in DTGfrmts:
            DTGstrs[DTGfrmtKey]=datetime.datetime.strftime(DTG,DTGfrmts[DTGfrmtKey])

    except: 
        msg="Unable to parse {}".format(DTG)
        error(LOG,msg,error_codes.EX_IOERR)

    return(DTGstrs)

def repStrTmpl(tmplString,templates,ldelim='%',rdelim=''):

    strTypes=(types.StringType, types.UnicodeType)
    newString=tmplString
    for tmplKey in templates:

        tmplValue=templates[tmplKey]
        if isinstance(tmplValue,strTypes):
           tmpl="{}{}{}".format(ldelim,tmplKey,rdelim)
	   # print "\t{} {} {} {}".format(tmplKey,tmpl,templates[tmplKey],newString) 
           newString=newString.replace(tmpl,templates[tmplKey])

    return(newString)
      
'''
parseDirEntries - parse a list of directory entries (dir, dir file, or dirRE) 
                  and return expanded dir list
'''
def parseDirEntries(entries):

    dirs=[]
    for entry in entries: 

        entry=str(entry)
        if os.path.isfile(entry):
           dirFH = open(entry,"r")
           for line in dirFH:
               dir=line.rstrip('\n')
               if os.path.isdir(dir):
                   dirs.append(dir)
               else:
                   msg="Dir file: {} dir not valid: {} ".format(entry,dir)
                   error(LOG,msg,error_codes.EX_IOERR)
           dirFH.close()
        elif os.path.isdir(entry):
           dirs.append(entry)
        elif re.search("\^.+\$",entry):
           entryRE=dirRE.dirRE(entry)
           for dir in (entryRE.getDirs()):
               dirs.append(dir) 
        else: 
           msg="Dir entry {} neither dir, dir file, or dir RE".format(entry)
           error(LOG,msg,error_codes.EX_IOERR)

    return(dirs)

'''
warning - append message to a log object 
'''
def warning(LOG,msg="Unexpected Warning:"):
    LOG.warn(msg)

'''
error - append message to a log object and throw an error 
'''
def error(LOG,msg="Unexpected Error:",code=1):
    LOG.exception(msg)
    sys.exit(code)

