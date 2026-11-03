"""
MetaHorizon Odyssey - Autonomous Enemy AI & Boss Hierarchy
"""

import math
import random
import pygame
from game.settings import (
    COLOR_RED, COLOR_AMBER, COLOR_PURPLE, COLOR_GOLD, 
    COLOR_CYAN, SCREEN_WIDTH, SCREEN_HEIGHT
)
from game.projectiles import Projectile

class Enemy:
    def __init__(self, x, y, tier=1, archetype="grunt", is_boss=False):
        self.x = float(x)
        self.y = float(y)
        self.tier = tier
        self.archetype = archetype
        self.is_boss = is_boss
        self.alive = True

        # Base Stats scaled by Tier
        multiplier = 1.0 + (tier - 1) * 0.75
        if is_boss:
            self.radius = 34
            self.max_hp = 350.0 * multiplier
            self.hp = self.max_hp
            self.speed = 2.0
            self.damage = 22.0 * multiplier
            self.xp_value = 250 * tier
            self.color = COLOR_GOLD if tier == 4 else COLOR_RED
            self.shoot_cooldown_max = 45
        elif archetype == "swarmer":
            self.radius = 12
            self.max_hp = 30.0 * multiplier
            self.hp = self.max_hp
            self.speed = 3.6
            self.damage = 10.0 * multiplier
            self.xp_value = 20 * tier
            self.color = COLOR_AMBER
            self.shoot_cooldown_max = 0
        elif archetype == "ranger":
            self.radius = 16
            self.max_hp = 45.0 * multiplier
            self.hp = self.max_hp
            self.speed = 2.2
            self.damage = 15.0 * multiplier
            self.xp_value = 35 * tier
            self.color = COLOR_PURPLE
            self.shoot_cooldown_max = 75
        else: # Standard Tank / Grunt
            self.radius = 20
            self.max_hp = 70.0 * multiplier
            self.hp = self.max_hp
            self.speed = 2.5
            self.damage = 18.0 * multiplier
            self.xp_value = 40 * tier
            self.color = COLOR_RED
            self.shoot_cooldown_max = 90

        self.shoot_cooldown = random.randint(20, self.shoot_cooldown_max) if self.shoot_cooldown_max > 0 else 0

    def update(self, player_x, player_y):
        # Tracking Vector toward player
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            if self.archetype == "ranger" and dist < 250:
                # Keep distance and strafe
                self.x -= (dx / dist) * (self.speed * 0.8)
                self.y -= (dy / dist) * (self.speed * 0.8)
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def try_shoot(self, player_x, player_y):
        if self.shoot_cooldown_max > 0 and self.shoot_cooldown == 0:
            self.shoot_cooldown = self.shoot_cooldown_max
            # Boss multi-shot
            if self.is_boss:
                bullets = []
                base_angle = math.atan2(player_y - self.y, player_x - self.x)
                for offset in (-0.25, 0.0, 0.25):
                    ang = base_angle + offset
                    tx = self.x + math.cos(ang) * 100
                    ty = self.y + math.sin(ang) * 100
                    bullets.append(Projectile(self.x, self.y, tx, ty, speed=7.5, damage=self.damage, is_player=False))
                return bullets
            else:
                return [Projectile(self.x, self.y, player_x, player_y, speed=7.0, damage=self.damage, is_player=False)]
        return None

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def draw(self, surface):
        pos = (int(self.x), int(self.y))
        
        # Enemy Body
        pygame.draw.circle(surface, (20, 10, 25), pos, self.radius)
        pygame.draw.circle(surface, self.color, pos, self.radius, 2)

        # Core Eye / Target Indicator
        eye_radius = max(2, self.radius // 3)
        pygame.draw.circle(surface, self.color, pos, eye_radius)

        # Health bar (if damaged)
        if self.hp < self.max_hp:
            bar_w = self.radius * 2
            bar_h = 4
            bx = self.x - self.radius
            by = self.y - self.radius - 8
            health_pct = max(0.0, min(1.0, self.hp / self.max_hp))
            pygame.draw.rect(surface, (30, 41, 59), (bx, by, bar_w, bar_h))
            pygame.draw.rect(surface, (239, 68, 68), (bx, by, bar_w * health_pct, bar_h))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
