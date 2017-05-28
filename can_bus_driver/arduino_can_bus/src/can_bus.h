#ifndef __SHIELD_H
#define __SHIELD_H

#include "arduino.h"
#include "mcp2515.h"
#include <stdlib.h>

// Mailbox commands
#define RESET       0xFF
#define READ        0xFE
#define WRITE       0xFD
#define BIT_MODIFY  0xFC
#define READ_STATUS 0xFB
#define GET_MESSAGE 0xEF
#define SEND_MESSAGE 0xEE
#define CHECK_MESSAGE 0xED

void read_from_mailbox(tCAN *message);

void write_to_mailbox(tCAN *message);

#endif
 