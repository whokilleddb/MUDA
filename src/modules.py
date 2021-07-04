#!/usr/bin/env python3
from tabulate import tabulate
import sys

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

# Banner Text
BANNER="""
██╗    ██╗██╗  ██╗ ██████╗ ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ ██████╗ ██████╗ 
██║    ██║██║  ██║██╔═══██╗██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗██╔══██╗██╔══██╗
██║ █╗ ██║███████║██║   ██║█████╔╝ ██║██║     ██║     █████╗  ██║  ██║██║  ██║██████╔╝
██║███╗██║██╔══██║██║   ██║██╔═██╗ ██║██║     ██║     ██╔══╝  ██║  ██║██║  ██║██╔══██╗
╚███╔███╔╝██║  ██║╚██████╔╝██║  ██╗██║███████╗███████╗███████╗██████╔╝██████╔╝██████╔╝
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═════╝ ╚═════╝ ╚═════╝ 
"""

def SHOW_BANNER():
    print(f"{GREEN}{BANNER}{NONE}")

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
    if table :
        print(f'{YELLOW}{heading}: \n{CYAN}{tabulate(table,headers=header, tablefmt="pretty")}{NONE}\n')
    
def CHECK_KEY(KEY,DICT):
    if KEY in DICT.keys():
        return True
    else :
        return False
    
def EXIT_FUNC(sig, frame):
    print(f"\n{RED}[-] Exiting!{NONE}")
    sys.exit(-1)
    
def EXIT_ERROR(ERROR,RET=-1):
    print("{RED}[-] Exception Occured As: {ERROR}")
    print(f"[-] Exiting With Status Code: {RET}{NONE}")
    sys.exit(RET)

def CALC_RESULT(RESULTS):
    table=list()
    for key in RESULTS.keys():
        table.append([key,RESULTS[key]])
    
    SHOW_TABLE("Scores",table)

    if RESULTS['ET']==1:
        print(f"{RED}[+] GIVEN URI IS MALICIOUS{NONE}")
    else:
        score=0
        counter=len(RESULTS)
        for key in RESULTS.keys():
            score=score+RESULTS[key]
        print(f"{CYAN}[+] Final Scores: {PURPLE}{score}/{counter} = {round((score/counter),4)}{NONE}")
        if score>(0.65*counter):
            print(f"{GREEN}[+] THE GIVEN LINK APPEARS TO BE SAFE{NONE}")
        elif score>(0.3*counter):
            print(f"{YELLOW}[+] THE GIVEN LINK MIGHT BE MALICIOUS{NONE}")
        else :
            print(f"{RED}[+] GIVEN URI IS MALICIOUS{NONE}")