# dragino lora testing
# Single lora testing app

CC=g++
CFLAGS=-c -Wall
LIBS=-lwiringPi

all: statistics

statistics: main.o
	$(CC) main.o  $(LIBS) -o statistics

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	rm *.o statistics	
