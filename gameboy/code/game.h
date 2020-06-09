#define MAX_BULLET 20
#define MAX_ENEMY 3
#define ENEMY_BULLET 18
#define ENEMY_TOP 10
#define MAX_ITEM 3
enum state {TITLE, START, RUNNING, DEAD, RESTART, CLEAR, STOP};  
extern void game_step(int sprite_num);             // 1ティックの動作を行なう．
extern enum state game_get_state(void);  // 今の状態を問い合わせる．
extern void game_set_state(enum state);  // 状態を変更する
extern int game_get_mode(void);
