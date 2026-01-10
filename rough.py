def decode_excute(self,opcode):
    nnn=opcode & 0x0FFF
    nn=opcode & 0x00FF
    n=opcode & 0x000F
    x=(opcode & 0x0F00) >>8
    y=(opcode & 0x00F0) >>4

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
        

                    
                



        