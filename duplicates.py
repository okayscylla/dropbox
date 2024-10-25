"""
Rewritten version of this https://stackoverflow.com/a/36113168/300783 algorithm,
based on this modified version https://gist.github.com/tfeldmann/fc875e6630d11f2256e746f67a09c1ae

Slight code changes and cleanup for this use case.
"""

import hashlib
import os
from collections import defaultdict


class FileHash:
    def __init__(self, file_path):
        self.handle = open(file_path, "rb")
        self.hasher = hashlib.sha1()
    
    def hash(self, full_hash=True, block_size=1024):
        if full_hash:
            while True:
                chunk = self.handle.read(block_size)
                if not chunk:
                    break
                self.hasher.update(chunk)
        else:
            self.hasher.update(self.handle.read(block_size))

        return self.hasher.digest()

def duplicate_finder(locations):
    files_size = defaultdict(list)
    files_small = defaultdict(list)
    files_full = dict()
    
    duplicates = set()

    for location in locations:
        for directory, _, files in os.walk(location):
            for file in files:
                path = os.path.join(directory, file)
                
                try:
                    path = os.path.realpath(path)
                    file_size = os.path.getsize(path)
                    
                    files_size[file_size].append(path)
                except OSError:
                    continue
    
    for file_size, files in files_size.items():
        if len(files) < 2:
            continue
        
        for file in files:
            try:
                small_hash = FileHash(file).hash(full_hash=False)
                files_small[small_hash].append(file)
            except OSError:
                continue

    for file_hash, files in files_small.items():
        if len(files) < 2:
            continue
        
        for file in files:
            try:
                full_hash = FileHash(file).hash()
                
                if full_hash in files_full:
                    duplicates.add(file)
                files_full[full_hash] = (file)
            except OSError:
                continue

    return duplicates


if __name__ == "__main__":
    print(duplicate_finder(["."]))