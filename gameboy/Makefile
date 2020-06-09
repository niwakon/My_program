AS     = as-arm
CC     = gcc-arm
LIBGCC = `gcc-arm -print-libgcc-file-name`
CFLAGS = -Wall -O -fno-builtin -fomit-frame-pointer -finhibit-size-directive \
	-fno-ident

all: shooting.bin

shooting.bin: game.o box.o crt.o main.o player.o enemy.o utils.o sprite.o whiteball.o objpal.o racket_ch.o point_ch.o bullet.o enemy1_ch.o enemy2_ch.o player_ch.o marker_ch.o laser_ch.o screen.o ball.o racket.o block.o item.o
	ld-arm -o player.out -T gcc.ls \
	  crt.o game.o box.o main.o player.o enemy.o utils.o sprite.o whiteball.o objpal.o racket_ch.o point_ch.o bullet.o enemy1_ch.o enemy2_ch.o player_ch.o marker_ch.o laser_ch.o screen.o ball.o racket.o block.o item.o ${LIBGCC} /Users/Tatsuhiro/kumikomios/lib/gcc-lib/arm-gba-elf/3.3.2/libgcc.a 
	objcopy-arm -O binary player.out shooting.bin

clean:
	rm -f *.o *.s *.out *.bin

game.o: gba.h utils.h game.h box.h
box.o: gba.h utils.h box.h
main.o: gba.h utils.h sprite.h game.h box.h item.h enemy.h player.h screen.h
enemy.o: gba.h utils.h sprite.h game.h box.h bullet.h enemy.h player.h
player.o: gba.h utils.h sprite.h game.h box.h bullet.h enemy.h player.h
utils.o: gba.h utils.h
sprite.o: gba.h sprite.h
objpal.o: gba.h
bullet.o: gba.h utils.h box.h sprite.h bullet.h
whiteball.o: gba.h
racket_ch.o: gba.h
enemy1_ch.o: gba.h
enemy2_ch.o: gba.h
player_ch.o: gba.h
marker_ch.o: gba.h
laser_ch.o: gba.h
point_ch.o: gba.h
screen.o: gba.h utils.h game.h box.h item.h enemy.h player.h screen.h
ball.o: gba.h utils.h sprite.h game.h box.h ball.h block.h racket.h
block.o: gba.h utils.h game.h box.h box.h ball.h block.h
racket.o: gba.h utils.h sprite.h game.h box.h ball.h racket.h
item.o: gba.h utils.h sprite.h game.h box.h bullet.h item.h player.h
