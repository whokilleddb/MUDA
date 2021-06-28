#!/usr/bin/env python3
import validators
import sys
import tldextract
from urllib.parse import urlparse
import socket
from tabulate import tabulate
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

class URI:
    def __init__(self,URI):
        self.URI=URI
        self.VALIDATE_URL()
        self.URL=""
        self.DOMAIN_IP=""                                  # IP Associated With The Domain
        self.PROTOCOL=""                                   # Protocol Being Used
        self.DOMAIN=""                                     # Domain Name
        self.GET_URI_INFO()

    # Check if the the provided URI is valid
    def VALIDATE_URL(self):
        if not validators.url(self.URI):
            print(f"{RED}[-] The Given URI Is Invalid!{NONE}")
            sys.exit(-1)
    
    # Get Information About The Provided URI
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
    
    # Print Domain Information
    def SHOW_DOMAIN_INFO(self):
        table=[["URI",self.URI],["URL",self.URL],['PROTOCOL',self.PROTOCOL],["DOMAIN",self.DOMAIN],["DOMAIN IP",self.DOMAIN_IP]]
        SHOW_TABLE("[+] URI Info",table)
