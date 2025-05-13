import aes
import cProfile

key = b"Sixteen byte key"         # 16 bytes → AES-128 key
text = b"TextMustBe16Byte"        # 16 bytes → AES block size

def run_encryption():
    cipher = aes.AES(key)
    for _ in range(100000):
        cipher.encrypt_block(text)   # ✅ fixed method name

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_encryption()
    profiler.disable()
    profiler.dump_stats("aes.prof")
    print("Profiling complete! Output saved to aes.prof")

