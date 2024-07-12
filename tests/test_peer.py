import unittest, sys, os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.peer import Peer

class TestPeer(unittest.TestCase):

    def setUp(self):
        """Set up a peer instance for testing."""
        self.peer = Peer(peer_id="12345", ip_address="192.168.1.2", port=54321)

    def test_initialization(self):
        """Test the initialization of the Peer class."""
        self.assertEqual(self.peer.peer_id, "12345")
        self.assertEqual(self.peer.ip_address, "192.168.1.2")
        self.assertEqual(self.peer.port, 54321)
        self.assertEqual(self.peer.status, "active")
        self.assertIsNone(self.peer.last_seen)
        self.assertEqual(self.peer.shared_files, [])

    def test_update_status(self):
        """Test updating the peer's status."""
        self.peer.update_status("inactive")
        self.assertEqual(self.peer.status, "inactive")

    def test_add_shared_file(self):
        """Test adding a shared file."""
        self.peer.add_shared_file("file1.txt")
        self.assertIn("file1.txt", self.peer.shared_files)

    def test_remove_shared_file(self):
        """Test removing a shared file."""
        self.peer.add_shared_file("file1.txt")
        self.peer.remove_shared_file("file1.txt")
        self.assertNotIn("file1.txt", self.peer.shared_files)

    def test_get_shared_files(self):
        """Test retrieving the list of shared files."""
        self.peer.add_shared_file("file1.txt")
        self.peer.add_shared_file("file2.txt")
        shared_files = self.peer.get_shared_files()
        self.assertIn("file1.txt", shared_files)
        self.assertIn("file2.txt", shared_files)

    def test_update_last_seen(self):
        """Test updating the last seen timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.peer.update_last_seen(timestamp)
        self.assertEqual(self.peer.last_seen, timestamp)

    def test_to_dict(self):
        """Test converting the peer's information to a dictionary format."""
        self.peer.add_shared_file("file1.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.peer.update_last_seen(timestamp)
        peer_dict = self.peer.to_dict()
        self.assertEqual(peer_dict["peer_id"], "12345")
        self.assertEqual(peer_dict["ip_address"], "192.168.1.2")
        self.assertEqual(peer_dict["port"], 54321)
        self.assertEqual(peer_dict["status"], "active")
        self.assertEqual(peer_dict["last_seen"], timestamp)
        self.assertIn("file1.txt", peer_dict["shared_files"])

if __name__ == '__main__':
    unittest.main()
