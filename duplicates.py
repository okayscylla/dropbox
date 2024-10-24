import hashlib
import os
import defaultdict


class ReadBuffer:
    def __init__(self, file_path, algorithm=hashlib.sha1):
        self.handle = open(file_path, "rb")
        self.buffer = b""
    
    def hash(self, full_hash=True, block_size=1024):
        if full_hash:
            wuh