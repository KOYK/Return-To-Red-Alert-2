#!/usr/bin/env python3
"""
Corrected MIX file packer for Red Alert 2 / Yuri's Revenge
Matches the Westwood MIX format exactly.
"""

import os
import struct
import sys

def pack_mix(source_folder, output_file):
    print(f"[*] Packing {source_folder} -> {output_file}")
    
    # Collect all files
    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in sorted(filenames):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, source_folder)
            # Normalize path separators to forward slashes (Westwood standard)
            rel_path = rel_path.replace('\\', '/')
            files.append({
                'name': rel_path,
                'path': full_path,
                'size': os.path.getsize(full_path)
            })

    if not files:
        print("[!] Error: No files found!")
        return False

    print(f"[+] Found {len(files)} files to pack")

    # MIX Header Constants
    MAGIC = b'MIX\x00'
    VERSION = 1  # Standard version for RA2/YR
    
    # Calculate header size: Magic(4) + Count(4) + (Entries * 8)
    entry_size = 8
    header_size = 8 + (len(files) * entry_size)
    
    # Build file data and calculate offsets
    file_data = b""
    offsets = []
    
    for f in files:
        with open(f['path'], 'rb') as src:
            data = src.read()
        
        offset = len(file_data) + header_size
        size = len(data)
        offsets.append((offset, size))
        file_data += data

    # Write MIX file
    with open(output_file, 'wb') as f:
        # 1. Magic
        f.write(MAGIC)
        
        # 2. File Count (Little Endian)
        f.write(struct.pack('<I', len(files)))
        
        # 3. File Entries (Offset, Size) - Little Endian
        for offset, size in offsets:
            f.write(struct.pack('<II', offset, size))
        
        # 4. File Data
        f.write(file_data)

    total_size = os.path.getsize(output_file)
    print(f"[+] Success! Created {output_file} ({total_size:,} bytes)")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python pack_mix.py <source_folder> <output_file>")
        sys.exit(1)
    
    success = pack_mix(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)