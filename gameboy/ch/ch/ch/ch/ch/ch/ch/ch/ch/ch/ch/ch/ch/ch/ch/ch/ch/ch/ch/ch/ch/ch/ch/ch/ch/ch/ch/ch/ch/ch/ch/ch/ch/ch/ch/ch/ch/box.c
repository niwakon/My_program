#include "gba.h"

#define COLOR_WHITE     BGR(31, 31, 31)
#define COLOR_BLACK     0
#define COLOR_RED       BGR(0, 0, 30)
#define COLOR_GREEN     BGR(0, 30, 0)
#define COLOR_BLUE      BGR(30, 0, 0)
#define COLOR_YELLOW    BGR(0, 30, 30)
#define COLOR_AQUA      BGR(30, 30, 0)

struct box {
        int x, y;
        int width, height;
};

void draw_box(struct box *b, int x, int y, hword color)
{
        hword *base, *d;
        int w, h;

        base = (hword*)VRAM + LCD_WIDTH * y + x;

        for(h = b->height; h > 0; h--){
                d = base;
                for(w = b->width; w > 0; w--)
                        *(d++) = color;
                base += LCD_WIDTH;
        }

        b->x = x;
        b->y = y;
}

void move_box(struct box *b, int x, int y, hword color)
{
        draw_box(b, b->x, b->y, COLOR_BLACK);
        draw_box(b, x, y, color);
}
