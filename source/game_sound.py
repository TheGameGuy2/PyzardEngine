import pygame
pygame.mixer.init()
music={}
def load(file,name):
    nsound=pygame.mixer.Sound(file)
    music[name]=nsound
def play(name):
    music[name].play()



