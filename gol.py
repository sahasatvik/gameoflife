#!/usr/bin/env python3

# Conway's Game of Life, implemented in python with curses
# Usage:
#   gol.py [cols] [rows]
# Here, [cols] and [rows] are the number of columns and rows
# you want to display in your terminal.
# Once running, press '?' to get a full list of commands.

import curses
import curses.textpad
from curses import wrapper
from random import choice
from os import sys

if len(sys.argv) > 1:
    cols = int(sys.argv[1])
    rows = int(sys.argv[2])
else:
    cols = 48
    rows = 16

width = cols // 2 - 10
height = rows - 2

def cell(g, i, j):
    i = (i + width) % width
    j = (j + height) % height
    return g[i, j]

def neighbours(g, i, j):
    n = []
    n.append(cell(g, i-1, j-1))
    n.append(cell(g, i-1, j))
    n.append(cell(g, i-1, j+1))
    n.append(cell(g, i, j-1))
    n.append(cell(g, i, j+1))
    n.append(cell(g, i+1, j-1))
    n.append(cell(g, i+1, j))
    n.append(cell(g, i+1, j+1))
    return sum(n)

def iterate(g):
    newgrid = dict()
    for i in range(width):
        for j in range(height):
            if cell(g, i, j):
                newgrid[i, j] = (neighbours(g, i, j) in [2, 3])
            else:
                newgrid[i, j] = (neighbours(g, i, j) == 3)
    return newgrid

def translate(g, x, y):
    newgrid = dict()
    for i in range(width):
        for j in range(height):
            newgrid[i, j] = cell(g, i + x, j + y)
    return newgrid

def display(g, stdscr):
    for i in range(width):
        for j in range(height):
            if cell(g, i, j):
                stdscr.addstr(j + 1, 2*i + 1, '██', curses.A_BOLD)
            else:
                stdscr.addstr(j + 1, 2*i + 1, '  ', curses.A_BOLD)
    drawbox(stdscr, 0, 0, 2 * width + 1, height + 1)

def drawbox(stdscr, x1, y1, x2, y2):
    for i in range(x1 + 1, x2):
        stdscr.addstr(y1, i, '─')
        stdscr.addstr(y2, i, '─')
    for j in range(y1 + 1, y2):
        stdscr.addstr(j, x1, '│')
        stdscr.addstr(j, x2, '│')
    stdscr.addstr(y1, x1, '┌')
    stdscr.addstr(y1, x2, '┐')
    stdscr.addstr(y2, x1, '└')
    stdscr.addstr(y2, x2, '┘')

def load(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    w = int(lines[0])
    h = int(lines[1])
    g = dict()
    for i in range(width):
        for j in range(height):
            if i < w and j < h:
                g[i, j] = (lines[j + 2][i] != ' ')
            else:
                g[i, j] = False
    return g

def save(g, filename):
    lines = []
    with open(filename, 'w') as f:
        f.write(str(width) + '\n')
        f.write(str(height) + '\n')
        for j in range(height):
            for i in range(width):
                if g[i, j]:
                    f.write('#')
                else:
                    f.write(' ')
            f.write('\n')

def show_help(stdscr):
    x = (2 * width - 26) // 2
    y = (height - 10) // 2
    x, y = max(x, 0), max(y, 0)
    stdscr.addstr( y + 1,      x, "  . <dot> :", curses.A_BOLD)
    stdscr.addstr( y + 1, x + 11, " iterate once   ")
    stdscr.addstr( y + 2,      x, " 1/2/../9 :", curses.A_BOLD)
    stdscr.addstr( y + 2, x + 11, " iterate n times")
    stdscr.addstr( y + 3,      x, "  w/a/s/d :", curses.A_BOLD)
    stdscr.addstr( y + 3, x + 11, " move pointer   ")
    stdscr.addstr( y + 4,      x, "  <space> :", curses.A_BOLD)
    stdscr.addstr( y + 4, x + 11, " toggle cell    ")
    stdscr.addstr( y + 5,      x, "  W/A/S/D :", curses.A_BOLD)
    stdscr.addstr( y + 5, x + 11, " move screen    ")
    stdscr.addstr( y + 6,      x, "        C :", curses.A_BOLD)
    stdscr.addstr( y + 6, x + 11, " clear and reset")
    stdscr.addstr( y + 7,      x, "        R :", curses.A_BOLD)
    stdscr.addstr( y + 7, x + 11, " randomize cells")
    stdscr.addstr( y + 8,      x, "        V :", curses.A_BOLD)
    stdscr.addstr( y + 8, x + 11, " save to file   ")
    stdscr.addstr( y + 9,      x, "        L :", curses.A_BOLD)
    stdscr.addstr( y + 9, x + 11, " load from file ")
    stdscr.addstr(y + 10,      x, "        q :", curses.A_BOLD)
    stdscr.addstr(y + 10, x + 11, " quit           ")
    drawbox(stdscr, x, y, x + 27, y + 11)

def main(stdscr):
    curses.curs_set(0)
    
    grid = dict()

    for i in range(width):
        for j in range(height):
            grid[i, j] = False

    count = 0
    i, j = 0, 0
    while True:
        # stdscr.clear()
        display(grid, stdscr)
        stdscr.addstr(2, width * 2 + 3, 'Iteration:')
        stdscr.addstr(3, width * 2 + 3, str(count))
        i = (i + width) % width
        j = (j + height) % height
        if not grid[i, j]:
            stdscr.addstr(j + 1, 2*i + 1, '┤├', curses.A_DIM)
        else:
            stdscr.addstr(j + 1, 2*i + 1, '┤├', curses.A_REVERSE)
        stdscr.addstr(5, width * 2 + 3, "? for help", curses.A_DIM)
        stdscr.refresh()
        c = stdscr.getch()
        if c == ord('.'):
            grid = iterate(grid)
            count += 1
        elif chr(c) in '123456789':
            for k in range(int(chr(c))):
                grid = iterate(grid)
                count += 1
        elif c == ord('?'):
            show_help(stdscr)
            stdscr.getch()
            stdscr.clear()
        elif c == ord('w') or c == curses.KEY_UP:
            j -= 1
        elif c == ord('s') or c == curses.KEY_DOWN:
            j += 1
        elif c == ord('a') or c == curses.KEY_LEFT:
            i -= 1
        elif c == ord('d') or c == curses.KEY_RIGHT:
            i += 1
        elif c == ord(' '):
            grid[i, j] = not grid[i, j]
        elif c == ord('W'):
            grid = translate(grid, 0, 1)
        elif c == ord('S'):
            grid = translate(grid, 0, -1)
        elif c == ord('A'):
            grid = translate(grid, 1, 0)
        elif c == ord('D'):
            grid = translate(grid, -1, 0)
        elif c == ord('C'):
            stdscr.clear()
            for k in range(width):
                for l in range(height):
                    grid[k, l] = False
            count = 0
        elif c == ord('R'):
            stdscr.clear()
            for k in range(width):
                for l in range(height):
                    grid[k, l] = choice([False, True])
            count = 0
        elif c == ord('L'):
            try:
                curses.echo()
                curses.curs_set(1)
                stdscr.addstr(7, width * 2 + 3, "Filename", curses.A_BOLD)
                stdscr.addstr(8, width * 2 + 3, "(load):", curses.A_BOLD)
                text = stdscr.getstr(10, width * 2 + 3)
                curses.curs_set(0)
                curses.noecho()
                grid = load(text)
                count = 0
            except:
                stdscr.addstr(12, width * 2 + 3, "Error!", curses.A_BOLD)
                stdscr.getch()
            stdscr.clear()
        elif c == ord('V'):
            try:
                curses.echo()
                curses.curs_set(1)
                stdscr.addstr(7, width * 2 + 3, "Filename", curses.A_BOLD)
                stdscr.addstr(8, width * 2 + 3, "(save):", curses.A_BOLD)
                text = stdscr.getstr(10, width * 2 + 3)
                curses.curs_set(0)
                curses.noecho()
                save(grid, text)
            except:
                stdscr.addstr(12, width * 2 + 3, "Error!", curses.A_BOLD)
                stdscr.getch()
            stdscr.clear()
        elif c == ord('q'):
            break


wrapper(main)
