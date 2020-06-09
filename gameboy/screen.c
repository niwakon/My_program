#include "gba.h"
#include "utils.h"
#include "game.h"
#include "box.h"
#include "item.h"
#include "enemy.h"
#include "player.h" 
#include "screen.h"

static char time[6] = "00:00";
static char result[7] = "Score:";
static int count, sum, score;
static int high_score = 0;
static int init = 1;

static void display_timer(){
	setcolor(COLOR_WHITE);
	locate(200, 0); 
	putstr(time);
}

static void init_timer(){
	int i;
	for(i = 0; i < 5; i++) time[i] = '0';
	time[2] = ':';
}

static void not_display_timer(){
	setcolor(COLOR_BLACK);
	locate(200, 0); 
	putstr(time);
}

static void add_time(){
	int i;
	not_display_timer();
	time[4] = (char)((int)time[4] + 1);
	for(i = 4; i >= 0; i--){
		if(i == 2) continue;
		if(i == 3 ){
			if(time[i] == '6'){
				time[i] = '0';
				time[i - 2] = (char) (time[i - 2] + 1);
			}
		}else if( time[i] == (char) ('9' + 1 ) ){
			time[i] = '0';
			time[i - 1] = (char) (time[i - 1] + 1);
		}
	}
}

static void display_score(int x, int y, int val, char* str){
	locate(x, y);
	if(score > high_score){
		setcolor(COLOR_RED);
		putstr("new ");
	}	
	setcolor(COLOR_YELLOW);
	putstr(str);
	putint(val);
}

static void not_display_high_score(int x, int y, int val, char* str){
	locate(x, y);
	setcolor(COLOR_BLACK);
    putstr(str);
    putint(val);
}

static void not_display_score(int x, int y, int val, char* str){
	setcolor(COLOR_BLACK);
    locate(x, y);
	if(score > high_score) putstr("new ");
    putstr(str);
    putint(val);
}

void screen_step(){
	switch (game_get_state()){
	case TITLE:
		not_display_timer();
		init_timer();
		not_display_high_score(0, 0, high_score, "Best:");
		init = 1;
		break;
	case START:
		count = 0;
		sum = 0;
		score = 0;
		if(init){
			display_timer();
			display_score(0, 0, high_score, "Best:");
			init = 0;
		}
		break;
	case RUNNING:
		if(count >= 60){
			count = 0;
			add_time();
			display_timer();
			sum++;
		}
		count++;
		break;
	case STOP:
		break;
	case DEAD:
		init = 1;
		break;
	case CLEAR:
		if(init == 0){
			score = 500 - sum * 10; // 残り時間ボーナス
			score -= player_sum_shot() * 2; // 弾数ボーナス
			score += get_sum_item() * 5;
			if(game_get_mode() == -2) score -= 200;
			if(score < 0) score = 0;
			score += 500; // クリア得点
			display_score(70, 0, score, result);
			init = 1;
		}
		break;
	case RESTART:
		if(init){
			not_display_timer();
			not_display_score(70, 0, score, result);
			if(score > high_score){
                not_display_high_score(0, 0, high_score, "Best:");
                high_score = score;
                display_score(0, 0, high_score, "Best:");
            }
			init_timer();
			count = 0;
			sum = 0;
			score = 0;
			display_timer();
			init = 0;
		}
		break;
	default:
		break;
	}
}
