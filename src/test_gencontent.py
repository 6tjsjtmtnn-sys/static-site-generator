import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        
    def test_invalid_h1(self):
        with self.assertRaises(Exception):
            extract_title("Hello")
            
    def test_no_h1_only_h2(self):
        with self.assertRaises(Exception):
            extract_title("## Subtitle")