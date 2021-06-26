#!/usr/bin/env python3
from VirusTotal import *
import argparse
from check_uri import *

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

def main():
    print(f"{GREEN}{BOLD}[+] Launching MUDA!")    
    parser = argparse.ArgumentParser(description="[+] Malicious URL Detector!")
    parser.add_argument('-u', metavar='URL', required=True, type=str, help="URL/URI to Inspect")
    args = parser.parse_args()

    uri=URI(args.u)
    uri.SHOW_DOMAIN_INFO()
    VIRUS_TOTAL_ANALYSIS(uri)
    
if __name__=='__main__':
    main()