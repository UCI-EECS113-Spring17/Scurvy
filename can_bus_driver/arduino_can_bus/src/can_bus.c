#include "can_bus.h"



int main() {
    // Configure SPI to idle low, and sample on rising edges
    arduino_init(0,0,0,0);
    config_arduino_switch(A_GPIO,A_GPIO,A_GPIO,
                          A_GPIO,A_GPIO,A_GPIO,
                          D_UART,
                          D_GPIO,D_GPIO,D_GPIO,
                          D_GPIO,D_GPIO,D_GPIO,
                          D_GPIO,D_GPIO,D_SS,
                          D_MOSI,D_MISO,D_SPICLK);
}