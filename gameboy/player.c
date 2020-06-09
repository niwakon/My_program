#include "gba.h"
#include "utils.h"
#include "sprite.h"
#include "game.h"
#include "box.h"
#include "bullet.h"
#include "enemy.h"
#include "player.h"
#define SPEED    2
#define INVINCIBLE 90

static int key;
static int dx, dy;
static int player_sprite;
static int num_bullet;
static int sum_shot; // 今まで撃った弾の合計
static int A_wait_flag; // キー入力の重複防止
static int player_life; // ライフ
static int invincible_time; // ダメージを受けた後の無敵時間

// プレイヤーの当たり判定を２つに分ける
struct box body = { .x = 95, .y = 137, .width = 16, .height = 8 };
struct box head = { .x = 101, .y = 130, .width = 3, .height = 6 };

struct bullet player_bullets[MAX_BULLET];

struct box *player_get_body(void) { return &body; }
struct box *player_get_head(void) { return &head; };

// 初期化
static void init(int life){
	dx = SPEED;
	dy = SPEED;
	body.x = 95;
	body.y = 137;
	head.x = 101;
	head.y = 130;

	A_wait_flag = 0;
	sum_shot = 0;
	invincible_time = 0;
	player_life = life;
	num_bullet = MAX_BULLET;

	sprite_move(player_sprite, body.x, head.y);
	sprite_display(player_sprite, OBJ_TURNON);
}

// 自機との当たり判定の結果を返す
int cross_player(struct box* other){
	return cross(other, &head) || cross(other, &body);
}

// 自機が攻撃を受けた時の処理
void damage_player(){
	if(invincible_time != 0) return;
	player_life--;
	invincible_time = 1;
	if(player_life <= 0) game_set_state(DEAD);
}

int player_sum_shot(void){ return sum_shot; }

// 弾の装填
void player_reload(int index){
	not_display_bullet(&player_bullets[index]);
	player_bullets[index].flag = 0;
	num_bullet++;
}

static void player_reload_all(){
	int i;
	for(i = 0; i < MAX_BULLET; i++){
        if(player_bullets[i].flag) player_reload(i);
    }
}

// 自機の動き
static void player_move(void){
	if( !(key & KEY_B)){
		dx *= 2;
		dy *= 2;
	}

	if( !(key & KEY_LEFT) ){
		if(body.x > dx){
			body.x -= dx;
			head.x -= dx;
			sprite_move(player_sprite, body.x, head.y);
		}
	}

	if( !(key & KEY_RIGHT) ){
		if(body.x < 240 - body.width - dx){
			body.x += dx;
			head.x += dx;
			sprite_move(player_sprite, body.x, head.y);
		}
	}

	if( !(key & KEY_UP) ){
		if(head.y > dy){
			body.y -= dy;
			head.y -= dy;
			sprite_move(player_sprite, body.x, head.y);
		}
	}

	if( !(key & KEY_DOWN) ){
		if(body.y < 160 - body.height - dy){
			body.y += dy;
			head.y += dy;
			sprite_move(player_sprite, body.x, head.y);
		}
	}

	dx = dy = SPEED;
}

// プレイヤーの攻撃処理
static void player_shot(){
	if( !(key & KEY_A) ){
		// 弾数が残っていれば打つ
		if(num_bullet > 0 && !A_wait_flag){
			int i;
			A_wait_flag = 1;
			for(i = 0; i < MAX_BULLET; i++){
				// 弾をうつ(1発のみ)
				if(player_bullets[i].flag == 0){
					player_bullets[i].flag = 1;
					display_bullet(&player_bullets[i], head.x - 2, head.y + 9);
					num_bullet--;
					sum_shot++;
					break;
				}
			}
		}
	}else if(key & KEY_A){
		A_wait_flag = 0;
	}
}

static void player_bullet_move(){
	int i;
	// フラグが立っている弾を移動させる
	for(i = 0; i < MAX_BULLET; i++){
		if(player_bullets[i].flag){
			move_bullet(&player_bullets[i]);
			if(player_bullets[i].flag == 0) {
				num_bullet++;
			}
		}
	}
}

void player_step(int num_sprite, int num_sprite_bullet, int life){
    int i;
    player_sprite = num_sprite;
    switch(game_get_state()){
	case TITLE:
		sprite_display(player_sprite, OBJ_TURNOFF);
		player_reload_all();
		break;
	case START:
		init(life);
		for(i = 0; i < MAX_BULLET; i++){
			struct box shot = { 0, 0, 2,  8 };
			player_bullets[i].dx = 0;
			player_bullets[i].dy = -2;
			player_bullets[i].sprite = num_sprite_bullet + i;
			player_bullets[i].flag = 0;
			player_bullets[i].body = shot;
		}
		break;
	case RUNNING:
		key = gba_register(KEY_STATUS);
		
		player_move();
		player_shot();
		player_bullet_move();

		// 無敵時間処理
		if(invincible_time){
            if(invincible_time & 4){
                sprite_display(player_sprite, OBJ_TURNOFF);
            }else{
                sprite_display(player_sprite, OBJ_TURNON);
            }
            invincible_time++;
        }
		if(invincible_time >= INVINCIBLE) {
            sprite_display(player_sprite, OBJ_TURNON);
            invincible_time = 0;
        }
		break;
	case STOP:
		break;
	case DEAD:
		break;
	case CLEAR:
		break;
	case RESTART:
		init(life);
		player_reload_all();
		break;
	default:
		break;
	}
}



