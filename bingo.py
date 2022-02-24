"""
Play a Bingo game using the PySimpleGUI framework.

The program generates random numbers between 1 and 75 (without replacement) and displays them on a canvas.
Previously taken numbers are shown in small circles on the canvas.
Also, the current number is spoken out loud, either by a Google Translate Voice in a language of your choice,
either by a Dutch voice which you can use offline (set the 'offline_voice' parameter to True or False).

Written by Thomas Janssen, December 2019.
"""

import PySimpleGUI as gui
from datetime import date
import random
import os
from gtts import gTTS
from playsound import playsound


# Choose a theme
gui.theme('Lightgreen')

# Set this parameter to True for offline voice in Dutch, or to False for a Google Translate voice in any language.
offline_voice = True

# Begin screen to enter begin number, end number and amount of numbers in the lottery.
font = ('Helvetica', 20)
layout = [[gui.Text(f'Welkom op de Bingo-trekking van {date.today().strftime("%d/%m/%Y")}!', font=font)],
          [gui.Button('Start', font=font), gui.Button('Afsluiten', font=font)]]
window = gui.Window('Bingo', layout)

begin_screen = True
close_program = False
global begin, end, max_numbers, graph, WIDTH, HEIGHT
while begin_screen:
    event, values = window.read()
    if event is None:
        begin_screen = False
        close_program = True
    if event == 'Afsluiten':  # if user closes window or clicks cancel
        confirm = gui.PopupOKCancel('Weet u zeker dat u wilt afsluiten?', title='Bevestigen', font=font, keep_on_top=True)
        if confirm == 'OK':
            print('Program ended!')
            begin_screen = False
            close_program = True
    if event == 'Start':
        begin, end, max_numbers = 1, 75, 75
        print(f'Picking {max_numbers} random numbers between {begin} and {end}.')
        begin_screen = False
window.close()

# Game screen to play the lottery (set fixed window size)
if not close_program:
    WIDTH, HEIGHT = 1300, 615
    layout = [[gui.Graph(canvas_size=(WIDTH, HEIGHT), graph_bottom_left=(0, 0), graph_top_right=(WIDTH, HEIGHT), enable_events=True, key='graph')],
              [gui.Button('Volgend nummer trekken', font=font), gui.Button('Afsluiten', font=font)]]
    window = gui.Window('Bingo', layout, finalize=True)
    graph = window['graph']

    previous_numbers = []
    bingo_numbers = random.sample(range(begin, end + 1), max_numbers)
    n_numbers = 0
    i = 0

while not close_program:
    event, values = window.read()

    if event is None:
        begin_screen = False
        close_program = True
    if event == 'Afsluiten':  # if user closes window or clicks cancel
        confirm = gui.PopupOKCancel('Weet u zeker dat u wilt afsluiten?', title='Bevestigen', font=font, keep_on_top=True)
        if confirm == 'OK':
            print('Program ended!')
            close_program = True
            window.close()

    # Get unique random numbers
    if event == 'Volgend nummer trekken':
        n_numbers += 1
        nr = bingo_numbers[i]
        i += 1
        print(f'Current number is {nr}')

        # Draw current number in large circle
        circle = graph.draw_circle((WIDTH/2, 210), 190, fill_color='red', line_color='black', line_width=5)
        number = graph.DrawText(nr, (WIDTH/2, 210), font=("Helvetica", 190), color='white', text_location='center')

        # Draw previous numbers in small circles
        x, y = 45, HEIGHT-50
        n_prev_nrs = 0
        for prev_nr in previous_numbers:
            n_prev_nrs += 1
            circle = graph.draw_circle((x, y), 28, fill_color='red', line_color='black', line_width=3)
            number = graph.DrawText(prev_nr, (x, y), font=('Helvetica', 30), color='white', text_location='center')
            x += 63
            if n_prev_nrs % 20 == 0:
                x = 45
                y -= 66
            if n_prev_nrs == 67:
                x += 378
        previous_numbers.append(nr)
        window.refresh()

        # Speak the current number
        try:
            if offline_voice:
                # Play offline sound file (in Dutch) (independent of OS used)
                playsound(os.path.join('records', f'Record-{nr:03}.mp3'))

            else:
                # Play number using Google Text To Speech in language of choice
                tts = gTTS(text=str(nr), lang='nl', slow=False)
                tts.save("nr.mp3")
                playsound('nr.mp3')

        except Exception as e:
            print(e)

    if not close_program and len(previous_numbers) == max_numbers:
        # gui.Popup('Het programma is afgelopen!', title='Einde', font=font)
        window.find_element('Volgend nummer trekken').Update(disabled=True)
