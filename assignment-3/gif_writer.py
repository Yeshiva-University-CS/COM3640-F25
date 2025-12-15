"""
GIF Writer Module
Writes GIF files from a generator yielding metadata and rows of RGB tuples.
Uses PIL/Pillow library for GIF encoding, which handles color quantization automatically.

Note: Unlike BMP writer which can stream, GIF requires buffering the entire
image due to LZW compression requirements.
"""

def write_gif(filename):
    """
    Curried function that returns a writer which consumes a row generator
    and writes a GIF file.
      
    Args:
        filename: Path to output GIF file  
    """
    pass

