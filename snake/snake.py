# -*- coding: utf-8 -*-
# @Time    : 2020,07,01
# @Author  : mk
from game_sprite import *


class Main(object):

    def __init__(self):
        self.load_init = pygame.init()  # 初始化模块
        self.root = pygame.display.set_mode(SCREEN_RECT.size)  # 设置屏幕
        self.title = pygame.display.set_caption(TITLE)  # 设置标题
        self.clock = pygame.time.Clock()  # 设置游戏时钟
        self.loop_switch = True  # 游戏开关
        self.score = 0  # 计分板
        self.screen_full = False  # 全屏与小屏切换开关

    def main_loop(self):
        # 创建精灵
        self.__create_sprite()
        while self.loop_switch:
            # 锁帧
            self.clock.tick(FPS)
            # 事件监听
            self.__event_listener()
            # 更新精灵
            self.__update_sprite()
            # 更新显示文字
            self.root.blit(self.__show_text(), (0, 0))
            # 碰撞检测
            self.__check_collision()
            # 刷新屏幕
            pygame.display.update()
        # 卸载游戏模块
        pygame.quit()

    def __show_text(self):
        """显示文字"""
        text = f"Score : {self.snake.score}"
        return pygame.font.SysFont(pygame.font.get_fonts()[0], 15).render(text, True, (0, 0, 0))  # 获取系统字体创建字体对象

    def __event_listener(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.loop_switch = False
            if e.type == pygame.KEYDOWN:
                # 方向检测
                if e.key in (pygame.K_w, pygame.K_UP):
                    self.snake.direct = "up"
                if e.key in (pygame.K_s, pygame.K_DOWN):
                    self.snake.direct = "down"
                if e.key in (pygame.K_a, pygame.K_LEFT):
                    self.snake.direct = "left"
                if e.key in (pygame.K_d, pygame.K_RIGHT):
                    self.snake.direct = "right"
                # 全屏退出快捷键设置
                if e.key == pygame.K_ESCAPE:  # 退出快捷键
                    self.loop_switch = False
                if e.key == pygame.K_SPACE:  # 最大化最小化快捷键
                    self.screen_full = not self.screen_full
                    if self.screen_full:
                        self.root = pygame.display.set_mode(SCREEN_RECT.size, flags=pygame.FULLSCREEN)
                    else:
                        self.root = pygame.display.set_mode(SCREEN_RECT.size, flags=0)

    def __check_collision(self):
        # 蛇吃食物时候
        result = pygame.sprite.spritecollide(self.snake, self.food_group, True)  # 检测蛇与食物精灵组之间碰撞，成功则销毁食物
        if result:  # 如果碰撞列表不为空
            self.food_group.add(Food(self.snake.body))  # 重新生成食物
            self.snake.grow_up()  # 蛇变长
        # 蛇吃自己时候
        result = pygame.sprite.spritecollide(self.snake, self.snake.body_group, False)
        if result:
            print('蛇吃到自己了！')
            self.loop_switch = False

    def __create_sprite(self):
        background = Background()
        self.background_group = pygame.sprite.Group(background)
        self.snake = Snake()
        self.snake_group = pygame.sprite.Group(self.snake)
        food = Food(self.snake.body)
        self.food_group = pygame.sprite.Group(food)

    def __update_sprite(self):
        self.background_group.update()
        self.background_group.draw(self.root)
        self.food_group.update()
        self.food_group.draw(self.root)
        self.snake_group.update()
        self.snake_group.draw(self.root)
        self.snake.body_group.update()
        self.snake.body_group.draw(self.root)


if __name__ == '__main__':
    s = Main()
    s.main_loop()
