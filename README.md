# IOT - Rapport
## Intro : installation des rasp et test de connexion

Installation de l'OS sur le rasp  
Connexion en ssh depuis le réseau (raspberrypi et raspberrypi2)  
Tuto https://www.dragino.com/downloads/downloads/LoRa-GPS-HAT/LoRa_GPS_HAT_UserManual_v1.0.pdf  

Installation de WiringPi :  
git clone https://github.com/WiringPi/WiringPi  
cd WiringPi  
./build  
cd ..  
  
sudo raspi-config  
interface options  
activer interface spi  
  
Sur un des rasp :   
./dragino_lora_app sender  
Sur l'autre  
./dragino_lora_app rec  
