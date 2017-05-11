# Makefile to build select Microblaze projects.
XILINX_SDK_PATH = /opt/Xilinx/SDK/2017.1
export PATH := ${XILINX_SDK_PATH}/bin:${XILINX_SDK_PATH}/gnu/microblaze/lin/bin:$(PATH)

MBBINS = mailbox.bin \
		arduino_can_bus.bin

all: iop_bins
	@echo "Completed Microblaze Projects' Builds"

mb_bsp: sdk_workspace
	cd bsp_pmod && make && cd ..
	cd bsp_arduino && make && cd ..

%.bin: mb_bsp
	cd $(subst .bin,,$@)/Debug && make clean && make 

iop_bins: $(MBBINS)
	@cp */Debug/*.bin ./bin/


sdk_workspace: base.hdf 
	xsdk -batch -source build_xsdk.tcl

clean:
	rm -f */Debug/*.bin
	rm -f */Debug/*.elf
	rm -f */Debug/*.elf.size
	rm -f */Debug/src/*.o
	rm -f */Debug/src/*.d
	rm -f bin/*
	rm -rf bsp_pmod bsp_arduino hw_def .Xil .metadata SDK.log	
	rm -rf sdk_import
