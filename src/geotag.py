#!/usr/bin/env python3
import requests
from modules import *
import os

IPSTACK_URL="http://api.ipstack.com/"

class GEO_IP:
    def __init__(self, IP):
        self.IP=IP
        self.API_KEY=os.getenv('IPSTACK_KEY')
        self.DATA=self.GET_CODE()
        self.COUNTRY=""
        self.COUNTR_CODE=""
        self.CONTINENT=""
        self.LATITUDE=""
        self.LONGITUDE=""
        self.REGION=""
        self.CITY=""
        self.ZIP=0
        self.FILL_DATA()
        
        
    def GET_CODE(self):
        url=IPSTACK_URL+self.IP+"?access_key="+self.API_KEY
        response=requests.get(url)
        #print(response.json())
        return response.json()
    
    def FILL_DATA(self):
        self.COUNTRY=self.DATA['country_name']+" "+self.DATA['location']['country_flag_emoji']
        self.COUNTRY_CODE=self.DATA['country_code']
        self.CONTINENT=self.DATA['continent_name']
        self.LATITUDE=self.DATA['latitude']
        self.LONGITUDE=self.DATA['longitude']
        self.REGION=self.DATA['region_name']
        self.CITY=self.DATA['city']
        self.ZIP=self.DATA['zip']
    
    def SHOW_DATA(self):
        table=[["Country",self.COUNTRY],["COUNTRY CODE", self.COUNTRY_CODE],["CONTINENT",self.CONTINENT],["REGION", self.REGION],["CITY",self.CITY],["ZIP CODE",self.ZIP],["LATITUDE",self.LATITUDE],["LONGITUDE",self.LONGITUDE]]
        SHOW_TABLE("[+] Location Information",table)
        
        
        
        
    