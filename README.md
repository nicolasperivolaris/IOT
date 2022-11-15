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
    #### Fréquence centrale de modulation :
    868.7MHz dans notre cas.
    #### Fréquences disponibles en Europe dans le monde : 
    -EU863-870	EU868\
    -US902-928	US915\
    -CN779-787	CN779\
    -EU433	EU433\
    -AU915-928	AU915\
    -CN470-510	CN470\
    -AS923	AS923\
    -KR920-923	KR920\
    -IN865-867	IN865\
    -RU864-870	RU864\
    -CN779-787: Applies to China. The duty cycle is <1% and there is no dwell time limitation. The default maximum EIRP allowed is +12.15 dBm.\
    -AU915-928: Applies to Australia and all other countries whose band extends from 915 to 928MHz. There is no duty cycle limitation applicable and the dwell time       limitation is 400ms. The default maximum EIRP allowed is +30 dBm.\
    -AS923: Applied for multiple regions (some countries in Asia and Oceania). All end-devices operated in Japan must perform Listen Before Talk (LBT) based on ARIB     STD-T108 regulations.\
    -KR920: The regulations in South Korea allow the choice of using either a duty-cycle limitation or Listen Before Talk Adaptive Frequency Agility (LBT AFA)           transmission management.\
    -IN865: Applies to India. The default maximum EIRP allowed is +30 dBm.
    
  
5. À quoi correspond le paramètre "SF" ? Chercher les conséquences de ce paramètre sur la transmission.\
  SF : Spreading factor : l'étalement de la transmission dans le temps. Ratio entre le chip rate et le actual data rate. \
  Si SF augmente => sensibilité plus importante, plus de risque de collision, plus grande portée, le airtime augmente.
