import pygame

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

mw = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

try:
    background_image = pygame.image.load("background.png").convert()
    background_image = pygame.transform.scale(background_image, (ANCHO_VENTANA, ALTO_VENTANA))
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar 'background.png'. Se usará un fondo negro. Error: {e}")
    background_image = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    background_image.fill((0, 0, 0))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, archivo_img, x, y, ancho, alto, color_alternativo=(0,0,0)):
        super().__init__()
        self.image = None
        try:
            self.image = pygame.image.load(archivo_img).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ancho, alto))
        except pygame.error as e:
            print(f"Advertencia: No se encontró el archivo '{archivo_img}'. Se usará un color sólido. Error: {e}")
            self.image = pygame.Surface((ancho, alto))
            self.image.fill(color_alternativo)

        self.rect = self.image.get_rect(topleft=(x, y))


plataforma = GameObject("platform.png", 350, 500, 100, 30, color_alternativo=(0, 0, 255))
pelota = GameObject("ball.png", 375, 400, 50, 50, color_alternativo=(255, 0, 0))

all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

all_sprites.add(plataforma)
all_sprites.add(pelota)

inicio_x = 5
inicio_y = 5
cantidad = 13
for i in range(3):
    y = inicio_y + (55 * i)
    x = inicio_x + (27.5 * i)
    for j in range(cantidad):
        enemigo = GameObject("enemigo.png", x, y, 50, 50, color_alternativo=(0, 255, 0))
        enemigos.add(enemigo)
        all_sprites.add(enemigo)
        x += 55
    cantidad -= 1

move_right = False
move_left = False
speed_x = 4
speed_y = 4

game_over = False
game_run = True
font = pygame.font.Font(None, 70)
win_label = font.render("¡GANASTE!", True, (0, 200, 0))
lose_label = font.render("¡PERDISTE!", True, (200, 0, 0))

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: move_right = True
                if event.key == pygame.K_LEFT: move_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT: move_right = False
                if event.key == pygame.K_LEFT: move_left = False

    if not game_over:
        if move_right and plataforma.rect.right < ANCHO_VENTANA:
            plataforma.rect.x += 5
        if move_left and plataforma.rect.left > 0:
            plataforma.rect.x -= 5
        
        pelota.rect.x += speed_x
        pelota.rect.y += speed_y

        if pelota.rect.top <= 0:
            speed_y *= -1
        if pelota.rect.left <= 0 or pelota.rect.right >= ANCHO_VENTANA:
            speed_x *= -1

        if pelota.rect.colliderect(plataforma.rect):
            speed_y *= -1

        enemigos_golpeados = pygame.sprite.spritecollide(pelota, enemigos, True) 
        if enemigos_golpeados:
            speed_y *= -1
        
        if not enemigos:
            game_over = True
        if pelota.rect.top > ALTO_VENTANA:
            game_over = True

    mw.blit(background_image, (0, 0))
    all_sprites.draw(mw)

    if game_over:
        if not enemigos:
            mw.blit(win_label, (250, 250))
        else:
            mw.blit(lose_label, (250, 250))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
