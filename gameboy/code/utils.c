#include "gba.h"
#include "utils.h"
#include "8x8.til"

#define FONT_SIZE 8
#define SEED 123456789

static int x, y;
static int var = SEED;
static hword color = COLOR_WHITE;

void setcolor(hword col){
	color = col;
}

void locate(int posi_x, int posi_y){
	x = posi_x;
	y = posi_y;
}

void draw_char(int code){
    hword *p, *ptr;
    int i, j;
	unsigned char *font = char8x8[code];
	ptr = (hword*)VRAM + LCD_WIDTH * y + x;

    for(i = 0; i < FONT_SIZE; i++){
        p = ptr + LCD_WIDTH * i;
 	    for(j = FONT_SIZE - 1; j >= 0; j--, p++){
            if(font[i] & (1 << j)) *p = color;
        }
    }
}

void putchar(int c){
	draw_char(c);
	x += FONT_SIZE;
}

void putstr(char *c){
	int i;
	i = 0;
	while(c[i]  != '\0'){
		putchar(c[i]);
		i++;
	}
}
// 数値 -> 文字列 ただし、対応する数値は 10000以下
void putint(int num){
	int size, i, count, val, len;
	// 桁数を求める
	if(num > 999)     size = 5;
	else if(num > 99) size = 4;
	else if(num > 9)  size = 3;
	else              size = 2;

	char str[size];
	str[size - 1] = '\0';
	len = size;
	// 1桁ずつ文字に変換していく
	while(len > 1){
		count = 0;
		val = 1;
		for(i = 1; i < len - 1; i++) val *= 10;
		while(num >= val){
			num -= val;
			count++;
		}
		str[size - len] = (char)(count + '0');
		len--;
	}
	putstr(str);
}

/*int fix2int(fix f){
	return (f + 0x80) >> 8;
}

fix int2fix(int i){
	return (fix)i << 8;
}

fix mulff(fix f1, fix f2){
	return f1 * fix2int(f2);
}*/

//乱数
int xorshift32(){
	var ^= (var << 13);
	var ^= (var >> 17);
	var ^= (var << 15);
	return var;
}
