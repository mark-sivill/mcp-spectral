#
# direct tests for Spectral commandline wrapper
#

import sys
import os
from pathlib import Path
import argparse

# Add parent directory to sys.path to import spectral_wrapper
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from spectral_wrapper import SpectralWrapper

#
# only used by main function for testing
#
def read_file_to_string(filename: str) -> str:
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except IOError as e:
        raise IOError(f"Error reading file: {e}")

#
# run for local testing
#
def main(spectral_command=None, default_ruleset=None):

    spectral = SpectralWrapper(spectral_command=spectral_command, default_ruleset=default_ruleset)

    script_path = Path(__file__).resolve().parent
    print(f"Script path - {script_path}")

    spectral_version = spectral.version()
    print(f"Spectral version - {spectral_version}")

    results = spectral.lint(read_file_to_string(f"{script_path}/openapi-with-errors.yaml"))
    print(f"Spectral linting openapi with errors - {results}")

    results = spectral.lint(read_file_to_string(f"{script_path}/openapi-no-errors.yaml"), read_file_to_string(f"{script_path}/test-ruleset.yaml"))
    print(f"Spectral linting openapi without errors - {results}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pass optional parameters to the program")
    parser.add_argument("--command", type=str, default=None, help="Spectral command including path, this parameter is optional")
    parser.add_argument("--ruleset", type=str, default=None, help="Spectral ruleset file including path, this parameter is optional")
    args = parser.parse_args()
    main(spectral_command=args.command, default_ruleset=args.ruleset)

