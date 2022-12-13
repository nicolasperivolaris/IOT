#include <stdio.h>
const unsigned char temperature = 't';
const unsigned char humidity = 'h';
const unsigned char light = 'l';
const unsigned char vibration = 'v';

char *toSend = {'\0','\0','\0','\0'};

/*  type : une des constentes précédentes
    data : une valeur numérique 
    retourne un string*/

char* encodeData(unsigned char type, signed short data){
    if(data > 255){
        data += 32767;
        toSend[0] = type;
        toSend[1] = data&255;
        toSend[2] = data>>8;
    }else{
        data += 127;
        toSend[0] = type;
        toSend[1] = data;
        toSend[2] = '\0';
    }
    return toSend;
}