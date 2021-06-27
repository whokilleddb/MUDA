#!/usr/bin/env python3
import requests
import os
import socket
from dotenv import load_dotenv
import tldextract
from urllib.parse import urlparse
from tabulate import tabulate
from time import sleep
import datetime

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
        self.API_KEY=os.getenv('VIRUS_TOTAL_KEY')           # Store API KEY
        self.URI= URI.URI                                    
        self.URL= URI.URL
        self.DOMAIN_IP= URI.DOMAIN_IP                                  
        self.PROTOCOL= URI.DOMAIN_IP                                
        self.DOMAIN= URI.DOMAIN                             
        self.ID=self.FETCH_URL_ID()    
        self.ATTRIBUTES=self.ANALYSE_URL()
        print(f"{YELLOW}{BOLD}[+] Virus Total ID(URL): {PURPLE}{self.ID}{NONE} \n")                    
        
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
    
    # Analyse The Target URL
    def ANALYSE_URL(self):
        header={
        'X-ApiKey':self.API_KEY,
        }
        url=VIRUS_TOTAL_API_URL+"analyses/"+str(self.ID)
        while True:
            response=requests.get(url,headers=header)   
            results=(response.json())['data']
            if results['attributes']['status'] != "queued" :
                break
            sleep(1)
        return results['attributes']
    
    # Print Overall Stats   
    def PRINT_STATS(self):
        STATS=self.ATTRIBUTES['stats']
        table=[]
        for key in STATS.keys():
            table.append([key,str(STATS[key])])
        print(f'{YELLOW}[+] Stats For Your URL: \n{CYAN}{tabulate(table, headers=["Status","Score"],tablefmt="pretty")}{NONE}\n')
        
    def PRINT_VENDOR_STATS(self):
        RESULTS=self.ATTRIBUTES['results']
        table=[]
        for KEY in RESULTS.keys():
            VENDOR=RESULTS[KEY]
            table.append([VENDOR['engine_name'],VENDOR['category'],VENDOR['result'],VENDOR['method']])
        print(f'{YELLOW}[+] Engine Analysis: \n{CYAN}{tabulate(table, headers=["Engine","Category","Result","Method"],tablefmt="pretty")}{NONE}\n')
