def game_loader(path:str) -> bytes:
    file=open(path,"rb")
    rom_data=file.read()
    return rom_data
