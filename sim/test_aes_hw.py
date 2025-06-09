"""
test_aes_hw.py

Cocotb-based testbench for AES hardware accelerator.

This testbench reads AES key, block, key length, and encryption/decryption control
from a test vector input file, drives them to the DUT (Device Under Test), and 
writes the output ciphertext/plaintext to an output file for comparison with 
expected values. Designed to work with the Python AES wrapper for hardware-software 
co-simulation.

Test(s):
    - test_aes_hw_block: Runs an AES encryption or decryption block test with DUT.

Author: Neil Austin Tauro
Date: 06/08/2025
"""


import os
import cocotb
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_aes_hw_block(dut):
    """
    Cocotb test: Drives AES core from file input, writes result to output.
    """
    cocotb.start_soon(clock_gen(dut.clk))

    # Always use sim/ directory (this script's location) for file I/O
    SIM_DIR = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(SIM_DIR, 'hw_aes_input.txt')
    output_path = os.path.join(SIM_DIR, 'hw_aes_output.txt')

    with open(input_path,'r') as f:
        key_hex   = f.readline().strip()
        block_hex = f.readline().strip()
        keylen    = int(f.readline().strip())
        encdec    = int(f.readline().strip())

    cocotb.log.info(f"Read key={key_hex} block={block_hex} keylen={keylen} encdec={encdec}")

    # Reset
    dut.reset_n.value = 0
    await Timer(10, units='ns')
    dut.reset_n.value = 1
    await RisingEdge(dut.clk)

    # Key expansion/init
    dut.key.value    = int(key_hex, 16)
    dut.keylen.value = keylen
    dut.init.value   = 1
    dut.next.value   = 0
    dut.encdec.value = encdec
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)   # Keep init high for 2 cycles
    dut.init.value = 0

    # Wait for ready = 1 (key schedule done)
    while not int(dut.ready.value):
        await RisingEdge(dut.clk)

    # Encryption/Decryption phase
    dut.block.value  = int(block_hex, 16)
    dut.next.value   = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)   # Keep next high for 2 cycles
    dut.next.value   = 0

    # Wait for result_valid
    while not int(dut.result_valid.value):
        await RisingEdge(dut.clk)

    cipher = int(dut.result.value)
    cocotb.log.info(f"Writing result to {output_path}: {cipher:032x}")
    with open(output_path, 'w') as f:
        f.write(f"{cipher:032x}\n")

async def clock_gen(clk):
    """Simple clock generator, 10ns period."""
    while True:
        clk.value = 0
        await Timer(5, units='ns')
        clk.value = 1
        await Timer(5, units='ns')
