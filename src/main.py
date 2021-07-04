#!/usr/bin/env python3
import argparse
import signal
from virustotal import *
from check_uri import *
from whoisinfo import *
from phishtank import *
from sslcheck import *
from geotag import *
from freq import *
from modules import *

# Global Dict
RESULTS=dict()

def VIRUS_TOTAL_ANALYSIS(uri):
    vt = VIRUS_TOTAL(uri)
    vt.ANALYSE_URL()
    vt.PRINT_STATS()
    vt.PRINT_VENDOR_STATS()
    res=vt.ATTRIBUTES['stats']
    if int(res['harmless'])>(int(res['malicious'])+int(res['suspicious'])+int(res['timeout'])):
        RESULTS['VT']=1
    else:
        RESULTS['VT']=0

def WHOIS_ANALYSIS(domain):
    w=WHOIS(domain)
    w.SHOW_WHOIS_INFO()
    diff=datetime.datetime.now()-w.TIME['CREATION']
    if diff < datetime.timedelta(days=366) :
        RESULTS['DT']=0
    else :
        RESULTS['DT']=1

def PHISHTANK_ANALYSIS(url):
    pt=PHISHTANK(url)
    pt.SHOW_DATA()
    if pt.IN_DB:
        if pt.IS_PHISH:
            RESULTS['PT']=1
    else:
        RESULTS['PT']=0

def GET_SSL_INFO(proto,domain):
    if proto.lower()=='https':
        s=SSL_INSPECTION(domain)
        s.SHOW_SSL_CERT_DETAILS()
        RESULTS['SSL']=1
    else:
        RESULTS['SSL']=0
    
def GET_GEOTAG(ip):
    geo=GEO_IP(ip)
    geo.SHOW_DATA()

def GET_FREQ(URI,PROTOCOL,FILENAME):
    string=URI.replace(PROTOCOL,'').replace('/','').replace(':','')
    fq=FREQ(FILENAME,string)
    fq.SHOW_PROBABILITY()
    total=float(fq.PROBABILITY[1])
    avg=float(fq.PROBABILITY[0])
    if total> avg:
        RESULTS['ET']=1
    else :
        RESULTS['ET']=round((total/avg),4)


def main():
    print(f"\n{PURPLE}{BOLD}[+] Launching MUDA!{NONE}\n")    
    parser = argparse.ArgumentParser(description="[+] Malicious URL Detector!")
    parser.add_argument('-u', metavar='URL', required=True, type=str, help="URL/URI to Inspect")
    parser.add_argument('-r', action='store_true', help="Follow Redirects")
    parser.add_argument('-f', metavar='Frequency File', required=False, type=str,default="freq.txt", nargs='?', const="freq.txt", help="Frequency File")
    args = parser.parse_args()
    
    uri=URI(args.u,args.r)
    uri.SHOW_DOMAIN_INFO()
    
    print(uri.HAS_DOWNLOAD)
    if uri.HAS_DOWNLOAD:
        RESULTS['DW']=0
    else:
        RESULTS['DW']=1
        
    GET_FREQ(uri.URI,uri.PROTOCOL,args.f)
    VIRUS_TOTAL_ANALYSIS(uri)
    WHOIS_ANALYSIS(uri.DOMAIN)
    PHISHTANK_ANALYSIS(uri.URL)
    GET_SSL_INFO(uri.PROTOCOL, uri.DOMAIN)
    GET_GEOTAG(uri.DOMAIN_IP)
    
    print()
    CALC_RESULT(RESULTS)
        
if __name__=='__main__':
    signal.signal(signal.SIGINT, EXIT_FUNC)
    SHOW_BANNER()
    main()