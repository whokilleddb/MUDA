#!/usr/bin/env python3
import requests
import os
import socket
from dotenv import load_dotenv
import tldextract
from urllib.parse import urlparse
from tabulate import tabulate

load_dotenv()
VIRUS_TOTAL_API_URL = "https://www.virustotal.com/api/v3/"

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

class VIRUS_TOTAL:
    def __init__(self, URI ):
        self.API_KEY=os.getenv('VIRUS_TOTAL_KEY')          # Store API KEY
        self.URI= URI                                      # URI to Examine
        self.URL=""
        self.DOMAIN_IP=""                                  # IP Of The Domain
        self.PROTOCOL=""                                   # Being Protocol Used
        self.DOMAIN=""
        self.GET_URI_INFO()                                # Fill In Various Details
        self.ID=self.FETCH_URL_ID()                        # Virus Total IP
        
    # Fill In Various Parameters Of The Class Object
    def GET_URI_INFO(self):
        PARSER=urlparse(self.URI)
        self.PROTOCOL=PARSER.scheme                        # Fetch Protocol
        EXTRACTOR=tldextract.extract(self.URI)
        for ext in EXTRACTOR:
            if ext !='':
                self.DOMAIN=self.DOMAIN+ext+'.'
        self.DOMAIN=self.DOMAIN[:-1]                       # Get Domain Name from URI
        self.URL=self.PROTOCOL+"://"+self.DOMAIN           # Get URL From URI
        self.DOMAIN_IP=socket.gethostbyname(self.DOMAIN)   # Getting IP Associated With Domain Name
        
    # Show Domain Info
    def SHOW_DOMAIN_INFO(self):
        table=[["URI",self.URI],["URL",self.URL],['PROTOCOL',self.PROTOCOL],["DOMAIN",self.DOMAIN],["DOMAIN IP",self.DOMAIN_IP],["URL ID",self.ID]]
        print(f'{YELLOW}[+] VIRUS TOTAL INFO: \n{CYAN}{tabulate(table, tablefmt="pretty")}{NONE}\n')
        
    # Fetch URL ID From VirusTotal
    def FETCH_URL_ID(self):
        header={
        'X-ApiKey':self.API_KEY,
        }
        data={
        'url':self.URI,
        }
        response=requests.post(VIRUS_TOTAL_API_URL+"urls", headers=header, data=data)
        resp_json=response.json()
        self.ID=resp_json['data']['id']
        return self.ID
    
    def ANALYSE_URL(self):
        header={
        'X-ApiKey':self.API_KEY,
        }
        url=VIRUS_TOTAL_API_URL+str(self.ID)
        response=requests.get(url,headers=header)
        print(response.text)
