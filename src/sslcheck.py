#!/usr/bin/env python3
import ssl
import socket
from modules import *

#colorschemes
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

class SSL_INSPECTION:
    def __init__(self,DOMAIN):
        self.DOMAIN=DOMAIN
        self.CERT_DICT=self.GET_SSL_INFO()
        
    def GET_SSL_INFO(self):
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=self.DOMAIN) as s:
            s.connect((self.DOMAIN, 443))
            cert = s.getpeercert()
        return cert
    
    def SHOW_SSL_CERT_DETAILS(self):
        print(self.CERT_DICT)
        print(f"{PURPLE}[+] SSL Certificate Details:\n{NONE}")
        SUBJECT=self.CERT_DICT['subject']
        table=[]
        for subject in reversed(SUBJECT) :
            table.append(subject[0])
        SHOW_TABLE("{+] Subject",table)
        
        ISSUER=self.CERT_DICT['issuer']
        table=[]
        for issuer in ISSUER:
            table.append(issuer[0])
        SHOW_TABLE("{+] Issuer Information",table)
        
        print(f"{YELLOW}[+] SSL Version: {CYAN}{self.CERT_DICT['version']}{NONE}\n")
        print(f"{YELLOW}[+] Serial Number: {CYAN}{self.CERT_DICT['serialNumber']}{NONE}\n")
        
        SHOW_TABLE("[+] Subject Alternate Name",self.CERT_DICT['subjectAltName'])
        
        print(f"{YELLOW}[+] OCSP: {CYAN}{self.CERT_DICT['OCSP'][0]}{NONE}\n")
        
        print(f"{YELLOW}[+] CA Issuers: {CYAN}{self.CERT_DICT['caIssuers'][0]}{NONE}\n")