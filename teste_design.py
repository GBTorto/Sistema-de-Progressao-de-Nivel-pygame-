import pygame

pygame.init()

# Configuração da tela
width, height = 1000, 800
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu com Botões de Atributos")

# Carregar imagem do menu
menu_img = pygame.image.load("Imagem menu/menu.png")
menu_img = pygame.transform.scale(menu_img, (400, 600))

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
            x_menos, x_mais, y = 500, 550, 50 + i * 30  # Ajuste de posição

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
                }
            }

    def atualizar_sprites(self):
        """ Atualiza os sprites dependendo do estado do botão. """
        for botoes in self.botoes.values():
            for botao in botoes.values():
                botao["atual"] = 1 if botao["pressionado"] else 0

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
                if botoes["diminuir"]["rect"].collidepoint(event.pos):
                    menu.valores[atributo] = max(0, menu.valores[atributo] - 1)  # Evita valores negativos
                    botoes["diminuir"]["pressionado"] = True
                    print(f"{atributo}: {menu.valores[atributo]}")

                if botoes["aumentar"]["rect"].collidepoint(event.pos):
                    menu.valores[atributo] += 1
                    botoes["aumentar"]["pressionado"] = True
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

    # Atualizar a tela
    pygame.display.update()

pygame.quit()
