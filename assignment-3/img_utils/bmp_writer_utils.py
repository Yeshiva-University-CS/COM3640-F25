def write_24bit_bmp(f, row_generator, width, height, top_down=False):
    """
    Write a 24-bit BMP file with given width, height, and row generator.
    
    Args:
        f: File object opened in binary write mode
        row_generator: Generator yielding rows of RGB tuples
        width: Image width
        height: Image height
        top_down: Whether image is stored top-down (True) or bottom-up (False)
    """
    import struct
    
    # Calculate sizes
    row_size = ((width * 3 + 3) // 4) * 4
    pixel_data_size = row_size * height
    dib_header_size = 40
    color_table_size = 0
    pixel_offset = 14 + dib_header_size + color_table_size
    file_size = pixel_offset + pixel_data_size
    
    # Write BMP header
    _write_bmp_file_header(f, file_size, pixel_offset)
    
    # Write DIB header (with proper height sign for top_down)
    _write_dib_header(f, dib_header_size, width, height, 24, pixel_data_size, top_down)
    
    # Write pixel data in original order
    for row in row_generator:
        row_bytes = _encode_24bit_row(row, width, row_size)
        f.write(row_bytes)
        

def write_8bit_bmp(f, row_generator, width, height, top_down=False):
    """
    Write a 8-bit BMP file with given width, height, palette, and pixel indices.
    
    Args:
        f: File object opened in binary write mode
        row_generator: Generator yielding rows of RGB tuples
        width: Image width
        height: Image height
        top_down: Whether image is stored top-down (True) or bottom-up (False)
    """
    import struct
    
    rows = list(row_generator)
    palette, pixel_indices = _quantize_colors(rows, width, height)
    
    # Calculate sizes
    row_size = ((width + 3) // 4) * 4
    pixel_data_size = row_size * height
    color_table_size = 256 * 4
    dib_header_size = 40
    pixel_offset = 14 + dib_header_size + color_table_size
    file_size = pixel_offset + pixel_data_size
    
    # Write BMP file header
    _write_bmp_file_header(f, file_size, pixel_offset)
    
    # Write DIB header (with proper height sign for top_down)
    _write_dib_header(f, dib_header_size, width, height, 8, pixel_data_size, top_down)
    
    # Write color palette
    _write_palette(f, palette)
    
    # Write pixel data in original order
    for index_row in pixel_indices:
        row_bytes = _encode_8bit_row(index_row, width, row_size)
        f.write(row_bytes)
        
        
def _quantize_colors(rows, width, height):
    """
    Quantize image colors to 256-color palette.
    
    Args:
        rows: List of rows (each row is list of RGB tuples)
        width: Image width
        height: Image height
        
    Returns:
        Tuple of (palette, pixel_indices)
        - palette: List of 256 (R,G,B) tuples
        - pixel_indices: List of rows, each row is list of palette indices
    """
    # Collect all unique colors
    color_set = set()
    for row in rows:
        for pixel in row:
            color_set.add(pixel)
    
    # Check if image is grayscale
    is_grayscale = all(r == g == b for r, g, b in color_set)
    
    if is_grayscale:
        # Use standard grayscale palette
        palette = [(i, i, i) for i in range(256)]
        
        # Map pixels directly to grayscale values
        pixel_indices = []
        for row in rows:
            index_row = [r for r, g, b in row]  # R == G == B
            pixel_indices.append(index_row)
    
    elif len(color_set) <= 256:
        # Image already has 256 or fewer colors
        palette = list(color_set)
        
        # Pad palette to 256 entries if needed
        while len(palette) < 256:
            palette.append((0, 0, 0))
        
        # Build color-to-index mapping
        color_to_index = {color: i for i, color in enumerate(palette)}
        
        # Map pixels to indices
        pixel_indices = []
        for row in rows:
            index_row = [color_to_index[pixel] for pixel in row]
            pixel_indices.append(index_row)
    
    else:
        # Need to quantize: reduce colors to 256
        # Use median cut or octree quantization
        palette, pixel_indices = _median_cut_quantize(rows, 256)
    
    return palette, pixel_indices


def _median_cut_quantize(rows, num_colors):
    """
    Quantize colors using median cut algorithm.
    
    Args:
        rows: List of rows
        num_colors: Target number of colors (256)
        
    Returns:
        Tuple of (palette, pixel_indices)
    """
    # Collect all pixels
    all_pixels = []
    for row in rows:
        all_pixels.extend(row)
    
    # Build initial bucket
    buckets = [all_pixels]
    
    # Iteratively split buckets
    while len(buckets) < num_colors:
        # Find bucket with greatest range
        bucket_to_split = max(buckets, key=lambda b: _get_color_range(b))
        buckets.remove(bucket_to_split)
        
        # Split bucket
        b1, b2 = _split_bucket(bucket_to_split)
        buckets.append(b1)
        buckets.append(b2)
    
    # Build palette from bucket averages
    palette = []
    for bucket in buckets:
        avg_color = _average_color(bucket)
        palette.append(avg_color)
    
    # Pad to 256
    while len(palette) < 256:
        palette.append((0, 0, 0))
    
    # Map each pixel to nearest palette color
    pixel_indices = []
    for row in rows:
        index_row = []
        for pixel in row:
            closest_idx = _find_closest_color(pixel, palette)
            index_row.append(closest_idx)
        pixel_indices.append(index_row)
    
    return palette, pixel_indices


def _get_color_range(pixels):
    """Get the range (max - min) across all color channels."""
    if not pixels:
        return 0
    
    r_vals = [p[0] for p in pixels]
    g_vals = [p[1] for p in pixels]
    b_vals = [p[2] for p in pixels]
    
    r_range = max(r_vals) - min(r_vals)
    g_range = max(g_vals) - min(g_vals)
    b_range = max(b_vals) - min(b_vals)
    
    return max(r_range, g_range, b_range)


def _split_bucket(pixels):
    """Split bucket along dimension with greatest range."""
    r_vals = [p[0] for p in pixels]
    g_vals = [p[1] for p in pixels]
    b_vals = [p[2] for p in pixels]
    
    r_range = max(r_vals) - min(r_vals)
    g_range = max(g_vals) - min(g_vals)
    b_range = max(b_vals) - min(b_vals)
    
    # Sort by dimension with greatest range
    if r_range >= g_range and r_range >= b_range:
        pixels.sort(key=lambda p: p[0])
    elif g_range >= b_range:
        pixels.sort(key=lambda p: p[1])
    else:
        pixels.sort(key=lambda p: p[2])
    
    # Split at median
    mid = len(pixels) // 2
    return pixels[:mid], pixels[mid:]


def _average_color(pixels):
    """Calculate average color of a bucket."""
    if not pixels:
        return (0, 0, 0)
    
    r_avg = sum(p[0] for p in pixels) // len(pixels)
    g_avg = sum(p[1] for p in pixels) // len(pixels)
    b_avg = sum(p[2] for p in pixels) // len(pixels)
    
    return (r_avg, g_avg, b_avg)


def _find_closest_color(pixel, palette):
    """Find index of closest color in palette."""
    min_dist = float('inf')
    closest_idx = 0
    
    for i, pal_color in enumerate(palette):
        # Euclidean distance in RGB space
        dist = ((pixel[0] - pal_color[0]) ** 2 +
                (pixel[1] - pal_color[1]) ** 2 +
                (pixel[2] - pal_color[2]) ** 2)
        
        if dist < min_dist:
            min_dist = dist
            closest_idx = i
    
    return closest_idx


def _write_bmp_file_header(f, file_size, pixel_offset):
    """
    Write BMP file header (14 bytes).
    
    Args:
        f: File object opened in binary write mode
        file_size: Total file size in bytes
        pixel_offset: Offset to pixel data from start of file
    """
    import struct
    f.write(b'BM')
    f.write(struct.pack('<I', file_size))
    f.write(struct.pack('<HH', 0, 0))
    f.write(struct.pack('<I', pixel_offset))


def _write_dib_header(f, dib_header_size, width, height, bit_depth, pixel_data_size, top_down=False):
    """
    Write DIB (Device Independent Bitmap) header (40 bytes for BITMAPINFOHEADER).
    
    Args:
        f: File object opened in binary write mode
        dib_header_size: Size of DIB header (always 40)
        width: Image width
        height: Image height (will be negated if top_down is True)
        bit_depth: Bits per pixel (8 or 24)
        pixel_data_size: Size of pixel data in bytes
        top_down: Whether image is stored top-down (True) or bottom-up (False)
    """
    import struct
    
    # In BMP format, negative height indicates top-down orientation
    header_height = -height if top_down else height
    
    f.write(struct.pack('<I', dib_header_size))
    f.write(struct.pack('<i', width))
    f.write(struct.pack('<i', header_height))
    f.write(struct.pack('<H', 1))  # Planes
    f.write(struct.pack('<H', bit_depth))
    f.write(struct.pack('<I', 0))  # Compression (0 = none)
    f.write(struct.pack('<I', pixel_data_size))
    f.write(struct.pack('<i', 2835))  # Horizontal resolution (pixels per meter)
    f.write(struct.pack('<i', 2835))  # Vertical resolution (pixels per meter)
    f.write(struct.pack('<I', 0))  # Colors in palette (0 = default)
    f.write(struct.pack('<I', 0))  # Important colors (0 = all)


def _write_palette(f, palette):
    """
    Write 256-entry color palette for 8-bit BMP.
    
    Args:
        f: File object opened in binary write mode
        palette: List of (R, G, B) tuples, will be padded to 256 entries
    """
    import struct
    for r, g, b in palette:
        f.write(struct.pack('BBBB', b, g, r, 0))


def _encode_24bit_row(row, width, row_size):
    """
    Encode a row of RGB pixels into 24-bit BMP format with padding.
    
    Args:
        row: List of (R, G, B) tuples
        width: Image width (number of pixels in row)
        row_size: Row size in bytes (width * 3 + padding)
        
    Returns:
        Bytes object containing encoded row with padding
    """
    row_bytes = bytearray()
    for r, g, b in row:
        row_bytes.extend([b, g, r])  # BMP uses BGR format
    padding = row_size - (width * 3)
    row_bytes.extend(b'\x00' * padding)
    return row_bytes


def _encode_8bit_row(index_row, width, row_size):
    """
    Encode a row of palette indices into 8-bit BMP format with padding.
    
    Args:
        index_row: List of palette indices (0-255)
        width: Image width (number of pixels in row)
        row_size: Row size in bytes (width + padding)
        
    Returns:
        Bytes object containing encoded row with padding
    """
    row_bytes = bytearray(index_row)
    padding = row_size - width
    row_bytes.extend(b'\x00' * padding)
    return row_bytes

