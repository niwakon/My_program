#include "gba.h"
#include "utils.h"
#include "box.h"

// 四角形を描画する
void draw_box(struct box *b, int x, int y, hword color){
    hword *base, *d;
    int w, h;
    base = (hword*)VRAM + LCD_WIDTH * y + x;
    for(h = b->height; h > 0; h--){
        d = base;
        for(w = b->width; w > 0; w--) *(d++) = color;
        base += LCD_WIDTH;
    }
    b->x = x;
    b->y = y;
}

// 四角形を描画し直す 
void move_box(struct box *b, int x, int y, hword color){
    draw_box(b, b->x, b->y, COLOR_BLACK);
    draw_box(b, x, y, color);
}

// 当たり判定 0始まりなので、等号をつける。
int cross(struct box *b1, struct box *b2){
    if(b1->y <= (b2->y + b2->height) && (b1->y + b1->height) >= b2->y){
	    if(b1->x <= (b2->x + b2->width) && (b1->x + b1->width) >= b2->x) return 1;
    }
    return 0;
}

/*int fcross(struct fbox *b1, struct box *b){
    // それぞれintをfixに変えて足し引き算して
    fix b_y, b_h, b_x, b_w, b1_w, b1_h;
    b_y = int2fix(b->y);
    b_h = int2fix(b->height);
    b_x = int2fix(b->x);
    b_w = int2fix(b->width);
    b1_h = int2fix(b1->height);
    b1_w = int2fix(b1->width);
    if(b1->y <= (b_y + b_h) && (b1->y + b1_h) >= b_y){
        if(b1->x <= (b_x + b_w) && (b1->x + b1_w) >= b_x) return 1;
    }
    return 0;
}*/
	
