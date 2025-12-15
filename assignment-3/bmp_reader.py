"""
BMP Reader Module
Reads BMP files and yields metadata followed by rows of RGB tuples.
Supports 8 and 24-bit BMPs.
"""

def read_bmp(filename):
    """
    Generator that reads a BMP file and yields:
    1. First: metadata dictionary with 'width', 'height', 'bit_depth'
    2. Then: rows of RGB tuples [(R,G,B), (R,G,B), ...]
    
    Args:
        filename: Path to BMP file
    """
    pass


