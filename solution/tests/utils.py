import os

def locate_test_file(filename):
    """Helper to locate test resource files."""
    return os.path.join(os.path.dirname(__file__), f"resources/{filename}")
