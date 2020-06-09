//
// s p r i t e . h
//
// Sprite driver
//
// July 27, 2003 by Wataru Nishida (http://www.skyfree.org)
//

#include "gba.h"

#ifndef _SPRITE_H_
#define _SPRITE_H_

void sprite_setup(int snum, int shape, int priority, int cnum);
void sprite_display(int snum, int swt);
void sprite_move(int snum, int x, int y);
int  sprite_register(character* ch, int size);
void init_sprite(void);

#endif
