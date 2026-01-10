#starting here 
import random
class chip8:
    def __init__(self, Display, rom: bytes):
        self.memory=[0]*4096 #bytes

        self.V=[0]*16  # 16 , 8 bit registers

        self.I=0

        self.pc=0x200

        self.stack=[]

        self.delay_timer=0

        self.sound_timer=0

        self.display=Display

        self.load_rom(rom)

        self.draw_flag=False

        self.wait_for_key=False

        self.wait_reg=0

        self.keys=[0]*16

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

    def load_rom(self,rom):
        for i, val in enumerate(rom):
            self.memory[0x200 +i]=val

    
    def push_stack(self,value):
        self.stack.append(value)

    def pop_stack(self):
        return self.stack.pop()
    
    def skip_next(self):
        self.pc +=2

    def add_with_carry(self,x,y):
        total=self.V[x]+self.V[y]
        self.V[0xF]=1 if total > 0xFF else 0
        self.V[x]= total & 0xFF

    def sub_with_borrow(self,x,y):
        self.V[0xF]=1 if self.V[x]>self.V[y] else 0
        self.V[x]=(self.V[x]-self.V[y]) & 0xFF

    def shift_right(self,x):
        self.V[0xF]=1 if self.V[x] & 0x1 else 0
        self.V[x]=self.V[x] >>1

    def shift_left(self,x):
        self.V[0xF]=1 if (self.V[x] & 0x80) >>7 else 0
        self.V[x]=(self.V[x] << 1) & 0xFF 
 
    def update_timers(self):
        if self.delay_timer >0:
            self.delay_timer -=1

        if self.sound_timer >0:
            self.sound_timer -=1
            print("beeep")
       
    def wait_keypress(self,x):
        self.wait_for_key=True
        self.wait_reg=x
        pc-=2
            
    def draw_sprite(self,x,y,n):
        x_pos=self.V[x]
        y_pos=self.V[y]

        self.V[0xF]=0 # colliion flag suruma 0

        for row in range(n):
            sprite_byte=self.memory[self.I +row]
            for bit in range(8):
                pixel=(sprite_byte>> (7-bit) & 1)
                if pixel==0:
                    continue

                x_coord=(x_pos + bit) % 64
                y_coord =(y_pos + row) %32

                if self.display.pixels[y_coord][x_coord] ==1:
                    self.V[0xF]=1

                self.display.pixels[y_coord][x_coord] ^=1

        self.draw_flag=True


    def opcode_fetch(self):
        opcode=self.memory[self.pc]<<8 | self.memory[self.pc +1]
        self.pc+=2
        return opcode
    
    def decode_excute(self,opcode):
        nnn=opcode & 0x0FFF
        nn=opcode & 0x00FF
        n=opcode & 0x000F
        x=(opcode & 0x0F00) >>8
        y=(opcode & 0x00F0) >>4

            
        match opcode & 0xF000:
            case 0x0000:
                match opcode:
                    case 0x00E0: #clear the display
                        self.display.clear()
                    case 0x00EE: #return from subroutine
                        self.pc=self.pop_stack()
            
            case 0x1000: #jump to address nnn
                self.pc=nnn

            case 0x2000:#call subroutine at nnn
                self.push_stack(self.pc)
                self.pc=nnn

            case 0x3000: # skip next instruction if vx=kk
                if self.V[x]==nn:
                    self.skip_next()
            
            case 0x4000: #skip next if vx not equal kk
                if self.V[x] !=nn:
                    self.skip_next()

            case 0x5000: # skip next if vx == vy
                if self.V[x]== self.V[y]:
                    self.skip_next()

            case 0x6000: #set vx=kk
                self.V[x]=nn

            case 0x7000: #add kk to vx
                self.V[x]=(self.V[x]+nn) & 0xFF

            case 0x8000:
                match n:
                    case 0x0: #set vx=vy
                        self.V[x]=self.V[y]
                    case 0x1: #set 
                        self.V[x]=self.V[x] | self.V[y]
                    case 0x2: #and
                        self.V[x]=self.V[x] & self.V[y]
                    case 0x3: #xor
                        self.V[x]=self.V[x] ^ self.V[y]
                    case 0x4: 
                        self.add_with_carry(x,y)
                    case 0x5:
                        self.sub_with_borrow(x,y)
                    case 0x6:
                        self.shift_right(x)
                    case 0x7:
                        self.V[0xF]=1 if self.V[y] > self.V[x] else 0
                        self.V[x]=(self.V[x]-self.V[y]) & 0xFF
                    case 0xE:
                        self.shift_left(x)
            case 0x9000: 
                if self.V[x]!=self.V[y]:
                    self.skip_next()
            
            case 0xA000:
                self.I=nnn

            case 0xB000:
                self.pc=nnn+self.V[0]

            case 0xC000:
                random_byte=random.randint(0,255)
                self.V[x]= random_byte & nn

            case 0xD000:
                self.draw_sprite(x,y,n)
            case 0xE000:
                match nn:
                    case 0x9E:
                        if self.keys[self.V[x]] == 1:
                            self.skip_next()
                    case 0xA1:
                        if self.keys[self.V[x]] == 0:
                            self.skip_next()
                
            case 0xF000:
                match nn:
                    case 0x07:
                        self.V[x]=self.delay_timer

                    case 0x0A:
                        self.wait_keypress(x)

                    case 0x15:
                        self.delay_timer=self.V[x]

                    case 0x18:
                        self.sound_timer=self.V[x]

                    case 0x1E:
                        self.I=(self.I + self.V[x]) & 0x0FFF

                    case 0x29:
                        digit = self.V[x]
                        self.I= 0x50 +(self.V[x]*5) # multiplyign by 5 skips the other font and get the font needed

                    case 0x33:
                        val=self.V[x]
                        self.memory[self.I]=val //100
                        self.memory[self.I+1]=(val // 10)%10
                        self.memory[self.I+2]=val %10

                    case 0x55:
                        self.V[x]=self.V[0]
                        for i in range(x+1):
                            self.memory[self.I + i]=self.V[i]

                    case 0x65:
                        for i in range(x+1):
                            self.V[i]=self.memory[self.I + i]

            case _:
                raise Exception(f"unknown opcode: {hex(opcode)}")
        

    def cpu_cycle(self):  #main cpu cycle
        if self.wait_for_key:
            for i in range(16):
                if self.keys[i]: # if 7 is pressed 
                    self.V[self.wait_reg]=i
                    self.wait_for_key=False
                    self.pc+=2
                    break
            return
        
        opcode=self.opcode_fetch()
        self.decode_excute(opcode)

    def update_timers(self):
        if self.delay_timer >0:
            self.delay_timer -=1

        if self.sound_timer >0:
            self.sound_timer -=1
            print("beeep")