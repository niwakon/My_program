#include "gba.h"
#include "box.h"
#include "ball.h"

#define COLOR_WHITE     BGR(31, 31, 31)
#define COLOR_BLACK     0

static int dx, dy;            /* ボールの現在の速度 */
static struct box b = { .x = 120, .y = 0, .width = 5, .height = 5 };;          /* ボールの箱の現在の位置 */

int ball_get_dy(void) { return dy; }
void ball_set_dy(int new_dy) { dy = new_dy; }
struct box *ball_get_box(void) { return &b; }

void ball_step(void)
{
	move_box(&b, b.x + dx, b.y + dy, COLOR_WHITE);
	if(b.x == 240 || b.x == 0) dx *= -1;
	if(b.y == 160 || b.y == 0) dy *= -1;
}
