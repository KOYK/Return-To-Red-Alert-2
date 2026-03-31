#!/usr/bin/env python3
"""
RA2/YR Compatible MIX Packer
Handles path normalization and header structure correctly.
"""

import os
import struct
import sys

def pack_mix(source_folder, output_file):
    print(f"[*] Packing {source_folder} -> {output_file}")
    
    files = []
    # Walk the directory
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, source_folder)
            
            # CRITICAL: RA2 expects forward slashes in paths, not backslashes
            rel_path = rel_path.replace('\\', '/')
            
            # CRITICAL: Paths in MIX files usually do NOT include the root folder name
            # If your folder is 'expandmd24', the files inside should be 'file.ini', not 'expandmd24/file.ini'
            # But since we are walking 'Source/expandmd24', rel_path is already relative to that folder.
            
            files.append({
                'name': rel_path,
                'path': full_path,
                'size': os.path.getsize(full_path)
            })

    if not files:
        print("[!] Error: No files found!")
        return False

    print(f"[+] Found {len(files)} files to pack")

    # Header Constants
    MAGIC = b'MIX\x00'
    
    # Calculate sizes
    entry_size = 8 # 4 bytes offset + 4 bytes size
    header_size = 8 + (len(files) * entry_size)
    
    # Build data buffer
    file_data = b""
    offsets = []
    
    for f in files:
        with open(f['path'], 'rb') as src:
            data = src.read()
        
        offset = len(file_data) + header_size
        size = len(data)
        offsets.append((offset, size))
        file_data += data

    # Write the file
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