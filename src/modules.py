#!/usr/bin/env python3

def GET_TIME(obj):
    if type(obj)==type([]):
        return obj[0]
    else :
        return obj