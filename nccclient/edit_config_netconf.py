#!/usr/bin/python
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError
import logging
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
    parser.add_argument('-xml','--xmlcommand', required=True, type=argparse.FileType('r'),
                        help="RPC command in XML format compatible with Netconf")
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    
    payload=[]

    with args.xmlcommand as filehandle:
        payload.append(filehandle.read())

    #logging.basicConfig(level=logging.DEBUG)
    
    #print payload
    
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
                print "Locking running config\n"
                lock_config = m.lock('running')

                print "Locking candidate config\n"
                lock_config = m.lock('candidate')

                print "Editing config\n"
                edit_command = m.dispatch(et.fromstring(snippet))
                data = edit_command.data_ele
                
                print "Saving to running config\n"
                commit_config = m.commit()
                
                print "Unlocking candidate config\n"
                unlock_config = m.unlock('candidate')

                print "Unlocking running config\n"
                unlock_config = m.unlock('running')
            except RPCError as e:
                data = e._raw
