#ifndef __SHIELD_H
#define __SHIELD_H

#include "arduino.h"
#include "mcp2515.h"

void read_from_mailbox(tCAN *message);

void write_to_mailbox(tCAN *message);

#endif
 