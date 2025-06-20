"""
pylintqmd: Lint Python code embedded in Quarto (.qmd) files using pylint.

Acknowledgements
----------------
Code generated by and adapted from Perplexity.
"""

import sys
import subprocess
from pathlib import Path

from .args import CustomArgumentParser
from .converter import convert_qmd_to_py


def process_qmd(qmd_file, keep_temp_files=False, verbose=False):
    """
    Convert a .qmd file to .py, lint it with pylint, and clean up.

    Parameters
    ----------
    qmd_file : str or Path
        Path to the input .qmd file.
    keep_temp_files : bool, optional
        If True, retain the temporary .py file after linting.
    verbose : bool, optional
        If True, print detailed progress information.

    Returns
    -------
    int
        0 on success, nonzero on error.

    Notes
    -----
    Adapted from code generated by Perplexity.
    """
    # Convert input to Path object
    qmd_path = Path(qmd_file)

    # Validate that the file exists and has a .qmd extension
    if not qmd_path.exists() or qmd_path.suffix != ".qmd":
        print(f"Error: {qmd_file} is not a valid .qmd file.", file=sys.stderr)
        return 1

    # Determine base name and temporary .py file path (as will need when lint)
    base = qmd_path.with_suffix("")
    py_file = base.with_suffix(".py")

    # Convert the .qmd file to a .py file
    try:
        convert_qmd_to_py(qmd_path=str(qmd_path), verbose=verbose)
    except Exception as e:  # pylint: disable=broad-except
        # Intentional broad catch for unknown conversion errors
        print(f"Error: Failed to convert {qmd_file} to .py: {e}",
              file=sys.stderr)
        return 1

    # Remove leading './' from base name
    nodot_base = str(base)
    if nodot_base.startswith('./'):
        nodot_base = nodot_base[2:]

    try:
        # Run pylint on the temporary .py file and capture output
        result = subprocess.run(
            ['pylint', str(py_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        # Replace references to the .py file in pylint output with the original
        # .qmd file
        output = result.stdout.replace(f"{nodot_base}.py", qmd_file)
        print(output, end='')
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    # Handle case where pylint is not installed
    except FileNotFoundError:
        print("Error: pylint not found. Please install pylint.",
              file=sys.stderr)
        return 1

    # Remove temporary .py file unless KEEP_TEMP_FILES is set
    if not keep_temp_files:
        try:
            py_file.unlink()
        except Exception as e:  # pylint: disable=broad-except
            # Broad catch ensures cleanup warnings don't crash process
            print(f"Warning: Could not remove temporary file {py_file}: {e}",
                  file=sys.stderr)
    return 0


def gather_qmd_files(paths):
    """
    Gather all .qmd files from a list of files and directories.

    Parameters
    ----------
    paths : list of str or Path
        List of file or directory paths.

    Returns
    -------
    list of str
        List of .qmd file paths found.

    Notes
    -----
    Adapted from code generated by Perplexity.
    """
    files = []
    for path in paths:
        p = Path(path)
        # If path is a single .qmd file, add it
        if p.is_file() and p.suffix == '.qmd':
            files.append(str(p))
        # If path is a directory, recursively add all .qmd files found within
        elif p.is_dir():
            files.extend(str(f) for f in p.rglob('*.qmd'))
    return files


def main():
    """
    Entry point for the pylintqmd CLI.

    Parses arguments, processes .qmd files, and exits with appropriate status
    code.

    Notes
    -----
    Adapted from code generated by Perplexity.
    """
    # Set up custom argumentparser with help statements
    parser = CustomArgumentParser(
        description="Lint Python code in Quarto (.qmd) files using pylint."
    )
    parser.add_argument(
        "paths", nargs='+',
        help="One or more .qmd files or directories to lint."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Verbose output."
    )
    parser.add_argument(
        "-k", "--keep-temp", action="store_true",
        help="Keep temporary .py files after linting."
    )
    args = parser.parse_args()

    # Gather all .qmd files from the provided arguments
    qmd_files = gather_qmd_files(args.paths)
    if not qmd_files:
        print("Error: No .qmd files found.", file=sys.stderr)
        sys.exit(1)

    exit_code = 0
    # Process each .qmd file found
    for qmd_file in qmd_files:
        ret = process_qmd(qmd_file=qmd_file,
                          keep_temp_files=args.keep_temp,
                          verbose=args.verbose)
        if ret != 0:
            exit_code = ret
    sys.exit(exit_code)


if __name__ == "__main__":
    # Run the main function if this module is executed as a script
    main()
