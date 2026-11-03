"""
MetaHorizon Odyssey - Procedural World Environment & Collectibles
"""

import math
import random
import pygame
from game.settings import (
    COLOR_GRID, COLOR_BG, COLOR_CYAN, COLOR_META_BLUE, 
    COLOR_NEON_GREEN, COLOR_GOLD, LEVELING_TIERS, SCREEN_WIDTH, SCREEN_HEIGHT
)

class Pickup:
    def __init__(self, x, y, p_type="xp"):
        self.x = float(x)
        self.y = float(y)
        self.p_type = p_type  # xp, health, shield, shard
        self.alive = True
        self.radius = 6
        self.pulse = 0.0

        if p_type == "health":
            self.color = COLOR_NEON_GREEN
            self.value = 35.0
        elif p_type == "shield":
            self.color = COLOR_META_BLUE
            self.value = 25.0
        elif p_type == "shard":
            self.color = COLOR_GOLD
            self.value = 1
        else: # xp
            self.color = COLOR_CYAN
            self.value = 25

    def update(self):
        self.pulse += 0.1

    def draw(self, surface):
        r = int(self.radius + math.sin(self.pulse) * 1.5)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), max(1, r - 3))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class World:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.obstacles = []
        self.pickups = []
        self._generate_layout()

    def _generate_layout(self):
        self.obstacles = []
        # Generate symmetrical cybernetic pillars
        pillar_coords = [
            (320, 200), (960, 200),
            (320, 520), (960, 520),
            (640, 360)
        ]
        for cx, cy in pillar_coords:
            self.obstacles.append(pygame.Rect(cx - 30, cy - 30, 60, 60))

    def spawn_pickup(self, x, y, p_type="xp"):
        self.pickups.append(Pickup(x, y, p_type))

    def update(self):
        for p in self.pickups:
            p.update()
        self.pickups = [p for p in self.pickups if p.alive]

    def draw(self, surface, tier=1):
        tier_info = LEVELING_TIERS.get(tier, LEVELING_TIERS[1])
        accent = tier_info["bg_accent"]

        # Background Fill
        surface.fill(COLOR_BG)

        # Procedural Grid Lines
        grid_step = 64
        for x in range(0, self.width, grid_step):
            pygame.draw.line(surface, accent, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, grid_step):
            pygame.draw.line(surface, accent, (0, y), (self.width, y), 1)

        # Draw Obstacles (Cyber Pillars)
        for obs in self.obstacles:
            pygame.draw.rect(surface, (15, 23, 42), obs)
            pygame.draw.rect(surface, tier_info["theme_color"], obs, 2)
            # Center diamond
            pygame.draw.circle(surface, tier_info["theme_color"], obs.center, 8, 1)

        # Draw Pickups
        for p in self.pickups:
            p.draw(surface)
