from tkinter import *
import pygame
import time

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', "'": '.----.', '"': '.-..-.',
    ' ': '/',  # Using / to separate words
}

MORSE_CODE_REVERSED = {v: k for k, v in MORSE_CODE_DICT.items()}

root = Tk()
root.title("Morse Code Translator")
root.geometry("400x200")

# Input Label + Entry
lbl = Label(root, text="Input text:")
lbl.grid(column=0, row=0)

txt = Entry(root, width=30)
txt.grid(column=1, row=0)

# Output labels (now separate!)
encoded_lbl = Label(root, text="Encoded Morse: ")
encoded_lbl.grid(column=0, row=2, columnspan=3, pady=10)

decoded_lbl = Label(root, text="Decoded Morse: ")
decoded_lbl.grid(column=0, row=3, columnspan=3, pady=10)

# Translate both directions
def morse(event=None):
    text = txt.get().strip()

    if set(text) <= {'.', '-', '/', ' '}:
        # It's Morse code: Decode it
        decoded = ''.join(MORSE_CODE_REVERSED.get(symbol, '?') for symbol in text.split())
        decoded_lbl.config(text="Decoded Text: " + decoded)
        encoded_lbl.config(text="Encoded Morse: " + text)
    else:
        # It's normal text: Encode it
        upper_text = text.upper()
        encoded = ' '.join(MORSE_CODE_DICT.get(char, '?') for char in upper_text)
        encoded_lbl.config(text="Encoded Morse: " + encoded)
        decoded_lbl.config(text="Decoded Text: " + text)

def get_encoded_morse():
    text = txt.get().upper()
    return ' '.join(MORSE_CODE_DICT.get(char, '?') for char in text)

pygame.init()
dot_sound = pygame.mixer.Sound('dot.wav')
dash_sound = pygame.mixer.Sound('dash.wav')

def play_morse_sound(morse):
    for symbol in morse:
        if symbol == '.':
            dot_sound.play()
            time.sleep(0.2)
        elif symbol == '-':
            dash_sound.play()
            time.sleep(0.4)
        elif symbol == '/':
            time.sleep(0/6)
        else:
            time.sleep(0.2)
def morse_sound(event=None):
    text = txt.get().upper()
    encoded = ' '.join(MORSE_CODE_DICT.get(char, '?') for char in text)
    encoded_lbl.config(text="Encoded Morse: " + encoded)
    play_morse_sound(encoded)

def morse_light(morse, index=0):
    if index >= len(morse):
        light_lbl.config(bg="black")
        return

    symbol = morse[index]

    if symbol == '.':
        light_lbl.config(bg="white")
        root.after(200, lambda: light_lbl.config(bg="black"))
        root.after(400, lambda: morse_light(morse, index + 1))
    elif symbol == '-':
        light_lbl.config(bg="white")
        root.after(600, lambda: light_lbl.config(bg="black"))
        root.after(800, lambda: morse_light(morse, index + 1))
    elif symbol == '/':
        root.after(600, lambda: morse_light(morse, index + 1))
    else:
        root.after(200, lambda: morse_light(morse, index + 1))

root.bind('<Return>', morse)

btn = Button(root, text="Translate", command=morse)
btn.grid(column=2, row=0)

btn = Button(root, text="Sound", command=morse_sound)
btn.grid(column=3, row=0)

btn = Button(root, text="Light", command=lambda: morse_light(get_encoded_morse()))
btn.grid(column=4, row=0)

light_lbl = Label(root, text="Light", bg="black", width=20, height=5)
light_lbl.grid(column=0, row=4, columnspan=3, pady=10)

root.mainloop()
