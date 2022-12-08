const unsigned char temperature = 't';
const unsigned char humidity = 'h';
const unsigned char light = 'l';
const unsigned char vibration = 'v';

typedef unsigned char byte;

byte toSend[2];

/*  type : une des constentes précédentes
    data : une valeur numérique de 0 à 255
    retourne un string*/
byte* encodeData(byte type, byte data){
    toSend[0] = type;
    toSend[1] = data;
    return toSend;
}