#include "gba.h"
#include "ball.h"
#include "racket.h"

#define COLOR_WHITE     BGR(31, 31, 31)
#define COLOR_BLACK     0
#define COLOR_RED       BGR(0, 0, 30)
#define COLOR_GREEN     BGR(0, 30, 0)
#define COLOR_BLUE      BGR(30, 0, 0)
#define COLOR_YELLOW    BGR(0, 30, 30)
#define COLOR_AQUA      BGR(30, 30, 0)
#define INTERVAL 0xf4

void wait(int val)
{
	int i,j;
	for(i = 0; i < val; i++){
		for(j = 0; j < val; j++){}
	}
}

void delay(hword val)
{
	val += gba_register(TMR_COUNT0);
	while( val != gba_register(TMR_COUNT0) );
	void delay(hword val)
	{
		val += gba_register(TMR_COUNT0);
		while( val != gba_register(TMR_COUNT0) );
	}
}

main()
{
	hword *fb = (hword*)VRAM;
	gba_register(LCD_CTRL) = LCD_BG2EN | LCD_MODE3;

	gba_register(TMR_COUNT0) = 0;
	gba_register(TMR_CTRL0 ) = TMR_ENABLE + TMR_1024CLOCK;

	while(1){
		ball_step();
		racket_step();
		delay(INTERVAL);
	}
}
