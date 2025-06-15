# AES_Core: Hardware Accelerator for AES Encryption and Decryption

## Overview

**AES_Core** is a hardware accelerator project designed to speed up the enciphering and deciphering operations of the AES (Advanced Encryption Standard) encryption algorithm. The core motivation behind this project is to offload the computationally intensive parts of AES—specifically the block encryption and decryption functions—from a general-purpose CPU to custom digital hardware for significantly improved performance.

## Motivation and Approach

- **Profiling**: Using the [secworks/aes](https://github.com/secworks/aes.git) GitHub repository, I analyzed the Python implementation of AES. Profiling with Snakeviz revealed that the `aes_encipher_block()` function alone took **2.25 milli seconds** for a single runs (see [profilingss.jpeg](https://github.com/neiltauro/AES_Core-A-Hardware-Accelerator-for-AES-Cryptographic-Algorithm/blob/main/profilingss.jpeg) for reference).
- **Initial Attempt**: The first design attempt targeted acceleration of the `mixcolumns()` function (inside `aes_encipher_block()`). However, profiling showed this approach did not yield significant performance improvements.
- **Final Design Choice**: The project shifted to accelerating both `aes_encipher_block()` and `aes_decipher_block()` functions, leading to the design of a unified hardware core—**aes_core**—that integrates both encryption and decryption capabilities.

## Architectural Diagram

![AES Core Architectural Diagram](https://raw.githubusercontent.com/neiltauro/AES_Core-A-Hardware-Accelerator-for-AES-Cryptographic-Algorithm/main/Photos/ArchitecturalDiagram.png)

> The above diagram illustrates the chiplet architecture for **AES_Core**.  
> The main modules include:
> - **Encryption Block (aes_encipher_block)**
> - **Decryption Block (aes_decipher_block)**
> - **Key Schedule Module (aes_key_mem)**
> - **SBox Module (aes_sbox)**
> - **Control Logic (aes_core controller)**

## Implementation Steps

### 1. **Design and Simulation**
- Functional modules were referenced from the [secworks/aes](https://github.com/secworks/aes.git) repository.
- The `aes_core` hardware design was simulated using Modelsim to verify correctness.

### 2. **Hardware/Software Co-Simulation with Cocotb**
- Modified the original Python AES implementation (`aes.py`) to enable hardware offloading:
  - Introduced a mode switch:  
    ```python
    def aes_encipher_block(self, key, block):
        if self.mode == "hardware":
            # Hardware acceleration: call Verilog module via wrapper
            return aes_encrypt_block_hw(key, block)
        else:
            # Original Python implementation
    ```
  - Similar changes were made for decryption.
  - This modified version was saved as `aes_hw.py`.
- Wrote a hardware/software wrapper (`aes_wrapper.py`), a cocotb testbench (`test_aes_hw.py`), and a Makefile.
- Successfully ran cocotb simulations with the hardware core, verifying HW/SW co-simulation.

### 3. **Synthesis and Physical Design with OpenLane**
- Synthesized the `aes_core` module using [OpenLane](https://github.com/The-OpenROAD-Project/OpenLane) (an open-source RTL-to-GDS toolchain).
- All 78 stages completed successfully, producing a final `aes_core.gds` layout.
- Final timing analysis showed a critical path delay of **14.7 nanoseconds**.

## Results

- **Acceleration**: Offloading `aes_encipher_block()` and `aes_decipher_block()` to hardware resulted in a dramatic performance improvement, reducing the execution time from 2.25 milliseconds in software to just 14.7 nanoseconds in hardware — an acceleration of over 150,000×.
- **Silicon-Proven Flow**: The project went through the complete digital implementation flow—RTL design, simulation, hardware/software co-simulation, synthesis, and GDSII generation.


## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/neiltauro/AES_Core-A-Hardware-Accelerator-for-AES-Cryptographic-Algorithm.git
   cd AES_Core-A-Hardware-Accelerator-for-AES-Cryptographic-Algorithm
   ```

2. **Set up Python + Cocotb environment:**
   ```bash
   python3 -m venv cocotb-env
   source cocotb-env/bin/activate
   pip install -r requirements.txt
   ```

3. **Install OpenLane** (via Docker or native build):  
   Refer to [OpenLane documentation](https://github.com/The-OpenROAD-Project/OpenLane)  
   Place `openlane` executable in your `PATH`.

---
