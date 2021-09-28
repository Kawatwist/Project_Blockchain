from Tools.ConfigClass import Config as cf
import argparse

def main():
    parser = argparse.ArgumentParser(description='Basic Blockchain')

    parser.add_argument('--nodeType', required=True, type=str, help='Choose the node type (Set node to help to display the possibility)')
    parser.add_argument('--name', required=False, type=str, help='Select a name for the node (Not really usefull for the moment)')
    parser.add_argument('--host', required=False, type=str, help='Host ip (select the url of the original node, initialised at localhost)')
    parser.add_argument('--hostPort', required=False, type=int, help='Blockchain Port (The fullnode port connection, initialised at 4242)')
    parser.add_argument('--nodePort', required=False, type=int, help='Listener port of the Node (Used for the other node connection)')
    parser.add_argument('--clientPort', required=False, type=int, help='Listener port of the Node (Used for the client connection, initialised at 4243)')
    parser.add_argument('--master', required=False, type=bool, help='Set the flag if its the real Genesis (either the node will not be connected)')
    args = parser.parse_args()

    config = cf(args)
    config.createNode()
    config.node.run()

if __name__ == '__main__':
    main()