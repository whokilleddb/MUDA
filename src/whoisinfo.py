#!/usr/bin/env python3
import whois
import datetime
from tabulate import tabulate
import datetime
from modules import *

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

class WHOIS:
    def __init__(self,domain):
        self.DOMAIN=domain
        self.TIME={}
        self.WHOIS_INFO=whois.whois(self.DOMAIN)
        self.TIME['CREATION']=GET_TIME(self.WHOIS_INFO['creation_date'])
        self.TIME['UPDATED']= GET_TIME(self.WHOIS_INFO['updated_date'])
        self.TIME['EXPIRATION']=GET_TIME(self.WHOIS_INFO['expiration_date'])
        
    def SHOW_WHOIS_INFO(self):
        #print(self.TIME)
        table=[["Domain",self.DOMAIN],["Creation Date",self.TIME['CREATION'].strftime("%H:%M:%S %Y-%m-%d")],["Updated Date",self.TIME['UPDATED'].strftime("%H:%M:%S %Y-%m-%d")],["Expiration Date",self.TIME['EXPIRATION'].strftime("%H:%M:%S %Y-%m-%d")]]
        print(f'{YELLOW}[+] WHOIS Info: \n{CYAN}{tabulate(table, tablefmt="pretty")}{NONE}\n')
        
    