import pygame
import random
class Pipe(object):
    gap = 200
    vel = 5
    pipeImg = None

    def __init__(self, x, pipeImg):
        self.x = x
        self.height = 0
        self.pipeImg = pipeImg

        self.top = 0
        self.bottom = 0
        self.pipeTop = pygame.transform.flip(self.pipeImg, False, True)
        self.pipeBottom = self.pipeTop.copy()
        self.pipeBottom = pygame.transform.flip(self.pipeBottom, False, True)

        self.passed = False
        self.setHeight()
    def setHeight(self):
        self.height  = random.randint(50, 450)
        self.top = self.height - self.pipeTop.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.pipeTop, (self.x,self.top))
        win.blit(self.pipeBottom, (self.x,self.bottom))

    def collide(self, bird):
        birdMask = bird.getMask()
        topMask = pygame.mask.from_surface(self.pipeTop)
        bottomMask = pygame.mask.from_surface(self.pipeBottom)

        topOffset = (self.x - bird.x, self.top - round(bird.y))
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y))

        bPoint = birdMask.overlap(bottomMask, bottomOffset)
        tPoint = birdMask.overlap(topMask, topOffset)
        if bPoint or tPoint:
            return True

        return False

class Base(object):
    vel = 5
    width = 0
    img = pygame.image

    def __init__(self, baseImg, y):
        self.width = baseImg.get_width()
        self.img = baseImg
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width <= 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))
