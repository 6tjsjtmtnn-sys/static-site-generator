import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

            blocks = markdown_to_blocks(md)
            self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
            

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
        
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        result = block_to_block_type("# this is an h1")
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        result = block_to_block_type("```\n this is a code \n```")
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        result = block_to_block_type("> this is a quote")
        self.assertEqual(result, BlockType.QUOTE)

    def test_ul(self):
        result = block_to_block_type("- this is an ul -")
        self.assertEqual(result, BlockType.UNORDERED_LIST)
        
    def test_ol(self):
        result = block_to_block_type("1. this is an ol\n2. this is an ol\n3. this is an ol")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_p(self):
        result = block_to_block_type("this is a p")
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    



if __name__ == "__main__":
    unittest.main()