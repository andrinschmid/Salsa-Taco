# My Physical Computing Project
Der **SALSA TACO** ist ein sprechender Tanzlehrer in Form eines Tacos.
Er ermöglicht, spielerisch Tanzschritte mittels einer Fussmatte und konkreten Anweisungen zu erlernen und mit passender Musik zu praktizieren.

## Konzept
### Spielmodi

Es gibt **zwei Modi**:
- Lernmodus
- Freestyle

#### Lernmodus

Hier lernst du Tanzen Schritt für Schritt.

**So funktioniert’s:**
1.	Drücke den blauen Knopf.
2.	Stelle dich auf die Fussmatte.
3.	Wenn du bereit bist zu tanzen, drücke den blauen Knopf erneut.
4.	Der Taco zeigt dir auf seinem Display, wohin du treten sollst.
5.	Du trittst genau auf das passende Feld des Boards.

**Regeln:**
- Machst du die richtigen Schritte eines Levels, gibt es ein Level Up.
- Machst du einen Fehler, hast du das Spiel verloren und fängst wieder
  bei Level 1 an.

*Levels:*
Es gibt 5 Levels, die immer schwieriger werden.

### Freestyle 

Im Freestyle-Modus kannst du tanzen wie du willst.

**So funktioniert’s:**
1.	Drücke den roten Knopf.
2.	Stelle dich auf die Fussmatte.
3.	Wenn du bereit bist zu tanzen, drücke den roten Knopf erneut.
4.	Du kannst frei tanzen. Der Taco bewertet deine Schritte nicht.

## Anforderungen
Um dieses Projekt nachzubauen, benötigst du:

### Hardware 
**Taco:** 
* [Ein Arduino Nano ESP32](https://store.arduino.cc/products/nano-esp32-with-headers)
* Ein Dual Button Unit 
* Ein Grove LCD Display 16x2 
* Ein OLED Display SH1106 
* Ein DFPlayer Mini MP3 Player inkl. Lautsprecher
* Ein Battery Pack 
* Ein Grove hub 

**Board:** 
* [Ein Arduino Nano ESP32](https://store.arduino.cc/products/nano-esp32-with-headers) 
* 5 Modulino Distanzsensoren
* Ein USB-C Kabel 
* Eine USB-C Powerbank

### Software
* [MicroPython](https://micropython.org/)
* [Arduino Lab for MicroPython](https://labs.arduino.cc/en/labs/micropython)
* [Arduino MicroPython Installer](https://labs.arduino.cc/en/labs/micropython-installer)


### Bibliotheken
* [MicroPython I2C 16x2 LCD driver](https://github.com/ubidefeo/micropython-i2c-lcd)
* [sh1106 OLED Library](https://github.com/robert-hh/SH1106/)
* [DFPlayer Mini Library für MicroPython](https://github.com/sebromero/micropython-dfplayer)
* [Modulino Distance] https://github.com/arduino/arduino-modulino-mpy/blob/main/docs/api.md#modulino.distance.ModulinoDistance)


## Aufbau / Installation

### Verkabelung
**Taco:**
![Verkabelung Taco](Verkabelung_Taco.png)

**Board:**
![Verkabelung Board](Verkabelung_Board.png)

### Code hochladen
* Im src-Ordner befinden sich zwei Unterordner:
* - taco → diesen Code lädst du ausschliesslich auf den Arduino im Taco
* - board → diesen Code lädst du ausschliesslich auf den Arduino im Board
* Installiere die oben aufgeführten Bibliotheken auf dem jeweiligen Arduino.

### Feedback und Fragen
Wenn du dich für dieses Projekt interessierst oder Fragen hast, kannst du gerne über Instagram, TikTok oder andere Kanäle mit uns Kontakt aufnehmen.
