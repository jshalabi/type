#!/usr/bin/env python
import sys
import curses
import random
import time
import signal

def CursesSetup():
    stdscr = curses.initscr()
    curses.noecho()
    return stdscr

def CursesTeardown():
    curses.echo()
    curses.endwin()

# Setup end of program handler
def SIGINT_Handler(signum, handler):
    CursesTeardown()
    sys.exit(0)
signal.signal(signal.SIGINT, SIGINT_Handler)

def get_next_char():
    valid_ascii = [\
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',\
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',\
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',\
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',\
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',\
        '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+',\
        ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',\
        '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',]

    index = random.randint(0, len(valid_ascii) - 1)
    return ord(valid_ascii[index])

num_chars = 0
num_chars_right = 0
def percent_correct():
    percent = 0
    if (num_chars != 0):
        percent = (float(num_chars_right) / num_chars) * 100
        percent = round(percent, 1)
    return str(percent) + "%"

start_time = time.time()
def cpm():
    time_elapsed = time.time() - start_time
    cpm = 0
    if time_elapsed != 0:
        cpm = float(60 * num_chars_right) / time_elapsed
        cpm = round(cpm, 1)
    return str(cpm)

def main():
    global num_chars, num_chars_right, start_time
    stdscr = CursesSetup()
    result = "+"
    # Initalize character queue
    queue_size = 10
    queue = [get_next_char() for i in range(0, queue_size)]
    while(True):
        stdscr.clear()
        chars = ''.join([str(chr(ch) + ' ') for ch in queue])
        display = ''.join([result, "> ", chars])
        stdscr.addstr(0, 0, display)
        display = ''.join(["cpm: ", cpm(), " | ",
                   "accuracy: ", percent_correct(), " | ",
                   "ascii: ", str(queue[0])])
        stdscr.addstr(1, 0, display, curses.COLOR_GREEN)
        stdscr.refresh()
        actual = stdscr.getch()
        if queue[0] == actual:
            result = "+"
            num_chars_right += 1
            queue.append(get_next_char())
            queue.pop(0)
        else:
            result = "-"
        num_chars += 1
try:
    main()
finally:
    CursesTeardown()
    print("cpm: " + cpm() + " @ " + percent_correct())
