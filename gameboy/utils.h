#define COLOR_WHITE     BGR(31, 31, 31)
#define COLOR_BLACK     0
#define COLOR_RED       BGR(31, 0, 0)
#define COLOR_YELLOW    BGR(31, 31, 0)
#define COLOR_AQUA      BGR(0, 31, 31)
//typedef int fix;
void locate(int x, int y);
void putchar(int c);
void setcolor(hword color);
void putstr(char *c);
void putint(int num);
/*int fix2int(fix f);
fix int2fix(int i);
fix mulff(fix f1, fix f2);*/
int xorshift32(void);
