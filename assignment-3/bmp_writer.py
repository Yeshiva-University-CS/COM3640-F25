"""
BMP Writer Module
Writes BMP files from a generator yielding metadata and rows of RGB tuples.
Supports 8-bit indexed and 24-bit RGB output.
"""


def write_bmp(bit_depth, filename):
    """
    Curried function that returns a writer which consumes a row generator
    and writes a BMP file.
      
    Args:
        bit_depth: Output bit depth (8 for indexed, 24 for RGB)
        filename: Path to output BMP file
    """
    pass



