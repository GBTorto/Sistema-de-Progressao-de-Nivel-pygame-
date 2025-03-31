import pygame
import plotly.express as px
import pandas as pd
from upar_nivel import Combate

pygame.init()


# Inicia o combate e o menu
combate = Combate()
# menu = Menu(3, 2, 3, 2, 3)  # Inicializando o menu com valores

class Menu():
    def __init__(self, valor_ataque, valor_defesa, valor_vida, valor_stamina, valor_velocidade):      
        self.valores = {
            "ataque": valor_ataque,
            "defesa": valor_defesa,
            "vida": valor_vida,
            "stamina": valor_stamina,
            "velocidade": valor_velocidade
        }

        self.menu_img = pygame.image.load("Imagem menu/menu.png")
        self.menu_img = pygame.transform.scale(self.menu_img, (400, 600))

        self.tamanho_fonte = 22
        self.fonte = pygame.font.SysFont(None, self.tamanho_fonte)

        self.botao_mais = pygame.image.load('Spritesheet/SpriteSheet_mais.png')
        self.botao_menos = pygame.image.load('Spritesheet/Spritesheet_menos.png')

        self.botoes = {}

        for i, atributo in enumerate(self.valores.keys()):
            x_menos, x_mais, x_texto, y = 500, 550, 530, 108 + i * 50
            frames_menos = [self.botao_menos.subsurface((j * 32, 0, 32, 32)) for j in range(2)]
            frames_mais = [self.botao_mais.subsurface((j * 32, 0, 32, 32)) for j in range(2)]

            self.botoes[atributo] = {
                "aumentar": {"rect": pygame.Rect(x_mais, y, 32, 32), "sprites": frames_mais, "atual": 0, "pressionado": False},
                "diminuir": {"rect": pygame.Rect(x_menos, y, 32, 32), "sprites": frames_menos, "atual": 0, "pressionado": False},
                "texto_pos": (x_texto, y)
            }

    def atualizar_sprites(self):
        for botoes in self.botoes.values():
            for botao in ["aumentar", "diminuir"]:
                botoes[botao]["atual"] = 1 if botoes[botao]["pressionado"] else 0

    def desenhar_valores(self, tela):
        for atributo, botoes in self.botoes.items():
            texto = self.fonte.render(str(self.valores[atributo]), True, (0, 0, 0))
            tela.blit(texto, botoes["texto_pos"])

    def processar_eventos(self, event):
        for atributo, botoes in self.botoes.items():
            if botoes["diminuir"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis < combate.pontos_disponiveis_copy:
                self.valores[atributo] = max(0, self.valores[atributo] - 1)
                botoes["diminuir"]["pressionado"] = True
                combate.pontos_disponiveis += 1

            if botoes["aumentar"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis > 0:
                self.valores[atributo] += 1
                botoes["aumentar"]["pressionado"] = True
                combate.pontos_disponiveis -= 1

    def resetar_botoes(self):
        for botoes in self.botoes.values():
            botoes["aumentar"]["pressionado"] = False
            botoes["diminuir"]["pressionado"] = False

# Inicialização do Pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sistema de Combate Simples")

# # Inicia o loop do jogo
# if __name__ == "__main__":
#     combate.game_loop()
#     for event in pygame.event.type:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_m:
#                 menu.menu_img