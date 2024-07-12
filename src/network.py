import socket
import threading
import logging
import time
import os

class Network:
    def __init__(self, discovery_port, tcp_port):
        """Initialize the network settings and data structures."""
        self.peer_list = []
        self.udp_socket = None
        self.tcp_socket = None
        self.discovery_port = discovery_port
        self.tcp_port = tcp_port
        self.active_connections = {}

        # Configure logging
        logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(os.path.join('logs', 'app.log')),
                        logging.StreamHandler()
                    ])

    # Peer Discovery Methods
    def broadcast_presence(self):
        """Send a UDP broadcast to announce the peer's presence."""
        # Create UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Allow broadcast
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Prepare the message
        message = f"Peer at {self.get_own_ip()}:{self.tcp_port}"
        
        # Encode the message to bytes
        message_bytes = message.encode('utf-8')
        
        # Send the broadcast message to the broadcast address and discovery port
        self.udp_socket.sendto(message_bytes, ('255.255.255.255', self.discovery_port))
        
        # Close the socket
        self.udp_socket.close()

    def listen_for_discovery(self):
        """Continuously listen for UDP discovery messages."""
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Allow broadcast
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
        # Bind to the discovery port
        self.udp_socket.bind(('', self.discovery_port))
        
        try:
            while True:
                # Receive a message
                message, address = self.udp_socket.recvfrom(4096)
                # Handle the received message
                self.handle_discovery_message(message, address)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            # Close the socket
            self.udp_socket.close()

    def handle_discovery_message(self, message, address):
        """Process incoming discovery messages and update the peer list."""
        # Decode the incoming message
        decoded_message = message.decode('utf-8')
        
        # Parse the message to extract peer details
        # Assuming the message is in the format "Peer at <IP>:<Port>"
        if decoded_message.startswith("Peer at "):
            peer_info = decoded_message[len("Peer at "):].strip()
            peer_ip, peer_port = peer_info.split(':')
            peer_port = int(peer_port)
            
            # Check for duplicate entries in the peer list
            peer_exists = any(peer for peer in self.peer_list if peer['ip'] == peer_ip and peer['port'] == peer_port)
            
            if not peer_exists:
                # Update the peer list with the new peer
                self.peer_list.append({'ip': peer_ip, 'port': peer_port})
                
                # Optionally, log the new peer discovery
                logging.info(f"Discovered new peer: {peer_ip}:{peer_port}")
            else:
                logging.info(f"Peer {peer_ip}:{peer_port} is already in the peer list")

    def connect_to_peer(self, ip, port):
        """Establish a TCP connection to a given peer."""
        try:
            # Create a TCP socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the peer's IP address and port
            tcp_socket.connect((ip, port))
            
            # Add the connection to the active connections
            self.active_connections[(ip, port)] = tcp_socket
            
            # Optionally, log the successful connection
            logging.info(f"Connected to peer at {ip}:{port}")
            
        except Exception as e:
            # Handle connection errors
            logging.error(f"Failed to connect to peer at {ip}:{port}. Error: {e}")

    def accept_connections(self):
        """Accept incoming TCP connections and handle them."""
        try:
            # Create a TCP socket
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Bind the socket to the server's IP address and the TCP port
            self.tcp_socket.bind((self.get_own_ip(), self.tcp_port))
            
            # Listen for incoming connections
            self.tcp_socket.listen(5)  # The argument specifies the number of unaccepted connections that the system will allow before refusing new connections
            
            logging.info(f"Listening for incoming connections on port {self.tcp_port}")
            
            while True:
                # Accept a new connection
                client_socket, client_address = self.tcp_socket.accept()
                logging.info(f"Accepted connection from {client_address}")
                
                # Handle the connection in a new thread
                threading.Thread(target=self.handle_new_connection, args=(client_socket, client_address)).start()
        
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            # Close the socket if needed
            if self.tcp_socket:
                self.tcp_socket.close()

    def handle_new_connection(self, connection, address):
        """Handle a new connection, possibly creating a new thread or task."""
        logging.info(f"Handling new connection from {address}")
        # Create a new thread to handle the connection
        connection_thread = threading.Thread(target=self.connection_handler, args=(connection, address))
        connection_thread.start()

    def connection_handler(self, connection, address):
        """Handle communication with the connected peer."""
        try:
            while True:
                # Example: Receiving data from the connection
                data = connection.recv(4096)
                if not data:
                    break  # Connection closed by the peer
                # Process the received data (e.g., save it, forward it, etc.)
                logging.info(f"Received data from {address}: {data.decode('utf-8')}")
                
                # Example: Sending a response (if needed)
                response = f"Echo: {data.decode('utf-8')}"
                connection.sendall(response.encode('utf-8'))
        
        except Exception as e:
            logging.error(f"Error handling connection from {address}: {e}")
        
        finally:
            # Clean up the connection
            connection.close()
            logging.info(f"Connection from {address} closed")

    # Data Transmission Methods
    def send_data(self, connection, data):
        """Send data (e.g., file chunks, messages) over a TCP connection."""
        buffer_size = 4096  # Size of each chunk to be sent
        try:
            # Ensure data is in bytes
            if isinstance(data, str):
                data = data.encode('utf-8')  # Convert string to bytes
            for i in range(0, len(data), buffer_size):
                connection.sendall(data[i:i+buffer_size])
            logging.info(f"Data sent to {connection} successfully")
        
        except Exception as e:
            logging.error(f"An error occurred while sending data: {e}")

    def receive_data(self, connection):
        """Receive data from a TCP connection."""
        buffer_size = 4096 
        data_buffer = bytearray()  # Initialize a buffer to store incoming data

        try:
            while True:
                # Receive data in chunks
                chunk = connection.recv(buffer_size)
                if not chunk:
                    # If chunk is empty, the connection is closed
                    break
                data_buffer.extend(chunk)
        except Exception as e:
            logging.error(f"An error occurred while receiving data: {e}")

        # Return the complete data as bytes
        return bytes(data_buffer)

    def send_file(self, file_path, connection):
        """Send a file over a TCP connection, splitting it into chunks if necessary."""
        buffer_size = 4096  # Size of each chunk to be sent

        try:
            # Open the file in binary read mode
            with open(file_path, 'rb') as file:
                while True:
                    # Read a chunk of data from the file
                    data_chunk = file.read(buffer_size)
                    
                    # If the chunk is empty, end of file is reached
                    if not data_chunk:
                        break
                    
                    # Send the chunk over the connection
                    connection.sendall(data_chunk)
                    
            logging.info(f"File {file_path} sent successfully.")

        except Exception as e:
            logging.error(f"An error occurred while sending the file: {e}")

    def receive_file(self, destination_path, connection):
        """Receive a file over a TCP connection and save it to the specified path."""
        buffer_size = 4096  # Size of each chunk to be received

        try:
            # Open the destination file in binary write mode
            with open(destination_path, 'wb') as file:
                while True:
                    # Receive a chunk of data from the connection
                    data_chunk = connection.recv(buffer_size)
                    
                    # If the chunk is empty, the connection is closed
                    if not data_chunk:
                        break
                    
                    # Write the chunk to the file
                    file.write(data_chunk)
                    
            logging.info(f"File received successfully and saved to {destination_path}.")

        except Exception as e:
            logging.error(f"An error occurred while receiving the file: {e}")

    def handle_network_error(self, error):
        """Handle network-related errors or exceptions."""
        # Log the error
        logging.error(f"Network error occurred: {error}")

        # Close affected connections
        # This example assumes we have access to the connection that caused the error
        # You might need to pass the connection as an argument to this method
        for conn in self.active_connections.values():
            try:
                conn.close()
            except Exception as e:
                logging.error(f"Failed to close connection: {e}")

    def reconnect_peer(self, peer):
        """Attempt to reconnect to a peer if a connection is lost."""
        ip = peer.get('ip')
        port = peer.get('port')
        retries = 5  # Number of reconnection attempts
        delay = 5  # Delay in seconds between attempts

        for attempt in range(1, retries + 1):
            try:
                logging.info(f"Attempting to reconnect to {ip}:{port} (Attempt {attempt}/{retries})")
                self.connect_to_peer(ip, port)
                logging.info(f"Successfully reconnected to {ip}:{port}")
                return  # Exit the method if reconnection is successful
            except Exception as e:
                logging.error(f"Reconnection attempt {attempt} failed: {e}")
                time.sleep(delay)

        logging.error(f"Failed to reconnect to {ip}:{port} after {retries} attempts")

    # Utility Functions
    def get_peer_list(self):
        """Return the list of known peers."""
        return self.peer_list

    def update_peer_list(self, peer_info):
        """
        Update the list of known peers with new peer information.
        
        Args:
            peer_info (dict): Dictionary containing 'ip' and 'port' of the peer.
        """
        # Ensure peer_info is in the correct format
        if not isinstance(peer_info, dict) or 'ip' not in peer_info or 'port' not in peer_info:
            raise ValueError("peer_info must be a dictionary with 'ip' and 'port' keys.")
        
        # Check for duplicates before adding
        peer_exists = any(peer for peer in self.peer_list if peer['ip'] == peer_info['ip'] and peer['port'] == peer_info['port'])
        
        if not peer_exists:
            self.peer_list.append(peer_info)
            logging.info(f"Added new peer: {peer_info}")
        else:
            logging.info(f"Peer {peer_info} is already in the peer list")

    def close_connections(self):
        """Close all active connections and sockets gracefully."""
        # Close all active connections
        for conn in self.active_connections.values():
            try:
                conn.close()
            except Exception as e:
                logging.error(f"Error closing connection: {e}")
        
        # Clear the active connections dictionary
        self.active_connections.clear()

        # Close the UDP socket if it exists
        if self.udp_socket:
            try:
                self.udp_socket.close()
            except Exception as e:
                logging.error(f"Error closing UDP socket: {e}")

        # Close the TCP socket if it exists
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
            except Exception as e:
                logging.error(f"Error closing TCP socket: {e}")

        logging.info("All connections and sockets closed.")

    @staticmethod
    def get_own_ip():
        """Utility method to get the own IP address."""
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp_socket.connect(("8.8.8.8", 80))
            ip_address = temp_socket.getsockname()[0]
        except Exception as e:
            logging.error(f"Error determining local IP: {e}")
            ip_address = "127.0.0.1"
        finally:
            temp_socket.close()
        
        return ip_address
