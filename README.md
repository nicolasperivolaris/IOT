# IOT - Rapport
## Intro : installation des rasp et test de connexion
### Manipulations :

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

### Questions :
1. Récupérer la bibliothèque transceiver depuis le repo du constructeur du l'émetteur/récepteur LoRa (voir plus haut)
2. Compiler le projet dragino_lora_app (si nécessaire : cela correspond à l'exemple 3 du user manual) (voir plus haut)
3. Après avoir modifié le fichier main.c pour chaque RPi, tester l'émission et la réception. (voir plus haut)
4. Quelle est la fréquence centrale de modulation ? Chercher quelles fréquences sont disponibles en Europe et dans le reste du monde. 
  868.1MHz dans ce cas.\
  Pour l'Eu : \
  Pour le monde :
  
5. À quoi correspond le paramètre "SF" ? Chercher les conséquences de ce paramètre sur la transmission.\
  SF : Spreading factor : l'étalement de la transmission dans le temps. \
  Si SF augmente => sensibilité plus importante, plus de risque de collision, plus grande portée
