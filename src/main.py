import argparse
import logging
import os
import time
from network import Network
from peer import Peer

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(os.path.join('logs', 'app.log')),
                        logging.StreamHandler()
                    ])


def load_config(config_file='config/config.yaml'):
    """Load configuration settings."""
    import yaml
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    """Main function to handle command-line arguments and run the P2P system."""
    config = load_config()
    
    # Initialize the network
    network = Network(config['discovery_port'], config['tcp_port'])
    
    # Initialize the peer
    peer = Peer(config['peer_id'], config['ip_address'], config['tcp_port'])
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="P2P File Sharing System")
    parser.add_argument('action', choices=['share', 'request'], help="Action to perform: share or request")
    parser.add_argument('file', help="File path to share or request")
    args = parser.parse_args()
    
    if args.action == 'share':
        share_file(peer, network, args.file)
    elif args.action == 'request':
        request_file(peer, network, args.file)
    
    # Keep the program running
    try:
        while True:
            # Periodically broadcast presence
            network.broadcast_presence()
            
            # Listen for incoming requests (you need to implement this method)
            network.listen_for_discovery()
            
            time.sleep(5)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")

def share_file(peer, network, file_path):
    """Share a file with the network."""
    peer.add_shared_file(file_path)
    logging.info(f"Sharing file: {file_path}")
    network.broadcast_presence()

def request_file(peer, network, file_name):
    """Request a file from the network."""
    logging.info(f"Requesting file: {file_name}")

if __name__ == '__main__':
    main()
