"""
MetaHorizon Odyssey - Projectile Physics & Bullet Trajectory System
"""

import math
import pygame
from game.settings import COLOR_CYAN, COLOR_META_BLUE, COLOR_PURPLE, COLOR_RED, COLOR_GOLD

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=10.0, damage=25.0, is_player=True, p_type="blaster"):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.damage = damage
        self.is_player = is_player
        self.p_type = p_type
        self.alive = True
        self.radius = 4

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1.0
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

        if p_type == "plasma":
            self.radius = 8
            self.color = COLOR_META_BLUE
        elif p_type == "quantum":
            self.radius = 12
            self.color = COLOR_PURPLE
        elif is_player:
            self.color = COLOR_CYAN
        else:
            self.color = COLOR_RED
            self.radius = 5

        self.max_distance = 900
        self.traveled = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.traveled += self.speed
        if self.traveled >= self.max_distance:
            self.alive = False

    def draw(self, surface):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, self.color, pos, self.radius)
        # Inner white energy core
        pygame.draw.circle(surface, (255, 255, 255), pos, max(1, self.radius - 2))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
