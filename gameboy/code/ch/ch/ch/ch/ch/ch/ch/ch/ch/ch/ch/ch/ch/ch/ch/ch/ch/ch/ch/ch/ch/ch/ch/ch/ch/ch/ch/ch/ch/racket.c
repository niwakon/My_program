#include "gba.h"
#include "box.h"
#include "racket.h"

#define COLOR_WHITE     BGR(31, 31, 31)
#define COLOR_BLACK     0
#define INTERVAL 0xf4

static int key;

static struct box bord = { .x = 0, .y = 120, .width = 50, .height = 5 };

void racket_step(void)
{
	 key = gba_register(KEY_STATUS);
	
	if( !(key & KEY_LEFT) ){
		if(bord.x > 0) move_box(&bord, bord.x - 1, bord.y, COLOR_WHITE);
	}

	if( !(key & KEY_RIGHT) ){
		if(bord.x < 240 - bord.width) move_box(&bord, bord.x + 1, bord.y, COLOR_WHITE);
	}
}

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
