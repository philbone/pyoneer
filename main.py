import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Nave en Gravedad Cero")

PIXEL = 5

# Colores
COLORES = {
    0: (0, 0, 0),           # fondo
    1: (255, 224, 189),     # cara/piel
    2: (180, 180, 255),     # traje
    3: (50, 50, 50),        # casco/botas
    4: (0, 128, 255),       # visor
    5: (255, 100, 0),       # fuego
}

# Sprite nave (12x14)
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

# Varios patrones de llama
llamas = [
    [
        [0, 0, 2],
        [0, 1, 0],
        [2, 0, 0],
    ],
    [
        [0, 1, 0],
        [2, 0, 2],
        [0, 1, 0],
    ],
    [
        [2, 0, 2],
        [0, 1, 0],
        [1, 0, 1],
    ],
    [
        [0, 2, 0],
        [1, 0, 1],
        [0, 2, 0],
    ]
]

# Colores: 0 = transparente, 1 = naranja, 2 = blanco brillante
colores_llama = {
    0: None,
    1: (255, 140, 0),     # naranja
    2: (255, 255, 255),   # blanco
}

particulas = []
impulsando_anteriormente = False

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

# Posición y física
pos_x, pos_y = 300, 200
vel_x, vel_y = 0, 0
acel = 0.3
rozamiento = 0.98
max_vel = 5

reloj = pygame.time.Clock()
corriendo = True

# Dirección para flip del sprite
hacia_izquierda = False

while corriendo:
    dt = reloj.tick(60)
    pantalla.fill((0, 0, 0))

    teclas = pygame.key.get_pressed()
    impulsando = False
    direccion_fuego = None

    if teclas[pygame.K_LEFT]:
        vel_x -= acel
        impulsando = True
        direccion_fuego = "izquierda"  # fuego se muestra a la derecha
        hacia_izquierda = True
    if teclas[pygame.K_RIGHT]:
        vel_x += acel
        impulsando = True
        direccion_fuego = "derecha"  # fuego se muestra a la izquierda
        hacia_izquierda = False
    if teclas[pygame.K_UP]:
        vel_y -= acel
        impulsando = True
        direccion_fuego = "abajo"
    if teclas[pygame.K_DOWN]:
        vel_y += acel
        impulsando = True
        direccion_fuego = "arriba"

    # Detectar transición de impulso a no-impulso
    # Solo generar partículas si venía de izquierda, derecha o arriba
    if not impulsando and impulsando_anteriormente and direccion_fuego != "abajo":
        for _ in range(3):  # menos partículas para hacerlo más sutil
            particulas.append({
                "x": pos_x + 6 * PIXEL,
                "y": pos_y + 7 * PIXEL,
                "vx": random.uniform(-0.2, 0.2),
                "vy": random.uniform(-0.4, -0.1),  # ascenso más lento
                "vida": random.randint(40, 60),
                "tam": random.randint(1, 2),
                "vida_total": 60
            })

    # Limitar velocidad
    vel_x = max(-max_vel, min(max_vel, vel_x))
    vel_y = max(-max_vel, min(max_vel, vel_y))

    # Aplicar rozamiento
    vel_x *= rozamiento
    vel_y *= rozamiento

    pos_x += vel_x
    pos_y += vel_y

    # Dibujar personaje
    dibujar_sprite(pantalla, nave, int(pos_x), int(pos_y), PIXEL, flip=hacia_izquierda)

    # Dibujar propulsión dependiendo de dirección
    if impulsando:
        if direccion_fuego == "arriba":            
            dibujar_llama_animada(pantalla, int(pos_x + 24), int(pos_y - 2 * PIXEL), PIXEL)
        if direccion_fuego == "abajo":            
            dibujar_llama_animada(pantalla, int(pos_x + 24), int(pos_y + 8 * PIXEL), PIXEL)
        if direccion_fuego == "izquierda":
            dibujar_llama_animada(pantalla, int(pos_x + 11 * PIXEL), int(pos_y + 5 * PIXEL), PIXEL)
        elif direccion_fuego == "derecha":
            dibujar_llama_animada(pantalla, int(pos_x - 2 * PIXEL), int(pos_y + 5 * PIXEL), PIXEL)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Actualizar y dibujar partículas
    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vida"] -= 1

        if p["vida"] <= 0:
            particulas.remove(p)
        else:
            t = p["vida"] / p["vida_total"]

            # Colores más pálidos y tenues
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

            # Halo difuso
            glow_surf = pygame.Surface((p["tam"] * 6, p["tam"] * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, glow, (p["tam"] * 3, p["tam"] * 3), p["tam"] * 3)
            pantalla.blit(glow_surf, (p["x"] - p["tam"] * 3, p["y"] - p["tam"] * 3))

            # Núcleo pequeño y suave
            pygame.draw.circle(pantalla, color, (int(p["x"]), int(p["y"])), p["tam"])


    pygame.display.flip()
    impulsando_anteriormente = impulsando

pygame.quit()
sys.exit()
