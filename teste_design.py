import pygame
import plotly.express as px
import pandas as pd
import upar_nivel as un

pygame.init()

# Configuração da tela
width, height = 1000, 800
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu com Botões de Atributos")

# Carregar imagem do menu
menu_img = pygame.image.load("Imagem menu/menu.png")
menu_img = pygame.transform.scale(menu_img, (400, 600))

# Fonte
tamanho_fonte = 22
fonte = pygame.font.SysFont(None, tamanho_fonte)

class Menu():
    def __init__(self, valor_ataque, valor_defesa, valor_vida, valor_stamina, valor_velocidade):
        self.valores = {
            "ataque": valor_ataque,
            "defesa": valor_defesa,
            "vida": valor_vida,
            "stamina": valor_stamina,
            "velocidade": valor_velocidade
        }

        # Carregar spritesheets dos botões
        self.botao_mais = pygame.image.load('Spritesheet/SpriteSheet_mais.png')
        self.botao_menos = pygame.image.load('Spritesheet/Spritesheet_menos.png')

        # Criar dicionário para armazenar botões e suas posições
        self.botoes = {}

        for i, atributo in enumerate(self.valores.keys()):
            x_menos, x_mais, x_texto, y = 500, 550, 530, 108 + i * 50  # Ajuste de posição

            # Carregar os sprites dos botões
            frames_menos = [self.botao_menos.subsurface((j * 32, 0, 32, 32)) for j in range(2)]
            frames_mais = [self.botao_mais.subsurface((j * 32, 0, 32, 32)) for j in range(2)]

            # Criar botões de aumentar e diminuir
            self.botoes[atributo] = {
                "aumentar": {
                    "rect": pygame.Rect(x_mais, y, 32, 32),
                    "sprites": frames_mais,
                    "atual": 0,
                    "pressionado": False
                },
                "diminuir": {
                    "rect": pygame.Rect(x_menos, y, 32, 32),
                    "sprites": frames_menos,
                    "atual": 0,
                    "pressionado": False
                },
                "texto_pos": (x_texto, y)  # Posição do número do atributo
            }

    def atualizar_sprites(self):
        """ Atualiza os sprites dependendo do estado do botão. """
        for botoes in self.botoes.values():
            for botao in ["aumentar", "diminuir"]:
                botoes[botao]["atual"] = 1 if botoes[botao]["pressionado"] else 0

    def desenhar_valores(self):
        """ Desenha os valores atuais dos atributos ao lado dos botões. """
        for atributo, botoes in self.botoes.items():
            texto = fonte.render(str(self.valores[atributo]), True, (0, 0, 0))
            tela.blit(texto, botoes["texto_pos"])

    def grafico(self):
        df = pd.DataFrame(dict(
            r=[self.valores.values()],
            theta=['processing cost', 'mechanical properties', 'chemical stability',
                'thermal stability', 'device integration', "nome"]))

        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')

        # Remover apenas a linha circular onde ficavam os números
        fig.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=False, linecolor="rgba(0,0,0,0)")
            )
        )

        fig.show()

menu = Menu(3, 2, 3, 2, 3)

# Loop principal
running = True
while running:
    tela.fill((255, 255, 255))  # Limpar tela

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for atributo, botoes in menu.botoes.items():
                if botoes["diminuir"]["rect"].collidepoint(event.pos) and un.pontos_disponiveis < un.pontos_disponiveis_copy:
                    menu.valores[atributo] = max(0, menu.valores[atributo] - 1)  # Evita valores negativos
                    botoes["diminuir"]["pressionado"] = True
                    un.pontos_disponiveis += 1
                    # print(f"{atributo}: {menu.valores[atributo]}")
                    print(un.pontos_disponiveis_copy)

                if botoes["aumentar"]["rect"].collidepoint(event.pos) and un.pontos_disponiveis > 0:
                    menu.valores[atributo] += 1
                    botoes["aumentar"]["pressionado"] = True
                    un.pontos_disponiveis -= 1
                    print(f"{atributo}: {menu.valores[atributo]}")

        if event.type == pygame.MOUSEBUTTONUP:
            for botoes in menu.botoes.values():
                botoes["aumentar"]["pressionado"] = False
                botoes["diminuir"]["pressionado"] = False

    # Atualizar sprites
    menu.atualizar_sprites()

    # Desenhar a imagem do menu
    tela.blit(menu_img, (200, 0))  # Posição na tela

    # Desenhar os botões
    for atributo, botoes in menu.botoes.items():
        tela.blit(botoes["diminuir"]["sprites"][botoes["diminuir"]["atual"]], botoes["diminuir"]["rect"].topleft)
        tela.blit(botoes["aumentar"]["sprites"][botoes["aumentar"]["atual"]], botoes["aumentar"]["rect"].topleft)

    # Desenhar os valores dos atributos
    menu.desenhar_valores()
    pontos_disponiveis = fonte.render(f"{un.pontos_disponiveis}", True, (0, 0, 0))

    # Atualizar a tela
    tela.blit(pontos_disponiveis, (0,0))
    pygame.display.flip()

pygame.quit()
