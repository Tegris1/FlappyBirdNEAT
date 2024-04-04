import pygame
class Bird(object):
    imgs = []
    maxRot = 25
    rotVel = 20
    animTime = 5

    def __init__(self, imgs, x, y):
        self.imgs = imgs
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.tickCount = 0
        self.height = self.y
        self.imgCount = 0
        self.img = self.imgs[0]

    def jump(self):
        self.vel = -10.5
        self.tickCount = 0
        self.height = self.y

    def move(self):
        self.tickCount += 1

        d = self.vel * self.tickCount + 1.5*self.tickCount**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.maxRot:
                self.tilt = self.maxRot
            else:
                if self.tilt > -90:
                    self.tilt -= self.rotVel

    def draw(self, win):
        self.imgCount += 1

        if self.imgCount < self.animTime:
            self.img = self.imgs[0]
        elif self.imgCount < self.animTime*2:
            self.img = self.imgs[1]
        elif self.imgCount < self.animTime*3:
            self.img = self.imgs[2]
        elif self.imgCount < self.animTime*4:
            self.img = self.imgs[1]
        elif self.imgCount == self.animTime*4 + 1:
            self.img = self.imgs[0]
            self.imgCount = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.imgCount = self.animTime*2

        rotatedImage = pygame.transform.rotate(self.img, self.tilt)
        newRect = rotatedImage.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotatedImage, newRect.topleft)

    def getMask(self):
        return pygame.mask.from_surface(self.img)