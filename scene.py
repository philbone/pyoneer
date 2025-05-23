import random
import pygame

TILE_SIZE = 50  # tamaño de cada bloque

BLOCK_TYPES = {
    '#': {
        "base_color": (70, 50, 30),
        "detail_colors": [(90, 70, 50), (100, 80, 60), (110, 85, 65)],
        "detail_amount": 3
    },
    '@': {
        "base_color": (120, 90, 60),
        "detail_colors": [(140, 110, 80), (160, 130, 100)],
        "detail_amount": 2
    }
}

class Scene:
    def __init__(self):
        # Mapa simple: '#' = pared, '.' = espacio libre
        self.map_data = [
            "#############################",
            "#...........................#",
            "#...........................#",
            "#..######..@@@@@@...........#",
            "#...#..........@@@@@@@......#",
            "#...#.......................#",
            "#...#....###................#",
            "#...#......@................#",
            "#...#......@@@@@@@@@@@......#",
            "#...........................#",
            "#...........................#",
            "#############################"
        ]

        self.tiles = []
        self.tile_textures = []
        self.tile_types = []

        for y, row in enumerate(self.map_data):
            for x, char in enumerate(row):
                if char in BLOCK_TYPES:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tiles.append(rect)
                    self.tile_types.append(char)

                    style = BLOCK_TYPES[char]
                    detalles = []
                    for _ in range(style["detail_amount"]):
                        offset_x = random.randint(4, TILE_SIZE - 8)
                        offset_y = random.randint(4, TILE_SIZE - 8)
                        tamaño = random.randint(2, 4)
                        color = random.choice(style["detail_colors"])
                        detalles.append((offset_x, offset_y, tamaño, color))
                    self.tile_textures.append(detalles)

    def draw(self, surface, highlight_rect=None):
        for i, tile in enumerate(self.tiles):
            block_type = self.tile_types[i]
            style = BLOCK_TYPES[block_type]
            base_color = style["base_color"]

            if highlight_rect and tile.colliderect(highlight_rect):
                pygame.draw.rect(surface, (255, 0, 0), tile)
            else:
                pygame.draw.rect(surface, base_color, tile)

                for offset_x, offset_y, size, color in self.tile_textures[i]:
                    pygame.draw.rect(
                        surface,
                        color,
                        (tile.x + offset_x, tile.y + offset_y, size, size)
                    )

    def check_collision(self, rect):
        for tile in self.tiles:
            if rect.colliderect(tile):
                return True
        return False
