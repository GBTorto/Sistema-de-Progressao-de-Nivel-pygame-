import pygame
import plotly.express as px
import pandas as pd

pygame.init()

# Configuração da tela
width, height = 1000, 800
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Redimensionar Imagem")

# Carregar imagem do menu
menu_img = pygame.image.load("Imagem menu/menu.png")
menu_img = pygame.transform.scale(menu_img, (400, 600))

# Fonte
tamanho_fonte = 100

class Menu():
    def __init__(self, valor_ataque, valor_defesa, valor_vida, valor_stamina, valor_velocidade):
        self.valores = {
            "ataque": valor_ataque,
            "defesa": valor_defesa,
            "vida": valor_vida,
            "stamina": valor_stamina,
            "velocidade": valor_velocidade
        }

        # Carregar spritesheet do botão de menos
        self.botao_menos = pygame.image.load('Spritesheet/spritesheet_menos.png')

        # Criar dicionário para armazenar botões e suas posições
        self.botoes = {}
        self.sprites = {}

        for i, atributo in enumerate(self.valores.keys()):
            x, y = 550, 110 + i * 30  # Posiciona os botões verticalmente

            # Carregar os sprites do botão de menos
            frames = [self.botao_menos.subsurface((j * 32, 0, 32, 32)) for j in range(2)]

            # Criar botão
            self.botoes[atributo] = {
                "diminuir": {
                    "rect": pygame.Rect(x, y, 32, 32),
                    "sprites": frames,
                    "atual": 0,
                    "pressionado": False
                }
            }

    def atualizar_sprites(self):
        for botoes in self.botoes.values():  # Percorre diretamente os valores do dicionário
            botao = botoes["diminuir"]
            if botao["pressionado"]:
                botao["atual"] = len(botao["sprites"]) - 1 
            else:
                botao['atual'] = 0

    def grafico(self):
        df = pd.DataFrame(dict(
            r=[2, 5, 2, 2, 3, 9],
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

menu = Menu(10, 5, 20, 8, 15)

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
                botao = botoes["diminuir"]
                if botao["rect"].collidepoint(event.pos):
                    menu.valores[atributo] -= 1  # Diminui o valor do atributo
                    botao["pressionado"] = True  # Define como pressionado
                    print(f"{atributo}: {menu.valores[atributo]}")

        if event.type == pygame.MOUSEBUTTONUP:
            for botoes in menu.botoes.values():
                botoes["diminuir"]["pressionado"] = False  # Solta o botão

    # Atualizar sprites
    menu.atualizar_sprites()

    # Desenhar a imagem do menu
    tela.blit(menu_img, (200, 0))  # Posição na tela

    # Desenhar os botões
    for atributo, botoes in menu.botoes.items():
        botao = botoes["diminuir"]
        tela.blit(botao["sprites"][botao["atual"]], botao["rect"].topleft)

    # Atualizar a tela
    pygame.display.update()

pygame.quit()
