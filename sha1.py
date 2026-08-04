import ctypes
from enum import Enum

# Define exact-width types mapping to C
c_int_least16_t = ctypes.c_int16
uint32_t = ctypes.c_uint32
uint8_t = ctypes.c_uint8

class ShaStatus(Enum):
    shaSuccess = 0
    shaNULL = 1
    shaInputTooLong = 2
    shaStateError = 3

class sha1:
    def __init__(self):
        # State variables (H0 - H4)
        self.intermediate_hash = (uint32_t * 5)(
            0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
        )
        
        # Message length in bits
        self.length_low = uint32_t(0)
        self.length_high = uint32_t(0)
        
        # Message block & index
        self.message_block_index = c_int_least16_t(0)
        self.message_block = (uint8_t * 64)()
        
        self.computed = False
        self.corrupt = ShaStatus.shaSuccess

    def _left_rotate(self, value, bits):
        return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF

    def _process_message_block(self):
        # Constants
        K = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]
        W = [0] * 80
        
        # Initialize the first 16 words from the message block
        for t in range(16):
            W[t] = (self.message_block[t * 4] << 24) | \
                   (self.message_block[t * 4 + 1] << 16) | \
                   (self.message_block[t * 4 + 2] << 8) | \
                   self.message_block[t * 4 + 3]
        # Extend into 80 words
        for t in range(16, 80):
            W[t] = self._left_rotate(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16], 1)
            
        a = self.intermediate_hash[0]
        b = self.intermediate_hash[1]
        c = self.intermediate_hash[2]
        d = self.intermediate_hash[3]
        e = self.intermediate_hash[4]
        
        # 80 rounds of compression
        for t in range(80):
            if t < 20:
                f = (b & c) | ((~b) & d)
                k = K[0]
            elif t < 40:
                f = b ^ c ^ d
                k = K[1]
            elif t < 60:
                f = (b & c) | (b & d) | (c & d)
                k = K[2]
            else:
                f = b ^ c ^ d
                k = K[3]
                
            temp = (self._left_rotate(a, 5) + f + e + k + W[t]) & 0xFFFFFFFF
            e = d
            d = c
            c = self._left_rotate(b, 30)
            b = a
            a = temp
            
        self.intermediate_hash[0] = (self.intermediate_hash[0] + a) & 0xFFFFFFFF
        self.intermediate_hash[1] = (self.intermediate_hash[1] + b) & 0xFFFFFFFF
        self.intermediate_hash[2] = (self.intermediate_hash[2] + c) & 0xFFFFFFFF
        self.intermediate_hash[3] = (self.intermediate_hash[3] + d) & 0xFFFFFFFF
        self.intermediate_hash[4] = (self.intermediate_hash[4] + e) & 0xFFFFFFFF
        
        self.message_block_index.value = 0

    def update(self, message_array: bytes) -> ShaStatus:
        if not message_array:
            return ShaStatus.shaSuccess
            
        if self.computed:
            self.corrupt = ShaStatus.shaStateError
            return self.corrupt
            
        if self.corrupt != ShaStatus.shaSuccess:
            return self.corrupt
            
        for byte in message_array:
            self.message_block[self.message_block_index.value] = byte
            self.message_block_index.value += 1
            
            # Increment total bit count length
            self.length_low.value += 8
            if self.length_low.value == 0:  # Overflow check
                self.length_high.value += 1
                if self.length_high.value == 0:
                    self.corrupt = ShaStatus.shaInputTooLong
                    return self.corrupt
                    
            if self.message_block_index.value == 64:
                self._process_message_block()
                
        return ShaStatus.shaSuccess

    def final(self) -> str:
        if self.corrupt != ShaStatus.shaSuccess:
            return ""
            
        if not self.computed:
            # 1. Append padding marker block starting with 0x80 bit
            self.message_block[self.message_block_index.value] = 0x80
            self.message_block_index.value += 1
            
            # If there isn't enough space for the 8-byte length suffix, pad out and process block
            if self.message_block_index.value > 56:
                while self.message_block_index.value < 64:
                    self.message_block[self.message_block_index.value] = 0
                    self.message_block_index.value += 1
                self._process_message_block()
                
            # Pad up to the length injection boundary
            while self.message_block_index.value < 56:
                self.message_block[self.message_block_index.value] = 0
                self.message_block_index.value += 1
                
            # Store message length in the last 8 bytes of the block
            self.message_block[56] = (self.length_high.value >> 24) & 0xFF
            self.message_block[57] = (self.length_high.value >> 16) & 0xFF
            self.message_block[58] = (self.length_high.value >> 8) & 0xFF
            self.message_block[59] = (self.length_high.value) & 0xFF
            self.message_block[60] = (self.length_low.value >> 24) & 0xFF
            self.message_block[61] = (self.length_low.value >> 16) & 0xFF
            self.message_block[62] = (self.length_low.value >> 8) & 0xFF
            self.message_block[63] = (self.length_low.value) & 0xFF
            self._process_message_block()
            self.computed = True
        return "".join(f"{val:08x}" for val in self.intermediate_hash)

if __name__ == "__main__":
    hasher = sha1()
    status = hasher.update(b"abc")
    
    if status == ShaStatus.shaSuccess:
        digest = hasher.final()
        print(f"SHA-1 Digest: {digest}")
        print(f"Matches Expected: {digest == 'a9993e36476816aba3e25717850c26c9cd0d89d'}")
