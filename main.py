# game/main.py
import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cria a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('World')

# Define as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carrega as imagens
player_image = pygame.image.load('assets/player.png')
obstacle_image = pygame.image.load('assets/obstacle.png')
background_image = pygame.image.load('assets/background.png')

# Carrega os sons
jump_sound = pygame.mixer.Sound('assets/jump.wav')
game_over_sound = pygame.mixer.Sound('assets/game_over.wav')

# Classe para o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.is_jumping = False
        self.jump_speed = 80
        self.gravity = 0.4
        self.vertical_speed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vertical_speed = -self.jump_speed
            jump_sound.play()  # Toca o som de pulo

        if self.is_jumping:
            self.rect.y += self.vertical_speed
            self.vertical_speed += self.gravity

            if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
                self.rect.y = SCREEN_HEIGHT - self.rect.height
                self.is_jumping = False
                self.vertical_speed = 0

# Classe para os obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.kill()

# Função para gerar novos obstáculos periodicamente
def generate_obstacles(obstacle_group):
    if random.randint(1, 100) < 10:  # Ajuste a probabilidade de geração conforme necessário
        obstacle = Obstacle()
        obstacle_group.add(obstacle)

# Função para exibir a tela de "Game Over"
def game_over_screen(score):
    game_over_sound.play()  # Toca o som de game over
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('Game Over', True, BLACK)
    score_text = font.render(f'Score: {score}', True, BLACK)
    restart_text = font.render('Press R to Restart', True, BLACK)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# Loop principal do jogo
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        player = Player()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        obstacle_group = pygame.sprite.Group()

        score = 0
        font = pygame.font.SysFont(None, 36)

        game_over = False
        while not game_over:
            # Processa os eventos (teclado, mouse, etc.)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = True

            # Atualiza o estado do jogo
            all_sprites.update()
            obstacle_group.update()
            generate_obstacles(obstacle_group)

            # Verifica colisões
            if pygame.sprite.spritecollideany(player, obstacle_group):
                game_over = True  # Game Over

            # Incrementa a pontuação
            score += 1

            # Renderiza o jogo
            screen.blit(background_image, (0, 0))  # Desenha o background
            all_sprites.draw(screen)  # Desenha os sprites
            obstacle_group.draw(screen)  # Desenha os obstáculos

            # Renderiza a pontuação
            score_text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

            # Atualiza a tela
            pygame.display.flip()

            # Controla a taxa de quadros
            clock.tick(60)

        if not running:
            break

        game_over_screen(score)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
