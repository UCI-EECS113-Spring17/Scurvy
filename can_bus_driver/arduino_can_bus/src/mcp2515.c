#include "mcp2515.h"

void mcp2515_write_register(uint8_t address, uint8_t data)
{
    WriteBuffer[0] = SPI_WRITE;
    WriteBuffer[1] = address;
    WriteBuffer[2] = data;
    spi_transfer(SHARED_SPI_BASEADDR, 3, NULL, WriteBuffer);
}

uint8_t mcp2515_read_register(uint8_t address)
{
    WriteBuffer[0] = SPI_READ;
    WriteBuffer[1] = address;
    WriteBuffer[2] = 0xFF;

    spi_transfer(SHARED_SPI_BASEADDR, 3, ReadBuffer, WriteBuffer);
    return ReadBuffer[2];
}

void mcp2515_bit_modify(uint8_t address, uint8_t mask, uint8_t data)
{
    WriteBuffer[0] = SPI_BIT_MODIFY;
    WriteBuffer[1] = address;
    WriteBuffer[2] = mask;
    WriteBuffer[3] = data;
    spi_transfer(SHARED_SPI_BASEADDR, 4, NULL, WriteBuffer);
}

uint8_t mcp2515_read_status(uint8_t type)
{
    WriteBuffer[0] = type;
    WriteBuffer[1] = 0xFF;
    spi_transfer(SHARED_SPI_BASEADDR, 2, ReadBuffer, WriteBuffer);
    return ReadBuffer[1];
}

uint8_t mcp2515_init(uint8_t speed)
{
    WriteBuffer[0] = SPI_RESET;
    spi_transfer(SHARED_SPI_BASEADDR, 1, NULL, WriteBuffer);

    delay_us(10);
    WriteBuffer[0] = SPI_WRITE;
    WriteBuffer[1] = CNF3;
    WriteBuffer[2] = (1<<PHSEG21);
    WriteBuffer[3] = (1<<BTLMODE)|(1<<PHSEG11);
    WriteBuffer[4] = speed;
    WriteBuffer[5] = (1<<RX1IE)|(1<<RX0IE);
    spi_transfer(SHARED_SPI_BASEADDR, 6, NULL,  WriteBuffer);

    	// test if we could read back the value => is the chip accessible?
	if (mcp2515_read_register(CNF1) != speed) {
		return 0;
	}
	
	// deaktivate the RXnBF Pins (High Impedance State)
	mcp2515_write_register(BFPCTRL, 0);
	
	// set TXnRTS as inputs
	mcp2515_write_register(TXRTSCTRL, 0);
	
	// turn off filters => receive any message
	mcp2515_write_register(RXB0CTRL, (1<<RXM1)|(1<<RXM0));
	mcp2515_write_register(RXB1CTRL, (1<<RXM1)|(1<<RXM0));
	
	// reset device to normal mode
	mcp2515_write_register(CANCTRL, 0);
//	SET(LED2_HIGH);
	return 1;
}

uint8_t mcp2515_check_free_buffer()
{
    if ( (mcp2515_read_status(SPI_READ_STATUS) & 0x54) == 0x54 )
        return 0;
    return 1;
}