import aes
import cProfile

# Convert 16 bytes (128 bits) to four 32-bit words for AES-128
def bytes_to_words(b):
    return tuple(int.from_bytes(b[i:i+4], 'big') for i in range(0, 16, 4))

key_bytes = b"Sixteen byte key"         # 16 bytes → AES-128 key
text_bytes = b"TextMustBe16Byte"        # 16 bytes → AES block size

key = bytes_to_words(key_bytes)
text = bytes_to_words(text_bytes)

def run_encryption():
    cipher = aes.AES(verbose=False, dump_vars=False)
    for _ in range(1000):
        cipher.aes_encipher_block(key, text)

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_encryption()
    profiler.disable()
    profiler.dump_stats("aes.prof")
    print("Profiling complete! Output saved to aes.prof")
