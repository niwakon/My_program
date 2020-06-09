#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "bullet.h"
#include "enemy.h"
#include "player.h"

#define ENEMY_WIDTH 22
#define ENEMY_HEIGHT 15
#define INVINCIBLE 120
#define APPEAR_TIME 60

static struct box enemy_body[MAX_ENEMY];
static struct bullet enemy_bullet[MAX_ENEMY][ENEMY_BULLET];
static int num_bullet[MAX_ENEMY]; // 各敵の弾のインデックス
static int speed[MAX_ENEMY][2];   /*速度 [][0] 横方向 [][1] 縦方向*/
static int cool_time[MAX_ENEMY];  // 敵の攻撃と攻撃の間
static int num_enemy;             // 敵の数
static int enemy_life;            // 敵の残機
static int level;                 // 現在の敵のレベル
static int enemy_3_tackle_flag;   // 3体目の敵の行動(突進)フラグ
static int invincible_time;       // ダメージを受けた後の無敵時間
static int appear_time;           // 出現時間
static int loop_count;            // 何ループ目か記憶
static int enemy_sprite, eb_sprite;

// 自機の弾
extern struct bullet player_bullets[];

static void enemy_reload(int index_e, int index_b){
    not_display_bullet(&enemy_bullet[index_e][index_b]);
    enemy_bullet[index_e][index_b].flag = 0;
    num_bullet[index_e]++;
}

static void all_reload(int index_e){
    int i = 0;
    for(i = 0; i < ENEMY_BULLET;i++){
        if(enemy_bullet[index_e][i].flag) enemy_reload(index_e, i);
    }
}

// 横移動のみ
static void enemy_move1(int index){
    // 画面外へ行かないように移動方向変更
    if (enemy_body[index].x + enemy_body[index].width + speed[index][0] >= 240) speed[index][0] *= -1;
    if (enemy_body[index].x + speed[index][0] <= 0) speed[index][0] *= -1;

    // 敵の移動
    enemy_body[index].x += speed[index][0];
    sprite_move(enemy_sprite + index, enemy_body[index].x - 6, enemy_body[index].y);
}

// 斜め移動(画面端及び y = 80 の時に折り返す)
static void enemy_move2(int index){
    // 画面外へ行かないように移動方向変更
    if(enemy_body[index].x + enemy_body[index].width + speed[index][0] >= 240) speed[index][0] *= -1;
    else if(enemy_body[index].x + speed[index][0] <= 0) speed[index][0] *= -1;

    if(enemy_body[index].y + enemy_body[index].height + speed[index][1] >= 80) speed[index][1] *= -1;
    else if(enemy_body[index].y + speed[index][1] <= 0) speed[index][1] *= -1;

    // 敵の移動
    enemy_body[index].x += speed[index][0];
    enemy_body[index].y += speed[index][1];
    sprite_move(enemy_sprite + index, enemy_body[index].x - 6, enemy_body[index].y);
}

// 一定間隔で突進する。それ以外は横移動
static void enemy_move3(int index){
    // 突進後一定時間前線で滞在
    if(loop_count > 124) return;
    /* 90ループ過ぎる　or 元の位置でなければ縦移動　それ以外は横移動*/
    if(loop_count > 90 || enemy_body[index].y > ENEMY_TOP){
    // フラグが立っていなければ、突進用のスプライトに変更
        if(!enemy_3_tackle_flag){
            invincible_time = 0;
            enemy_3_tackle_flag = 1;
            sprite_display(enemy_sprite + index, OBJ_TURNOFF);
            sprite_move(enemy_sprite + index + 1, enemy_body[index].x - 6, enemy_body[index].y);
            sprite_display(enemy_sprite + index + 1, OBJ_TURNON);
        }
        enemy_body[2].y += speed[2][1];
        sprite_move(enemy_sprite + 3, enemy_body[2].x - 6, enemy_body[2].y);
        if(speed[index][1] < 0) loop_count = 0; // loop_countの帳尻合わせ
    }else{
    // フラグが立っていれば、突進用のスプライトから元に戻す
        if(enemy_3_tackle_flag){
            enemy_3_tackle_flag = 0;
            sprite_display(enemy_sprite + index + 1, OBJ_TURNOFF);
            sprite_move(enemy_sprite + index, enemy_body[index].x - 6, enemy_body[index].y);
            sprite_display(enemy_sprite + index, OBJ_TURNON);
        }
        if(speed[index][1] < 0) speed[index][1] *= -1;
        enemy_move1(index);
    }
    if(loop_count == 124) speed[index][1] *= -1;
}

// 弾の発射 弾が残っていれば45ループに１回撃つ
static void fire_1way(int index){
    int i;
    if(cool_time[index] == 0 && num_bullet[index] > 0){
        for(i = 0; i < ENEMY_BULLET; i++){
            if(enemy_bullet[index][i].flag == 0){
                enemy_bullet[index][i].flag = 1;
                enemy_bullet[index][i].dy = level;
                display_bullet(&enemy_bullet[index][i], enemy_body[index].x + (enemy_body[index].width>>1), enemy_body[index].y + enemy_body[index].height + 1);
                num_bullet[index]--;
                break;
            }
        }
        cool_time[index]++;
    }else{
        cool_time[index]++;
        if(cool_time[index] == 45) cool_time[index] = 0;
    }
}

// 弾の発射(3way) 弾が残っていれば50ループに１回撃つ
static void fire_3way(int index){
    int i;
    if(cool_time[index] == 0 && num_bullet[index] > 0){
        for(i = 0; i < ENEMY_BULLET; i += 3){
            if(enemy_bullet[index][i].flag == 0){
                enemy_bullet[index][i].flag = 1;
                enemy_bullet[index][i + 1].flag = 1;
                enemy_bullet[index][i + 2].flag = 1;
    
                enemy_bullet[index][i].dx = -1;
                enemy_bullet[index][i + 2].dx = 1;

                display_bullet(&enemy_bullet[index][i], enemy_body[index].x + (enemy_body[index].width>>1), enemy_body[index].y + enemy_body[index].height + 1);
                display_bullet(&enemy_bullet[index][i + 1], enemy_body[index].x + (enemy_body[index].width>>1), enemy_body[index].y + enemy_body[index].height + 1);
                display_bullet(&enemy_bullet[index][i + 2], enemy_body[index].x + (enemy_body[index].width>>1), enemy_body[index].y + enemy_body[index].height + 1);
                num_bullet[index] -= 3;
                break;
            }
        }
        cool_time[index]++;
    }else{
        cool_time[index]++;
        if(cool_time[index] == 50) cool_time[index] = 0;
    }
}

// 敵の弾の移動(1way)
static void enemy_bullet_move_1way(int index){
    int i;
    for(i = 0; i < ENEMY_BULLET; i++){
        if(enemy_bullet[index][i].flag){
            move_reflection_bullet(&enemy_bullet[index][i]);
            if(enemy_bullet[index][i].flag == 0) num_bullet[index]++;
        }
    }
}

// 敵の弾の移動(3way)
static void enemy_bullet_move_3way(int index){
    int i;
    for(i = 0; i < ENEMY_BULLET; i += 3){
        if(enemy_bullet[index][i].flag){
            move_reflection_bullet(&enemy_bullet[index][i]);
            move_bullet(&enemy_bullet[index][i + 1]);
            move_reflection_bullet(&enemy_bullet[index][i + 2]);
            
            if(enemy_bullet[index][i].flag == 0) num_bullet[index] += 3;
	    }
    }
}

// 追尾弾の移動　横方向のみプレイヤーに追尾する(一度だけ縦方向の反射を行う)
static void enemy_bullet_move_tracking(int index){
    int diff_x, new_dx, i;
    struct box *player = player_get_body();
    for(i = 0; i < ENEMY_BULLET; i++){
        if(enemy_bullet[index][i].flag){
	    // 速度の更新
            diff_x = player->x - enemy_bullet[index][i].body.x;
            if(diff_x < 0) new_dx = -1;
            else new_dx = 1;
            enemy_bullet[index][i].dx = new_dx;
	    // 画面端（縦）の反射
            if(enemy_bullet[index][i].dy > 0 && enemy_bullet[index][i].body.y > 140) enemy_bullet[index][i].dy *= -1;
            
	        move_bullet(&enemy_bullet[index][i]);
            if(enemy_bullet[index][i].flag == 0) num_bullet[index]++;
	    }
    }
}

/* 敵とプレイヤーの弾との当たり判定*/
static void hit_enemy(int index){
    int i;
    for(i = 0; i < MAX_BULLET; i++){
        if (player_bullets[i].flag){
            if (cross(&enemy_body[index], &player_bullets[i].body)){
                player_reload(i);
		        // 敵が無敵時間であれば、弾のみ消して次へ
                if(invincible_time > 0 || enemy_3_tackle_flag) continue;

                enemy_life--;
                if(enemy_life <= 0){
                    sprite_display(enemy_sprite + index, OBJ_TURNOFF);
                    num_enemy--;
                    all_reload(index);
                    level++;
                    appear_time++;
                    enemy_life = 3;
                }else{
                    invincible_time++;
                }
            }
        }    
    }
}

// 敵とプレイヤーの当たり判定
static void cross_player_enemy(int index){
    if(cross_player(&enemy_body[index])) damage_player();
}

// 敵の弾とプレイヤーの当たり判定
static void hit_player(int index){
    int i;
    for(i = 0; i < ENEMY_BULLET; i++){
        if(enemy_bullet[index][i].flag){
            if(cross_player(&enemy_bullet[index][i].body)){
                damage_player();
            }
        }
    }
}

// 初期化
static void init(int start){
    int i,j;
    invincible_time = 0;
    appear_time = 0;
    level = 0;
    loop_count = 0;
    enemy_3_tackle_flag = 0;
    enemy_life = 3;
    num_enemy = MAX_ENEMY;
    for (i = 0; i < MAX_ENEMY; i++){
        enemy_body[i].x = 108;
        enemy_body[i].y = -15;
        enemy_body[i].width = ENEMY_WIDTH;
        enemy_body[i].height = ENEMY_HEIGHT;

        // 速さの初期化
        speed[i][0] = 1 + i;
        speed[i][1] = 1 + i;
        // 攻撃するかどうかのフラグ
        cool_time[i] = 0;
        // 弾の初期化　start画面時のみbulletにスプライトの登録を行う
        if(start){
            struct box eb = { .x = enemy_body[i].x, .y = enemy_body[i].y, .width = 8, .height = 8};
            for(j = 0; j < ENEMY_BULLET; j++){
                enemy_bullet[i][j].dx = 0;
                enemy_bullet[i][j].dy = 1;
                enemy_bullet[i][j].sprite = eb_sprite + j;
                enemy_bullet[i][j].flag = 0;
                enemy_bullet[i][j].body = eb;
            }
            num_bullet[i] = ENEMY_BULLET;
        }else{
            all_reload(i);    
        }

        sprite_move(enemy_sprite + i, enemy_body[i].x - 6, enemy_body[i].y);
    }
    sprite_display(enemy_sprite + MAX_ENEMY, OBJ_TURNOFF);
    // 最初の敵表示
    enemy_body[0].y = ENEMY_TOP;
    sprite_move(enemy_sprite, enemy_body[0].x, enemy_body[0].y);
    sprite_display(enemy_sprite, OBJ_TURNON);
}

void enemy_step(int sprite_num, int b_sprite_num){
    int i;
    enemy_sprite = sprite_num;
    eb_sprite = b_sprite_num;

    switch (game_get_state()){
    case TITLE:
        for(i = 0; i < MAX_ENEMY; i++){
            sprite_display(enemy_sprite + i, OBJ_TURNOFF);
            all_reload(i);
        }
        sprite_display(enemy_sprite + MAX_ENEMY, OBJ_TURNOFF); // 突進時のスプライト
        break;
    case START:
        init(1);
        break;
    case RUNNING:
        // 出現時間　この間敵は無敵
        if(appear_time){
            sprite_display(enemy_sprite + level, OBJ_TURNON);
            sprite_move(enemy_sprite + level, enemy_body[level].x, enemy_body[level].y);
            if((appear_time & 4) && (appear_time & 2) == 0){
                enemy_body[level].y++;
            }
            appear_time++;
            loop_count = 0;
            if(appear_time >= APPEAR_TIME) appear_time = 0;
            break;
        }
        /*処理の流れ
           エネミーの移動 -> エネミーの弾の発射 -> 弾の移動 -- 
           -> プレイヤーとエネミー弾の当たり判定 -> エネミーとプレイヤーの弾の当たり判定
           -> プレイヤーとエネミーの当たり判定*/
        switch (level){
        case 0:
            enemy_move1(0);
            fire_3way(0);
            enemy_bullet_move_3way(0);
            hit_player(0);
            hit_enemy(0);
            cross_player_enemy(0);
            break;
        case 1:
            enemy_move2(1);
            fire_1way(1);
            // 約１秒に１回追跡してくる
            if(loop_count & 64){
                enemy_bullet_move_tracking(1);
                loop_count = 0;
            }
            else{
                enemy_bullet_move_1way(1);
            }
            hit_player(1);
            hit_enemy(1);
            cross_player_enemy(1);
            loop_count++;
            break;
        case 2:
            enemy_move3(2);
            fire_1way(2);
            enemy_bullet_move_1way(2);
            hit_player(2);
            hit_enemy(2);
            cross_player_enemy(2);
            loop_count++;
            if(loop_count > 130) loop_count = 0;
            break;
        default:
            break;
        }
        // クリア判定
        if (num_enemy <= 0) {
            game_set_state(CLEAR);
            break;
        }
        // 無敵時間処理　点滅させる
        if(invincible_time){
            if(invincible_time & 4){
                sprite_display(enemy_sprite + level, OBJ_TURNOFF);
            }else{
                sprite_display(enemy_sprite + level, OBJ_TURNON);
            }
            invincible_time++;
        }
        
        if(invincible_time >= INVINCIBLE) {
            sprite_display(enemy_sprite + level, OBJ_TURNON);
            invincible_time = 0;
        }
        break;
    case STOP:
        break;
    case DEAD:
        break;
    case RESTART:
        init(0);
        break;
    case CLEAR:
        break;
    default:
        break;
    }
}
