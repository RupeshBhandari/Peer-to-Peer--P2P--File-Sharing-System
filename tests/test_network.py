import unittest
import socket
import threading, sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.network import Network

class TestNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up any state that is shared across tests."""
        cls.discovery_port = 12345
        cls.tcp_port = 54321
        cls.network = Network(cls.discovery_port, cls.tcp_port)

    def setUp(self):
        """Clear the peer list and active connections before each test."""
        self.network.peer_list = []
        self.network.active_connections = {}

    def test_initialization(self):
        """Test initialization of the Network class."""
        self.assertEqual(self.network.discovery_port, self.discovery_port)
        self.assertEqual(self.network.tcp_port, self.tcp_port)
        self.assertEqual(self.network.peer_list, [])
        self.assertEqual(self.network.active_connections, {})

    @patch('socket.socket')
    def test_broadcast_presence(self, mock_socket):
        """Test broadcasting presence."""
        mock_socket_inst = mock_socket.return_value
        self.network.get_own_ip = MagicMock(return_value='127.0.0.1')

        self.network.broadcast_presence()

        mock_socket_inst.setsockopt.assert_called_with(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mock_socket_inst.sendto.assert_called()
        mock_socket_inst.close.assert_called()

    @patch('socket.socket')
    def test_listen_for_discovery(self, mock_socket):
        """Test listening for peer discovery."""
        mock_socket_inst = mock_socket.return_value
        mock_socket_inst.recvfrom.return_value = (b'Peer at 127.0.0.1:54321', ('127.0.0.1', 54321))

        def stop_listening(*args, **kwargs):
            self.network.udp_socket.close()
            raise Exception("Stop listening")

        mock_socket_inst.recvfrom.side_effect = stop_listening

        with self.assertRaises(Exception) as context:
            self.network.listen_for_discovery()

        self.assertEqual(str(context.exception), "Stop listening")

    def test_handle_discovery_message(self):
        """Test handling discovery messages."""
        message = b'Peer at 127.0.0.1:54321'
        address = ('127.0.0.1', 54321)

        self.network.handle_discovery_message(message, address)

        self.assertIn({'ip': '127.0.0.1', 'port': 54321}, self.network.peer_list)

    @patch('socket.socket')
    def test_connect_to_peer(self, mock_socket):
        """Test connecting to a peer."""
        mock_socket_inst = mock_socket.return_value
        self.network.connect_to_peer('127.0.0.1', 54321)

        mock_socket_inst.connect.assert_called_with(('127.0.0.1', 54321))
        self.assertIn(('127.0.0.1', 54321), self.network.active_connections)

    @patch('socket.socket')
    def test_accept_connections(self, mock_socket):
        """Test accepting connections."""
        mock_socket_inst = mock_socket.return_value
        mock_socket_inst.accept.return_value = (mock_socket_inst, ('127.0.0.1', 54321))

        def stop_accepting(*args, **kwargs):
            self.network.tcp_socket.close()
            raise Exception("Stop accepting")

        mock_socket_inst.accept.side_effect = stop_accepting

        with self.assertRaises(Exception) as context:
            self.network.accept_connections()

        self.assertEqual(str(context.exception), "Stop accepting")

    def test_send_data(self):
        """Test sending data."""
        connection = MagicMock()
        data = "Hello, World!"

        self.network.send_data(connection, data)

        connection.sendall.assert_called()

    def test_receive_data(self):
        """Test receiving data."""
        connection = MagicMock()
        connection.recv.side_effect = [b'Hello', b', World!', b'']

        result = self.network.receive_data(connection)

        self.assertEqual(result, b'Hello, World!')

    def test_send_file(self):
        """Test sending a file."""
        connection = MagicMock()
        test_file_path = 'test_file.txt'

        with open(test_file_path, 'wb') as f:
            f.write(b'This is a test file.')

        self.network.send_file(test_file_path, connection)

        connection.sendall.assert_called()
        os.remove(test_file_path)

    def test_receive_file(self):
        """Test receiving a file."""
        connection = MagicMock()
        connection.recv.side_effect = [b'This is ', b'a test file.', b'']
        destination_path = 'received_test_file.txt'

        self.network.receive_file(destination_path, connection)

        with open(destination_path, 'rb') as f:
            content = f.read()

        self.assertEqual(content, b'This is a test file.')
        os.remove(destination_path)

if __name__ == '__main__':
    unittest.main()
