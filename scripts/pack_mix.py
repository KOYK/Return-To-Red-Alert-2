#!/usr/bin/env python3
"""
Self-contained Westwood MIX Packer for Red Alert 2 / Yuri's Revenge.
No external libraries required. Implements the format exactly.
"""

import os
import struct
import sys

def pack_mix(source_folder, output_file):
    print(f"[*] Scanning folder: {source_folder}")
    
    if not os.path.isdir(source_folder):
        print(f"[!] ERROR: Folder '{source_folder}' does not exist.")
        return False

    files = []
    # Walk directory
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            # Get path relative to the source folder
            rel_path = os.path.relpath(full_path, source_folder)
            
            # CRITICAL: RA2 expects forward slashes, not backslashes
            rel_path = rel_path.replace('\\', '/')
            
            size = os.path.getsize(full_path)
            files.append({
                'name': rel_path,
                'path': full_path,
                'size': size
            })

    if not files:
        print("[!] ERROR: No files found to pack.")
        return False

    print(f"[+] Found {len(files)} files to pack.")

    # --- MIX FORMAT STRUCTURE ---
    # 1. Magic: "MIX" + 0x00 (4 bytes)
    # 2. File Count: 4 bytes (Little Endian)
    # 3. File Entries: (Offset 4 bytes, Size 4 bytes) * Count
    # 4. File Data: Concatenated file contents
    
    MAGIC = b'MIX\x00'
    ENTRY_SIZE = 8  # 4 bytes offset + 4 bytes size
    HEADER_BASE = 8 # Magic + Count
    
    # Calculate total header size
    header_size = HEADER_BASE + (len(files) * ENTRY_SIZE)
    
    # Build file data buffer and calculate offsets
    file_data_buffer = bytearray()
    file_entries = []
    
    for f in files:
        with open(f['path'], 'rb') as src:
            data = src.read()
        
        offset = len(file_data_buffer) + header_size
        size = len(data)
        
        file_entries.append((offset, size))
        file_data_buffer.extend(data)

    # --- WRITE THE MIX FILE ---
    print(f"[*] Writing {output_file}...")
    
    with open(output_file, 'wb') as f:
        # 1. Magic
        f.write(MAGIC)
        
        # 2. File Count (Little Endian)
        f.write(struct.pack('<I', len(files)))
        
        # 3. File Entries (Offset, Size) - Little Endian
        for offset, size in file_entries:
            f.write(struct.pack('<II', offset, size))
        
        # 4. File Data
        f.write(file_data_buffer)

    final_size = os.path.getsize(output_file)
    print(f"[+] SUCCESS! Created {output_file} ({final_size:,} bytes).")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python pack_mix.py <source_folder> <output_file>")
        sys.exit(1)
    
    success = pack_mix(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)