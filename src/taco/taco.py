# -------------------
# Imports
# -------------------
from time import sleep, sleep_ms, ticks_ms, ticks_diff
import time
from machine import UART, Pin, I2C, SoftI2C
from lcd_i2c import LCD
from dfplayer import DFPlayer
import random
import sh1106
import math
from espnow_manager import ESPNowManager
from StepManager import StepManager


# -------------------
# Configuration
# -------------------

# Dual Buttons
button_blue = Pin("A0", Pin.IN)
button_red = Pin("A1", Pin.IN)
mode = "home"
prev_blue = 1
prev_red = 1

# MP3 Player
uart = UART(0, tx=Pin("TX"), rx=Pin("RX"))
player = DFPlayer(uart)
music_playing = False
player.pause()    
volume = 70

# LCD Display
I2C_ADDR = 0x27 # Default address
NUM_ROWS = 2
NUM_COLS = 16
i2c = I2C(0)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)
lcd.begin()

# OLED Display
display = sh1106.SH1106_I2C(128, 64, I2C(0), rotate=180)

# ESPNowManager
esp_manager = ESPNowManager()
my_mac = esp_manager.start()
print(f"My MAC address: {my_mac}")
peer = "ec da 3b 54 d4 1c" #MAC-Adresse vom Arduino Board

# StepManager
step_manager = StepManager()

# -------------------
# Functions
# -------------------

# functions - happy smiley
happy_start = time.ticks_ms() # OLED Display Animation neu starten

def kreis_happy_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                oled.pixel(x0 + x, y0 + y, color)
              
def draw_happy_smiley(eyes_open=True, offset_y=0):
    display.fill(0)

    cx = 64
    cy = 32 + offset_y
    r_face = 20

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad))
        display.pixel(x, y, 1)

    eye_dx = 7
    eye_dy = 5
    eye_r = 2

    if eyes_open:
        kreis_happy_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
        kreis_happy_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)
    else:
        y_eye = cy - eye_dy
        for x in range(cx - eye_dx - eye_r, cx - eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)
        for x in range(cx + eye_dx - eye_r, cx + eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)

    r_mouth = 10
    y_mouth = cy + 5
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth + int(y / 2)
        display.pixel(px, py, 1)

    display.show()

def update_happy_smiley():
    global happy_start

    t = (time.ticks_ms() - happy_start) / 1000
  
    offset_y = int(2 * math.sin(t * 2))
    blink_period = 1.5
    blink_len = 0.15
    phase = t % blink_period
    eyes_open = not (phase < blink_len)

    draw_happy_smiley(eyes_open=eyes_open, offset_y=offset_y)


# functions - bouncing smiley
bouncing_start = time.ticks_ms() # OLED Display Animation neu starten

def kreis_bouncing_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                oled.pixel(x0 + x, y0 + y, color)

def draw_bouncing_smiley(cx, cy, eyes_open=True, squash=1.0):
    display.fill(0)

    r_face = 16

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad) * squash)
        display.pixel(x, y, 1)

    eye_dx = 6
    eye_dy = int(4 * squash)
    eye_r = 2

    if eyes_open:
        kreis_bouncing_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
        kreis_bouncing_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)
    else:
        y_eye = cy - eye_dy
        for x in range(cx - eye_dx - eye_r, cx - eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)
        for x in range(cx + eye_dx - eye_r, cx + eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)

    r_mouth = 10
    y_mouth = cy + int(4 * squash)
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth + int(y / 2)
        display.pixel(px, py, 1)

    display.show()

def update_bouncing_smiley():
    global bouncing_start
 
    t = (time.ticks_ms() - bouncing_start) / 1000

    cx = 64 + int(25 * math.sin(t * 3))
    cy = 32 + int(15 * math.sin(t * 4 + 1))
    squash = 0.7 + 0.4 * math.sin(t * 6)
    eyes_open = (int(t * 5) % 7) != 0

    draw_bouncing_smiley(cx, cy, eyes_open, squash)


# functions - byebye smiley
byebye_start = time.ticks_ms() # OLED Display Animation neu starten

def kreis_byebye_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                display.pixel(x0 + x, y0 + y, color)

def draw_byebye_smiley(eyes_open=True, offset_y=0, arm_phase=0.0):
    display.fill(0)

    cx = 64
    cy = 25 + offset_y
    r_face = 20

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad))
        display.pixel(x, y, 1)

    shoulder_x = cx + r_face
    shoulder_y = cy -2

    angle_deg = -40 + 45 * arm_phase
    angle_rad = math.radians(angle_deg)

    arm_length = 18
    hand_x = int(shoulder_x + arm_length * math.cos(angle_rad))
    hand_y = int(shoulder_y + arm_length * math.sin(angle_rad))

    steps = arm_length
    for i in range(steps):
        t = i / steps
        ax = int(shoulder_x + t * (hand_x - shoulder_x))
        ay = int(shoulder_y + t * (hand_y - shoulder_y))
        display.pixel(ax, ay, 1)

    kreis_byebye_smiley(display, hand_x, hand_y, 2, 1)

    eye_dx = 7
    eye_dy = 5
    eye_r = 2

    if eyes_open:
        kreis_byebye_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
        kreis_byebye_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)
    else:
        y_eye = cy - eye_dy
        for x in range(cx - eye_dx - eye_r, cx - eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)
        for x in range(cx + eye_dx - eye_r, cx + eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)

    r_mouth = 10
    y_mouth = cy + 5
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth + int(y / 2)
        display.pixel(px, py, 1)

    display.text("Hasta la vista!", 10, 57, 1)
    display.show()

def update_byebye_smiley():
    global byebye_start
    
    t = (time.ticks_ms() - byebye_start) / 1000

    offset_y = int(2 * math.sin(t * 2))
    blink_period = 2.0
    blink_len = 0.15
    phase = t % blink_period
    eyes_open = not (phase < blink_len)
    arm_phase = (math.sin(t * 8) + 1) / 2

    draw_byebye_smiley(eyes_open, offset_y, arm_phase)


# functions - kopfschuettel smiley
kopfschuettel_start = time.ticks_ms() # OLED Display Animation neu starten

def kreis_kopfschuettel_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                oled.pixel(x0 + x, y0 + y, color)

def draw_kopfschuettel_smiley(offset_x=0):
    display.fill(0)

    cx = 64 + offset_x
    cy = 32
    r_face = 20

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad))
        display.pixel(x, y, 1)

    eye_dx = 7
    eye_dy = 3
    eye_r = 2

    kreis_kopfschuettel_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
    kreis_kopfschuettel_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)

    r_mouth = 10
    y_mouth = cy + 8
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth - int(y / 2)
        display.pixel(px, py, 1)

    display.show()

def update_kopfschuettel_smiley():
    global kopfschuettel_start
  
    t = (time.ticks_ms() - kopfschuettel_start) / 1000
        
    offset_x = int(8 * math.sin(t * 8))
    
    draw_kopfschuettel_smiley(offset_x)
       
      
# functions - party smiley
WIDTH = 128
HEIGHT = 64
party_start = time.ticks_ms() # OLED Display Animation neu starten

def p(x, y, color=1):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        display.pixel(x, y, color)

def kreis_party_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                p(x0 + x, y0 + y, color)

def draw_party_smiley(horn_phase=0.0):
    display.fill(0)

    cx = 64
    cy = 32
    r_face = 20

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad))
        p(x, y, 1)

    brim_width = 80
    brim_thickness = 3
    brim_y = cy - r_face

    for y in range(brim_thickness):
        for x in range(-brim_width // 2, brim_width // 2 + 1):
            offset = int(1.5 * math.sin((x / brim_width) * math.pi))
            p(cx + x, brim_y - y + offset, 1)

    crown_height = 18
    crown_width = 20

    for y in range(crown_height):
        half_width = crown_width // 2 - y // 2
        for x in range(-half_width, half_width + 1):
            p(cx + x, brim_y - brim_thickness - y, 1)

    eye_dx = 7
    eye_dy = 5
    eye_r = 2
    kreis_party_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
    kreis_party_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)

    r_mouth = 10
    y_mouth = cy + 5
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth + int(y / 2)
        p(px, py, 1)

    mouth_x = cx + 6
    mouth_y = y_mouth + 5
    horn_length = 10 + int(20 * horn_phase)

    for i in range(horn_length):
        p(mouth_x + i, mouth_y, 1)
        if i > 4:
          p(mouth_x + i, mouth_y + 3, 3)
        if i % 4 == 0:
          p(mouth_x + i, mouth_y - 1, 1)

    confetti = [(20, 10), (100, 8), (30, 50), (110, 40), (10, 30), (120, 20)]
    for idx, (x, y) in enumerate(confetti):
        if ((int(horn_phase * 10) + idx) % 2) == 0:
            p(x, y, 1)

    display.show()

def update_party_smiley():
    global party_start
    t = (time.ticks_ms() - party_start) / 1000
  
    horn_phase = (math.sin(t * 10) + 1) / 2
  
    draw_party_smiley(horn_phase)
      
      
# functions - waiting smiley
waiting_start = time.ticks_ms() # OLED Display Animation neu starten

def kreis_waiting_smiley(oled, x0, y0, r, color=1):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x*x + y*y <= r*r:
                oled.pixel(x0 + x, y0 + y, color)

def draw_waiting_smiley(eyes_open=True):
    display.fill(0)

    cx = 48
    cy = 32
    r_face = 18

    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r_face * math.cos(rad))
        y = int(cy + r_face * math.sin(rad))
        display.pixel(x, y, 1)

    eye_dx = 6
    eye_dy = 4
    pupil_offset = 2

    eye_r = 2
    kreis_waiting_smiley(display, cx - eye_dx, cy - eye_dy, eye_r, 1)
    kreis_waiting_smiley(display, cx + eye_dx, cy - eye_dy, eye_r, 1)

    if eyes_open:
        display.fill_rect(cx - eye_dx + pupil_offset - 1, cy - eye_dy - 1, 2, 2, 0)
        display.fill_rect(cx + eye_dx + pupil_offset - 1, cy - eye_dy - 1, 2, 2, 0)
    else:
        y_eye = cy - eye_dy
        for x in range(cx - eye_dx - eye_r, cx - eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)
        for x in range(cx + eye_dx - eye_r, cx + eye_dx + eye_r + 1):
            display.pixel(x, y_eye, 1)

    r_mouth = 10
    y_mouth = cy + 5
    for x in range(-r_mouth, r_mouth + 1):
        y = math.sqrt(r_mouth*r_mouth - x*x)
        px = cx + x
        py = y_mouth + int(y / 3)
        display.pixel(px, py, 1)

    display.text("...", 90, 30, 1)

    display.show()

def update_waiting_smiley():
    global waiting_start
    
    t = (time.ticks_ms() - waiting_start) / 1000

    blink_period = 3.0
    blink_len = 0.12
    phase = t % blink_period
    eyes_open = not (phase < blink_len)

    draw_waiting_smiley(eyes_open)
      

# function - show text on LCD Display
def show_text(text_oben = "", text_unten = ""):
  
  # Text oben
  text_oben_padded = text_oben + " " * (NUM_COLS - len(text_oben))
  lcd.set_cursor(0,0)
  lcd.print(text_oben_padded)

  # Text unten
  text_unten_padded = text_unten + " " * (NUM_COLS - len(text_unten))
  lcd.set_cursor(0,1)
  lcd.print(text_unten_padded)

  
# function - start music
def start_music(volume, track_folder, track_number, track_time):
  global music_playing, music_start_time, music_duration
  player.volume = volume
  music_playing = True
  player.play_track(track_folder, track_number)
  music_start_time = ticks_ms()
  music_duration = track_time * 1000 # seconds to ms


# function - update status of music without blocking the while loop
def update_music():
  global music_playing
  if music_playing:
    if ticks_diff(ticks_ms(), music_start_time) >= music_duration:
      player.pause()
      music_playing = False


# functions - Step Anzeige für OLED Display
# Feld-Definitionen: name -> (x, y, breite, höhe)
FIELDS = {
    "top":    (55,  0, 15, 15),
    "bottom": (55, 48, 15, 15),
    "left":   (20, 20, 15, 15),
    "right":  (90, 20, 15, 15),
    "center": (48, 20, 30, 20),
}

STEP_TO_FIELD = {
    "Mitte": "center",
    "Vorne": "top",
    "Hinten": "bottom",
    "Links": "left",
    "Rechts": "right"
}

def draw_fields(active=None):
    """Zeichnet alle Felder. 
    active = Name des Feldes, das zusätzlich zu 'center' 
    ausgefüllt werden soll
    (top, bottom, left, right) oder None"""
  
    display.fill(0)  # Bildschirm löschen
    for name, (x, y, w, h) in FIELDS.items():
        if name == "center" or name == active:
            display.fill_rect(x, y, w, h, 1)
        else:
            display.rect(x, y, w, h, 1)
    display.show()

def show_and_draw(step: list):
    """Zeigt die Visualisierung auf dem Display. 
    'center' ist immer aktiv."""

    active = None
    for pos in step:
        if pos != "Mitte":
            active = STEP_TO_FIELD.get(pos, None)
            break
    draw_fields(active)


# -------------------
# while loop
# -------------------

while True:
      
    # update the current values of dual button
    curr_blue = button_blue.value()
    curr_red = button_red.value()

    # Musikstatus aktualisieren
    update_music()

    # change state of dual button only if previous value was not value
    blue_pressed = prev_blue == 1 and curr_blue == 0
    red_pressed = prev_red == 1 and curr_red == 0
  
    # mode home 
    if mode == "home":
      countdown_blue_done = False
      countdown_red_done = False 
      show_text("Blau: Lernmodus", "Rot: Freestyle")
      update_waiting_smiley()
      
      if not music_playing:
        start_music(volume, track_folder = 2, track_number = 1, track_time = 20)
      
      if blue_pressed:
        player.pause()
        music_playing = False
        mode = "blue_selected"
          
      if red_pressed:
        player.pause()
        music_playing = False
        mode = "red_selected"

    # mode blue_selected
    elif mode == "blue_selected":
      show_text("Blau: Starten", "Rot: Zurueck")
      update_waiting_smiley()
      
      if not music_playing:
        start_music(volume, track_folder = 2, track_number = 2, track_time = 20)

      if blue_pressed:
        player.pause()
        music_playing = False
        mode = "blue_start"

      if red_pressed:
        player.pause()
        music_playing = False
        mode = "home"
      
    # mode red_selected
    elif mode == "red_selected":
      show_text("Blau: Starten", "Rot: Zurueck")
      update_waiting_smiley()
      
      if not music_playing:
        start_music(volume, track_folder = 2, track_number = 3, track_time = 20)
        
      if blue_pressed:
        player.pause()
        music_playing = False
        mode = "red_start"

      if red_pressed:
        player.pause()
        music_playing = False
        mode = "home"
  
    # mode blue_start
    elif mode == "blue_start":
      if not countdown_blue_done:
        for i in range(3, 0, -1):
          show_text(str(i))
          sleep_ms(500)
        show_text("Los!")
        sleep_ms(500)

        level = 1
        max_level = 5
        game_over = False
        game_won = False
        display.fill(0)
        
        # Puffer leeren
        while True:
          host, message = esp_manager.get_message(timeout=0)
          if message is None:
            break
      
        countdown_blue_done = True

        # Level an Board senden
        esp_manager.send_message(peer, str(level))

        # Musik für Level 1
        player.pause()
        music_playing = False
        start_music(volume, track_folder = 1, track_number = level, track_time = 60)
        show_text("Lernmodus", f"Level: {level}")

        # Steps für Level 1
        steps = step_manager.getSteps(1)

        for step in steps:
          show_and_draw(step)
          time.sleep(0.8)
      
      if not game_over and not game_won:

        host, message = esp_manager.get_message()
        if message:
          value_received = message.decode() == "True"
          print(f"Value received from Board: {value_received}")
    
          if value_received:
            if level < max_level:
              level +=1
      
              # Level Up
              player.pause()
              music_playing = False
              start_music(volume, track_folder = 2, track_number = level + 3, track_time = 8)
              update_party_smiley()
              sleep_ms(8000)
              show_text("Lernmodus", f"Level: {level}")

              # Level an Board senden
              esp_manager.send_message(peer, str(level))
              
              # Musik für Levels
              player.pause()
              music_playing = False
              start_music(volume, track_folder = 1, track_number = level, track_time = 60)

              # Steps für Levels
              steps = step_manager.getSteps(level)
              for step in steps:
                show_and_draw(step)
                time.sleep(0.8)
              
            else:
              game_won = True
              
          else:
            game_over = True
            
      # Game Over 
      if game_over:
        update_kopfschuettel_smiley()
        show_text("GAME OVER", f"Score: Level {level}")
        player.pause()
        start_music(volume, track_folder = 2, track_number = 9, track_time = 14)
        sleep_ms(14000)
        mode = "home"
        countdown_blue_done = False

      # Game Won
      if game_won:
        update_byebye_smiley()
        show_text("GLUECKWUNSCH!", "LEVELS GESCHAFFT")
        player.pause()
        music_playing = False
        start_music(volume, track_folder = 2, track_number = 10, track_time = 16)
        sleep_ms(16000)
        mode = "home"
        countdown_blue_done = False
        
      if blue_pressed or red_pressed:
        player.pause()
        music_playing = False
        countdown_blue_done = False
        mode = "home"

    # mode red_start
    elif mode == "red_start":

      # Countdown startet nur einmal
      if not countdown_red_done:
        countdown_start = ticks_ms()
        countdown_red_done = True
        countdown_step = 3
        countdown_done = False
        
      # Countdown nicht-blockierend
      if not countdown_done:
        elapsed = ticks_diff(ticks_ms(), countdown_start)
        if elapsed >= (4 - countdown_step) * 500:  # jede 0.5s
          if countdown_step > 0:
                show_text(str(countdown_step))
                countdown_step -= 1
          elif countdown_step == 0:
                show_text("Los!")
                countdown_step -= 1
                countdown_done = True

                # Musik starten 
                random_track = random.randint(1, 5)
                start_music(volume, track_folder = 1, track_number = random_track, track_time = 60)
                music_start_time_auto = ticks_ms()
      else:   
        # Smiley kontinuerlich aktualisieren
        update_bouncing_smiley()

        # LCD-Text nur einmal setzen, wenn nötig
        if ticks_diff(ticks_ms(), music_start_time_auto) < 500:
            show_text("Freestyle Modus", "Rot: Home")
      
        if ticks_diff(ticks_ms(), music_start_time_auto) >= 60 * 1000:
            player.pause()
            music_playing = False
            mode = "home"
            countdown_red_done = False  # Reset für nächsten Start

      if red_pressed:
          player.pause()
          music_playing = False
          mode = "home"
        
    # print modes and state
    print("Blue:", curr_blue, "Red:", curr_red, "Mode:", mode)

    # update previous values of dual button
    prev_blue = curr_blue
    prev_red = curr_red









