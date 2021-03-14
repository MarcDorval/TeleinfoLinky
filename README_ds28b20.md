# Scripts bash et Python permettant de monitorer la temperature via des capteurs ds18b20

## ds18b20 vers MQTT

3 étapes:

### 1. Installation des resources '1-wire'

[temperatures_setup.sh (triggers a reboot!)](temperatures_setup.sh)

### 2. Installation d'un broker mosquitto en local sur la Pi

sudo apt-get install mosquitto

> Le broker mosquitto est directement installé et lancé

> vérif:

```bash
sudo systemctl list-unit-files --type=service | grep mosquitto
sudo systemctl status mosquitto.service
```

### 3. Recherche des capteurs ds18b20

Dans mqtt_ds18b20_read_publish.py:

```python
import os

w1_dir = "/sys/bus/w1/devices/"
item = "temperature"
item_values={}
sensors = os.listdir(f"{w1_dir}")

nb_sensors = 0
for id in sensors:
    if "28-" in id:
        print(f"Existing ds18b20 sensor: {w1_dir}{id}")
        item_values[id]=""
        nb_sensors += 1

```

### 4. Lecture de la valeur de chacun des capteurs

Dans mqtt_ds18b20_read_temp_publish.py:

```python
    for id in sensors:
        if "28-" in id:
            ds18b20_file = open(f"/sys/bus/w1/devices/{id}/{item}", "r")
            file_content = ds18b20_file.read()
            ds18b20_file.close()
            for line in file_content.split("\n"):
                if len(line) > 0:
                    if line != item_values[id]:
                        print(f"topic=ds28b20/{id}/{item} msg={line}")
. . .
```

### 5. Publication vers le broker

Dans mqtt_ds18b20_read_temp_publish.py:

```python
from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

client_id="ds18_mqtt"
broker="PiCuisine"
port = 1883
mqttc = myMqtt(client_id)

. . . 
                        mqttc.publish(topic=f"ds28b20/{id}{item}", msg=line, retain=True)
. . .
```

### 6. Lancement au demarrage du script

#### creation d'un service `mqtt_ds18b20`

fichier mqtt_ds18b20.service:

[mqtt_ds18b20.service](mqtt_ds18b20.service)

#### Installation du service `mqtt_ds18b20`

```bash
sudo cp mqtt_ds18b20.service /usr/local/lib/systemd/system/mqtt_ds18b20.service
sudo systemctl daemon-reload
sudo systemctl enable mqtt_ds18b20.service
sudo systemctl start  mqtt_ds18b20.service
sudo systemctl status mqtt_ds18b20.service
```

Une fois lancé, les infos listées dans mqtt_ds18b20_read_temp_publish.py/linky_args sont publiées dans le broker
si elles diffèrent des précedentes.

le service est démarré au démarrage du réseau (Ethernet) et relancé si jamais il s'arrête

#### Redémarrage du service `mqtt_ds18b20` après modifications

```bash
sudo systemctl daemon-reload
sudo systemctl restart mqtt_ds18b20.service
```

#### validation facile

```bash
/usr/bin/python3 /home/pi/TeleinfoLinky/mqtt_ds18b20_read_temp_publish.py
```

Les valeurs de température sont listées à la première lecture, puis à chaque changement de valeur.

#### Suivi des messages postés

On surveille les messages dans le fichier de log `mqtt.log`

```bash
tail -f /home/pi/TeleinfoLinky/mqtt.log
```

#### Surveillance des soucis du service `mqtt_ds18b20`

Afin d'essayer de comprendre pourquoi le service est parfois arrêté, on lance un client qui surveille le message de 'will'

```bash
/usr/bin/python3 /home/pi/TeleinfoLinky/mqtt_linky_undertaker.py
```
