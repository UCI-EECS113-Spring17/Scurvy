#include "mcp2515.h"
#include "mcp2515_defs.h"
#include "global.h"

/*
 * Send a byte of data
 */
uint8_t spi_putc(uint8_t data)
{

}

/*
 * Write to an mcp2515 register via SPI
 */
void mcp2515_write_register(uint8_t adress, uint8_t data)
{
    RESET(MCP2515_CS);

    spi_putc(SPI_WRITE);
    spi_putc(address);
    spi_putc(data);

    SET(MCP2515_CS);
}

uint8_t mcp2515_init(uint8_t speed)
{
    // Set SPI Baud rate

    // SPI Handshake
}