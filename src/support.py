from settings import *
#this file to support lodaing files

def import_image(*path, format = 'png', transform=False, scale=(0,0)):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha()
    if transform:
        surf = pygame.transform.scale(surf, scale)
    return surf

def import_folder(*path): #for more than one frame 
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path,file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames

def audio_importer(*path):
    audio_dict ={}
    for folder_path, _,file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path,file_name)
            audio_dict[file_name.split('.')[0]]=pygame.mixer.Sound(full_path)
    return audio_dict
    
