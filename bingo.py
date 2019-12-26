import PySimpleGUI as gui
from datetime import date
import random

gui.theme('Lightgreen')
end_program = False

# Begin screen to enter begin number, end number and amount of numbers in the lottery.
font = ('Helvetica', 20)
layout = [[gui.Text(f'Welkom op de Bingo-trekking van {date.today().strftime("%d/%m/%Y")}!', font=font)],
          [gui.Button('Start', font=font), gui.Button('Afsluiten', font=font)]]
window = gui.Window('Bingo', layout)

begin_screen = True
global begin, end, max_numbers, graph
while begin_screen:
    event, values = window.read()
    if event in (None, 'Afsluiten'):  # if user closes window or clicks cancel
        begin_screen = False
        end_program = True
    if event == 'Start':
        begin, end, max_numbers = 1, 75, 75
        try:
            begin = int(begin)
            end = int(end)
            max_numbers = int(max_numbers)
        except:
            gui.Popup('Gelieve enkel getallen op te geven!', font=font)
        if begin >= end:
            gui.Popup('Gelieve een geldig begin en eind nummer in te geven!', font=font)
        else:
            print(f'Picking {max_numbers} random numbers between {begin} and {end}.')
            begin_screen = False
window.close()

# Game screen to play the lottery.
if not end_program:
    layout = [[gui.Graph(canvas_size=(1000, 800), graph_bottom_left=(0, 0), graph_top_right=(1000, 800), enable_events=True, key='graph')],
              [gui.Button('Volgend nummer trekken', font=font), gui.Button('Afsluiten', font=font)]]
    window = gui.Window('Bingo', layout, finalize=True)
    window.Maximize()
    graph = window['graph']

previous_numbers = []
bingo_numbers = random.sample(range(begin, end + 1), max_numbers)
n_numbers = 0
i = 0

while not end_program:
    event, values = window.read()
    if event in (None, 'Afsluiten'):
        end_program = True
        window.close()

    # Get unique random numbers
    if event == 'Volgend nummer trekken':
        n_numbers += 1
        nr = bingo_numbers[i]
        i += 1
        print(f'Next number is {nr}')

        # Draw current number in large circle
        circle = graph.draw_circle((500, 220), 200, fill_color='red', line_color='black', line_width=5)
        number = graph.DrawText(nr, (500, 220), font=("Helvetica", 200), color='white', text_location='center')

        # Draw previous numbers in small circles
        x, y = 45, 750
        n_prev_nrs = 0
        for prev_nr in previous_numbers:
            n_prev_nrs += 1
            circle = graph.draw_circle((x, y), 28, fill_color='red', line_color='black', line_width=3)
            number = graph.DrawText(prev_nr, (x, y), font=('Helvetica', 30), color='white', text_location='center')
            x += 65
            if n_prev_nrs % 15 == 0:
                x = 45
                y -= 70

        previous_numbers.append(nr)
        if len(previous_numbers) == max_numbers:
            #end_program = True
            gui.Popup('Het programma is afgelopen!', title='Einde', font=font)
            window.find_element('Volgend nummer trekken').Update(disabled=True)


# IDEAS & REMARKS
# * Geluid: TTS?