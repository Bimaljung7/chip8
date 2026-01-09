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
                if self.pixels[y][x]: #row and column
                    pygame.draw.rect(self.window,(255,255,255),(x*scale,y*scale,scale,scale))

        pygame.display.flip()


key_map={
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_4: 0xC,

    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_r: 0xD,

    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_f: 0xE,

    pygame.K_z: 0xA,
    pygame.K_x: 0x0,
    pygame.K_c: 0xB,
    pygame.K_v: 0xF,
}

class keypad:
    def __init__(self):
        self.keys=[0]*16

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in key_map:
                    self.keys[key_map[event.key]] = 1

            elif event.type == pygame.KEYUP:
                if event.key in key_map:
                    self.keys[key_map[event.key]]= 0

