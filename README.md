# 🔐 TinyAES-HW: Hardware Acceleration of AES MixColumns and AddRoundKey

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![SystemVerilog](https://img.shields.io/badge/SystemVerilog-Synthesizable-green)]()
[![SnakeViz](https://img.shields.io/badge/Profiling-SnakeViz-yellow)](https://jiffyclub.github.io/snakeviz/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📘 Overview

This project accelerates the bottleneck operations of the AES-128 encryption algorithm using custom-designed hardware. By profiling a Python implementation of AES, we identified two computationally expensive functions — `MixColumns` and `AddRoundKey` — and implemented them in **synthesizable SystemVerilog** for efficient execution on hardware like FPGAs.

---

## 🔎 Motivation

AES (Advanced Encryption Standard) is a cornerstone of modern cryptography, used in secure data transmission (TLS, VPNs), wireless encryption (WPA2/WPA3), and embedded systems. The algorithm is computation-heavy and benefits greatly from hardware acceleration — particularly in Galois field operations and bitwise XORs.

This project aims to:
- 📈 Identify time-consuming AES sub-functions through profiling
- 🛠 Implement those functions in synthesizable HDL
- 🔄 Explore co-design strategies between Python and RTL logic

---

## 🧩 Architecture

> 🔧 The following diagram illustrates the integration of software and hardware components in the AES pipeline:

![AES Hardware Acceleration Diagram](./A_diagram_illustrates_a_hardware-accelerated_AES_(.png)

---

## 📂 Repository Structure

├── aes/ # Python implementation
│ ├── aes.py # Pure Python AES-128 logic
│ ├── tests.py # Unit tests
│ ├── profile_aes.py # cProfile + SnakeViz
│ └── line_profiler_aes.py # kernprof-based line profiler
├── sv/ # Synthesizable SystemVerilog modules
│ ├── mix_single_column.sv # GF(2^8) MixColumns logic
│ └── add_round_key.sv # 128-bit bitwise XOR logic
├── profiling/
│ └── aes.prof # cProfile results for SnakeViz
├── README.md


---

## 🔬 Profiling Summary

Using `cProfile` and `SnakeViz`, we observed the following:

- 🔺 `mix_single_column()` → **dominates execution time** (687 ms out of 1.4 s)
- 🔺 `add_round_key()` → frequent XOR operation; easy to parallelize in hardware
- 📌 `encrypt_block()` → top-level target function composed of smaller AES steps

These observations guided the decision to accelerate these two subroutines in SystemVerilog.

---

## ⚙️ Tools Used

- [Python 3.8+](https://www.python.org/)
- [SnakeViz](https://jiffyclub.github.io/snakeviz/) for flame graph visualization
- [line_profiler](https://github.com/pyutils/line_profiler) for precise function timing
- [SystemVerilog (synthesizable)](https://ieeexplore.ieee.org/document/5764786) for RTL implementation

To install profiling tools:

```bash
pip install snakeviz line_profiler

⚙️ HDL Acceleration Targets
mix_single_column.sv: Accepts 32-bit AES column, performs GF(2⁸) matrix multiplication

add_round_key.sv: 128-bit XOR between state and round key

These modules are synthesizable and ready for FPGA deployment or testbench simulation.

🚀 Future Work
🔁 Add full AES pipeline in RTL

🧪 Integrate with cocotb for verification

⛓️ Implement CBC mode or streaming AES

🚀 Synthesize and benchmark on FPGA
