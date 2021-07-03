#!/usr/bin/env python3
import requests
import os

IPSTACK_URL="http://api.ipstack.com/"

class GEO_IP:
    def __init__(self, IP):
        self.IP=IP
        self.API_KEY=os.getenv('IPSTACK_KEY')
        self.JSON=self.GET_CODE()
        self.COUNTRY=""
        
    def GET_CODE(self):
        url=IPSTACK_URL+self.IP+"?access_key="+self.API_KEY
        response=requests.get(url)
        print(response.json())
        return response.json()
        
    