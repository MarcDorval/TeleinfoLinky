
# (Python3) ds18b20 to MQTT on Rapsberry Pi

**Scripts bash et Python3 permettant de monitorer la temperature via des capteurs ds18b20 en MQTT via un service démarré au boot**

## Installation des resources '1-wire'

[temperatures_setup.sh (triggers a reboot!)](temperatures_setup.sh)

## Installation d'un broker mosquitto en local sur la Pi

[mosquitto install](README_mosquitto.md)

## module python3 mymqtt

> Generic MQTT module to publish or subscribe to a MQTT broker with logging

[mymqtt.py](mymqtt.py)

## [mqtt_ds18b20_read_temp_publish.py](mqtt_ds18b20_read_temp_publish.py)

### Recherche des capteurs ds18b20

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

### Connection au broker local en tant que publisher

```python
mqttc.connect_to(broker, port, publisher=True)
mqttc.log.info(f"time/{client_id}/start/loop")
```

### Lecture de la valeur de chacun des capteurs

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

### Publication vers le broker local

```python
from mymqtt import myMqtt
from paho.mqtt import client as mqtt_client

client_id="ds18_mqtt"
broker="127.0.01"
port = 1883
mqttc = myMqtt(client_id)

. . . 
                        mqttc.publish(topic=f"ds28b20/{id}{item}", msg=line, retain=True)
. . .
```

## Test du script python

### Lancement en 'python direct'

```bash
/usr/bin/python3 /home/pi/TeleinfoLinky/mqtt_ds18b20_read_temp_publish.py
```

Les valeurs de température sont listées à la première lecture, puis à chaque changement de valeur.

### Suivi des messages postés

```bash
tail -f /home/pi/TeleinfoLinky/mqtt.log
```

## Lancement au demarrage du script

(à ne faire qu'une fois que le script fonctionne en 'python direct')

### creation d'un service `mqtt_ds18b20`

fichier mqtt_ds18b20.service:

[mqtt_ds18b20.service](mqtt_ds18b20.service)

### Installation du service `mqtt_ds18b20`

```bash
sudo cp mqtt_ds18b20.service /usr/local/lib/systemd/system/mqtt_ds18b20.service
sudo systemctl daemon-reload
sudo systemctl enable mqtt_ds18b20.service
sudo systemctl start  mqtt_ds18b20.service
sudo systemctl status mqtt_ds18b20.service
```

> Une fois lancé, les infos listées dans mqtt_ds18b20_read_temp_publish.py/linky_args sont publiées dans le broker
si elles diffèrent des précedentes.

> le service est démarré au démarrage du réseau (Ethernet) et relancé si jamais il s'arrête

### Redémarrage du service `mqtt_ds18b20` (après modifications)

```bash
sudo systemctl daemon-reload
sudo systemctl restart mqtt_ds18b20.service
```

## Suivi des logs de mosquitto

```bash
tail -f /tmp/mosquitto.log
```
