"""
BMP Reader Utility Functions
Helper functions for reading and parsing BMP file structures.
"""

import struct


def read_bmp_headers(f):
    """
    Read BMP file header and DIB header from file.
    
    Args:
        f: File object opened in binary read mode
        
    Returns:
        Tuple of (pixel_offset, dib_header_size, width, height, bit_depth, top_down)
        
    Raises:
        ValueError: If file is not a valid BMP
    """
    # Read BMP file header (14 bytes)
    header = f.read(14)
    if header[0:2] != b'BM':
        raise ValueError("Not a valid BMP file")
    
    pixel_offset = struct.unpack('<I', header[10:14])[0]
    
    # Read DIB header size
    dib_header_size = struct.unpack('<I', f.read(4))[0]
    f.seek(14)  # Go back to read full DIB header
    dib_header = f.read(dib_header_size)
    
    # Parse DIB header
    width = struct.unpack('<i', dib_header[4:8])[0]
    height = struct.unpack('<i', dib_header[8:12])[0]
    bit_depth = struct.unpack('<H', dib_header[14:16])[0]
    
    # Handle negative height (top-down bitmap)
    top_down = height < 0
    height = abs(height)
    
    return pixel_offset, dib_header_size, width, height, bit_depth, top_down


def read_color_table(f, dib_header_size, bit_depth):
    """
    Read color table (palette) for indexed color formats.
    
    Args:
        f: File object opened in binary read mode
        dib_header_size: Size of the DIB header (determines where color table starts)
        bit_depth: Bits per pixel (only reads table for bit_depth <= 8)
        
    Returns:
        List of (R, G, B) tuples, or None if not an indexed format
    """
    if bit_depth > 8:
        return None
    
    num_colors = 2 ** bit_depth
    f.seek(14 + dib_header_size)
    color_table = []
    for _ in range(num_colors):
        b, g, r, reserved = struct.unpack('BBBB', f.read(4))
        color_table.append((r, g, b))
    
    return color_table


def calculate_row_size(width, bit_depth):
    """
    Calculate the size of a row in bytes, including padding to 4-byte boundary.
    
    Args:
        width: Image width in pixels
        bit_depth: Bits per pixel
        
    Returns:
        Row size in bytes (including padding)
    """
    return int((bit_depth * width + 31) / 32) * 4


def parse_row(row_data, width, bit_depth, color_table):
    """
    Parse a single row of pixel data into RGB tuples.
    
    Args:
        row_data: Raw bytes for the row
        width: Number of pixels in the row
        bit_depth: Bits per pixel
        color_table: Color palette for indexed formats (or None)
        
    Returns:
        List of (R, G, B) tuples
    """
    pixels = []
    
    if bit_depth == 1:
        pixels = _parse_1bit_row(row_data, width, color_table)
    elif bit_depth == 4:
        pixels = _parse_4bit_row(row_data, width, color_table)
    elif bit_depth == 8:
        pixels = _parse_8bit_row(row_data, width, color_table)
    elif bit_depth == 16:
        pixels = _parse_16bit_row(row_data, width)
    elif bit_depth == 24:
        pixels = _parse_24bit_row(row_data, width)
    elif bit_depth == 32:
        pixels = _parse_32bit_row(row_data, width)
    
    return pixels


def _parse_1bit_row(row_data, width, color_table):
    """Parse 1-bit indexed row (8 pixels per byte)."""
    pixels = []
    for byte_idx in range((width + 7) // 8):
        byte = row_data[byte_idx]
        for bit_idx in range(8):
            if byte_idx * 8 + bit_idx >= width:
                break
            pixel_idx = (byte >> (7 - bit_idx)) & 1
            pixels.append(color_table[pixel_idx])
    return pixels


def _parse_4bit_row(row_data, width, color_table):
    """Parse 4-bit indexed row (2 pixels per byte)."""
    pixels = []
    for byte_idx in range((width + 1) // 2):
        byte = row_data[byte_idx]
        # High nibble
        pixel_idx = (byte >> 4) & 0x0F
        pixels.append(color_table[pixel_idx])
        # Low nibble
        if byte_idx * 2 + 1 < width:
            pixel_idx = byte & 0x0F
            pixels.append(color_table[pixel_idx])
    return pixels


def _parse_8bit_row(row_data, width, color_table):
    """Parse 8-bit indexed row (1 pixel per byte)."""
    pixels = []
    for i in range(width):
        pixel_idx = row_data[i]
        pixels.append(color_table[pixel_idx])
    return pixels


def _parse_16bit_row(row_data, width):
    """Parse 16-bit RGB555 row."""
    pixels = []
    for i in range(width):
        word = struct.unpack('<H', row_data[i*2:i*2+2])[0]
        r = ((word >> 10) & 0x1F) << 3  # Scale 5-bit to 8-bit
        g = ((word >> 5) & 0x1F) << 3
        b = (word & 0x1F) << 3
        pixels.append((r, g, b))
    return pixels


def _parse_24bit_row(row_data, width):
    """Parse 24-bit BGR row."""
    pixels = []
    for i in range(width):
        b, g, r = struct.unpack('BBB', row_data[i*3:i*3+3])
        pixels.append((r, g, b))
    return pixels


def _parse_32bit_row(row_data, width):
    """Parse 32-bit BGRA row (ignoring alpha)."""
    pixels = []
    for i in range(width):
        b, g, r, a = struct.unpack('BBBB', row_data[i*4:i*4+4])
        pixels.append((r, g, b))
    return pixels


def get_next_row(f, width, bit_depth, color_table, row_size):
    """
    Read and parse the next row from a BMP file.
    
    Args:
        f: File object positioned at the start of a row
        width: Image width in pixels
        bit_depth: Bits per pixel
        color_table: Color palette for indexed formats (or None)
        row_size: Row size in bytes (including padding)
        
    Returns:
        List of (R, G, B) tuples for the row, or None if EOF
    """
    row_data = f.read(row_size)
    if not row_data:
        return None
    
    return parse_row(row_data, width, bit_depth, color_table)


class BMPRowReader:
    """Helper class to read and manage BMP rows with proper orientation."""
    
    def __init__(self, f, width, height, bit_depth, color_table, row_size, top_down):
        """
        Initialize row reader.
        
        Args:
            f: File object positioned at start of pixel data
            width: Image width in pixels
            height: Image height in pixels
            bit_depth: Bits per pixel
            color_table: Color palette for indexed formats (or None)
            row_size: Row size in bytes (including padding)
            top_down: Whether image is stored top-down
        """
        self.f = f
        self.width = width
        self.height = height
        self.bit_depth = bit_depth
        self.color_table = color_table
        self.row_size = row_size
        self.top_down = top_down
    
    def read_rows(self):
        """
        Generator that yields rows one at a time from file.
        
        Yields:
            List of (R, G, B) tuples for each row
            Rows are yielded in the order they appear in the file
            (bottom-to-top for standard BMPs, top-to-bottom for top-down BMPs)
        """
        # Yield rows one at a time (streaming)
        for _ in range(self.height):
            row = get_next_row(self.f, self.width, self.bit_depth, 
                             self.color_table, self.row_size)
            if row is not None:
                yield row
