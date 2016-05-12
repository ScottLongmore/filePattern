#!/usr/bin/python
"""
libvspp.py - library of vspp data file filter routines 
"""

# Stock modules
import sys
import os
import re
import logging
import traceback
import datetime
import collections
import operator

# Local modules
import error_codes
from setup_cira_logging import setup_logging

LOG = logging.getLogger(__name__)

# Filter Routines

def cira2gina(input,time,files):
    
    fileRE=re.compile(input['re'])

    newfiles={}
    for file in files:

       fileMatch=re.match(fileRE,file) 
       if fileMatch: 

           fileFields=fileMatch.groupdict()
           fileDTGstr="".join(operator.itemgetter('YYYY','mm','dd','HH','MM')(fileFields))
           fileDTG=datetime.datetime.strptime(fileDTGstr,"%Y%m%d%H%M")

           ginaSubDir1="npp.{}.{}".format(fileDTG.strftime("%y%j"),fileDTG.strftime("%H%M"))
           ginaDir=os.path.join(str(input['targetRootDir']),ginaSubDir1,'viirs') 

           newfiles[file]={}
           newfiles[file]['name']=os.path.join(ginaDir,file)
           if not os.path.exists(ginaDir):
              os.makedirs(ginaDir)

           os.symlink(files[file]['name'],newfiles[file]['name'])

    return(newfiles)

def gina2cira(input,time,files):
    
    fileRE=re.compile(input['re'])

    newfiles={}
    for file in files:

       fileMatch=re.match(fileRE,file) 
       if fileMatch: 

           fileFields=fileMatch.groupdict()
           fileDTGstr="".join(operator.itemgetter('YYYY','mm','dd','HH','MM')(fileFields))
           fileDTG=datetime.datetime.strptime(fileDTGstr,"%Y%m%d%H%M")

           ciraDir=os.path.join(str(input['targetRootDir']),fileFields['id'])
           
           newfiles[file]={}
           newfiles[file]['name']=os.path.join(ciraDir,file)
           if not os.path.exists(ciraDir):
              os.makedirs(ciraDir)

           os.symlink(files[file]['name'],newfiles[file]['name'])

    return(newfiles)

