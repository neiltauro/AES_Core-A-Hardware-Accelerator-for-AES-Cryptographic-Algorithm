"""
aes_wrapper.py

Hardware-software co-simulation wrapper for AES block cipher.

This script provides utility functions to communicate between the Python-side AES 
testbench and a Verilog hardware accelerator using cocotb. It writes input vectors 
(test keys, blocks, control signals) to a file, launches the cocotb-based hardware 
simulation via Makefile, and reads output results back into Python for validation.

Functions:
    - aes_encrypt_block_hw(key_tuple, block_tuple): Encrypt a block using hardware.
    - aes_decrypt_block_hw(key_tuple, block_tuple): Decrypt a block using hardware.
    - tuple_to_hex128, tuple_to_hex256, hex128_to_tuple: Data conversion utilities.

Author: Neil Austin Tauro
Date: 06/08/2025
"""


import os
import subprocess

def tuple_to_hex256(tup):
    """Convert (8-word) tuple to 64-digit hex string (big endian, left-padded with zeros if 128b)."""
    if len(tup) == 4:
        tup = tup + (0, 0, 0, 0) # pad to 256b (big endian: high words first)
    return ''.join([f"{w:08x}" for w in tup])

def tuple_to_hex128(tup):
    """Convert (4-word) tuple to 32-digit hex string (big endian)."""
    return ''.join([f"{w:08x}" for w in tup])

def hex128_to_tuple(hexstr):
    """Convert 32-digit hex string to (w0,w1,w2,w3) tuple (big endian)."""
    hexstr = hexstr.lower().replace('0x','').zfill(32)
    return tuple(int(hexstr[i*8:(i+1)*8], 16) for i in range(4))

# Project root = parent of src/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM_DIR = os.path.join(ROOT_DIR, "sim")

def aes_encrypt_block_hw(key_tuple, block_tuple):
    """
    Run AES block encryption on hardware accelerator via cocotb testbench.
    key_tuple: (4 or 8 words)
    block_tuple: (4 words)
    """
    keylen = 0 if len(key_tuple) == 4 else 1
    encdec = 1  # encryption

    input_path = os.path.join(SIM_DIR, 'hw_aes_input.txt')
    output_path = os.path.join(SIM_DIR, 'hw_aes_output.txt')

    # Write test vector
    with open(input_path, 'w') as f:
        f.write(f"{tuple_to_hex256(key_tuple)}\n")
        f.write(f"{tuple_to_hex128(block_tuple)}\n")
        f.write(f"{keylen}\n")
        f.write(f"{encdec}\n")

    print("Running hardware simulation for AES block encrypt...")

    # Run cocotb/Makefile in project root
    ret = subprocess.run(
        ['make', 'HW_AES'],
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if ret.returncode != 0:
        print("Simulation failed:\n", ret.stderr.decode())
        raise RuntimeError("AES hardware simulation failed.")

    # Read result
    with open(output_path, 'r') as f:
        out_line = f.readline().strip()
    return hex128_to_tuple(out_line)

def aes_decrypt_block_hw(key_tuple, block_tuple):
    """
    Run AES block decryption on hardware accelerator via cocotb testbench.
    key_tuple: (4 or 8 words)
    block_tuple: (4 words)
    """
    keylen = 0 if len(key_tuple) == 4 else 1
    encdec = 0  # decryption

    input_path = os.path.join(SIM_DIR, 'hw_aes_input.txt')
    output_path = os.path.join(SIM_DIR, 'hw_aes_output.txt')

    # Write test vector
    with open(input_path, 'w') as f:
        f.write(f"{tuple_to_hex256(key_tuple)}\n")
        f.write(f"{tuple_to_hex128(block_tuple)}\n")
        f.write(f"{keylen}\n")
        f.write(f"{encdec}\n")

    print("Running hardware simulation for AES block decrypt...")

    # Run cocotb/Makefile in project root
    ret = subprocess.run(
        ['make', 'HW_AES'],
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if ret.returncode != 0:
        print("Simulation failed:\n", ret.stderr.decode())
        raise RuntimeError("AES hardware simulation failed.")

    # Read result
    with open(output_path, 'r') as f:
        out_line = f.readline().strip()
    return hex128_to_tuple(out_line)
