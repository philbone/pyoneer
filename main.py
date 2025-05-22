import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Nave en Gravedad Cero")

# Constantes
PIXEL = 5
FPS = 60

# Colores
COLORES = {
    0: (0, 0, 0),           # fondo
    1: (255, 224, 189),     # piel
    2: (180, 180, 255),     # traje
    3: (50, 50, 50),        # casco/botas
    4: (0, 128, 255),       # visor
}

colores_llama = {
    0: None,
    1: (255, 140, 0),     # naranja
    2: (255, 255, 255),   # blanco
}

# Sprite nave
nave = [
    [0,0,0,3,3,3,3,3,3,0,0,0],
    [0,0,3,4,4,4,4,4,4,3,0,0],
    [0,3,4,4,4,4,4,4,4,4,3,0],
    [3,4,4,4,4,1,1,1,1,1,4,3],
    [3,4,4,4,4,1,1,1,1,1,4,3],
    [3,2,4,4,4,4,4,4,4,4,4,3],
    [3,2,2,2,4,4,4,4,4,4,2,3],
    [0,3,2,2,2,2,2,2,2,2,3,0],
    [0,0,3,2,2,2,2,2,2,3,0,0],
    [0,0,0,3,3,3,3,3,3,0,0,0],    
]

# Patrones de llama
llamas = [
    [[0, 0, 2], [0, 1, 0], [2, 0, 0]],
    [[0, 1, 0], [2, 0, 2], [0, 1, 0]],
    [[2, 0, 2], [0, 1, 0], [1, 0, 1]],
    [[0, 2, 0], [1, 0, 1], [0, 2, 0]],
]

# Funciones de dibujo
def dibujar_llama_animada(pantalla, x, y, escala):
    sprite_llama = random.choice(llamas)
    for fila_idx, fila in enumerate(sprite_llama):
        for col_idx, pixel in enumerate(fila):
            color = colores_llama.get(pixel)
            if color:
                pygame.draw.rect(pantalla, color, (
                    x + col_idx * escala,
                    y + fila_idx * escala,
                    escala,
                    escala
                ))

def dibujar_sprite(pantalla, sprite, x, y, pixel_size, flip=False):
    for fila_idx, fila in enumerate(sprite):
        for col_idx, val in enumerate(fila):
            if val != 0:
                color = COLORES[val]
                col = len(fila) - col_idx - 1 if flip else col_idx
                pygame.draw.rect(
                    pantalla,
                    color,
                    (x + col * pixel_size, y + fila_idx * pixel_size, pixel_size, pixel_size)
                )

# Inicialización
Vector2 = pygame.math.Vector2
pos = Vector2(300, 200)
vel = Vector2(0, 0)
acel = 0.3
rozamiento = 0.98
max_vel = 5

particulas = []
impulsando_anteriormente = False
direccion_fuego = None
hacia_izquierda = False

reloj = pygame.time.Clock()
corriendo = True

# Bucle principal
while corriendo:
    dt = reloj.tick(FPS)
    pantalla.fill((0, 0, 0))

    teclas = pygame.key.get_pressed()
    impulsando = False
    impulso_vector = Vector2(0, 0)

    if teclas[pygame.K_LEFT]:
        impulso_vector.x -= acel
        impulsando = True
        direccion_fuego = "izquierda"
        hacia_izquierda = True
    if teclas[pygame.K_RIGHT]:
        impulso_vector.x += acel
        impulsando = True
        direccion_fuego = "derecha"
        hacia_izquierda = False
    if teclas[pygame.K_UP]:
        impulso_vector.y -= acel
        impulsando = True
        direccion_fuego = "arriba"
    if teclas[pygame.K_DOWN]:
        impulso_vector.y += acel
        impulsando = True
        direccion_fuego = "abajo"

    vel += impulso_vector
    if not impulsando:
        vel *= rozamiento
    if vel.length() > max_vel:
        vel.scale_to_length(max_vel)

    pos += vel

    # Dibujar nave
    dibujar_sprite(pantalla, nave, int(pos.x), int(pos.y), PIXEL, flip=hacia_izquierda)

    # Propulsión visual
    if impulsando:
        if direccion_fuego == "abajo":
            dibujar_llama_animada(pantalla, int(pos.x + 24), int(pos.y - 3 * PIXEL), PIXEL)
        elif direccion_fuego == "arriba":
            dibujar_llama_animada(pantalla, int(pos.x + 24), int(pos.y + 12 * PIXEL), PIXEL)
        elif direccion_fuego == "izquierda":
            dibujar_llama_animada(pantalla, int(pos.x + 12 * PIXEL), int(pos.y + 5 * PIXEL), PIXEL)
        elif direccion_fuego == "derecha":
            dibujar_llama_animada(pantalla, int(pos.x - 3 * PIXEL), int(pos.y + 5 * PIXEL), PIXEL)

    # Generar partículas sutiles al soltar impulso (excepto si era hacia abajo)
    if not impulsando and impulsando_anteriormente and direccion_fuego != "abajo":
        for _ in range(3):
            particulas.append({
                "pos": pos + Vector2(6 * PIXEL, 7 * PIXEL),
                "vel": Vector2(random.uniform(-0.2, 0.2), random.uniform(-0.4, -0.1)),
                "vida": random.randint(40, 60),
                "tam": random.randint(1, 2),
                "vida_total": 60
            })

    # Actualizar y dibujar partículas
    for p in particulas[:]:
        p["pos"] += p["vel"]
        p["vida"] -= 1

        if p["vida"] <= 0:
            particulas.remove(p)
            continue

        t = p["vida"] / p["vida_total"]
        if t > 0.75:
            color = (200, 160, 100)
            glow = (200, 160, 100, 20)
        elif t > 0.5:
            color = (180, 180, 130)
            glow = (180, 180, 130, 15)
        elif t > 0.25:
            color = (160, 200, 230)
            glow = (160, 200, 230, 10)
        else:
            color = (220, 220, 220)
            glow = (220, 220, 220, 5)

        glow_surf = pygame.Surface((p["tam"] * 6, p["tam"] * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, glow, (p["tam"] * 3, p["tam"] * 3), p["tam"] * 3)
        pantalla.blit(glow_surf, (p["pos"].x - p["tam"] * 3, p["pos"].y - p["tam"] * 3))
        pygame.draw.circle(pantalla, color, (int(p["pos"].x), int(p["pos"].y)), p["tam"])

    impulsando_anteriormente = impulsando

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pygame.display.flip()

pygame.quit()
sys.exit()
