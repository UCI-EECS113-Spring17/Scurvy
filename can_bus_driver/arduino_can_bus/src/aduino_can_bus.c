#include "mcp2515_defs.h"
#include "mcp2515.h"

#include "arduino.h"
#include "xgpio.h"
#include "xparameters.h"

XGpio 

int ConfigureSpi(void) {
    int status;

    status = XGpio_Initialize();
}