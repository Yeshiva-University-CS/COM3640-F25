"""
GIF Writer Utility Functions
Helper functions for writing GIF files using PIL/Pillow.
"""

try:
    from PIL import Image
except ImportError:
    raise ImportError("PIL/Pillow is required for GIF writing. Install with: pip install Pillow")


def convert_to_gif(row_generator, width, height, top_down=False):
    """
    Convert rows from a generator to a GIF image.
    
    Note: GIF format requires buffering the entire image before writing due to
    LZW compression requirements. Unlike BMP, we cannot stream rows directly.
    
    Args:
        row_generator: Generator yielding rows of RGB tuples
        width: Image width
        height: Image height
        top_down: Whether image rows are in top-down order (True) or bottom-up (False)
    """
    # Buffer all rows (required for GIF)
    rows = list(row_generator)
    
    # GIF expects rows in top-down order
    # If rows are in bottom-up order, reverse them
    if not top_down:
        rows.reverse()
    
    # Flatten rows into a single list of pixels
    pixels = []
    for row in rows:
        pixels.extend(row)
    
    # Check if image is grayscale
    is_grayscale = all(r == g == b for r, g, b in pixels)
    
    if is_grayscale:
        # Grayscale mode - convert to single channel
        gray_pixels = [r for r, g, b in pixels]  # R == G == B
        img = Image.new('L', (width, height))
        img.putdata(gray_pixels)
    else:
        # RGB mode - convert to palette with 256 colors
        img = Image.new('RGB', (width, height))
        img.putdata(pixels)
        # Convert to palette mode (256 colors)
        # PIL uses intelligent quantization (median cut by default)
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    
    return img
