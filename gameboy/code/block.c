#include "gba.h"
#include "utils.h"
#include "game.h"
#include "box.h"
#include "ball.h"
#include "block.h"

#define BLOCK_COLS 8
#define BLOCK_ROWS 3
#define BLOCK_TOP 10
#define BLOCK_WIDTH 30
#define BLOCK_HEIGHT 20
#define BLOCK_NUM BLOCK_COLS * BLOCK_ROWS

static struct box blocks[BLOCK_COLS][BLOCK_ROWS];
static char flags[BLOCK_COLS][BLOCK_ROWS];
static int num_blocks;
static int updown, leftright;
static struct box *ball;

// ブロックとボールが当たっていれば1を返す
static int hit(int x, int y){
	int i,j;
	i = x / BLOCK_WIDTH;
	j = (y - BLOCK_TOP) / BLOCK_HEIGHT;
	if(i < 0 || j >= BLOCK_ROWS) return 0;
	if(j < 0 || i >= BLOCK_COLS) return 0;
	if(flags[i][j]) return 1;
	return 0;
}

static void delete(int x, int y){
	int i, j;
	i = x / BLOCK_WIDTH;
    j = (y - BLOCK_TOP) /  BLOCK_HEIGHT;
	draw_box(&blocks[i][j], blocks[i][j].x, blocks[i][j].y, COLOR_BLACK);
	if(flags[i][j] == 1) {
		num_blocks--;
		flags[i][j] = 0;
	}
	
}

static void all_delete_block(){
	int i, j;
	if(num_blocks <= 0) return;
	for(i = 0; i < BLOCK_COLS; i++){
		for(j = 0; j < BLOCK_ROWS; j++){
			draw_box(&blocks[i][j], blocks[i][j].x, blocks[i][j].y, COLOR_BLACK);
			num_blocks--;
		}
	}
}

void block_step(void){
	int i,j, bx, by, upleft, upright, downleft, downright;
	switch (game_get_state()) {
	case TITLE:
		all_delete_block();
		break;
	case START:
		if(num_blocks != BLOCK_NUM){
			for(i = 0; i < BLOCK_COLS; i++){
				for(j = 0; j < BLOCK_ROWS; j++){
					blocks[i][j].x = i * BLOCK_WIDTH;
					blocks[i][j].y = j * BLOCK_HEIGHT + BLOCK_TOP;
					blocks[i][j].width = BLOCK_WIDTH - 1;
					blocks[i][j].height = BLOCK_HEIGHT - 1;
					flags[i][j] = 1;
					draw_box(&blocks[i][j], blocks[i][j].x, blocks[i][j].y, COLOR_AQUA);
				}
			}
		}
		updown = 0;
		leftright = 0;
		num_blocks = BLOCK_NUM;
	    break;
	case RUNNING:
		ball = ball_get_box();
		bx = ball->x;
		by = ball->y;
		updown = 0;
		leftright = 0;
		upleft = 0;
		upright = 0;
		downleft = 0;
		downright = 0;
		// ボールのどの部分がブロックに当たったか調べる当たったか調べる
		if((upleft = hit(bx, by))){
			updown++;
			leftright++;
		}
		if((upright = hit(bx + ball->width, by))){
			updown++;
			leftright--;
		}
		if((downleft = hit(bx, by + ball->height))){
			updown--;
			leftright++;
		}
		if((downright = hit(bx + ball->width, by + ball->height))){
			updown--;
			leftright--;
		}
		// 当たった結果ボールがどう跳ね返るか
		if(updown > 0 && ball_get_dy() < 0) ball_mul_dy(-1);
		else if(updown < 0 && ball_get_dy() > 0) ball_mul_dy(-1);

		if(leftright > 0 && ball_get_dx() < 0) ball_mul_dx(-1);
		else if(leftright < 0 && ball_get_dx() > 0) ball_mul_dx(-1);

		//  当たったブロックを削除
		if(upleft) delete(bx, by);
        if(upright) delete(bx + ball->width, by);
        if(downleft) delete(bx, by + ball->height);
        if(downright) delete(bx + ball->width, by + ball->height);
		
		// ゲームの終了判定
		if(num_blocks <= 0) game_set_state(CLEAR);
		break;
	case STOP:
		break;
	case DEAD:
		break;
	case RESTART:
		if(num_blocks != BLOCK_NUM){
			for(i = 0; i < BLOCK_COLS; i++){
    	        for(j = 0; j < BLOCK_ROWS; j++){
        	        blocks[i][j].x = i * BLOCK_WIDTH;
            	    blocks[i][j].y = j * BLOCK_HEIGHT + BLOCK_TOP;
                	blocks[i][j].width = BLOCK_WIDTH - 1;
               		blocks[i][j].height = BLOCK_HEIGHT - 1;
                	flags[i][j] = 1;
                	draw_box(&blocks[i][j], blocks[i][j].x, blocks[i][j].y, COLOR_AQUA);
            	}
        	}
		}
		num_blocks = BLOCK_NUM;
		updown = 0;
		leftright = 0;
		break;
	case CLEAR:
		break;
	}
}
