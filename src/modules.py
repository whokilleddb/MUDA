#!/usr/bin/env python3
import validators
import sys

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

def VALIDATE_URL(url):
    if not validators.url(url):
        print(f"{RED}[+] The Given URI Is Invalid!{NONE}")
        sys.exit(-1)
        