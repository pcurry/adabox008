import time
import audioio
import board
import neopixel

from adafruit_crickit import crickit


ADAFRUIT_BLUE = 0x0099FF
PIX_OFF = 0x000000

# NeoPixels on the Circuit Playground Express
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2)
pixels.fill(PIX_OFF)

# Set audio out on SPEAKER
SPEAKER = audioio.AudioOut(board.A0)

# Start playing the file (in the background)
def play_file(wavfile):
    audio_file = open(wavfile, "rb")
    wav = audioio.WaveFile(audio_file)
    SPEAKER.play(wav)
    while SPEAKER.playing:
        pass


def symmetric_set(pixelring, one_side, pixel_color):
    other_side = -1 * (one_side + 1)
    pixelring[one_side] = pixelring[other_side] = pixel_color


def wink(pixelring, wink_eye, wink_time, eye_color):
    pixelring[wink_eye] = PIX_OFF
    time.sleep(wink_time)
    pixelring[wink_eye] = eye_color
    time.sleep(wink_time)


def eyes_and_smile(pixelring, smile_color, eye_sep=0):
    prior_write = pixelring.auto_write 
    pixelring.auto_write = True
    pixelring.fill(PIX_OFF)
    time.sleep(1.0)
    first_eye = eye_sep # Space between eyes and centerline, for bigger rings.
    symmetric_set(pixelring, first_eye, smile_color)  # Light up the eyes 
    time.sleep(0.5)
    
    # Animate the smile, 
    smile_sep = first_eye + eye_sep + 1  # leave space between eyes and smile corners.
    for tooth in range(len(pixelring) // 2, smile_sep, -1):
        symmetric_set(pixelring, tooth, smile_color)
        time.sleep(0.2)
    time.sleep(1.0)
    pixelring.auto_write = prior_write


while True:
    print("Smile!")
    eyes_and_smile(pixels, ADAFRUIT_BLUE)
    print("Hello world!")
    play_file("hello.wav")       # play Hello World WAV file
    print("Wink!")
    wink(pixels, 0, 0.25, ADAFRUIT_BLUE)
    print("Wave!")
    crickit.servo_1.angle = 75   # Set servo angle to 75 degrees
    time.sleep(0.5)              # do nothing for a 1 second
    crickit.servo_1.angle = 135  # Set servo angle to 135 degrees
    time.sleep(0.5)              # do nothing for a 1 second