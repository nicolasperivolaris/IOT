#include <stdio.h>
#include <MKRWAN.h>
#include <string.h>

  ///////////////////////////// Constante pour lire les Pin ///////////////////////////

# define PIN_LUMI A3           // Capteur de Luminosité tept 5700
# define PIN_HUMI A4           // Capteur Humidité H25K5A
# define PIN_VIB  0             // Capteur de Vibration Adafruit 1766
# define PIN_TEMP A6           // Capteur Temperature LMT84

  ///////////////////////////// Constante pour encoder l'encodage des données ////////////////

const unsigned char temperature = 't';
const unsigned char humidity = 'h';
const unsigned char light = 'l';
const unsigned char vibration = 'v';

char toSend[] = {'\0','\0','\0','\0'};

  ///////////////////////////// Constante Pour l'envoie des données /////////////////////////

String appEui = "0000000000000000";  
String appKey = "EFE1FDF54B4A15B12E416C232A65B530"; 

LoRaModem modem;



void setup() {

//////////////////////////////////// Pour Envoyer ////////////////////////////////////////

  Serial.begin(115200);

  while (!Serial);
  Serial.println("Welcome to MKR WAN 1300/1310 first configuration sketch");
  Serial.println("Register to your favourite LoRa network and we are ready to go!");

  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };
  Serial.print("Your module version is: ");
  Serial.println(modem.version());
  Serial.print("Your device EUI is: ");
  Serial.println(modem.deviceEUI());
  
  /////////////////////////////////// Pour les Capteur ///////////////////////////////

  pinMode(PIN_LUMI, INPUT);     
  pinMode(PIN_HUMI, INPUT);     
  pinMode(PIN_VIB, INPUT);     
  pinMode(PIN_TEMP, INPUT);     
  
}

  ////////////////////////////////// Fonction pour l'encodage ////////////////////////////

char* encodeData(unsigned char type, signed short data){
  if(data > 255){
      data += 32767;
      toSend[0] = type;
      toSend[1] = data&255;
      toSend[2] = data>>8;
  }
  else{
    data += 127;
    toSend[0] = type;
    toSend[1] = data;
    toSend[2] = '\0';
  }
    return toSend;
}


 ////////////////////////////////// Tableau pour lire la Température en fonction des mV lu par le Capteur //////////////////////////

float temp_map[200][2] = {
    {1299, -50}, {1294, -49}, {1289, -48}, {1284, -47}, {1278, -46}, {1273, -45}, {1268, -44}, {1263, -43}, {1257, -42}, {1252, -41},
    {1247, -40}, {1242, -39}, {1236, -38}, {1231, -37}, {1226, -36}, {1221, -35}, {1215, -34}, {1210, -33}, {1205, -32}, {1200, -31},
    {1194, -30}, {1189, -29}, {1184, -28}, {1178, -27}, {1173, -26}, {1168, -25}, {1162, -24}, {1157, -23}, {1152, -22}, {1146, -21},
    {1141, -20}, {1136, -19}, {1130, -18}, {1125, -17}, {1120, -16}, {1114, -15}, {1109, -14}, {1104, -13}, {1098, -12}, {1093, -11},
    {1088, -10}, {1082, -9},  {1077, -8},  {1072, -7},  {1066, -6},  {1061, -5},  {1055, -4},  {1050, -3},  {1044, -2},  {1039, -1},
    {1034, 0},   {1028, 1},   {1023, 2},   {1017, 3},   {1012, 4},   {1007, 5},   {1001, 6},   {996, 7},    {990, 8},    {985, 9},
    {980, 10},   {974, 11},   {969, 12},   {963, 13},   {958, 14},   {952, 15},   {947, 16},   {941, 17},   {936, 18},   {931, 19},
    {925, 20},   {920, 21},   {914, 22},   {909, 23},   {903, 24},   {898, 25},   {892, 26},   {887, 27},   {882, 28},   {876, 29},
    {871, 30},   {865, 31},   {860, 32},   {854, 33},   {849, 34},   {843, 35},   {838, 36},   {832, 37},   {827, 38},   {821, 39},
    {816, 40},   {810, 41},   {804, 42},   {799, 43},   {793, 44},   {788, 45},   {782, 46},   {777, 47},   {771, 48},   {766, 49},
    {760, 50},   {754, 51},   {749, 52},   {743, 53},   {738, 54},   {732, 55},   {726, 56},   {721, 57},   {715, 58},   {710, 59},
    {704, 60},   {698, 61},   {693, 62},   {687, 63},   {681, 64},   {676, 65},   {670, 66},   {664, 67},   {659, 68},   {653, 69},
    {647, 70},   {642, 71},   {636, 72},   {630, 73},   {625, 74},   {619, 75},   {613, 76},   {608, 77},   {602, 78},   {596, 79},
    {591, 80},   {585, 81},   {579, 82},   {574, 83},   {568, 84},   {562, 85},   {557, 86},   {551, 87},   {545, 88},   {539, 89},
    {534, 90},   {528, 91},   {522, 92},   {517, 93},   {511, 94},   {505, 95},   {499, 96},   {494, 97},   {488, 98},   {482, 99},
    {476, 100},  {471, 101},  {465, 102},  {459, 103},  {453, 104},  {448, 105},  {442, 106},  {436, 107},  {430, 108},  {425, 109},
    {419, 110},  {413, 111},  {407, 112},  {401, 113},  {396, 114},  {390, 115},  {384, 116},  {378, 117},  {372, 118},  {367, 119},
    {361, 120},  {355, 121},  {349, 122},  {343, 123},  {337, 124},  {332, 125},  {326, 126},  {320, 127},  {314, 128},  {308, 129},
    {302, 130},  {296, 131},  {291, 132},  {285, 133},  {279, 134},  {273, 135},  {267, 136},  {261, 137},  {255, 138},  {249, 139},
    {243, 140},  {237, 141},  {231, 142},  {225, 143},  {219, 144},  {213, 145},  {207, 146},  {201, 147},  {195, 148},  {189, 149}};

    
  //////////////////////////////////////// Fonction pour trouver la valeur de la température dans le tableau ////////////////////////////

int get_temperature_lmt84(int voltage) {
    int map_index = 199;
    for (int i = 0; i < 200; i++) {
        if (voltage > temp_map[i][0]) {
            map_index = i;
            break;
        }
    }
    return temp_map[map_index][1];
}    


 ///////////////////////////////////// Fonction pour compter le nombre de fois que le cateur de vibration et toucher ////////////////////

int Nb_touch = 0;

void Cpt_touch(){
  Nb_touch++;
}


void loop() {

  ///////////////////////////////////////////////////////// Code POUR LMT84 ////////////////////////////////////////////////////////////

  float Data_mV_Temp =  analogRead(PIN_TEMP) * (5000/1023) + 40;  // Pour avoir un truc en millivolt car formule et tableau en mV,
                                                                  // On fait plus 40 pour avoir plus de precision
 
  get_temperature_lmt84(Data_mV_Temp);                            // Utilise le tableau de donnés
  Serial.print("Temperature en C° :");
  Serial.println(get_temperature_lmt84(Data_mV_Temp));            // Data envoyer
  Serial.println();
 
  
  ////////////////////////////////////////////////////// CODE POUR LE CAPTEUR D'HUMIDITE ///////////////////////////////////////////////////
  
  int Data_mV_HUMI = analogRead(PIN_HUMI) * (5000/1023);    // Pour avoir quelque chose en mV, On divise par 1023 car ADC sur 10bits,
                                                            // il peut être sur 8 ou 12 aussi,

  int RH = ((5000.0 - Data_mV_HUMI) * 47000) / 5000;        //resistance du sensor en Ohm  

  Serial.print("Resistance RH du capteur en Ohm: ");
  Serial.println(RH);                                       // Data Envoyer


  ////////////////////////////////////// CODE POUR LE CAPTEUR DE LUMIERE DATA ENVOYER EN POURCENTAGE/////////////////////////////

  
  int Data_mV_Lumi = analogRead(PIN_LUMI) * (5000/1024) ;
  int DataLPourcent = (Data_mV_Lumi * 100)/5000;

  Serial.print("Pourcentage de Luminosité: ");
  Serial.println(DataLPourcent);                            // Data envoyer
 

  //////////////////// CODE POUR LE CAPTEUR DE VIBRATION, ON UTILISE LES INTERRUPTION DE L'ARDUINO POUR COMPTER LE NOMBRE DE FOIS //////////////
  /////////////////////////////////////////// QUE LE CAPTEUR A ETE TOUCHER //////////////////////////////////////

 attachInterrupt(digitalPinToInterrupt(0),Cpt_touch(),CHANGE);
 Serial.println(Nb_touch);


  //////////////////////////////////////////////////// Envoie des données ////////////////////////////////////////////////////////////////////////
 
   
  int connected;

  appKey.trim();
  appEui.trim();

  connected = modem.joinOTAA(appEui, appKey);
  
  if (!connected) {
    Serial.println("Something went wrong; are you indoor? Move near a window and retry");
  }

  delay(5000);

  int err;


  /////////////paquet /////////////////

  modem.setPort(3);
  modem.beginPacket();
  modem.print(encodeData(temperature, get_temperature_lmt84(Data_mV_Temp)));    // On ecrit ce qu'on envoie
  modem.print(encodeData(light, DataLPourcent)); 
  modem.print(encodeData(vibration, Nb_touch));
  modem.print(encodeData(humidity, RH/1000)); 
   

  err = modem.endPacket(true);
  if (err > 0) {
    Serial.println("Message sent correctly!");
  } 
  else {
    Serial.println("Error sending message :");
  }
  while (modem.available()) {
    Serial.write(modem.read());  
  }
  modem.poll();

  delay(10000);
}


