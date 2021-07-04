#!/usr/bin/env python3
import argparse
import signal
from virustotal import *
from check_uri import *
from whoisinfo import *
from phishtank import *
from sslcheck import *
from geotag import *

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

def VIRUS_TOTAL_ANALYSIS(uri):
    vt = VIRUS_TOTAL(uri)
    vt.ANALYSE_URL()
    vt.PRINT_STATS()
    vt.PRINT_VENDOR_STATS()

def WHOIS_ANALYSIS(domain):
    w=WHOIS(domain)
    w.SHOW_WHOIS_INFO()

def PHISHTANK_ANALYSIS(url):
    pt=PHISHTANK(url)
    pt.SHOW_DATA()

def GET_SSL_INFO(proto,domain):
    if proto.lower()=='https':
        s=SSL_INSPECTION(domain)
        s.SHOW_SSL_CERT_DETAILS()

def GET_GEOTAG(ip):
    geo=GEO_IP(ip)
    geo.SHOW_DATA()

def main():
    print(f"\n{PURPLE}{BOLD}[+] Launching MUDA!{NONE}\n")    
    parser = argparse.ArgumentParser(description="[+] Malicious URL Detector!")
    parser.add_argument('-u', metavar='URL', required=True, type=str, help="URL/URI to Inspect")
    parser.add_argument('-r', action='store_true', help="Follow Redirects")
    args = parser.parse_args()
    uri=URI(args.u,args.r)
    uri.SHOW_DOMAIN_INFO()
    VIRUS_TOTAL_ANALYSIS(uri)
    WHOIS_ANALYSIS(uri.DOMAIN)
    PHISHTANK_ANALYSIS(uri.URL)
    GET_SSL_INFO(uri.PROTOCOL, uri.DOMAIN)
    GET_GEOTAG(uri.DOMAIN_IP)
    
if __name__=='__main__':
    signal.signal(signal.SIGINT, EXIT_FUNC)
    SHOW_BANNER()
    main()