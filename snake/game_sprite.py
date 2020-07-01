# -*- coding: utf-8 -*-
# @Time    : 2020,07,01
# @Author  : mk

import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 300, 300)
TITLE = "Snake"
FPS = 6


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super(GameSprite, self).__init__()
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= self.speed


class Background(GameSprite):
    def __init__(self, image_path="./images/bg.png", speed=0):
        super(Background, self).__init__(image_path, speed)


class Food(GameSprite):
    def __init__(self, snake_body: list, image_path="./images/food.png", speed=0):
        super(Food, self).__init__(image_path, speed)
        self.rect.x = random.randint(0, SCREEN_RECT.width - 10)
        self.rect.y = random.randint(0, SCREEN_RECT.height - 10)
        self.__generator_food_not_in_snake_body(snake_body)

    def __generator_food_not_in_snake_body(self, snake_body: list):
        while [self.rect.x, self.rect.y] in snake_body:
            self.rect.x = random.randint(0, SCREEN_RECT.width - 10)
            self.rect.y = random.randint(0, SCREEN_RECT.height - 10)

    def __del__(self):
        print("食物对象已销毁%s", self.rect)


class Snake(GameSprite):
    def __init__(self, direct="left", image_path="./images/head.png", speed=10, score=0):
        super(Snake, self).__init__(image_path, speed)
        self.speed = self.rect.width
        self.rect.x, self.rect.y = SCREEN_RECT.width // 2, SCREEN_RECT.height // 2
        self.direct = direct
        self.score = score
        self.body_group = pygame.sprite.Group()
        self.body = [[self.rect.x + self.rect.width * 0, self.rect.y],
                     [self.rect.x + self.rect.width * 1, self.rect.y],
                     [self.rect.x + self.rect.width * 2, self.rect.y]]

    def update(self):
        self.__collision_direct()
        self.__collision_hit_wall()
        self.__link_header_with_body()

    def __collision_direct(self):
        """方向检测"""
        if self.direct == "left":
            self.rect.x -= self.speed
        if self.direct == "right":
            self.rect.x += self.speed
        if self.direct == "up":
            self.rect.y -= self.speed
        if self.direct == "down":
            self.rect.y += self.speed

    def __collision_hit_wall(self):
        """撞墙检测"""
        if self.rect.x > SCREEN_RECT.width:
            print("右边撞墙")
            self.rect.x = SCREEN_RECT.x + 1 / 10 ** 5
        if self.rect.x < SCREEN_RECT.x:
            print("左边撞墙")
            self.rect.x = SCREEN_RECT.width
        if self.rect.y > SCREEN_RECT.height:
            print("下边撞墙")
            self.rect.y = SCREEN_RECT.y + 1 / 10 ** 5
        if self.rect.y < SCREEN_RECT.y:
            print("上边撞墙")
            self.rect.y = SCREEN_RECT.height

    def __link_header_with_body(self):
        self.head = [self.rect.x, self.rect.y]
        self.body.insert(0, self.head)
        self.body.pop()
        self.body_group.empty()
        print("蛇身坐标为：", self.body)
        for pos in self.body[1:]:
            snake_body = SnakeBody()
            snake_body.rect.x, snake_body.rect.y = pos[0], pos[1]
            self.body_group.add(snake_body)
        print('蛇身精灵组中精灵数目:', self.body_group)

    def grow_up(self):
        """成长"""
        self.score += 1
        print("分数:%d" % self.score)
        self.body.insert(0, [self.rect.x, self.rect.y])


class SnakeBody(GameSprite):
    def __init__(self, image_path="./images/body.png", speed=10):
        super(SnakeBody, self).__init__(image_path, speed)
        self.speed = self.rect.width

    def update(self):
        pass
