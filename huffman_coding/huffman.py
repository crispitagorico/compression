import heapq
from collections import Counter


class HuffmanCoding:
    class Node:
        """Represents a node in the Huffman Tree."""
        def __init__(self, char=None, freq=0):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self):
        self.huffman_dict = {}
        self.reverse_huffman_dict = {}

    def create_huffman_tree(self, frequency):
        """Create the Huffman Tree based on character frequencies."""
        heap = [self.Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = self.Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0]

    def create_dictionary(self, root):
        """Create a Huffman dictionary from the tree."""
        self.huffman_dict = {}

        def traverse_tree(node, code):
            if node:
                if node.char is not None:
                    self.huffman_dict[node.char] = code
                traverse_tree(node.left, code + "0")
                traverse_tree(node.right, code + "1")

        traverse_tree(root, "")
        self.reverse_huffman_dict =\
            {v: k for k, v in self.huffman_dict.items()}
        return self.huffman_dict

    def compress(self, stream):
        """Compress the input stream using Huffman coding."""
        frequency = Counter(stream)
        root = self.create_huffman_tree(frequency)
        self.create_dictionary(root)
        compressed = ''.join(self.huffman_dict[char] for char in stream)
        return compressed

    def get_dictionary(self):
        """Returns the current Huffman dictionary."""
        return self.huffman_dict

    def decode(self, encoded_data):
        """Decode the encoded data back to the original stream\
            using the Huffman dictionary."""
        decoded_output = []
        current_code = ""

        for bit in encoded_data:
            current_code += bit
            if current_code in self.reverse_huffman_dict:
                decoded_output.append(self.reverse_huffman_dict[current_code])
                current_code = ""

        return ''.join(decoded_output)


# Example usage:
if __name__ == "__main__":
    stream = "Walk with a pair of lovers beneath a starry night.\
        Look up at swirling clouds and cypress trees swaying in the wind.\
            Stay a little while in Van Gogh’s favourite park,\
                the ‘Poet’s Garden’, or under a shady tree in Saint-Rémy."
    huffman = HuffmanCoding()
    compressed_stream = huffman.compress(stream)
    print("Huffman Dictionary:", huffman.get_dictionary())
    print("Compressed Stream:", compressed_stream)
    decoded_stream = huffman.decode(compressed_stream)
    print("Decoded Stream:", decoded_stream)
    assert stream == decoded_stream, \
        "The decoded stream doesn't match the original!"
