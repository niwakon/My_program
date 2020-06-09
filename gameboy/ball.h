extern int ball_get_dy(void);             // ボールのy方向の速度を返す．
extern int ball_get_dx(void);
extern void ball_set_dy(int new_dy);      // ボールのy方向の速度をセットする．
extern void ball_set_dx(int new_dx);
extern void ball_add_x(int add_x);
extern void ball_add_y(int add_y);
extern void ball_mul_dx(int mul_dx);
extern void ball_mul_dy(int mul_dy);
extern struct box *ball_get_box(void);    // ボールの箱の位置を返す．
extern void ball_step(int sprite_num);              // アニメーションの1ステップを行なう
