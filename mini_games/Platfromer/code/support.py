from settings import *

def load_images(*path, format = 'png', alpha = True):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha == True else pygame.image.load(full_path).convert()
    return surf

def load_folder(*path):
    folder = []
    for folder_path, sub_folder, file_names in walk(join(*path)):
        for file_name in sorted(file_names , key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            folder.append(surf)
    return folder

def load_audio(*path,format = 'wav', volume = 1):
    full_path = join(*path) + f'.{format}'
    audio = pygame.mixer.Sound(full_path)
    audio.set_volume(volume)
    return audio