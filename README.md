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

```text
├── aes/                         # Python implementation
│   ├── aes.py                   # Pure Python AES-128 logic
│   ├── tests.py                 # Unit tests
│   ├── profile_aes.py           # cProfile + SnakeViz
│   └── line_profiler_aes.py     # kernprof-based line profiler
├── sv/                          # Synthesizable SystemVerilog modules
│   ├── mix_single_column.sv     # GF(2^8) MixColumns logic
│   └── add_round_key.sv         # 128-bit bitwise XOR logic
├── profiling/                   # Profiling outputs
│   └── aes.prof                 # cProfile results for SnakeViz
├── README.md                    # Project documentation
```

---

## 🔬 Profiling Summary

Profiling was done using `cProfile`, `line_profiler`, and visualized with `SnakeViz`. Key findings:

- 🔺 **`mix_single_column()`** – Most time-consuming operation within `encrypt_block()`
  - Handles Galois Field matrix multiplication over 4 bytes
  - ~50% of total block encryption time
- 🔺 **`add_round_key()`** – Repeated XOR operations over 128-bit blocks
  - Lightweight but frequently executed
- ✅ These functions were chosen for hardware acceleration due to their deterministic, bit-parallel behavior and suitability for FPGA/ASIC design.

---

## ⚙️ Tools Used

| Tool            | Purpose                             |
|-----------------|-------------------------------------|
| **Python 3.8+** | Running AES implementation & profiling |
| `cProfile`      | Function-level performance profiling |
| `line_profiler` | Line-by-line execution timing        |
| `SnakeViz`      | Flame graph + visual call analysis   |
| **SystemVerilog** | RTL design for hardware acceleration |
| `Icarus Verilog` / `ModelSim` | (Optional) HDL simulation |

Install profiling tools via pip:

```bash
pip install snakeviz line_profiler
```

---

## 💡 HDL Acceleration Targets

Based on profiling insights, the following AES subroutines were selected for hardware acceleration using synthesizable SystemVerilog:

---

### 🔷 1. `mix_single_column.sv`

#### 📌 Role:
Performs the **MixColumns** transformation on a single 4-byte column of the AES state matrix using **Galois Field (GF 2⁸) matrix multiplication**.

#### ⚙️ Inputs & Outputs:
- **Input**: 32-bit column (4 bytes: `{s0, s1, s2, s3}`)
- **Output**: 32-bit transformed column

#### 🧠 Logic Overview:
Implements the matrix multiplication:

```
| 2 3 1 1 |   | s0 |
| 1 2 3 1 | * | s1 |
| 1 1 2 3 |   | s2 |
| 3 1 1 2 |   | s3 |
```

Over the Galois Field (GF 2⁸), using `xtime()` for field multiplication by 2 and combinations of XOR operations. This transformation contributes significantly to the security and diffusion of AES, and is computation-heavy in software.

---

### 🔷 2. `add_round_key.sv`

#### 📌 Role:
Applies a **bitwise XOR** between the current AES state and the round key — a core step repeated in every AES round.

#### ⚙️ Inputs & Outputs:
- **Input**: 
  - `state_in` (128-bit AES state)
  - `round_key` (128-bit key for that round)
- **Output**: 
  - `state_out` (128-bit XOR result)

#### 🧠 Logic Overview:
Each byte of the AES state is XOR’d with the corresponding byte from the round key:

```
state_out[i] = state_in[i] ^ round_key[i]
```

---

## 🔗 Source Acknowledgment

This project builds upon the educational open-source AES implementation from:

- **Repository**: [boppreh/aes](https://github.com/boppreh/aes)  
- **Author**: Boaz Yaniv

> *"A minimal implementation of the AES encryption algorithm in pure Python."*

This code was used as the **software baseline** for:
- Functional verification  
- Performance profiling  
- Identifying compute bottlenecks for hardware acceleration
