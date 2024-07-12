class Peer:
    def __init__(self, peer_id, ip_address, port):
        """Initialize the peer with an ID, IP address, and port."""
        self.peer_id = peer_id
        self.ip_address = ip_address
        self.port = port
        self.status = 'active'
        self.last_seen = None
        self.shared_files = []

    def update_status(self, status):
        """Update the status of the peer."""
        self.status = status

    def add_shared_file(self, file):
        """Add a file to the peer's shared files list."""
        self.shared_files.append(file)

    def remove_shared_file(self, file):
        """Remove a file from the peer's shared files list."""
        if file in self.shared_files:
            self.shared_files.remove(file)

    def get_shared_files(self):
        """Retrieve the list of shared files."""
        return self.shared_files

    def update_last_seen(self, timestamp):
        """Update the last seen timestamp."""
        self.last_seen = timestamp

    def to_dict(self):
        """Convert the peer's information to a dictionary format."""
        return {
            'peer_id': self.peer_id,
            'ip_address': self.ip_address,
            'port': self.port,
            'status': self.status,
            'last_seen': self.last_seen,
            'shared_files': self.shared_files
        }
