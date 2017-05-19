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

uint8_t mcp2515_reset(uint8_t speed)
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

void clear_buffer(uint8_t *buffer)
{
    for(int i =0; i < MAX_BUFFER_SIZE; ++i)
        buffer[i] = 0xFF;
}

uint8_t mcp2515_get_message(tCAN *message)
{
    clear_buffer(WriteBuffer);
    clear_buffer(ReadBuffer);
    
    uint8_t addr;
    uint8_t i;
    uint8_t status;

    WriteBuffer[0] = SPI_RX_STATUS;
    spi_transfer(SHARED_SPI_BASEADDR, 1, ReadBuffer, WriteBuffer);
    status = ReadBuffer[0];

    if(BIT_IS_SET(status,6)) {
        addr = SPI_READ_RX;
    } else if (BIT_IS_SET(status,7)) {
        addr = SPI_READ_RX | 0x04;
    } else {
        return 0;
    }

    WriteBuffer[0] = addr;
    // GIGO
    spi_transfer(SHARED_SPI_BASEADDR, 20, ReadBuffer, WriteBuffer);

    message->id = (uint16_t) ReadBuffer[1] << 3;
    message->id |= ReadBuffer[2] >> 5;

    message->header.length = ReadBuffer[5] & 0x0F;
    message->header.rtr = (BIT_IS_SET(status,3)) ? 1 : 0;

    // Read in buffer at 4th command
    for(i=6; i < message->header.length+6; ++i)
        message->data[i] = ReadBuffer[i];

    if(BIT_IS_SET(status, 6)) {
        mcp2515_bit_modify(CANINTF, (1<<RX0IF), 0);
    } else {
        mcp2515_bit_modify(CANINTF, (1<<RX1IF), 0);
    }

    return (status & 0x07) + 1;
}

uint8_t mcp2515_send_message(tCAN *message)
{
    clear_buffer(WriteBuffer);
    clear_buffer(ReadBuffer);

    uint8_t addr;
    uint8_t t;
    uint8_t status;

    WriteBuffer[0] = SPI_READ_STATUS;
    spi_transfer(SHARED_SPI_BASEADDR, 1, ReadBuffer, WriteBuffer);
    status = ReadBuffer[0];

    if(!BIT_IS_SET(status,6)) {
        addr = SPI_READ_RX;
    } else if (!BIT_IS_SET(status,7)) {
        addr = SPI_READ_RX | 0x0;
    } else {
        return 0;
    }

    WriteBuffer[0] = SPI_WRITE_TX | addr;
    WriteBuffer[1] = message->id >> 3;
    WriteBuffer[2] = message->id << 5;

    uint8_t length = message->header.length & 0x0f;

    if (message->header.rtr) {
        WriteBuffer[3] = (1<<RTR | length);
    } else {
        WriteBuffer[3] = length;
        for(t=0; t<length; ++t) {
            WriteBuffer[t+4] = message->data[t];
        }
    }
    // GIGO
    spi_transfer(SHARED_SPI_BASEADDR, 20, ReadBuffer, WriteBuffer);

    delay_us(1);

    addr = (addr == 0) ? 1 : addr;
    WriteBuffer[0] = (SPI_RTS | addr);
    spi_transfer(SHARED_SPI_BASEADDR, 1, NULL, WriteBuffer);
    return addr;
}
