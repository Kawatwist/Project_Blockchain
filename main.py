from ConfigClass import Config as cf
import argparse

def main():
    parser = argparse.ArgumentParser(description='Basic Blockchain')
    parser.add_argument('--node', required=True, type=str, help='Choose the node type (Set node to help to display the possibility)')
    parser.add_argument('--host', required=False, type=str, help='Host ip (select the url of the original node, initialised at localhost)')
    parser.add_argument('--port', required=False, type=int, help='Blockchain Port (The fullnode port connection, initialised at 4242)')
    parser.add_argument('--portNode', required=False, type=int, help='Listener port of the Node (Used for the other node connection)')
    parser.add_argument('--portClient', required=False, type=int, help='Listener port of the Node (Used for the client connection, initialised at 4243)')
    parser.add_argument('--new', required=False, type=bool, help='Doest it need to be connected to someone')
    args = parser.parse_args()

    config = cf(args)
    config.createNode()
    config.node.run()

if __name__ == '__main__':
    main()