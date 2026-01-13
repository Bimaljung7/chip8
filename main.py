import pygame
from emulating import chip8
from display import Display,keypad
from file_manager import game_loader

pygame.init()

load_game=game_loader("games\\pong.ch8")
display=Display()
keypad=keypad()
cpu=chip8(display,load_game)



clock=pygame.time.Clock()

running=True
while running:
    keypad.handle_event()
    cpu.keys= keypad.keys
    
    for _ in range(700//60):# almost 11 times le dhilo chalxa ,cpu (700hz)vanda delay and sound timer,almost 11 instrucions 
       cpu.cpu_cycle() #//floot division operator

    cpu.update_timers() #timer is updated once per frame

    if cpu.draw_flag:
      display.draw()
      cpu.draw_flag=False
      
    clock.tick(60)
