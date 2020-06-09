#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "bullet.h"
#include "item.h"
#include "player.h"
#define SPEED 1

static int sum; // アイテムの取得数の合計
static int item_sprite;
static int loop_count;
static struct bullet item[MAX_ITEM];

static void init(){
    int i;
    sum = 0;
    loop_count = 0;
    for(i = 0; i < MAX_ITEM; i++){
        struct box b = {.x = 0, .y = 10, .width = 8, .height = 8};
        item[i].dx = 0;
        item[i].dy = SPEED;
        item[i].flag = 0;
        item[i].sprite = item_sprite + i;
        item[i].body = b;
        sprite_display(item_sprite + i, OBJ_TURNOFF);
    }
}

int get_sum_item(){ return sum; }

static void cross_item_player(){
    int i;
    for(i = 0; i < MAX_ITEM; i++){
        if(cross_player(&item[i].body)){
            sum++;
            item[i].flag = 0;
            item[i].body.y = 10;
            sprite_display(item_sprite + i, OBJ_TURNOFF);
        }
    }
}

static void item_fire(){
    int i, var;
    for(i = 0; i < MAX_ITEM; i++){
        if(item[i].flag) return;
        var = xorshift32();
        // 確率 1/2 でアイテム生成を生成し、生成された乱数の値を元に出現位置を決定
        if(var & 1){
            item[i].flag = 1;
            item[i].body.x = (var & 255);
            if(item[i].body.x > 232) item[i].body.x = var & 123; 
            sprite_display(item_sprite + i, OBJ_TURNON);
            return;
        } 
    }
}

static void item_move(){
    int i;
    for(i = 0; i < MAX_ITEM; i++){
        if(item[i].flag){
            move_bullet(&item[i]);
        }
    }
}

void item_step(int sprite_num){
    int i;
	item_sprite = sprite_num;

	switch (game_get_state()){
	case TITLE:
        for(i = 0; i < MAX_ITEM; i++) not_display_bullet(&item[i]);
        sum = 0;
		break;
	case START:
        init();
		break;
	case RUNNING:
        if(loop_count > 120){
            item_fire();
            loop_count = 0;
        }
        item_move();
        cross_item_player();
        loop_count++;
		break;
	case STOP:
		break;
	case DEAD:
		break;
	case RESTART:
        init();
		break;
	case CLEAR:
		break;
	default:
		break;
	}
}
