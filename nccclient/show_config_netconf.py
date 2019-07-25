#!/usr/bin/python
import xmltodict
import xml.dom.minidom
from ncclient import manager
from ncclient.operations import RPCError
#import logging
import argparse
import sys
from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    parser.add_argument('-a', '--address', type=str, required=True,
                        help="Host IP address or DNS name")
    parser.add_argument('-u', '--user', type=str, required=True,
                        help="Username allowed to connect over netconf")
    parser.add_argument('-s', '--secret', type=str, required=True,
                        help="User password required to connect")
    parser.add_argument('-p','--port', type=int, default=830,
                        help="Netconf port. By default is 830")
    parser.add_argument('-f','--filter',type=argparse.FileType('r'),
                        help="Netconf filter in XML format compatible with Netconf")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    
    payload=[]

    with args.filter as filehandle:
        payload.append(filehandle.read())

    filterdata = ' '.join(payload)

#    logging.basicConfig(level=logging.DEBUG)
    
    with manager.connect(
            host = args.address, 
            port = args.port, 
            username = args.user, 
            password = args.secret, 
            device_params = {'name': 'csr'}, 
            allow_agent = False, 
            timeout=180) as m:
        for snippet in payload:
            try:
                print "Output\n"
                if not filterdata.strip(): 
                    print_output = m.get_config('running')
                else:
                   print_output = m.get_config('running', filterdata)
                print(xml.dom.minidom.parseString(str(print_output)).toprettyxml())
            except RPCError as e:
                data = e._raw
