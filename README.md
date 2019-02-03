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



#### cat /boot/config.txt | grep -v ^# | grep -v ^$
```
dtparam=audio=on
dtoverlay=w1-gpio
dtoverlay=pi3-disable-bt
dtoverlay=sdio
```
