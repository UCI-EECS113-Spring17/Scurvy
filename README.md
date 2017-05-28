# Scurvy


# Building CanBus Driver
There are several requirements to build the CanBus Driver
1. Xilinx SDK must be installed (Specify install location in `./can_bus_driver/makefile` as `XILINX_SDK_PATH`)
2. `bsp_pmod`, `bsp_arduino` and `base.hdf` must be copied to `can_bus_driver` from the [PYNQ repository](https://github.com/Xilinx/PYNQ)

# Installation
Requires that `arduino_can_bus.bin` be built
1. Copy `python/can` folder to the PYNQ home directory
2. Copy `arduino_can_bus.bin` from `can_bus_driver/bin` to the `can` folder on the PYNQ
3. Run `deploy.sh`

# Usage
1. `from pynq.iop.arduino_can_bus import Can,Message`
