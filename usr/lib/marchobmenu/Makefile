CC=gcc
CFLAGS=-W -Wall -pedantic
LDFLAGS=-linotifytools
EXEC=mom-watch
SRC=mom-watch.c

all:
	${CC} ${SRC} -o ${EXEC} ${LDFLAGS}

.PHONY: clean 

clean:
	rm ${EXEC}

