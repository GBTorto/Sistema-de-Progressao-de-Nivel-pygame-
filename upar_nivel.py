import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema de Combate Simples")

class Combate():
    def __init__(self):
        # Cores
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)

        # Parâmetros do jogador e inimigo
        self.player_size = 50
        self.player_speed = 5
        self.player = pygame.Rect(WIDTH // 4, HEIGHT // 2, self.player_size, self.player_size)

        self.enemy_size = 50
        self.enemy = pygame.Rect(WIDTH * 3 // 4, HEIGHT // 2, self.enemy_size, self.enemy_size)

        # Barra de vida do inimigo
        self.enemy_health = 100
        self.max_health = 100

        # Sistema de xp
        self.xp = 0
        self.xp_limitador = 0
        self.xp_max = 100
        self.nivel = 1
        self.nivel_anterior = self.nivel
        self.tamanho_nivel = 40
        self.dano = 15
        self.multiplicador_xp = 1.1
        self.temporizador_mensagem = None 

        # Variáveis xp
        self.xp_width = 200
        self.xp_height = 10
        self.xp_ratio = 0
        self.temporizador_xp = None
        self.ganhando_xp = False

        # Posição desenho do nivel
        self.pos_xp_x = (WIDTH // 2) - (self.xp_width // 2)
        self.pos_xp_y = HEIGHT - (self.xp_height * 2)
        self.pos_nivel_x = (WIDTH // 2) - (self.nivel)
        self.pos_nivel_y = self.pos_xp_y - (self.tamanho_nivel - 10)

        # Distribuição de pontos
        self.pontos_disponiveis = 0
        self.pontos_disponiveis_copy = 0

        # Inicializa o Pygame Clock
        self.clock = pygame.time.Clock()

        self.show_menu = False

    # Função para desenhar a barra de vida
    def draw_health_bar(self, x, y, health, max_health):
        health_width = 200
        health_height = 20
        health_ratio = health / max_health
        pygame.draw.rect(screen, self.RED, (x, y, health_width, health_height))
        pygame.draw.rect(screen, self.GREEN, (x, y, health_width * health_ratio, health_height))

    # Função para atacar
    def attack(self, dano):
        """Reduz a vida do inimigo ao atacar"""
        self.enemy_health -= dano
        if self.enemy_health < 0:
            self.enemy_health = 0

    # Movimentação do jogador
    def movimentacao(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player.x > 0:
            self.player.x -= self.player_speed
        if keys[pygame.K_d] and self.player.x < WIDTH - self.player_size:
            self.player.x += self.player_speed
        if keys[pygame.K_w] and self.player.y > 0:
            self.player.y -= self.player_speed
        if keys[pygame.K_s] and self.player.y < HEIGHT - self.player_size:
            self.player.y += self.player_speed

        # Movimentação do inimigo
        if self.enemy.x > self.player.x:
            self.enemy.x -= 1
        elif self.enemy.x < self.player.x:
            self.enemy.x += 1

        if self.enemy.y > self.player.y:
            self.enemy.y -= 1
        elif self.enemy.y < self.player.y:
            self.enemy.y += 1

    # Atualiza a barra de XP
    def atualizar_xp(self, tela, x, y):
        if self.enemy_health == 0 and not self.ganhando_xp:
            self.temporizador_xp = pygame.time.get_ticks()
            self.ganhando_xp = True
            self.xp_limitador += 100

        if self.ganhando_xp:
            if self.xp <= self.xp_limitador and pygame.time.get_ticks() - self.temporizador_xp > 30:
                self.xp += 5
                self.xp_ratio = (self.xp / self.xp_max) * 200
                self.temporizador_xp = pygame.time.get_ticks()
            elif self.xp > self.xp_limitador - 5:
                self.ganhando_xp = False
                self.enemy_health = 100

        if self.xp >= self.xp_max and self.temporizador_mensagem is None:
            self.temporizador_mensagem = pygame.time.get_ticks()

            self.nivel += 1
            self.pontos_disponiveis += 5
            print(self.pontos_disponiveis)
            self.pontos_disponiveis_copy = self.pontos_disponiveis
            print(self.pontos_disponiveis_copy)
            self.xp_excedente = self.xp_limitador - self.xp_max
            self.xp_max *= self.multiplicador_xp
            self.xp = 0
            self.xp_limitador = self.xp_excedente
            self.xp_ratio = (self.xp / self.xp_max) * 200

        if self.nivel_anterior < self.nivel:
            self.nivel_anterior = self.nivel
            self.dano += 10

        if self.temporizador_mensagem is not None:
            font = pygame.font.SysFont(None, 55)
            text = font.render("Você upou de nível", True, self.GREEN)
            tela.blit(text, (x // 2 - 120, y // 2 - 50))
            if pygame.time.get_ticks() - self.temporizador_mensagem > 1500:
                self.temporizador_mensagem = None

    # Exibe a tela com os componentes
    def render(self, tela):
        screen.fill(self.BLUE)  # Cor de fundo

        # Desenha o jogador (quadrado branco)
        pygame.draw.rect(screen, self.WHITE, self.player)

        # Desenha o inimigo (quadrado vermelho)
        pygame.draw.rect(screen, self.RED, self.enemy)

        # Desenha a barra de vida do inimigo
        self.draw_health_bar(self.enemy.x, self.enemy.y - 30, self.enemy_health, self.max_health)

        # Desenha a barra de xp
        pygame.draw.rect(screen, self.WHITE, (self.pos_xp_x, self.pos_xp_y, self.xp_width, self.xp_height), 0, 10)
        pygame.draw.rect(screen, self.GREEN, (self.pos_xp_x, self.pos_xp_y, self.xp_ratio, self.xp_height), 0, 10)

        # Desenha o nivel
        self.font_nivel = pygame.font.SysFont(None, self.tamanho_nivel)
        self.text_nivel = self.font_nivel.render(f"{self.nivel}", True, self.GREEN)
        tela.blit(self.text_nivel, (self.pos_nivel_x, self.pos_nivel_y))

#     # Loop do jogo
#     def game_loop(self):
#         running = True
#         while running:
#             self.movimentacao()
#             self.atualizar_xp()
#             self.render()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         self.attack(self.dano)  # Ataca quando o espaço é pressionado

#             pygame.display.flip()
#             self.clock.tick(60)

#         pygame.quit()

# # Inicia o jogo
# if _name_ == "_main_":
#     combate = Combate()
#     combate.game_loop()