# Scripts bash et Python permettant de monitorer la telealimentation du compteur Linky

* Le Linky est en mode 'standard' (nouveau mode à 9600 bauds au lieu de 1200), ici en triphasé donc avec IRMS1/2/3 et URMS1/2/3.
NB: Ces items ne sont pas forcément disponibles ni n'ont les mêmes noms en mode 'historique' (à 1200 bauds)

* Changer baudrate=9600 en baudrate=1200 pour fonctionner en mode 'historique'
* Expérimenter `python teleinfo.py all` pour connaitre les items disponibles

## teleinfo.py
Utilisé pour tester la récupération des données en Python sur la Pi

Si la liste des paramètres est 'all', tous les paramètres sous ajoutés dans la liste des items
Chaque item listé en paramètre voit sa valeur copiée sous /home/pi/teleinfo/<item>

## teleinfo_ram.py
Utilisé pour la récupération des données en Python sur la Pi à partir de Jeedom

Test en ligne de commande : python teleinfo_ram.py  IRMS1 IRMS2 IRMS3 URMS1 URMS2 URMS3 loop

A partir de Jeedom : Requete SCRIPT : /var/www/html/plugins/script/core/ressources/teleinfo_ram.py "IRMS1 IRMS2 IRMS3 URMS1 URMS2 URMS3"

## cat_file.php
Utilisé pour lire les fichiers créées par teleinfo_ram.py par Jeedom

A partir de Jeedom : 1 Requete SCRIPT par item : /var/www/html/plugins/script/core/ressources/cat_file.php "/var/tmp_ram/IRMS1"

## Option 2: Linky vers MQTT

3 étapes:

### 1. Installation d'un broker mosquitto en local sur la Pi

sudo apt-get install mosquitto

> Le broker mosquitto est directement installé et lancé

> vérif:

```bash
sudo systemctl list-unit-files --type=service | grep mosquitto
sudo systemctl status mosquitto.service
```

modification du service mosquitto pour sauver les logs dans /tmp/mosquitto.log

fichier /etc/mosquitto/mosquitto.conf:

```bash
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /tmp/mosquitto.log
#log_type all
include_dir /etc/mosquitto/conf.d
```

### 2. Lecture des infos de teleinformation

```bash
sudo pip3 install paho-mqtt
sudo pip3 install pyserial
```

Dans mqtt_linky_read_publish.py:

```python
import serial
baudrate=9600

ser = serial.Serial('/dev/ttyAMA0', baudrate, bytesize=7, timeout=1)
ser.isOpen()
response = ser.readline()
if response != "":
    . . .
```

### 3. Publication vers le broker

Dans mqtt_linky_read_publish.py:

```python
from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

linky_args = ["URMS1", "IRMS1", "URMS2", "IRMS2", "URMS3", "IRMS3"]
broker="PiCuisine"
mqttc = myMqtt("linky2mqtt")
. . .
mqttc.publish(mqtt_item, value)
```

### 4. Lancement au demarrage du script

#### creation d'un service `mqtt_linky`

fichier mqtt_linky.service:

[mqtt_linky.service](mqtt_linky.service)

#### Installation du service `mqtt_linky`

```bash
sudo cp mqtt_linky.service /usr/local/lib/systemd/system/mqtt_linky.service
sudo systemctl daemon-reload
sudo systemctl enable mqtt_linky.service
sudo systemctl start  mqtt_linky.service
sudo systemctl status mqtt_linky.service
```

Une fois lancé, les infos listées dans mqtt_linky_read_publish.py/linky_args sont publiées dans le broker dès réception.

le service est démarré au démarrage du réseau (Ethernet) et relancé si jamais il s'arrête

#### Redémarrage du service `mqtt_linky` après modifications

```bash
sudo systemctl daemon-reload
sudo systemctl restart mqtt_linky.service
```

#### Suivi des messages postés

On démarre un client sur tous les topics 'linky'

```bash
/usr/bin/python3 /home/pi/TeleinfoLinky/mqtt_linky_listen.py
```

#### Surveillance des soucis du service `mqtt_linky`

Afin d'essayer de comprendre pourquoi le service est parfois arrêté, on lance un client qui surveille le message de 'will'

```bash
/usr/bin/python3 /home/pi/TeleinfoLinky/mqtt_linky_undertaker.py
```
