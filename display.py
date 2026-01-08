import pygame 

scale=10
width=64
height=32

class Display:
    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode((width*scale,height*scale))
        pygame.display.set_caption("chip8 emulator")
        self.clear()

    def clear(self):
        self.pixels=[[0 for _ in range(64)] for _ in range(32)]

    def draw(self):
        self.window.fill((0,0,0))

        for y in range(32):
            for x in range(64):
                if self.pixels[y][x]:
                    pygame.draw.rect(self.window,(255,255,255),(x*scale,y*scale,scale,scale))

        pygame.display.flip()
