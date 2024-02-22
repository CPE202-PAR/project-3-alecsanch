from typing import List, Union, Optional

HTree = Union[None, 'HuffmanNode']


class HuffmanNode:
    char_ascii: int
    freq: int
    left: HTree = None
    right: HTree = None

    def __init__(self, char_ascii: int, freq: int, left: HTree = None, right: HTree = None):
        self.char_ascii = char_ascii
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: 'HuffmanNode') -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    if a.freq != b.freq:
        return a.freq < b.freq
    else:
        return a.char_ascii < b.char_ascii


def combine(a: Optional[HuffmanNode], b: Optional[HuffmanNode]) -> HuffmanNode:
    if a is None:
        if b is None:
            raise ValueError("Both arguments cannot be None")
        return b
    elif b is None:
        return a
    if comes_before(a, b):
        return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
    else:
        return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)


def cnt_freq(filename: str) -> List[int]:
    frequencies = [0] * 256
    try:
        with open(filename, 'r') as file:
            file_contents = file.read()
            if not file_contents:
                raise ValueError("Input file is empty.")
            for char in file_contents:
                frequencies[ord(char)] += 1
    except FileNotFoundError:
        raise FileNotFoundError("File not found!")
    return frequencies


def create_huff_tree(char_freq: List[int]) -> Optional[HuffmanNode]:
    if all(freq == 0 for freq in char_freq):
        return None
    nodes = [HuffmanNode(i, char_freq[i]) for i in range(256) if char_freq[i] > 0]
    while len(nodes) > 1:
        nodes.sort()
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = combine(left, right)
        nodes.append(parent)
    return nodes[0] if nodes else None


def create_code(node: Union[None, HuffmanNode]) -> List[str]:
    if node is None:
        return [''] * 256

    def traverse(node: HuffmanNode, code: str, codes: List[str]) -> None:
        if node is None:
            return
        if node.char_ascii is not None:
            codes[node.char_ascii] = code
        traverse(node.left, code + '0', codes) if node.left is not None else None
        traverse(node.right, code + '1', codes) if node.right is not None else None

    codes = [''] * 256
    traverse(node, '', codes)
    return codes


def create_header(freqs: List[int]) -> str:
    header = []
    for i in range(256):
        if freqs[i] > 0:
            header.append(str(i))
            header.append(str(freqs[i]))
    return ' '.join(header)


def huffman_encode(in_file: str, out_file: str) -> None:
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
