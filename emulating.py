#starting here 
class chip8:
    def __init__(self):
        self.memory=[0]*4096 #bytes

        self.V=[0]*16  # 16 , 8 bit registers

        self.I=0

        self.pc=0x200

        self.stack=[]

        self.delay_timer=0

        self.sound_timer=0

        self.display=[[0]*64 for _ in range(32)]

        self.fontset=[
             0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

        for i, val in enumerate(self.fontset):
            self.memory[0x50+i]=val #  the reserved fonsets are given into adrr from 80 to up

        #initailization is done here

    def load_rom(self,rom_data):
        with open("rom_data.ch8","rb") as f:
            rom_data=f.read()
        for i, val in enumerate(rom_data):
            self.memory[0x200 +i]=val


    def opcode_fetch(self):
        opcode=self.memory[self.pc]<<8 | self.memory[self.pc +1]
        return opcode
    
    def decode_excute(self,opcode):
        if opcode == 0x00E0:  #clear the screen
            self.display=[[0]*64 for _ in range(32)]
            print("clear the screen")

    def cpu_cycle(self):  #main cpu cycle
        opcode=self.opcode_fetch()
        self.decode_excute(opcode)

        if self.delay_timer > 0:
            self.delay_timer -=1
             #ya sund timer ralxu

        elif opcode == 0x00EE: #returnig from the subroutine
            self.pc=self.stack.pop()
            print("return form sunroutine")

        elif opcode & 0xF000 == 0x6000: #setting the register vx to nn
            x=(opcode & 0x0F00)>>8
            nn=opcode & 0x00FF
            self.V[x]=nn
        
        elif opcode & 0xF000 == 0x7000: #adding nn to register vx
            x=(opcode & 0x0F00)>>8
            nn=opcode & 0x00FF
            self.v[x]=(self.V[x]+nn) & 0xFF

        elif opcode & 0xF000 == 0xA000:
            address=opcode & 0x0FFF
            self.I=address
            return # doing so the 12 bit adress is stored in i register therefore we dont need to increment pc by2


        elif opcode & 0xF000 == 0x1000:
            address=opcode & 0x0FFF
            self.pc=address
            return
        else:
            print(f"unknown opcode: {hex(opcode)}")

        self.pc +=2

        
            

emu =chip8()
emu.load_rom("rom_data.ch8")

for i in range(10):
    print(hex(emu.memory[0x200 +i]))


