//
// b a l l . c
//
// Draw a ball on the screen
//
// July 27, 2003 by Wataru Nishida (http://www.wnishida.com)
//

#include "gba.h"
#include "screen.h"
#include "console.h"
#include "printf.h"
#include "sprite.h"

#define MAX_BALLS	12

// Empty interrupt handler

void int_handler(void) {
 }

int main() {
  int i, cnum;
  extern character greenball[];

  // Initialize screen

  init_screen();
  selectpage(BG_TEXT1);
  locate(4, 10);
  printf("%c My first sprites! %c", 2, 2);

  // Initialize sprite

  init_sprite();

  // Draw multiple balls

  cnum = sprite_register(greenball, 4);
  for (i = 0; i < MAX_BALLS; i++) {
    sprite_setup(i, OBJ_16x16, PRIORITY_2ND, cnum);
    sprite_move(i, LCD_WIDTH / MAX_BALLS * i, LCD_HEIGHT / MAX_BALLS * i);
    sprite_display(i, OBJ_TURNON);
   }

  // Loop forever

  while (1) {
   }
 }
