from dataclasses import dataclass
from typing import List, Union, TypeAlias

HTree: TypeAlias = Union[None, 'HuffmanNode']


@dataclass
class HuffmanNode:
    char_ascii: int  # stored as an integer - the ASCII character code value
    freq: int  # the frequency associated with the node
    left: HTree = None  # Huffman tree (node) to the left
    right: HTree = None  # Huffman tree (node) to the right

    def __lt__(self, other: 'HuffmanNode') -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq != b.freq:
        return a.freq < b.freq
    else:
        return a.char_ascii < b.char_ascii


def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""
    if a is None:
        return b
    elif b is None:
        return a
    if comes_before(a, b):  # Check if a comes before b
        return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
    else:
        return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)


def cnt_freq(filename: str) -> List[int]:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    frequencies = [0] * 256
    try:
        with open(filename, 'r') as file:
            for line in file:
                for char in line:
                    frequencies[ord(char)] += 1
    except FileNotFoundError:
        pass  # Handle file not found error
    return frequencies


def create_huff_tree(char_freq: List[int]) -> HTree:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    nodes = [HuffmanNode(i, char_freq[i]) for i in range(256) if char_freq[i] > 0]
    while len(nodes) > 1:
        nodes.sort()
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = combine(left, right)
        nodes.append(parent)
    if nodes:
        return nodes[0]
    else:
        return None


def create_code(node: HTree) -> List[str]:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    def traverse(node, code, codes):
        """Helper function to traverse the Huffman tree and generate codes"""
        if node:
            if node.char_ascii is not None:
                codes[node.char_ascii] = code
            traverse(node.left, code + '0', codes)
            traverse(node.right, code + '1', codes)

    codes = [''] * 256
    traverse(node, '', codes)
    return codes


def create_header(freqs: List[int]) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header = []
    for i in range(256):
        if freqs[i] > 0:
            header.append(str(i))
            header.append(str(freqs[i]))
    return ' '.join(header)


def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""
    freqs = cnt_freq(in_file)
    header = create_header(freqs)
    with open(out_file, 'w', newline='') as file:
        file.write(header + '\n')
        codes = create_code(create_huff_tree(freqs))
        with open(in_file, 'r') as input_file:
            for line in input_file:
                for char in line:
                    file.write(codes[ord(char)])
