#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "box.h"
#include "bullet.h"

void display_bullet(struct bullet *bu, int x, int y){
    bu->body.x = x;
    bu->body.y = y;
    sprite_move(bu->sprite, bu->body.x, bu->body.y);
    sprite_display(bu->sprite, OBJ_TURNON);
}

void not_display_bullet(struct bullet *bu){
    sprite_display(bu->sprite, OBJ_TURNOFF);
    bu->flag = 0;
}

void move_bullet(struct bullet *bu){
    int x, y;
    x = (bu->body.x += bu->dx);
    y = (bu->body.y += bu->dy);
    sprite_move(bu->sprite, x, y);
    // 画面外に消えたら消す
    if(x + bu->body.width < 0 || x >240 || y < 0 || y + bu->body.height > 160) not_display_bullet(bu);
}

// 横の画面端では反射をする弾
void move_reflection_bullet(struct bullet *bu){
    int x, y;
    x = (bu->body.x += bu->dx);
    y = (bu->body.y += bu->dy);
    sprite_move(bu->sprite, x, y);
    
    if(x < 0 || x + bu->body.width >240) bu->dx *= -1;
    if(y < 0 || y + bu->body.height > 160) not_display_bullet(bu);
}
