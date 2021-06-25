#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
VIRUS_TOTAL_URL = "https://www.virustotal.com/api/v3/urls"
VIRUS_TOTAL_ANALYSES = "https://www.virustotal.com/api/v3/analyses"


class VIRUS_TOTAL:
    def __init__(self):
        self.API_KEY=os.getenv('VIRUS_TOTAL_KEY')
        self.ID=0

    def FETCH_URL_ID(self,url):
        header={
        'X-ApiKey':self.API_KEY,
        }
        data={
        'url':url,
        }
        response=requests.post(VIRUS_TOTAL_URL,headers=header, data=data)
        resp_json=response.json()
        self.ID=resp_json['data']['id']
        return self.ID
    
    def ANALYSE_URL(self):
        header={
        'X-ApiKey':self.API_KEY,
        }
        url=VIRUS_TOTAL_ANALYSES+str(self.ID)
        response=requests.get(url,headers=header)
        print(response.text)

vt = VIRUS_TOTAL()
print(vt.FETCH_URL_ID("https://zerodollarsecurity.in"))
vt.ANALYSE_URL()