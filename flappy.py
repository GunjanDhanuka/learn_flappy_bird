import os
import time
import random
import neat
import pygame

#defined the window dimensions
WIN_WIDTH = 500
WIN_HEIGHT = 800

#Imported all the images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG =  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    #Initilise the bird with these values
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    #Implement jumping of the bird by giving it a velocity
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    #Implement movement by using s = ut + 0.5at^2
    #here the time t is denoted by the tick_count
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5*self.tick_count**2

        #To prevent the bird from moving too large a distance
        #i.e. giving it a terminal velocity
        if d>=16:
            d = 16
        
        #Smoothes out the upward movement of the bird
        if d<0:
            d-=2
        
        #update the position of the bird
        self.y += d

        #Implement the logic for tilting downward when moving down and vice versa
        if d<0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            #If the bird is moving down, make it look like a nosedive
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    #Draw the bird onto the window
    def draw(self, win):
        self.img_count +=1

        #This if-else block basically checks which bird image to display
        if self.img_count < self.ANIMATION_TIME:
            #Feathers up
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            #Feathers in the middle
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            #Feathers down
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            #Feathers in the middle
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            #Feather up and reset
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        #This titls the bird by the tilt angle from the center
        #Not exactly sure how this works but alright!
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()

main()
