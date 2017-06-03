#ifndef __SHIELD_H
#define __SHIELD_H

#include "arduino.h"
#include "mcp2515.h"
#include <stdlib.h>

// Mailbox commands
#define RESET       0x01
#define READ        0x02
#define WRITE       0x03
#define BIT_MODIFY  0x04
#define READ_STATUS 0x05
#define GET_MESSAGE 0x06
#define SEND_MESSAGE 0x07
#define CHECK_MESSAGE 0x08

#define LED_7 0x07
#define LED_8 0x08

// Test commands
#define TEST_MESSAGE_WRITE 0xFF
#define TEST_MESSAGE_READ 0xFE


void read_from_mailbox(tCAN *message);

void write_to_mailbox(tCAN *message);

#endif
 