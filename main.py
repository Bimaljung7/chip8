import pygame
from emulating import chip8
from display import Display
from file_manager import game_loader

pygame.init()

load_game=game_loader("games\\ibm.ch8")
display=Display()
cpu=chip8(display,load_game)

clock=pygame.time.Clock()

running=True
while running:
    cpu.cpu_cycle()
    display.draw()
    clock.tick(60)
