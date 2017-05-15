#include "can_bus.h"

// Mailbox commands
#define RESET       0xFF
#define READ        0xFE
#define WRITE       0xFD
#define BIT_MODIFY  0xFC
#define READ_STATUS 0xFB
#define GET_MESSAGE 0xEF
#define SEND_MESSAGE 0xEE


void read_mailbox_message(tCAN *message)
{
    // Read in id
    message->id = 0;
    message->id |= (uint8_t)MAILBOX_DATA_ADDR(0);
    message->id |= (uint8_t)(MAILBOX_DATA_ADDR(1)<<4);

    message->header.rtr = (int8_t)MAILBOX_DATA_ADDR(2);
    message->header.length = (uint8_t)MAILBOX_DATA_ADDR(3);

    for(int i = 0; i < 8; ++i) {
        message->data[i] = MAILBOX_DATA_ADDR(4+i);
    }
}

void write_mailbox_message(tCAN *message)
{
    MAILBOX_DATA_ADDR(0) = (int8_t)message->id;
    MAILBOX_DATA_ADDR(1) = (int8_t)(message->id>>4);
    MAILBOX_DATA_ADDR(2) = message->header.rtr;
    MAILBOX_DATA_ADDR(3) = message->header.length;

    for(int i = 0; i < 8; ++i) {
        MAILBOX_DATA_ADDR(4+i) = message->data[i];
    }
}

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

    while(1) {
        // Command address is empty (ie no commands)
        // We might want to actually do some work while idle
        while(MAILBOX_CMD_ADDR == 0x00);

        switch(MAILBOX_CMD_ADDR) {
            case RESET:
                mcp2515_reset(MAILBOX_DATA(0));
                break;
            case READ:
                MAILBOX_DATA(0) = mcp2515_read_register(MAILBOX_DATA(0));
                break;
            case WRITE:
                mcp2515_write_register(MAILBOX_DATA(0),MAILBOX_DATA(1));
                break;
            case BIT_MODIFY:
                mcp2515_bit_modify(MAILBOX_DATA(0),MAILBOX_DATA(1),MAILBOX_DATA(2));
                break;
            case READ_STATUS:
                mcp2515_read_status(MAILBOX_DATA(0));
                break;
            case GET_MESSAGE:
                tCAN *message = malloc(sizeof(tCAN));
                write_mailbox_message(message);
                mcp2515_get_message(message);
                free(message);
                break;
            case SEND_MESSAGE:
                tCAN *message = malloc(sizeof(tCAN));
                read_mailbox_message(message);
                mcp2515_send_message(message);
                free(message);
                break;
            default:
                break;
        }
        // Reset mailbox command to a finished state
        MAILBOX_CMD_ADDR = 0x00;

    }
}