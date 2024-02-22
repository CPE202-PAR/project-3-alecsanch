import unittest
from huffman import *


class TestList(unittest.TestCase):
    def test_cnt_freq(self) -> None:
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

    def test_combine(self) -> None:
        a = HuffmanNode(65, 1)
        b = HuffmanNode(66, 2)

        # Test for the case when a is returned
        c = combine(a, None)
        self.assertEqual(c.char_ascii, a.char_ascii)
        self.assertEqual(c.freq, a.freq)
        self.assertIsNone(c.left)
        self.assertIsNone(c.right)

        # Test for the case when b is returned
        c = combine(None, b)
        self.assertEqual(c.char_ascii, b.char_ascii)
        self.assertEqual(c.freq, b.freq)
        self.assertIsNone(c.left)
        self.assertIsNone(c.right)

        # Test for the case when a is returned
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:
            self.fail("Failed to create Huffman node with children a and b")

        # Test for the case when b is returned
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:
            self.fail("Failed to create Huffman node with children b and a")

    def test_create_header(self) -> None:
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self) -> None:
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1_out.txt", "file1_soln.txt"))

    def test_combine_01(self) -> None:
        a = HuffmanNode(65, 1)
        b = HuffmanNode(66, 2)
        c = combine(a, b)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:
            self.fail("Failed to create Huffman node with children a and b")

        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:
            self.fail("Failed to create Huffman node with children b and a")

    def test_cnt_freq_file_not_found(self) -> None:
        # Call the function with a non-existent file
        with self.assertRaises(FileNotFoundError):
            cnt_freq("nonexistent_file.txt")

    def test_create_huff_tree_empty(self):
        # Test with empty character frequencies list
        char_freq = [0] * 256
        root = create_huff_tree(char_freq)
        self.assertIsNone(root)

    def test_create_huff_tree_single_char(self):
        # Test with only one character having non-zero frequency
        char_freq = [0] * 256
        char_freq[97] = 5  # Character 'a' with frequency 5
        root = create_huff_tree(char_freq)
        self.assertIsInstance(root, HuffmanNode)
        self.assertEqual(root.freq, 5)

    def test_create_huff_tree_multiple_chars(self):
        # Test with multiple characters
        char_freq = [0] * 256
        char_freq[97] = 5  # Character 'a' with frequency 5
        char_freq[98] = 3  # Character 'b' with frequency 3
        char_freq[99] = 7  # Character 'c' with frequency 7
        root = create_huff_tree(char_freq)
        self.assertIsInstance(root, HuffmanNode)
        self.assertEqual(root.freq, 15)  # Total frequency
        self.assertEqual(root.char_ascii, 99)  # ASCII value of character 'c'
        self.assertIsNotNone(root.left)
        self.assertIsNotNone(root.right)

# Compare files - takes care of CR/LF, LF issues
def compare_files(file1: str, file2: str) -> bool:  # pragma: no cover
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match


if __name__ == '__main__':
    unittest.main()
