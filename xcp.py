# 导入必要的模块
import pygame
import random
from sys import exit
from pygame.locals import QUIT, K_w, K_s, K_a, K_d, MOUSEBUTTONDOWN, MOUSEBUTTONUP
import ctypes


# 注释由通义灵码生成

# 初始化pygame
pygame.init()

# 设置窗口尺寸
WIN_WIDTH, WIN_HEIGHT = 1000, 800
# 创建游戏窗口
window_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# 设置窗口标题
pygame.display.set_caption('Simple Shooting Game')

# 加载玩家、敌人和子弹的图像
player_image = pygame.image.load('images\\player.png')
xcp_image = pygame.image.load('images\\xcp.png')
bullet_image = pygame.image.load('images\\bullet.png')

# 初始化Windows API用于键盘输入处理
user32 = ctypes.windll.user32
imm32 = ctypes.windll.imm32
# 获取窗口句柄
hwnd = pygame.display.get_wm_info()['window']
# 关联输入法上下文，避免游戏过程中输入法切换导致的问题
imm32.ImmAssociateContext(hwnd, None)

# 定义玩家类，继承自pygame的Sprite类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # 调用父类构造器
        super().__init__()
        # 设置玩家图像
        self.image = player_image
        # 获取图像的矩形区域
        self.rect = self.image.get_rect()
        # 设置初始位置
        self.rect.center = (50, WIN_HEIGHT // 2)
        # 设置移动速度
        self.speed = 5

    def update(self, pressed_keys):
        # 根据按键状态更新玩家位置
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        # 确保玩家不会移出屏幕边界
        self.rect.clamp_ip(window_surface.get_rect())

# 定义敌人类
class Xcp(pygame.sprite.Sprite):
    def __init__(self):
        # 调用父类构造器
        super().__init__()
        # 设置敌人图像
        self.image = xcp_image
        # 获取图像的矩形区域
        self.rect = self.image.get_rect()
        # 设置初始位置在屏幕右侧随机高度
        self.rect.x = WIN_WIDTH
        self.rect.y = random.randint(0, WIN_HEIGHT - self.rect.height)
        # 设置移动速度
        self.speed = random.randint(1, 3)

    def update(self):
        # 更新敌人位置，使其向左移动
        self.rect.move_ip(-self.speed, 0)
        # 如果敌人移出屏幕左侧，则销毁
        if self.rect.right < 0:
            self.kill()

# 定义子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # 调用父类构造器
        super().__init__()
        # 设置子弹图像
        self.image = bullet_image
        # 获取图像的矩形区域
        self.rect = self.image.get_rect()
        # 设置子弹初始位置
        self.rect.centerx = x
        self.rect.centery = y
        # 设置移动速度
        self.speed = 20

    def update(self):
        # 更新子弹位置，使其向右移动
        self.rect.move_ip(self.speed, 0)
        # 如果子弹移出屏幕右侧，则销毁
        if self.rect.right > WIN_WIDTH:
            self.kill()

# 创建精灵组用于管理玩家、敌人和子弹
player_group = pygame.sprite.Group()
xcp_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# 创建玩家实例并加入到玩家组
player = Player()
player_group.add(player)

# 初始化得分和字体
score = 0
font = pygame.font.Font(None, 36)

# 创建游戏时钟对象
clock = pygame.time.Clock()

# 游戏主循环标志
running = True
# 鼠标按下状态标志
mouse_pressed = False

# 游戏主循环
while running:
    # 获取按键状态
    pressed_keys = pygame.key.get_pressed()

    # 处理事件
    for event in pygame.event.get():
        # 如果用户关闭窗口，退出游戏
        if event.type == QUIT:
            running = False
        # 如果鼠标左键被按下，设置标志
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
        # 如果鼠标左键被释放，重置标志
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False

    # 随机生成敌人
    if random.randint(0, 50) == 10:
        xcp = Xcp()
        xcp_group.add(xcp)

    # 更新所有精灵的位置
    player_group.update(pressed_keys)
    xcp_group.update()
    bullet_group.update()

    # 检测子弹与敌人的碰撞
    for bullet in bullet_group:
        hit_xcps = pygame.sprite.spritecollide(bullet, xcp_group, True)
        for xcp in hit_xcps:
            # 销毁碰撞的子弹和敌人，增加得分
            bullet.kill()
            score += 1

    # 如果鼠标左键被按下且玩家未在发射子弹，创建子弹
    if mouse_pressed:
        bullet = Bullet(player.rect.right, player.rect.centery)
        bullet_group.add(bullet)

    # 检测玩家与敌人的碰撞
    if pygame.sprite.spritecollideany(player, xcp_group):
        running = False
        # 显示游戏结束文本
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        window_surface.blit(game_over_text, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50))
        pygame.display.update()

    # 检查敌人是否到达屏幕左侧
    for xcp in xcp_group:
        if xcp.rect.left < 0:
            running = False
            # 显示游戏结束文本
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            window_surface.blit(game_over_text, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50))
            pygame.display.update()
            break

    # 绘制背景
    window_surface.fill((0, 0, 0))
    # 绘制所有精灵
    player_group.draw(window_surface)
    xcp_group.draw(window_surface)
    bullet_group.draw(window_surface)
    # 显示得分
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    window_surface.blit(score_text, (WIN_WIDTH - 120, 10))

    # 更新显示
    pygame.display.update()
    # 控制游戏帧率
    clock.tick(60)

# 游戏结束后的循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # 清除屏幕
    window_surface.fill((0, 0, 0))
    # 显示游戏结束和最终得分文本
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    window_surface.blit(game_over_text, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50))
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    window_surface.blit(score_text, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 + 10))
    pygame.display.update()
    clock.tick(100000000)

    # 如果游戏主循环已停止，等待一段时间后退出pygame
    if not running:
        pygame.time.wait(1000)
        pygame.quit()
        exit()

# 退出pygame
pygame.quit()
