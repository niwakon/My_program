#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "enemy.h"
#include "player.h"
#include "ball.h"
#include "block.h"
#include "item.h"
#include "racket.h"
#include "screen.h"

// 垂直ブランク期間になるまで待つ
void wait_until_vblank(void){
    while((gba_register(LCD_STATUS) & 1) == 0);
}
// 垂直ブランク期間が終わるまで待つ
void wait_while_vblank(void){
    while((gba_register(LCD_STATUS) & 1));
}

main(){
    gba_register(LCD_CTRL) = LCD_BG2EN | LCD_MODE3;

    gba_register(TMR_COUNT0) = 0;
    gba_register(TMR_CTRL0 ) = TMR_ENABLE + TMR_1024CLOCK;

    extern character whiteball[];
    extern character laser[];
    extern character racket_ch[];
    extern character enemy1[];
    extern character enemy2[];
    extern character enemy3[];
    extern character enemy4[];
    extern character enemy5[];
    extern character player_ch[];
    extern character marker[];
    extern character point[];
    
    int cnum, ball_sprite, racket_sprite, player_sprite, pb_sprite, enemy_sprite, eb_sprite, marker_sprite, sprite_num, item_sprite, i;
    sprite_num = 0;
    init_sprite();
    // 自機の登録
    cnum = sprite_register(player_ch, 4) + 512;
    player_sprite = sprite_num;
    sprite_setup(player_sprite, OBJ_16x16, PRIORITY_1ST, cnum);
    sprite_num++;
    // 自機の弾の登録
    cnum = sprite_register(laser, 1) + 512;
    pb_sprite = sprite_num;
    for(i = 0; i < MAX_BULLET; i++){
        sprite_setup(sprite_num, OBJ_8x8, PRIORITY_1ST, cnum);
        sprite_num++;
    }
     // エネミー登録
    enemy_sprite = sprite_num;
    cnum = sprite_register(enemy2, 8) + 512;
    sprite_setup(sprite_num, OBJ_32x16, PRIORITY_1ST, cnum);
    sprite_num++;
    cnum = sprite_register(enemy3, 8) + 512;
    sprite_setup(sprite_num, OBJ_32x16, PRIORITY_1ST, cnum);
    sprite_num++;
    cnum = sprite_register(enemy4, 8) + 512;
    sprite_setup(sprite_num, OBJ_32x16, PRIORITY_1ST, cnum);
    sprite_num++;
    cnum = sprite_register(enemy5, 8) + 512;
    sprite_setup(sprite_num, OBJ_32x16, PRIORITY_1ST, cnum);
    sprite_num++;
    // エネミーの弾登録
    eb_sprite = sprite_num;
    cnum = sprite_register(enemy1, 1) + 512;
    for(i = 0; i < ENEMY_BULLET; i++){
        sprite_setup(sprite_num, OBJ_8x8, PRIORITY_1ST, cnum);
        sprite_num++;
    }
    // ラケットの登録
    racket_sprite = sprite_num;
    cnum = sprite_register(racket_ch, 4) + 512;
    sprite_setup(sprite_num, OBJ_32x8, PRIORITY_1ST, cnum);
    sprite_num++;
    // ボールの登録
    ball_sprite = sprite_num;
    cnum = sprite_register(whiteball, 1) + 512;
    sprite_setup(ball_sprite, OBJ_8x8, PRIORITY_1ST, cnum);
    sprite_num++;
    // 点の登録
    marker_sprite = sprite_num;
    cnum = sprite_register(marker, 1) + 512;
    sprite_setup(sprite_num, OBJ_8x8, PRIORITY_1ST, cnum);
    sprite_num++;
    // アイテムの登録
    item_sprite = sprite_num;
    cnum = sprite_register(point, 1) + 512;
    for(i = 0; i < MAX_ITEM; i++){
        sprite_setup(sprite_num, OBJ_8x8, PRIORITY_1ST, cnum);
        sprite_num++;
    }
    
    while(1){
        wait_until_vblank();
        if(game_get_mode() == 1){
            // ブロック崩し
            ball_step(ball_sprite);
            racket_step(racket_sprite);
            block_step();
        }else{
            // シューティング
            if(game_get_mode() == -2) player_step(player_sprite, pb_sprite, 2);
            else player_step(player_sprite, pb_sprite, 1);
            enemy_step(enemy_sprite, eb_sprite);
            item_step(item_sprite);
            screen_step();
        }
        game_step(marker_sprite);
        wait_while_vblank();
    }
}
