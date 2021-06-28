#!/usr/bin/env python3
from tabulate import tabulate

# Colorschemes
NONE='\033[00m'
BLACK='\033[01;30m'
RED='\033[01;31m'
GREEN='\033[01;32m'
YELLOW='\033[01;33m'
BLUE='\033[0;34m'
PURPLE='\033[01;35m'
CYAN='\033[01;36m'
WHITE='\033[01;37m'
BOLD='\033[1m'
BLINK='\033[5m'
UNDERLINE='\033[4m'

def GET_TIME(obj):
    if type(obj)==type([]):
        return obj[0]
    else :
        return obj

def RETURN_BOOLEAN(str):
    if str.lower()=='true':
        return True
    return False

def SHOW_TABLE(heading,table,header=[]):
    print(f'{YELLOW}{heading}: \n{CYAN}{tabulate(table,headers=header, tablefmt="pretty")}{NONE}\n')
    
    