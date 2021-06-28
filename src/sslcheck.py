#!/usr/bin/env python3
import ssl
import socket

class SSL_INSPECTION:
    def __init__(self,DOMAIN):
        self.DOMAIN=DOMAIN
        self.GET_SSL_INFO()
        
    def GET_SSL_INFO(self):
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=self.DOMAIN) as s:
            s.connect((self.DOMAIN, 443))
            cert = s.getpeercert()
        
        print(cert)
        print(f"Keys:\n{cert.keys()}")
        