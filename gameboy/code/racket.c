#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "ball.h"
#include "racket.h"

#define SPEED 4

static int dx;
static int racket_sprite;
static struct box racket = { .x = 95, .y = 130, .width = 32, .height = 8 };
static struct box *ball;

struct box *racket_get_box(){ return &racket; }

/* ラケットの左の面に衝突　return 3
   ラケットの右の面に衝突  return 2
   ラケットの表面に衝突    return 1
   横の誤差 +-3, 縦の誤差 +- 1*/
static int hit(int x, int y){
	int ball_w, ball_h;
	ball_w = ball->width;
	ball_h = ball->height;

	if(x + ball_w <= racket.x + 3  && y + ball_h > racket.y + 1) return 3;
	if(x >= racket.x + racket.width - 3 && y + ball_h > racket.y + 1) return 2;

	// ボールがラケットにめり込んでいたら、押し出す
	if(y + ball_h > racket.y && y <= racket.y + racket.height ){
        ball_add_y(racket.y - ball_h);
    }
	return 1;
}

void racket_step(int num_sprite){
	int key;
    racket_sprite = num_sprite;
    switch(game_get_state()){
	case TITLE:
		racket.x = 95;
		sprite_display(racket_sprite, OBJ_TURNOFF);
		break;
	case START:
		dx = SPEED;
		sprite_move(racket_sprite, racket.x, racket.y);
		sprite_display(racket_sprite, OBJ_TURNON);
		ball = ball_get_box();
		break;
	case RUNNING:
		key = gba_register(KEY_STATUS);
		// 移動
		if( !(key & KEY_LEFT) ){
			if(racket.x > dx){
				racket.x -= dx;
				sprite_move(racket_sprite, racket.x, racket.y);
			}
		}

		if( !(key & KEY_RIGHT) ){
			if(racket.x < 240 - racket.width - dx){
				racket.x += dx;
				sprite_move(racket_sprite, racket.x, racket.y);
			}
		}
		// ボールとの当たり判定
		if(cross(ball, &racket)){
			switch(hit(ball->x, ball->y) ){
			case 1:
				if(ball_get_dy() > 0) ball_mul_dy(-1);
				break;
			case 2:
				if(ball_get_dy() > 0) ball_mul_dy(-1);
				if(ball_get_dx() < 0) ball_mul_dx(-1);
				break;
			case 3:
				if(ball_get_dy() > 0) ball_mul_dy(-1);
				if(ball_get_dx() > 0) ball_mul_dx(-1);
				break;
			default:
				break;
			}
		}
		break;
	case STOP:
		break;
	case DEAD:
		break;
	case CLEAR:
		break;
	case RESTART:
		racket.x = 95;
		racket.y = 130;
		sprite_move(racket_sprite, racket.x, racket.y);
		break;
	default:
		break;
	}
}



