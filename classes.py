import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1205:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, y, speed, surf, hp, score, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(1240, y))
        self.speed = speed
        self.hp = hp
        self.score = score
        self.add(group)

    def update(self, *args):
        if self.rect.x > -70:
            self.rect.x -= self.speed
        else:
            self.kill()
