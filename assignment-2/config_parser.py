# config_parser.py
# TODO: implement the parse_file function
# TODO: Complete the transformer methods to implement all features

from lark import Lark, Transformer, v_args

@v_args(inline=True)
class ConfigTransformer(Transformer):
    """
    Transformer for config files with extended features
    """
    pass


# ==================================================================
# PARSER SETUP
# ==================================================================

# Load grammar
with open("config.lark", "r") as f:
    _grammar = f.read()

_parser = Lark(_grammar, start='start', parser='lalr')

def parse_file(filepath):
    """
    Parse a config file and return the config dictionary.
    
    Args:
        filepath: Path to config file
    
    Returns:
        Dictionary containing parsed configuration
    
    Raises:
        ValueError: On undefined variables, circular includes, etc.
        TypeError: On type validation failures
    """
    pass
