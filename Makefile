# Makefile for AES hardware cocotb simulation

# All your Verilog sources (space-separated, paths relative to project root)
VERILOG_SOURCES = \
    $(PWD)/hw/aes_core.v \
    $(PWD)/hw/aes_encipher_block.v \
    $(PWD)/hw/aes_decipher_block.v \
    $(PWD)/hw/aes_key_mem.v \
    $(PWD)/hw/aes_inv_sbox.v \
    $(PWD)/hw/aes_sbox.v

TOPLEVEL = aes_core
MODULE = test_aes_hw
SIM = icarus

# Used by cocotb to find your python code
PYTHONPATH := $(PWD)/src:$(PWD)/sim
export PYTHONPATH

# Find the Cocotb makefile for the simulator
COCOTB_MAKEFILE := $(shell python3 -c 'import cocotb, os; print(os.path.join(os.path.dirname(cocotb.__file__), "share", "makefiles", "Makefile.sim"))')

# HW_AES target runs cocotb using Icarus Verilog as the simulator
HW_AES:
	@echo "Running AES hardware cocotb testbench with icarus..."
	PYTHONPATH="$(PYTHONPATH)" \
	TOPLEVEL="$(TOPLEVEL)" \
	MODULE="$(MODULE)" \
	SIM="$(SIM)" \
	VERILOG_SOURCES="$(VERILOG_SOURCES)" \
	make -f $(COCOTB_MAKEFILE)

# Clean up simulation artifacts and logs
clean:
	rm -rf sim_build __pycache__ *.vcd *.log sim/*.vcd sim/*.log sim/hw_aes_input.txt sim/hw_aes_output.txt .pytest_cache results.xml

.PHONY: HW_AES clean