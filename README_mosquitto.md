# Installation d'un broker mosquitto en local sur la Pi

sudo apt-get install mosquitto

> Le broker mosquitto est directement installé et lancé

> vérif:

```bash
sudo systemctl list-unit-files --type=service | grep mosquitto
sudo systemctl status mosquitto.service
```

# Modification du service mosquitto pour sauver les logs dans /tmp/mosquitto.log

> /tmp/mosquitto.log, comme tous les fichiers de log, sera effacèe à chaque reboot de la Pi

## Fichier /etc/mosquitto/mosquitto.conf:

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

## Relance de mosquitto (après modif)

> Une fois fonctionnel, mosquitto sera lancé en tant que service à chaque démarrage de la Pi

```bash
sudo systemctl daemon-reload
sudo systemctl restart mosquitto.service
```

## Verification du service mosquitto

> vérif:

```bash
sudo systemctl list-unit-files --type=service | grep mosquitto
sudo systemctl status mosquitto.service
```

## Suivi des logs de mosquitto

tail -f /tmp/mosquitto.log

