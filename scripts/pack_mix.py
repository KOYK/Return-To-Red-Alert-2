#!/usr/bin/env python3
import os
import struct
import sys

def pack_mix(source_folder, output_file):
    print(f"[*] Packing {source_folder} -> {output_file}")
    
    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, source_folder)
            files.append({'name': rel_path, 'path': full_path, 'size': os.path.getsize(full_path)})

    if not files:
        print("[!] Error: No files found!")
        return False

    header_size = 8 + (len(files) * 8)
    current_offset = header_size
    offsets = []

    # Read all data first to calculate offsets
    all_data = b""
    for f in files:
        with open(f['path'], 'rb') as src:
            data = src.read()
        offsets.append((current_offset, len(data)))
        all_data += data
        current_offset += len(data)

    # Write MIX file
    with open(output_file, 'wb') as f:
        f.write(b'MIX\x00')
        f.write(struct.pack('<I', len(files)))
        
        for offset, size in offsets:
            f.write(struct.pack('<II', offset, size))
        
        f.write(all_data)

    print(f"[+] Success! Created {output_file} ({os.path.getsize(output_file)} bytes)")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python pack_mix.py <source_folder> <output_file>")
        sys.exit(1)
    pack_mix(sys.argv[1], sys.argv[2])