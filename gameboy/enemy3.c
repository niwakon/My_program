#include "gba.h"

character enemy5[] = {
    {{0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000}}, // 0
    {{0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0505, 0x0000,
      0x0000, 0x0000, 0x0505, 0x0000,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0000, 0x0505,
      0x0505, 0x0505, 0x0000, 0x0505}}, // 1
    {{0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0505, 0x0000,
      0x0000, 0x0000, 0x0505, 0x0000,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0000, 0x0505,
      0x0505, 0x0505, 0x0000, 0x0505}}, // 2
    {{0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0505, 0x0000, 0x0000, 0x0000,
      0x0505, 0x0000, 0x0000, 0x0000,
      0x0505, 0x0000, 0x0000, 0x0000,
      0x0505, 0x0000, 0x0000, 0x0000}}, // 3
    {{ 0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000}}, // 4
    {{ 0x0505, 0x0505, 0x0505, 0x0505,
      0x0000, 0x0505, 0x0505, 0x0505,
      0x0000, 0x0505, 0x0505, 0x0505,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0505, 0x0505,
      0x0000, 0x0000, 0x0505, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0000}}, // 5
    {{ 0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0505, 0x0505, 0x0505, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0000, 0x0000, 0x0505,
      0x0000, 0x0505, 0x0505, 0x0000,
      0x0000, 0x0505, 0x0505, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000}}, // 6
    {{ 0x0505, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0505, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000,
      0x0000, 0x0000, 0x0000, 0x0000}}, // 7
};
