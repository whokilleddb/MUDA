#!/usr/bin/env python3
import validators
import sys
import tldextract
from urllib.parse import urlparse
import socket
import requests
from tabulate import tabulate
from modules import *
from bs4 import BeautifulSoup

class URI:
    def __init__(self,URI,REDIRECT):
        self.URI=URI
        self.REDIRECT=REDIRECT
        self.VALIDATE_URL()
        self.REQUEST=None
        self.URL=""
        self.DOMAIN_IP=""                                  # IP Associated With The Domain
        self.PROTOCOL=""                                   # Protocol Being Used
        self.DOMAIN=""                                     # Domain Name
        self.SIZE=0                                        # Get Size Of Page (Remember boys, it does not matter! Weightage is more on the quality!)
        self.URL_SET=set()
        self.INTERNAL_COUNT=0
        self.EXTERNAL_COUNT=0
        self.GET_URI_INFO()
        self.GET_LINKS()
        self.HAS_DOWNLOAD=self.CHECK_DOWNLOAD()

    # Check if the the provided URI is valid
    def VALIDATE_URL(self):
        if not validators.url(self.URI):
            print(f"{RED}[-] The Given URI Is Invalid!{NONE}")
            sys.exit(-1)
    
    # Get Information About The Provided URI
    def GET_URI_INFO(self):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',}
        self.REQUEST=requests.get(self.URI, headers=headers)
        #print(r.content)
        self.SIZE=len(self.REQUEST.text)
        if self.REQUEST.history and self.REDIRECT:
            self.URI=self.REQUEST.url
            self.REQUEST=requests.get(self.URI,headers=headers)
            self.SIZE=len(self.REQUEST.text)
        PARSER=urlparse(self.URI)
        self.PROTOCOL=PARSER.scheme                        # Fetch Protocol
        EXTRACTOR=tldextract.extract(self.URI)
        for ext in EXTRACTOR:
            if ext !='':
                self.DOMAIN=self.DOMAIN+ext+'.'
        self.DOMAIN=self.DOMAIN[:-1]                       # Get Domain Name from URI
        self.URL=self.PROTOCOL+"://"+self.DOMAIN           # Get URL From URI
        try :
            self.DOMAIN_IP=socket.gethostbyname(self.DOMAIN)   # Getting IP Associated With Domain Name
        except Exception as e :
            EXIT_ERROR(e,-2)
    
    # Check If URL has any downloadables
    def CHECK_DOWNLOAD(self):
        flag = False
        headers=requests.head(self.URI).headers
        if 'attachment' in headers.get('Content-Disposition', ''):
            flag=True
        if 'application' in self.REQUEST.headers['Content-type']:
            flag=True
        return flag
    
    
    # Get Count Of Internal And External Links
    def GET_LINKS(self):
        soup=BeautifulSoup(self.REQUEST.text,'html.parser')
        urls=set()
        for link in soup.find_all('a'):
            href=link.get('href')
            if href:
                if href.startswith('./'):
                    urls.add(href.replace('./',''))
                elif href.startswith('/'):
                    urls.add(href.replace('/',''))
                else :
                    urls.add(href)
        self.URL_SET=urls        
        
        for url in self.URL_SET:
            try :
                p=urlparse(url)
                if p.scheme =="https" or p.scheme=="http":
                    t=tldextract.extract(url)
                    if t.domain != self.DOMAIN:
                        self.EXTERNAL_COUNT=self.EXTERNAL_COUNT+1
            except Exception as e:
                print(f"{RED}Error Occured As: {e}{NONE}")
                sys.exit(-1)
        self.INTERNAL_COUNT=len(self.URL_SET)-self.EXTERNAL_COUNT
          
    # Print Domain Information
    def SHOW_DOMAIN_INFO(self):
        table=[['PROTOCOL',self.PROTOCOL],["DOMAIN IP",self.DOMAIN_IP],["HAS DOWNLOADABLE",self.HAS_DOWNLOAD],["SIZE OF PAGE",self.SIZE],["NUMBER OF LINKS",len(self.URL_SET)],["INTERNAL LINKS",self.INTERNAL_COUNT],["EXTERNAL LINKS",self.EXTERNAL_COUNT],["DOMAIN",self.DOMAIN],["URI",self.URI],["URL",self.URL]]
        SHOW_TABLE("[+] URI Info",table)
