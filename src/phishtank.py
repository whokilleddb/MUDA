#!/usr/bin/env python3
import requests
import urllib.parse
import xmltodict
from modules import *

PHISHTANK_URL="https://checkurl.phishtank.com/checkurl/"

class PHISHTANK:
    def __init__(self,URL):
        self.URL=URL
        self.IN_DB=False
        self.IS_PHISH=None
        self.DETAILS=""
        self.VERIFIED=[]
        self.CHECK_PHISH()
        
    def CHECK_PHISH(self):
        data={
            "url":urllib.parse.quote(self.URL),
        }
        response=requests.post(PHISHTANK_URL,params=data)
        data=xmltodict.parse(response.text)['response']['results']['url0']
        #print(data)
        if data['in_database'] == "true":
            self.IN_DB=True
            self.DETAILS=data['phish_detail_page']
            self.VERIFIED.append(RETURN_BOOLEAN(data['verified']))
            self.VERIFIED.append(data['verified_at'])
            self.IS_PHISH=RETURN_BOOLEAN(data['valid'])
    
    def SHOW_DATA(self):
        if self.IN_DB:
            table=[['In Database','True'],["Is Phish?",self.IS_PHISH],["Verified At",self.VERIFIED[1]],["Info Page",self.DETAILS]]
            SHOW_TABLE("[+] PhishTank Info",table)
        else :
            print(f"{RED}[-] No Information Available On PhishTank{NONE}")
            
            
            
        

        