#!/usr/bin/env python3
"""
Compile duckyScript .txt files to .dsb bytecode.

Usage:
    ./compile.py                      # Compile all profiles
    ./compile.py profile_General      # Compile one profile
    ./compile.py profile_General/key1.txt  # Compile one file
"""

import sys
import os
from pathlib import Path

# Add the configurator src to path
CONFIGURATOR_SRC = Path(__file__).parent.parent / "duckyPad-Configurator" / "src"
sys.path.insert(0, str(CONFIGURATOR_SRC))

from shared import ds_line
from make_bytecode import make_dsb_no_exception

def compile_script(txt_path: Path) -> bool:
    """Compile a single .txt file to .dsb"""
    dsb_path = txt_path.with_suffix('.dsb')

    try:
        with open(txt_path, 'r') as f:
            text_listing = f.read().split('\n')

        program_listing = []
        for index, item in enumerate(text_listing):
            program_listing.append(ds_line(item, index + 1))

        status_dict, bin_arr = make_dsb_no_exception(program_listing)

        if bin_arr is None:
            print(f"  ✗ {txt_path.name}: {status_dict.get('comments', 'Unknown error')}")
            if 'error_line_number_starting_from_1' in status_dict:
                print(f"    Line {status_dict['error_line_number_starting_from_1']}: {status_dict.get('error_line_str', '')}")
            return False

        with open(dsb_path, 'wb') as f:
            f.write(bin_arr)

        print(f"  ✓ {txt_path.name} → {dsb_path.name} ({len(bin_arr)} bytes)")
        return True

    except Exception as e:
        print(f"  ✗ {txt_path.name}: {e}")
        return False

def compile_profile(profile_dir: Path) -> tuple[int, int]:
    """Compile all key*.txt files in a profile directory"""
    print(f"\n{profile_dir.name}/")

    success = 0
    failed = 0

    # Find all key*.txt files (including key*-release.txt)
    txt_files = sorted(profile_dir.glob("key*.txt"))

    if not txt_files:
        print("  (no key files found)")
        return 0, 0

    for txt_file in txt_files:
        if compile_script(txt_file):
            success += 1
        else:
            failed += 1

    return success, failed

def main():
    profiles_dir = Path(__file__).parent

    if len(sys.argv) > 1:
        target = Path(sys.argv[1])

        # Handle relative paths
        if not target.is_absolute():
            target = profiles_dir / target

        if target.is_file() and target.suffix == '.txt':
            # Compile single file
            print(f"Compiling {target.name}...")
            success = compile_script(target)
            sys.exit(0 if success else 1)

        elif target.is_dir():
            # Compile single profile
            success, failed = compile_profile(target)
            print(f"\nDone: {success} compiled, {failed} failed")
            sys.exit(0 if failed == 0 else 1)

        else:
            print(f"Error: {target} not found")
            sys.exit(1)

    else:
        # Compile all profiles
        print("Compiling all profiles...")

        total_success = 0
        total_failed = 0

        for profile_dir in sorted(profiles_dir.glob("profile_*")):
            if profile_dir.is_dir():
                success, failed = compile_profile(profile_dir)
                total_success += success
                total_failed += failed

        print(f"\n{'='*40}")
        print(f"Total: {total_success} compiled, {total_failed} failed")
        sys.exit(0 if total_failed == 0 else 1)

if __name__ == "__main__":
    main()
