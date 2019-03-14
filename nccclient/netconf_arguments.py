#!/home/murmanov/netconf/bin/python
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--address', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-s', '--secret', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('-p','--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.address,
                         port=args.port,
                         username=args.username,
                         password=args.secret,
                         timeout=180,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

        # execute netconf operation
            try:
                for response in m.server_capabilities:
                    print response
            except RPCError as e:
                response = e._raw

            # beautify output
            print response
