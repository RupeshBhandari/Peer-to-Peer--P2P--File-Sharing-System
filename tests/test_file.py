import unittest
import os
import sys
import hashlib
import stat

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file import File

class TestFile(unittest.TestCase):
    
    def setUp(self):
        # Define paths to test files
        self.test_readable_file_path = os.path.join('tests', 'resources', 'readable_file.txt')
        self.test_non_readable_file_path = os.path.join('tests', 'resources', 'non_readable_file.txt')
        
        # Create a sample readable file for testing
        with open(self.test_readable_file_path, 'w') as f:
            f.write('This is a test file for unit testing.')
        
        # Create a File object for testing
        self.file = File(self.test_readable_file_path)
    
    def tearDown(self):
        # Remove test files after testing
        if os.path.exists(self.test_readable_file_path):
            os.remove(self.test_readable_file_path)
        if os.path.exists(self.test_non_readable_file_path):
            os.remove(self.test_non_readable_file_path)
    
    def test_initialization(self):
        self.assertEqual(self.file.file_path, self.test_readable_file_path)
        self.assertEqual(self.file.file_name, 'readable_file.txt')
        self.assertEqual(self.file.file_size, os.path.getsize(self.test_readable_file_path))
        self.assertEqual(self.file.file_type, '.txt')
    
    def test_validate_file(self):
        # Test valid file
        self.assertIsNone(File.validate_file(self.test_readable_file_path))
        
        # Test non-existent file
        with self.assertRaises(ValueError):
            File.validate_file('non_existent_file.txt')
        
        # Test non-readable file (Windows specific using stat module)
        with open(self.test_non_readable_file_path, 'w') as f:
            f.write('Content')
        os.chmod(self.test_non_readable_file_path, stat.S_IREAD)  # Set file to read-only
        with self.assertRaises(ValueError):
            File.validate_file(self.test_non_readable_file_path)
        os.chmod(self.test_non_readable_file_path, stat.S_IWRITE)  # Make file writable again for cleanup
    
    def test_get_file_name(self):
        self.assertEqual(self.file.get_file_name(), 'readable_file.txt')

    def test_get_file_size(self):
        self.assertEqual(self.file.get_file_size(), os.path.getsize(self.test_readable_file_path))

    def test_get_file_type(self):
        self.assertEqual(self.file.get_file_type(), '.txt')

    def test_calculate_hash(self):
        expected_hash = hashlib.sha256(b'This is a test file for unit testing.').hexdigest()
        self.assertEqual(self.file.calculate_hash(), expected_hash)

    def test_split_into_chunks(self):
        self.file.split_into_chunks()
        expected_chunks = [b'This is a test file for unit testing.']
        self.assertEqual(self.file.chunks, expected_chunks)

    def test_combine_chunks(self):
        self.file.split_into_chunks()
        output_path = os.path.join('tests', 'resources', 'combined_test_file.txt')
        self.file.combine_chunks(output_path)
        with open(output_path, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'This is a test file for unit testing.')
        os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
