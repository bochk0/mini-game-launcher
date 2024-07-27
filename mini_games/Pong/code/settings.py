import pygame
from os.path import join


screen_width = 1280
screen_height = 720
SIZE = {'paddle': (40,100), 'ball': (30,30)}
POS = {'player': (screen_width - 50, screen_height / 2), 'opponent': (50, screen_height / 2)}
SPEED = {'player': 500, 'opponent': 250, 'ball': 450}
COLORS = {
    'paddle': '#ee322c',
    'paddle shadow': '#b12521',
    'ball': '#ee622c',
    'ball shadow': '#c14f24',
    'bg': '#002633',
    'bg detail': '#004a63'
}
