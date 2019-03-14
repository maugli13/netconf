#!/usr/bin/python
from ncclient import manager

host = '10.48.35.91'
port = '22'
user = 'cisco'
pw = 'cisco123'


payload = """
    <config>
        <cli-config-data>
            <cmd>hostname test-02</cmd>
        </cli-config-data>
    </config>
"""

print "Using port "+ port

with manager.connect(host = host, port = port, username = user, password = pw, device_params = {'name': 'csr'}, allow_agent = False, timeout=180) as m:
    try:
        lock_config = m.lock('running')
        edit_command = m.edit_config(target='running', config=payload)
        unlock_config = m.unlock('running')
        print "Successfully completed"
    except Exception as e:
        print "Following Error appeared!"
        print e
