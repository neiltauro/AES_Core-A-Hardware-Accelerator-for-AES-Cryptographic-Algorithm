import aes

key = b"Sixteen byte key"
text = b"TextMustBe16Byte"

@profile
def run_encryption():
    cipher = aes.AES(key)
    for _ in range(10000):
        cipher.encrypt_block(text)

if __name__ == "__main__":
    run_encryption()
