import pygame
import plotly.express as px
import pandas as pd
from xp import Combate

pygame.init()


# Inicia o combate e o menu
combate = Combate()
# menu = Menu(3, 2, 3, 2, 3)  # Inicializando o menu com valores

class Menu():
    def __init__(self, valor_ataque, valor_defesa, valor_vida, valor_stamina, valor_velocidade, atr_ataque, atr_defesa, atr_vida, atr_stamina, atr_velocidade):  
        self.valores = {
            "ataque": valor_ataque,
            "defesa": valor_defesa,
            "vida": valor_vida,
            "stamina": valor_stamina,
            "velocidade": valor_velocidade
        }

        self.atributos = {
            "ataque": atr_ataque,
            "defesa": atr_defesa,
            "vida": atr_vida,
            "stamina": atr_stamina,
            "velocidade": atr_velocidade
        }

        self.valores_copy = 0

        self.tamanho_menu_img_x = 0
        self.tamanho_menu_img_y = 0

        self.menu_img_original = pygame.image.load("Imagem menu/menu.png")
        self.menu_img = pygame.transform.scale(self.menu_img_original, (self.tamanho_menu_img_x, self.tamanho_menu_img_y))

        self.tamanho_fonte = 22
        self.fonte = pygame.font.SysFont(None, self.tamanho_fonte)

        self.botao_mais = pygame.image.load('Spritesheet/SpriteSheet_mais.png')
        self.botao_menos = pygame.image.load('Spritesheet/Spritesheet_menos.png')

        self.botoes = {}

        for i, atributo in enumerate(self.valores.keys()):
            x_menos, x_mais, x_texto, y, y_texto = 300, 350, 330, 227 + i * 30.9, 230 + i * 30.7
            frames_menos = [self.botao_menos.subsurface((j * 25, 0, 20, 20)) for j in range(2)]
            frames_mais = [self.botao_mais.subsurface((j * 25, 0, 20, 20)) for j in range(2)]

            self.botoes[atributo] = {
                "aumentar": {"rect": pygame.Rect(x_mais, y, 25, 25), "sprites": frames_mais, "atual": 0, "pressionado": False},
                "diminuir": {"rect": pygame.Rect(x_menos, y, 25, 25), "sprites": frames_menos, "atual": 0, "pressionado": False},
                "texto_pos": (x_texto, y_texto)
            }
        
    # def aumentar_tamanho(self):
        """Aumenta gradualmente o tamanho do menu até um limite"""
        # if self.tamanho_menu_img_x < 600 and self.tamanho_menu_img_y < 400:
        #     self.tamanho_menu_img_x += 10  # Ajuste a velocidade do zoom
        #     self.tamanho_menu_img_y += 5
        #     self.menu_img = pygame.transform.scale(self.menu_img_original, (self.tamanho_menu_img_x, self.tamanho_menu_img_y))

    def desenhar_botoes(self, tela):
        for atributo, botoes in self.botoes.items():
            tela.blit(botoes["diminuir"]["sprites"][botoes["diminuir"]["atual"]], botoes["diminuir"]["rect"].topleft)
            tela.blit(botoes["aumentar"]["sprites"][botoes["aumentar"]["atual"]], botoes["aumentar"]["rect"].topleft)

    def atualizar_sprites(self):
        for botoes in self.botoes.values():
            for botao in ["aumentar", "diminuir"]:
                botoes[botao]["atual"] = 1 if botoes[botao]["pressionado"] else 0

    def desenhar_valores(self, tela, font_nivel, text_nivel, nivel, pontos_disponiveis):
        font_nivel = pygame.font.SysFont(None, self.tamanho_fonte)
        text_nivel = font_nivel.render(f"{nivel}", True, (0,0,0))
        tela.blit(text_nivel, (270, 166))

        font_pontos_disponiveis = pygame.font.SysFont(None, self.tamanho_fonte)
        text_pontos_disponiveis = font_pontos_disponiveis.render(f"{pontos_disponiveis}", True, (0,0,0))
        tela.blit(text_pontos_disponiveis, (300, 426))

        for atributo, botoes in self.botoes.items():
            texto = self.fonte.render(str(self.valores[atributo]), True, (0, 0, 0))
            tela.blit(texto, botoes["texto_pos"])

        for i, key in enumerate(self.atributos.keys()):
            text_atributo = self.fonte.render(str(self.atributos[key]), True, (0,0,0))
            tela.blit(text_atributo, (610, 231 + i * 30))

    def resetar_botoes(self):
        for botoes in self.botoes.values():
            botoes["aumentar"]["pressionado"] = False
            botoes["diminuir"]["pressionado"] = False
        self.atualizar_sprites()  # Garante que os sprites são atualizados


# Inicialização do Pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sistema de Combate Simples")

# print(Menu(5, 5, 5, 5, 5, 1, 1, 1, 1, 1, tamanho_menu_img_x, tamanho_menu_img_y))
# # Inicia o loop do jogo
# if __name__ == "__main__":
#     combate.game_loop()
#     for event in pygame.event.type:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_m:
#                 menu.menu_img