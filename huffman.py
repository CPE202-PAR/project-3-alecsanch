import os
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
        """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
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
    if comes_before(a, b):
        return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
    else:
        return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)


def cnt_freq(filename: str) -> List[int]:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    freq_list = [0] * 256
    try:
        with open(filename, 'r') as file:
            for line in file:
                for char in line:
                    freq_list[ord(char)] += 1
    except FileNotFoundError:
        print(f"File not found: {filename}")
        pass
    return freq_list


def create_huff_tree(char_freq: List[int]) -> HTree:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    nodes = [HuffmanNode(i, freq) for i, freq in enumerate(char_freq) if freq > 0]

    while len(nodes) > 1:
        nodes.sort(key=lambda x: (x.freq, x.char_ascii))
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = combine(left, right)
        nodes.append(parent)

    return nodes[0] if nodes else None


def create_code(node: HTree) -> List[str]:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    if node is None:
        return [''] * 256
    codes = [''] * 256

    def traverse(current_node: HuffmanNode, current_code: str) -> None:
        if current_node.left is None and current_node.right is None:
            codes[current_node.char_ascii] = current_code
        if current_node.left:
            traverse(current_node.left, current_code + '0')
        if current_node.right:
            traverse(current_node.right, current_code + '1')

    traverse(node, '')
    return codes


def create_header(freqs: List[int]) -> str:
    """Creates and returns a header for the output file"""
    header = []
    for i, freq in enumerate(freqs):
        if freq != 0:
            header.extend([str(i), str(freq)])
    return ' '.join(header)


def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes input file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""
    freqs = cnt_freq(in_file)
    header = create_header(freqs)
    with open(out_file, 'w', newline='') as file:
        file.write(header + '\n')
        tree = create_huff_tree(freqs)
        if tree is None:
            return
        codes = create_code(tree)
        with open(in_file, 'r') as input_file:
            for line in input_file:
                for char in line:
                    if 0 <= ord(char) < 256:
                        file.write(codes[ord(char)])
                    else:
                        print(f"Ignoring character: {char} (Not in valid ASCII range)")


def huffman_decode(encoded_file: str, decode_file: str) -> None:
    """Reads an encoded file and writes the decoded text to an output file using the recreated Huffman tree."""
    # Check if the encoded file exists
    if not os.path.exists(encoded_file):
        raise FileNotFoundError(f"Encoded file not found: {encoded_file}")

    try:
        # Read encoded file
        with open(encoded_file, 'r') as file:
            # Read header
            header = file.readline().strip()
            # Parse header to create list of frequencies
            freq_list = parse_header(header)
            # Recreate Huffman tree
            huffman_tree = create_huff_tree(freq_list)

            # Open output file for writing decoded text
            with open(decode_file, 'w') as output_file:
                # Start with root node
                current_node = huffman_tree

                # Read remaining lines (encoded text) from file
                for line in file:
                    # Iterate over characters in line
                    for char in line.strip():
                        # Navigate Huffman tree based on encoded bits
                        if char == '0':
                            current_node = current_node.left
                        elif char == '1':
                            current_node = current_node.right

                        # Check if leaf node is reached
                        if current_node.left is None and current_node.right is None:
                            # Write decoded character to output file
                            output_file.write(chr(current_node.char_ascii))
                            # Reset current_node to root for next character
                            current_node = huffman_tree

    except FileNotFoundError:
        print(f"Error decoding: {encoded_file}")
        raise


def parse_header(header_string: str) -> List[int]:
    """Parses the header string to create a list of frequencies."""
    freq_list = [0] * 256
    header_list = header_string.split()
    try:
        for i in range(0, len(header_list), 2):
            char_ascii = int(header_list[i])
            freq = int(header_list[i + 1])
            freq_list[char_ascii] = freq
    except (ValueError, IndexError):
        raise ValueError("Malformed header string.")
    return freq_list
