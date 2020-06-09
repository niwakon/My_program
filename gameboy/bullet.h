struct bullet{
        int dx, dy, sprite, flag;
        struct box body;
};
extern void display_bullet(struct bullet *b, int x, int y);
extern void not_display_bullet(struct bullet *b);
extern void move_bullet(struct bullet *b);
extern void move_reflection_bullet(struct bullet *b);
