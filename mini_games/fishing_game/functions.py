import pygame
from pygame.locals import *
import os
import time
import random

pygame.init()
clock = pygame.time.Clock()

sand = pygame.image.load(os.path.join("textures", "images", "_sand.png"))
rod_store = pygame.image.load(os.path.join("textures", "images", "_rod_store.png"))
dock = pygame.image.load(os.path.join("textures", "images", "_dock.png"))
bucket = pygame.image.load(os.path.join("textures", "images", "_bucket.png"))
bobber = pygame.image.load(os.path.join("textures", "images", "_bobber.png"))

sand_image = sand.get_rect(topleft=(-6, 0))
shop_image = rod_store.get_rect(center=(120, 110))
dock_image = dock.get_rect(center=(355, 365))
bucket_image = bucket.get_rect(center=(475, 410))

def refresh_window(window, balance, current_rod, circle_x, circle_y, radius):

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        window.blit(img, (x, y))
    text_font = pygame.font.Font(os.path.join("textures", "pixellari.ttf"),16)

    window.blit(sand, (sand_image))
    window.blit(rod_store, (shop_image))
    window.blit(dock, (dock_image))
    window.blit(bucket, (bucket_image))
    fisherman = pygame.image.load(os.path.join("textures", "images", "_fisherman_fishing.png"))
    line_x = 440
    line_y = 339
    pygame.draw.rect(window, (255, 255, 255), (0, 0, 24, 24))
    draw_text("?", text_font, (255, 0, 0), 8, 5)
    
