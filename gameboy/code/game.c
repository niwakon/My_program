#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"

static enum state current_state; // 現在の状態
static int game_mode = -1; // シューティング or ブロック崩し
static int count = 0;      // ループ数を数える

enum state game_get_state(void){ return current_state; }

void game_set_state(enum state new_state){
    current_state = new_state;
}

int game_get_mode(void){ return game_mode; }

void game_step(int point_sprite){
    int key;
    key = gba_register(KEY_STATUS);

    switch (game_get_state()){
    case TITLE:
        setcolor(COLOR_WHITE);
        locate(60, 40);
        putstr("SELECT GAME");
        locate(60, 50);
        putstr("PUSH 'A'");
        locate(60, 100);
        putstr("SHOOTING");
        locate(60, 120);
        putstr("BLOCK BREAK");

        // ゲームの選択
        if(!(key & KEY_UP) || !(key & KEY_DOWN)){
            game_mode *= -1;
            count = 0;
            while(!(key & KEY_UP) || !(key & KEY_DOWN)) key = gba_register(KEY_STATUS);
        }
	    // 三角形のマーカー処理 (移動・点滅)
        if(game_mode == -1) sprite_move(point_sprite, 50, 99);
        else sprite_move(point_sprite, 50, 119);
        if(count < 30) sprite_display(point_sprite, OBJ_TURNON);
        else sprite_display(point_sprite, OBJ_TURNOFF);

        // ゲーム開始
	    if(!(key & KEY_A)){
            if(game_mode == -1 && !(key & KEY_LEFT)) game_mode = -2;
            setcolor(COLOR_BLACK);
            locate(60, 40);
            putstr("SELECT GAME");
            locate(60, 50);
            putstr("PUSH 'A'");
            locate(60, 100);
            putstr("SHOOTING");
            locate(60, 120);
            putstr("BLOCK BREAK");
            sprite_display(point_sprite, OBJ_TURNOFF);
            game_set_state(START);
        }

        count++;
        if(count >= 60) count = 0;
        break;
    case START:
	if(!(key & KEY_START)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_START) break;
            }
            game_set_state(RUNNING);
        }
        break;
    case RUNNING:
	if(!(key & KEY_SELECT)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_SELECT) break;
            }
            game_set_state(STOP);
        }
        break;
    case STOP:
        setcolor(COLOR_WHITE);
        locate(105, 110);
        putstr("STOP");
        if (!(key & KEY_SELECT)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_SELECT) break;
            }
            setcolor(COLOR_BLACK);
            locate(105, 110);
            putstr("STOP");
            game_set_state(RUNNING);
        }
        if(!(key & KEY_R) && !(key & KEY_L)){
            setcolor(COLOR_BLACK);
            locate(105, 110);
            putstr("STOP");
            if(game_mode < -1) game_mode = -1;
            game_set_state(TITLE);
        }
        break;
    case DEAD:
        setcolor(COLOR_RED);
        locate(85, 110);
        putstr("GAME OVER");
        if(!(key & KEY_START)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_START) break;
            }
            setcolor(COLOR_BLACK);
            locate(85, 110);
            putstr("GAME OVER");
            game_set_state(RESTART);
        }
        break;
    case RESTART:
        if (! (key & KEY_START)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_START) break;
            }
            game_set_state(RUNNING);
	}
        break;
    case CLEAR:
        setcolor(COLOR_YELLOW);
        locate(85, 110);
        putstr("GAME CLEAR");
        if (! (key & KEY_START)){
            while(1){
                key = gba_register(KEY_STATUS);
                if(key & KEY_START) break;
            }
            setcolor(COLOR_BLACK);
            locate(85, 110);
            putstr("GAME CLEAR");
            game_set_state(RESTART);
        }
        break;
    }
}
