#!/usr/bin/env python3
"""
Pack files into a Westwood MIX archive using the cnc-mix library.
"""
import os
import sys

try:
    from cnc_mix import MixFile
except ImportError:
    print("Error: cnc-mix library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cnc-mix"])
    from cnc_mix import MixFile

def pack_mix(source_folder, output_file):
    print(f"[*] Packing {source_folder} -> {output_file}")
    
    if not os.path.exists(source_folder):
        print(f"[!] Error: Source folder '{source_folder}' not found!")
        return False

    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, source_folder)
            # Normalize to forward slashes
            rel_path = rel_path.replace('\\', '/')
            files.append((rel_path, full_path))

    if not files:
        print("[!] Error: No files found!")
        return False

    print(f"[+] Found {len(files)} files to pack")

    # Create MixFile object
    mix = MixFile()
    
    # Add files
    for rel_path, full_path in files:
        with open(full_path, 'rb') as f:
            data = f.read()
        mix.add_file(rel_path, data)

    # Save
    mix.save(output_file)
    
    print(f"[+] Success! Created {output_file}")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python pack_mix.py <source_folder> <output_file>")
        sys.exit(1)
    
    success = pack_mix(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)