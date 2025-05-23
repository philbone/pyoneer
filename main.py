import pygame
import random
import sys
from scene import Scene

pygame.init()

# Constantes generales
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
PIXEL = 5
FPS = 60

# Colores base
PALETTE = {
    0: (0, 0, 0),
    1: (255, 224, 189),
    2: (180, 180, 255),
    3: (50, 50, 50),
    4: (0, 128, 255),
}

LLAMA_COLORS = {
    0: None,
    1: (255, 140, 0),
    2: (255, 255, 255),
}

# Patrones de llama animada
LLAMA_FRAMES = [
    [[0, 0, 2], [0, 1, 0], [2, 0, 0]],
    [[0, 1, 0], [2, 0, 2], [0, 1, 0]],
    [[2, 0, 2], [0, 1, 0], [1, 0, 1]],
    [[0, 2, 0], [1, 0, 1], [0, 2, 0]],
]

# Sprite astronauta
ASTRONAUTA_SPRITE = [
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

class PhysicsConfig:
    def __init__(self, gravity=(0, 0.1)):
        self.gravity = pygame.math.Vector2(gravity)

class Particle:
    def __init__(self, pos):
        self.pos = pos + pygame.math.Vector2(6 * PIXEL, 7 * PIXEL)
        self.vel = pygame.math.Vector2(random.uniform(-0.2, 0.2), random.uniform(-0.4, -0.1))
        self.life = random.randint(40, 60)
        self.size = random.randint(1, 2)
        self.total_life = self.life

    def update(self):
        self.pos += self.vel
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        t = self.life / self.total_life
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

        glow_surf = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, glow, (self.size * 3, self.size * 3), self.size * 3)
        surface.blit(glow_surf, (self.pos.x - self.size * 3, self.pos.y - self.size * 3))
        pygame.draw.circle(surface, color, (int(self.pos.x), int(self.pos.y)), self.size)

class Player:
    def __init__(self, pos, physics_config):
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.flip = False
        self.thrust_dir = None
        self.was_thrusting = False
        self.thrusting = False
        self.sprite = ASTRONAUTA_SPRITE
        self.max_speed = 5
        self.acc = 0.3
        self.friction = 0.98
        self.physics = physics_config  # ← guardar config física

    def get_rect(self):
        return pygame.Rect(
            int(self.pos.x),
            int(self.pos.y),
            12 * PIXEL,  # ancho del personaje
            10 * PIXEL   # alto del personaje
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        thrust = pygame.math.Vector2(0, 0)
        self.thrusting = False

        if keys[pygame.K_LEFT]:
            thrust.x -= self.acc
            self.flip = True
            self.thrust_dir = "left"
            self.thrusting = True
        if keys[pygame.K_RIGHT]:
            thrust.x += self.acc
            self.flip = False
            self.thrust_dir = "right"
            self.thrusting = True
        if keys[pygame.K_UP]:
            thrust.y -= self.acc
            self.thrust_dir = "up"
            self.thrusting = True
        if keys[pygame.K_DOWN]:
            thrust.y += self.acc
            self.thrust_dir = "down"
            self.thrusting = True

        return thrust

    def draw(self, surface):
        for y, row in enumerate(self.sprite):
            for x, val in enumerate(row):
                if val == 0:
                    continue
                color = PALETTE[val]
                px = x if not self.flip else len(row) - x - 1
                pygame.draw.rect(
                    surface,
                    color,
                    (self.pos.x + px * PIXEL, self.pos.y + y * PIXEL, PIXEL, PIXEL)
                )

    def draw_thruster(self, surface):
        if not self.thrusting or not self.thrust_dir:
            return
        # if self.thrust_dir == "down":
        #     x = int(self.pos.x + 24)
        #     y = int(self.pos.y - 3 * PIXEL)
        elif self.thrust_dir == "up":
            x = int(self.pos.x + 24)
            y = int(self.pos.y + 12 * PIXEL)
        elif self.thrust_dir == "left":
            x = int(self.pos.x + 12 * PIXEL)
            y = int(self.pos.y + 5 * PIXEL)
        elif self.thrust_dir == "right":
            x = int(self.pos.x - 3 * PIXEL)
            y = int(self.pos.y + 5 * PIXEL)
        else:
            return

        sprite_llama = random.choice(LLAMA_FRAMES)
        for fy, row in enumerate(sprite_llama):
            for fx, val in enumerate(row):
                color = LLAMA_COLORS.get(val)
                if color:
                    pygame.draw.rect(surface, color, (x + fx * PIXEL, y + fy * PIXEL, PIXEL, PIXEL))

class Game:
    def __init__(self):
        self.scene = Scene()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pyoneer")
        self.clock = pygame.time.Clock()
        self.running = True

        # Configuración física del escenario actual
        self.physics = PhysicsConfig(gravity=(0, 0.05))  # ← puedes cambiar esto según el entorno

        self.player = Player((300, 200), self.physics)
        self.particles = []

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Obtener vector de impulso del jugador
        thrust = self.player.handle_input()
        self.player.vel += thrust

        # Aplicar gravedad
        self.player.vel += self.physics.gravity

        # Aplicar fricción si no hay impulso
        if not self.player.thrusting:
            self.player.vel *= self.player.friction

        # Limitar velocidad máxima
        if self.player.vel.length() > self.player.max_speed:
            self.player.vel.scale_to_length(self.player.max_speed)

        # Calcular posición tentativa
        new_pos = self.player.pos + self.player.vel
        future_rect = pygame.Rect(new_pos.x, new_pos.y, 12 * PIXEL, 10 * PIXEL)

        if not self.scene.check_collision(future_rect):
            self.player.pos = new_pos
        else:
            self.player.vel = pygame.math.Vector2(0, 0)

    def draw(self):
        self.screen.fill((0, 0, 0))             # LIMPIEZA COMPLETA del frame
        self.scene.draw(self.screen, highlight_rect=self.player.get_rect())

        # Traza el área de colisión del jugador
        #pygame.draw.rect(self.screen, (0, 255, 0), self.player.get_rect(), 1)
        for p in self.particles:
            p.draw(self.screen)
        self.player.draw(self.screen)
        if self.player.thrusting:
            self.player.draw_thruster(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
