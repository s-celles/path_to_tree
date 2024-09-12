"""
This module creates a tree representation of the directory structure
starting from a specified directory (or the current directory by default),
using a nested defaultdict, and exports it as YAML.
"""

import os
import argparse
import yaml
from pathlib import Path
from collections import defaultdict


def nested_defaultdict():
    """
    Creates a defaultdict that recursively returns another defaultdict when a key is missing.

    Returns:
        defaultdict: A defaultdict that automatically creates nested sub-dictionaries.
    """
    return defaultdict(nested_defaultdict)


def set_nested(d, keys):
    """
    Navigates through the nested dictionary and returns the sub-dictionary corresponding to the provided keys.

    Args:
        d (defaultdict): The nested dictionary to navigate.
        keys (list): The list of keys defining the path in the dictionary.

    Returns:
        defaultdict: The sub-dictionary corresponding to the path specified by the keys.
    """
    for key in keys:
        d = d[key]
    return d


def print_tree(d, indent=0):
    """
    Recursively prints the structure of the nested dictionary as a tree.

    Args:
        d (defaultdict): The dictionary to display.
        indent (int, optional): The indentation level for display. Defaults to 0.
    """
    for k, v in d.items():
        print("  " * indent + str(k))
        if isinstance(v, defaultdict):
            print_tree(v, indent + 1)


def defaultdict_to_dict(d):
    """
    Recursively converts a defaultdict to a regular dict.

    Args:
        d (defaultdict): The defaultdict to convert.

    Returns:
        dict: A regular dictionary representation of the input defaultdict.
    """
    if isinstance(d, defaultdict):
        return {k: defaultdict_to_dict(v) for k, v in d.items()}
    return d


def main(start_path, output_file):
    """
    Main function that traverses the directory tree starting from the specified path,
    creates a representation as a nested dictionary, displays this representation,
    and exports it as YAML.

    Args:
        start_path (str): The path to start the directory traversal from.
        output_file (str): The path to the output YAML file.
    """
    tree = nested_defaultdict()
    p = Path(start_path)
    for root, dirs, files in os.walk(p):
        root_parts = Path(root).relative_to(p).parts
        if not root_parts:
            root_parts = (p.name,)
        current_dict = set_nested(tree, root_parts)
        for dir in dirs:
            current_dict[dir]  # Creates an empty defaultdict for each subdirectory

    print("Directory structure:")
    print_tree(tree)

    # Convert defaultdict to regular dict for YAML export
    regular_dict = defaultdict_to_dict(tree)

    # Export to YAML
    with open(output_file, "w") as f:
        yaml.dump(regular_dict, f, default_flow_style=False)

    print(f"\nYAML representation exported to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a tree representation of a directory structure and export as YAML."
    )
    parser.add_argument(
        "-p",
        "--path",
        default=".",
        help="The path to start the directory traversal from. Defaults to the current directory.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="directory_structure.yaml",
        help="The output YAML file. Defaults to 'directory_structure.yaml' in the current directory.",
    )
    args = parser.parse_args()

    main(args.path, args.output)
