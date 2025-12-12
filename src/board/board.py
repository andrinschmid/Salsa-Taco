from machine import I2C, SoftI2C, Pin
from modulino import ModulinoDistance
from time import sleep_ms, ticks_ms
from StepManager import StepManager
from espnow_manager import ESPNowManager

# Distance sensoren
g1_scl = Pin("RX", Pin.OPEN_DRAIN, Pin.PULL_UP)
g1_sda= Pin("TX", Pin.OPEN_DRAIN, Pin.PULL_UP)

g2_scl = Pin("D8", Pin.OPEN_DRAIN, Pin.PULL_UP)
g2_sda= Pin("D9", Pin.OPEN_DRAIN, Pin.PULL_UP)

g3_scl = Pin("A1", Pin.OPEN_DRAIN, Pin.PULL_UP)
g3_sda= Pin("A0", Pin.OPEN_DRAIN, Pin.PULL_UP)

g4_scl = Pin("A2", Pin.OPEN_DRAIN, Pin.PULL_UP)
g4_sda= Pin("A3", Pin.OPEN_DRAIN, Pin.PULL_UP)

soft_i2c1 = SoftI2C(scl=g1_scl,sda=g1_sda, freq=100000) # G1
soft_i2c2 = SoftI2C(scl=g2_scl,sda=g2_sda, freq=100000) # G2
soft_i2c3 = SoftI2C(scl=g3_scl,sda=g3_sda, freq=100000) # G3
soft_i2c4 = SoftI2C(scl=g4_scl,sda=g4_sda, freq=100000) # G4
i2c0 = I2C(0, freq=100000) # QWIIC

distance_mitte = ModulinoDistance(i2c0)
distance_vorne = ModulinoDistance(soft_i2c1)
distance_rechts = ModulinoDistance(soft_i2c2)
distance_hinten = ModulinoDistance(soft_i2c3)
distance_links = ModulinoDistance(soft_i2c4)

# Mapping der Sensorobjekte zu ihren Namen
SENSORS = {
    "Mitte":  distance_mitte,
    "Vorne":  distance_vorne,
    "Rechts": distance_rechts,
    "Hinten": distance_hinten,
    "Links":  distance_links
}

# --- Schwellenwerte ---
STEP_DISTANCE_DETECTED = 2.0    # 2cm = Schritt erkannt
STEP_TIMEOUT_MS = 5_000  # 5 Sekunden pro Schritt

# StepManager initialisieren
sm = StepManager()  

# Config ESPNowManager
esp_manager = ESPNowManager()
my_mac = esp_manager.start()
print(f"My MAC address: {my_mac}")
peer = "48 ca 43 2f 01 44" #MAC-Adresse vom Arduino TACO

CURRENT_LEVEL = 1
SOLL_FOLGE = []

def waitForLevelMessage():
    global CURRENT_LEVEL
    host, message = esp_manager.get_message()
    if message:
      try:
        CURRENT_LEVEL = int(message.decode())
        print("Level received:", CURRENT_LEVEL)
        loadStepsForLevel(CURRENT_LEVEL)
        startStepDetection()
      except ValueError:
        print("Ungültige Nachricht empfangen:", message)

def loadStepsForLevel(level):
    global SOLL_FOLGE
    steps = sm.getSteps(level)
    SOLL_FOLGE = [set(step) for step in steps]
    print("SOLL_FOLGE für Level", level, "geladen:", SOLL_FOLGE)


def onLevelCompleted():
    #Wird aufgerufen, sobald das Level abgeschlossen ist.
    print("🎉 Alle Schritte für Level ", CURRENT_LEVEL, "abgeschlossen!")
    esp_manager.send_message(peer, str(True))

def startStepDetection():
  global SOLL_FOLGE
  print("Starte Schrittprüfung für Level", CURRENT_LEVEL)
  current_index = 0
  last_active = set()
  step_active = set()  # speichert Sensoren, die für den aktuellen Schritt bereits erkannt wurden
  
  step_start_time = ticks_ms()  # Timer starten
  while True:
    # Prüfen, ob 5 Sekunden pro Schritt vorbei sind
    if ticks_ms() - step_start_time > STEP_TIMEOUT_MS:
      print(f"⏱ Zeit abgelaufen für Schritt {current_index+1}! Schritt nicht geschafft.")
      # Level nicht geschafft an Taco senden
      esp_manager.send_message(peer, str(False))
      return
        
    active = set()

    # Aktive sensoren einlesen
    for name, sensor in SENSORS.items():
      dist = sensor.distance
      if dist < STEP_DISTANCE_DETECTED:
          active.add(name)

    # falls unverändert überspringen
    if active == last_active:
        sleep_ms(20)
        continue

    print("Änderung erkannt:", last_active, "→", active)
    last_active = active

    expected = SOLL_FOLGE[current_index]

    # Neue aktivierte Sensoren für aktuellen Schritt hinzufügen, aktive welche auch erwartet werden
    step_active.update(active & expected)

    # Prüfen auf unerwartete Sensoren
    unexpected = active - expected
    if unexpected:
      # eigentlich hier false an taco aber weil sensoren zu ungenau nur per zeitlimite
      print("❌ Falscher Schritt:", active, "statt", expected)

    # Schritt vollständig?
    if step_active == expected:
      print("✔ Richtiger Schritt:", step_active)
      step_active.clear()  # für nächsten Schritt zurücksetzen
      step_start_time = ticks_ms()  # Timer für nächsten Schritt zurücksetzen
      current_index += 1
      if current_index >= len(SOLL_FOLGE):
        onLevelCompleted()
        return

    sleep_ms(50)

while True:
  waitForLevelMessage()
