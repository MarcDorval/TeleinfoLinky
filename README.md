Scripts bash et Python permettant de monitorer la telealimentation du compteur Linky


# cat /boot/config.txt | grep -v ^# | grep -v ^$

```
dtparam=audio=on
dtoverlay=w1-gpio
dtoverlay=pi3-disable-bt
dtoverlay=sdio
```