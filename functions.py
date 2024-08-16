from random import randint
from classes import Meteor


def create_meteors(group, meteors_surf, meteors_data, W):
    index = randint(0, len(meteors_surf) - 1)
    y = randint(0, 621)  # H = 621
    speed = randint(5, 9)
    meteor = Meteor(y, speed, meteors_surf[index], meteors_data[index]['hp'], meteors_data[index]['score'], group)
    group.add(meteor)


def collide_player(player_rect, meteors, lives, gameplay, lose):
    for meteor in meteors:
        if player_rect.collidepoint(meteor.rect.center):
            lives -= 1
            meteor.kill()
            if lives == 0:
                lose = True
                gameplay = False
    return lives, gameplay, lose


def collide_bullet(bullets, meteors, game_score):
    for bullet in bullets:
        for meteor in meteors:
            if bullet.rect.colliderect(meteor.rect):
                meteor.hp -= 1
                bullet.kill()
                if meteor.hp <= 0:
                    game_score += meteor.score
                    meteor.kill()
    return game_score
