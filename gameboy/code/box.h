struct box {
        int x, y;
        int width, height;
};
/*struct fbox {
        fix x, y;
        int width, height;
};*/
extern void draw_box(struct box *b, int x, int y, hword color);
extern void move_box(struct box *b, int x, int y, hword color);
extern int cross(struct box *b1, struct box *b2);
//extern int fcross(struct fbox *ball, struct box *b);
