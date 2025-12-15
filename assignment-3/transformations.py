"""
Image Transformations Module
Functional transformations that operate on row generators.
"""


def flip_horizontal(row_generator):
    """
    Flip image horizontally (mirror left-right).
    
    Args:
        row_generator: Generator yielding metadata, then rows
    """
    pass


def flip_vertical(row_generator):
    """
    Flip image vertically (mirror top-bottom).
    
    Args:
        row_generator: Generator yielding metadata, then rows
    """
    pass


def grayscale(row_generator):
    """
    Convert RGB image to grayscale using luminance formula.
    Formula: 0.299*R + 0.587*G + 0.114*B
    
    Args:
        row_generator: Generator yielding metadata, then rows
    """
    pass


def brightness(factor):
    """
    Adjust brightness of all pixels by multiplication factor.
    
    Args:
        factor: Brightness multiplier (1.0 = no change, >1.0 = brighter, <1.0 = darker)
    """
    pass

