#!/usr/bin/python
import lxml.etree as et
import xmltodict
import xml.dom.minidom
from ncclient import manager
from ncclient.operations import RPCError
#import logging

host = '10.48.35.91'
port = 830
user = 'cisco'
pw = 'cisco123'

hostname_filter = '''
                          <filter>
                              <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                  <hostname></hostname>
                              </native>
                          </filter>
                  '''

payload = [
'''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <candidate/>
  </target>
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <hostname>test-01</hostname>
    </native>
  </config>
</edit-config>
'''
]

#    logging.basicConfig(level=logging.DEBUG)

with manager.connect(host = host, port = port, username = user, password = pw, device_params = {'name': 'csr'}, allow_agent = False, timeout=180) as m:
        for snippet in payload:
            try:
                print "Locking candidate config\n"
                lock_config = m.lock('running')

                print "Current hostname\n"
                print_hostname_before = m.get_config('running', hostname_filter)
                print(xml.dom.minidom.parseString(str(print_hostname_before)).toprettyxml())

                print "Editing config\n"
                edit_command = m.dispatch(et.fromstring(snippet))
                data = edit_command.data_ele

                print "Saving to running config\n"
                commit_config = m.commit()

                print "Unlocking config\n"
                unlock_config = m.unlock('running')

                print "After change\n"
                print_hostname_after = m.get_config('running', hostname_filter)
                print(xml.dom.minidom.parseString(str(print_hostname_after)).toprettyxml())
            except RPCError as e:
                data = e._raw
