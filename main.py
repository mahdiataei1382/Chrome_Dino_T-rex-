import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/ARIAL.TTF", size=24)

# Classes

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        self.jumping_status = pygame.image.load("assets/Dino/DinoJump.png")
        self.dead_sprite = pygame.image.load("assets/Dino/DinoDead.png")
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino/DinoRun1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino/DinoRun2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/Dino/DinoDuck1.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/Dino/DinoDuck2.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 3
        self.ducking = False
        self.jumping = False
        self.dead = False

    def jump(self):
        if not self.jumping and not self.dead:
            self.jumping = True
            if self.rect.centery >= 360:
                while self.rect.centery - self.velocity > 40:
                    self.rect.centery -= 1

    def duck(self):
        if not self.dead:
            self.ducking = True
            self.rect.centery = 380

    def unduck(self):
        if not self.dead:
            self.ducking = False
            self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360 and not self.dead:
            self.rect.centery += self.gravity
        else:
            self.jumping = False

    def update(self):
        if not self.dead:
            self.animate()
            self.apply_gravity()

    def animate(self):
        if self.dead:
            self.image = self.dead_sprite
        elif self.jumping:
            self.image = self.jumping_status
        elif self.ducking:
            self.current_image += 0.05
            if self.current_image >= len(self.ducking_sprites):
                self.current_image = 0
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.current_image += 0.05
            if self.current_image >= len(self.running_sprites):
                self.current_image = 0
            self.image = self.running_sprites[int(self.current_image)]


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Other/Cloud.png")
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect(center=(1280, random.randint(50, 200)))
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/Cactus/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Bird1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = 350
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


class Bird2(Bird1):
    def __init__(self):
        super().__init__()
        self.y_pos = 290

# Variables

game_speed = 5
game_active = False
game_over = False
cloud_probability = 0.2
player_score = 0
try:
    file = open("highscore.txt", 'r')
    high_score = int(file.readline())
    file.close()
except:
    high_score = 0
last_cloud_time = 0
cloud_interval = 3000
last_obstacle_time = 0
obstacle_interval = 1500

# Surfaces

ground = pygame.image.load("assets/Other/Track.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))

# Groups

dino_group = pygame.sprite.GroupSingle()
cloud_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Functions

def start_screen():
    screen.fill("white")
    start_screen = pygame.image.load("assets/DinoWallpaper.png")
    start_screen_rect = start_screen.get_rect(center=(640, 300))
    text1 = game_font.render(
        f"Press any key to Start", True, ("black"))
    text2 = game_font.render(
        f"high score: {int(high_score)}", True, ("black"))
    screen.blit(start_screen, start_screen_rect)
    screen.blit(text1, (520, 350))
    screen.blit(text2, (520, 380))
    pygame.display.update()


def game_over_screen():
    screen.fill("white")
    game_over_surface = game_font.render(
        "Game Over", True, ("black"))
    game_over_rect = game_over_surface.get_rect(center=(640, 300))
    score_surface = game_font.render(
        f"Score: {int(player_score)}", True, ("black"))
    score_rect = score_surface.get_rect(center=(640, 340))
    restart_surface = game_font.render(
        "Press 'R' to Restart", True, ("black"))
    restart_rect = restart_surface.get_rect(center=(640, 380))
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.update()

def reset_game():
    global game_speed, player_score, obstacle_group, cloud_group, dinosaur
    game_speed = 5
    player_score = 0
    obstacle_group.empty()
    cloud_group.empty()
    dinosaur.rect.center = (50, 360)
    dinosaur.dead = False

# Main game loop

while True:
    if not game_active:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_active = True
        continue

    if game_over:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_active = True
                    game_over = False
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()

    screen.fill("white")

    game_speed += 0.001
    player_score += 0.1
    if player_score >= high_score:
        high_score = player_score
    player_score_surface = game_font.render(
        "high score: " + str(int(high_score)) + " Points: " + str(int(player_score)), True, ("black"))
    screen.blit(player_score_surface, (950, 10))
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > obstacle_interval:
        random_number = random.randint(1, 10)
        if 1 <= random_number <= 6:
            new_obstacle = Cactus(1280, 340)
        elif 7 <= random_number <= 10:
            if random_number % 2 == 1:
                new_obstacle = Bird1()
            else:
                new_obstacle = Bird2()
        obstacle_group.add(new_obstacle)
        last_obstacle_time = current_time
    if random.random() < cloud_probability and current_time - last_cloud_time > cloud_interval:
        cloud_group.add(Cloud())
        last_cloud_time = current_time

    dino_group.update()
    dino_group.draw(screen)
    cloud_group.update()
    cloud_group.draw(screen)
    obstacle_group.update()
    obstacle_group.draw(screen)

    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        dinosaur.dead = True
        game_over = True
        try:
            file = open("highscore.txt", 'w')
            file.write(str(int(high_score)))
            file.close()
        except:
            pass

    ground_x -= game_speed
    screen.blit(ground, (ground_x, 360))
    screen.blit(ground, (ground_x + 1280, 360))
    if ground_x <= -1280:
        ground_x = 0

    clock.tick(120)
    pygame.display.update()
