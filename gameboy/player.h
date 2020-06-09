extern void player_step(int sprite_num, int sprite_num_bullet, int life);
extern void player_reload(int index);
extern int player_sum_shot(void);
extern int cross_player(struct box *b);
extern void damage_player(void);
extern int get_player_life(void);
extern struct box *player_get_body(void);
extern struct box *player_get_head(void);
