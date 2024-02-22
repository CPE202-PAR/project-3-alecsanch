import unittest
from huffman import *


class TestHuffman(unittest.TestCase):
    def test_cnt_freq(self) -> None:
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

    def test_combine(self) -> None:
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
        else:  # pragma: no cover
            self.fail()
        c = combine(b, a)
        if (c.left is not None) and (c.right is not None):
            self.assertEqual(c.left.char_ascii, 65)
            self.assertEqual(c.left.freq, 1)
            self.assertEqual(c.right.char_ascii, 66)
            self.assertEqual(c.right.freq, 2)
            self.assertEqual(c.char_ascii, 65)
            self.assertEqual(c.freq, 3)
        else:  # pragma: no cover
            self.fail()

    def test_create_huff_tree(self) -> None:
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        if hufftree is not None:
            self.assertEqual(hufftree.freq, 32)
            self.assertEqual(hufftree.char_ascii, 97)
            left = hufftree.left
            right = hufftree.right
            if (left is not None) and (right is not None):
                self.assertEqual(left.freq, 16)
                self.assertEqual(left.char_ascii, 97)
                self.assertEqual(right.freq, 16)
                self.assertEqual(right.char_ascii, 100)
            else:  # pragma: no cover
                self.fail()
        else:  # pragma: no cover
            self.fail()

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

    def test__lt__(self) -> None:
        # Test when self node has lower frequency
        node_a = HuffmanNode(97, 1)
        node_b = HuffmanNode(98, 2)
        self.assertTrue(node_a < node_b)

        # Test when other node has lower frequency
        node_c = HuffmanNode(99, 3)
        node_d = HuffmanNode(100, 2)
        self.assertFalse(node_c < node_d)

        # Test when nodes have equal frequency but different ASCII values
        node_e = HuffmanNode(101, 2)
        node_f = HuffmanNode(102, 2)
        self.assertTrue(node_e < node_f)
        self.assertFalse(node_f < node_e)

        # Test when nodes have equal frequency and ASCII values
        node_g = HuffmanNode(103, 2)
        node_h = HuffmanNode(103, 2)
        self.assertFalse(node_g < node_h)
        self.assertFalse(node_h < node_g)

    def test_cnt_freq_01(self) -> None:
        # Test with a sample file
        filename = "sample.txt"
        expected_freq_list = [0] * 256
        expected_freq_list[97] = 2  # ASCII value of 'a'
        expected_freq_list[98] = 1  # ASCII value of 'b'
        expected_freq_list[99] = 3  # ASCII value of 'c'
        expected_freq_list[100] = 1  # ASCII value of 'd'

        with open(filename, "w") as file:
            file.write("aacccbd")

        freq_list = cnt_freq(filename)

        self.assertEqual(len(freq_list), 256)
        self.assertEqual(freq_list, expected_freq_list)

    def test_cnt_freq_empty_file(self) -> None:
        # Test with an empty file
        filename = "empty.txt"
        expected_freq_list = [0] * 256

        with open(filename, "w") as file:
            file.write("")

        freq_list = cnt_freq(filename)

        self.assertEqual(len(freq_list), 256)
        self.assertEqual(freq_list, expected_freq_list)

    def test_cnt_freq_nonexistent_file(self) -> None:
        # Test with a nonexistent file
        filename = "nonexistent_file.txt"

        freq_list = cnt_freq(filename)

        self.assertEqual(len(freq_list), 256)
        self.assertEqual(freq_list, [0] * 256)

    def test_create_code_empty_tree(self) -> None:
        # Test with an empty tree
        tree: HTree = None
        expected_codes = [''] * 256

        codes = create_code(tree)

        self.assertEqual(codes, expected_codes)

    #def test_cnt_freq_file_not_found(self) -> None:
        # Test with a file that does not exist
        #filename = "nonexistent_file.txt"

        # Ensure FileNotFoundError is raised
        #with self.assertRaises(FileNotFoundError):
            #cnt_freq(filename)


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
