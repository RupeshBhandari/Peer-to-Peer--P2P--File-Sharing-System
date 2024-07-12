import hashlib
import os

class File:
    
    BUFFER_SIZE = 1000
    
    def __init__(self, file_path) -> None:
        """
        Initialize the File object with the given file path.

        Args:
            file_path (str): The path to the file.
        """
        self.validate_file(file_path)
        self.file_path = file_path
        self.file_name = self.get_file_name()
        self.file_size = self.get_file_size()
        self.file_type = self.get_file_type()
        self.file_hash = self.calculate_hash()
        self.chunks = []
        self.availability = "available"
        
    @staticmethod
    def validate_file(file_path, check_write_access=True) -> None:
        """
        Validate the given file path.

        Args:
            file_path (str): The path to the file.
            check_write_access (bool): Whether to check if the file is writable. Defaults to True.

        Raises:
            ValueError: If the file does not exist, is not readable, or is not writable.
        """
        # Check file existence
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_path} doesn't exist.")
        
        # Check read access
        if not os.access(file_path, os.R_OK):
            raise ValueError(f"File {file_path} is not readable.")
        
        # Check write access (optional)
        if check_write_access and not os.access(file_path, os.W_OK):
            raise ValueError(f"File {file_path} is not writable.")
    
    def get_file_name(self) -> str:
        """Get the name of the file."""
        return os.path.basename(self.file_path)
    
    def get_file_size(self) -> int:
        """Get the size of the file in bytes."""
        return os.path.getsize(self.file_path)
    
    def get_file_type(self) -> str:
        """Get the file extension."""
        return os.path.splitext(self.file_name)[1]
    
    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the file.

        Returns:
            str: The SHA-256 hash of the file.
        """
        hasher = hashlib.sha256()
        with open(file=self.file_path, mode='rb') as f:
            while True:
                chunk = f.read(self.BUFFER_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def split_into_chunks(self) -> None:
        """Split the file into chunks of BUFFER_SIZE."""
        with open(file=self.file_path, mode='rb') as f:
            while True:
                chunk = f.read(File.BUFFER_SIZE)
                if not chunk:
                    break
                self.chunks.append(chunk)
        
    def combine_chunks(self, output_path) -> None:
        """
        Combine chunks and write them to the specified output file.

        Args:
            output_path (str): The path to the output file.
        """
        with open(file=output_path, mode='wb') as f:
            for chunk in self.chunks:
                f.write(chunk)
    
    def __str__(self) -> str:
        """Return a string representation of the File object."""
        return (f"File: {self.file_name}\n"
                f"Path: {self.file_path}\n"
                f"Size: {self.file_size} bytes\n"
                f"Hash: {self.file_hash}")
    
    @classmethod
    def change_buffer_size(cls, new_buffer_size):
        """
        Change the buffer size for reading the file.

        Args:
            new_buffer_size (int): The new buffer size in bytes.
        """
        cls.BUFFER_SIZE = new_buffer_size
