#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "ball.h"
#include "block.h"
#include "racket.h"
#define SPEED           2

static int dx, dy;         /* ボールの現在の速度 */
static int ball_sprite;
static struct box b;          /* ボールの本体 */
static struct box *racket;

// ボールの速さ取得
int ball_get_dy(void) { return dy; }
int ball_get_dx(void) { return dx;}
// ボールの速さ設定
void ball_set_dy(int new_dy) { dy = new_dy; }
void ball_set_dx(int new_dx) { dx = new_dx; }
// ボールの速さ変更
void ball_mul_dx(int mul_dx) { dx *= mul_dx; }
void ball_mul_dy(int mul_dy) { dy *= mul_dy; }
// ボールの座標をいじる
void ball_add_x(int add_x){
	if(b.x + add_x < 240 && b.x + add_x > 0){
		b.x += add_x;
	}else if(b.x + add_x >= 240){
		b.x = 239;
	}else{
		b.x = 0;
	}
	sprite_move(ball_sprite, b.x, b.y);
}
void ball_add_y(int add_y) {
	if(b.y + add_y < 180 && b.y + add_y > 0){
		b.y += add_y;
	}else if(b.y + add_y >= 180){
		b.y = 179;
	}else{
		b.y = 0;
	}
	sprite_move(ball_sprite, b.x, b.y);
}
// ボールのアドレスを返す
struct box *ball_get_box(void) { return &b; }

void ball_step(int sprite_num){
	ball_sprite = sprite_num;
	switch(game_get_state()){
	case TITLE:
		sprite_display(ball_sprite, OBJ_TURNOFF);
		break;
	case START:
		racket = racket_get_box();
		b.width = 10;
        b.height = 10;
		b.x = racket->x + ((racket->width - b.width) >> 1);
		b.y = racket->y - racket->height - 1;
		dy = SPEED;
		dx = SPEED;
        // スプライト
		sprite_move(ball_sprite, b.x, b.y);
		sprite_display(ball_sprite, OBJ_TURNON);	
		break;
	case RUNNING:
		//移動
		b.x += dx;
		b.y += dy;
		sprite_move(ball_sprite, b.x + dx, b.y + dy);
		// 画面端の処理 横
		if(b.x <= 0){
			b.x = -dx;
			sprite_move(ball_sprite, - dx, b.y);
			dx *= -1;
		}else if(b.x + b.width >= 240){
			b.x = 240 - b.width - dx;
			sprite_move(ball_sprite, 240 - b.width - dx, b.y);
			dx *= -1;
		}
		// 画面端の処理 縦
		if(b.y <= 0) {
			b.y = -dy;
			sprite_move(ball_sprite, b.x, -dy);
			if(dy < 0) dy *= -1;
		}
		if(b.y > 160) game_set_state(DEAD);
		break;
	case STOP:
		break;
	case DEAD:
		break;
	case CLEAR:
		break;
	case RESTART:
		b.x = racket->x + (racket->width - b.width) / 2;
        b.y = racket->y - racket->height - 1;
        dy = SPEED;
        dx = SPEED;
        sprite_move(ball_sprite, b.x, b.y);
		break;
	default:
		break;
	}
}
