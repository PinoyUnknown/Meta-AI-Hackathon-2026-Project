"""
MetaHorizon Odyssey - Cyber-Guardian Player Controller & Leveling Progression
"""

import math
import pygame
from game.settings import (
    COLOR_CYAN, COLOR_META_BLUE, COLOR_PURPLE, COLOR_GOLD, 
    COLOR_NEON_GREEN, LEVELING_TIERS, SCREEN_WIDTH, SCREEN_HEIGHT
)
from game.projectiles import Projectile

class Player:
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2):
        self.x = float(x)
        self.y = float(y)
        self.radius = 18
        self.speed = 4.8
        self.base_speed = 4.8

        # Progression & Stats
        self.level = 1
        self.current_tier = 1
        self.xp = 0
        self.xp_to_next = 100
        self.stat_points = 0
        
        self.max_hp = 100.0
        self.hp = 100.0
        self.max_shield = 50.0
        self.shield = 50.0
        self.shield_regen_delay = 0

        self.attack_power = 25.0
        self.defense = 5.0

        # Movement physics
        self.vx = 0.0
        self.vy = 0.0

        # Dashing
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_speed = 14.0

        # Combat Cooldowns
        self.shoot_cooldown = 0
        self.plasma_cooldown = 0
        self.special_cooldown = 0

        # Score & Shards
        self.meta_shards = 0
        self.enemies_defeated = 0

    def get_tier_info(self):
        return LEVELING_TIERS.get(self.current_tier, LEVELING_TIERS[1])

    def gain_xp(self, amount, particle_mgr=None):
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.35)
            self._on_level_up()
            leveled_up = True
            if particle_mgr:
                particle_mgr.spawn_level_up(self.x, self.y)
        return leveled_up

    def _on_level_up(self):
        # Promote Tier
        if self.level >= 16:
            self.current_tier = 4
        elif self.level >= 11:
            self.current_tier = 3
        elif self.level >= 6:
            self.current_tier = 2
        else:
            self.current_tier = 1

        # Stat boosts
        self.max_hp += 15.0
        self.hp = self.max_hp
        self.max_shield += 10.0
        self.shield = self.max_shield
        self.attack_power += 6.0
        self.base_speed = min(7.5, self.base_speed + 0.15)
        self.speed = self.base_speed

    def take_damage(self, amount):
        if self.is_dashing:
            return 0  # Invulnerable during dash

        actual_damage = max(1.0, amount - (self.defense * 0.3))
        # Absorb with shield first
        if self.shield > 0:
            if self.shield >= actual_damage:
                self.shield -= actual_damage
                absorbed = actual_damage
            else:
                remaining = actual_damage - self.shield
                absorbed = self.shield
                self.shield = 0
                self.hp -= remaining
        else:
            self.hp -= actual_damage
            absorbed = actual_damage

        self.shield_regen_delay = 120 # 2 seconds
        self.hp = max(0.0, self.hp)
        return actual_damage

    def handle_input(self, keys, mouse_pressed, mouse_pos):
        # Movement vector
        move_x = 0
        move_y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1

        # Normalize
        dist = math.hypot(move_x, move_y)
        if dist > 0:
            move_x /= dist
            move_y /= dist

        # Dash
        if (keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]) and self.dash_cooldown == 0 and dist > 0:
            self.is_dashing = True
            self.dash_timer = 12
            self.dash_cooldown = 60
            self.vx = move_x * self.dash_speed
            self.vy = move_y * self.dash_speed
        elif not self.is_dashing:
            self.vx = move_x * self.speed
            self.vy = move_y * self.speed

    def update(self, bounds=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
        # Dash decay
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # Shield regen
        if self.shield_regen_delay > 0:
            self.shield_regen_delay -= 1
        elif self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + 0.25)

        # Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.plasma_cooldown > 0:
            self.plasma_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Screen boundaries
        min_x, min_y, max_x, max_y = bounds
        self.x = max(min_x + self.radius, min(max_x - self.radius, self.x))
        self.y = max(min_y + self.radius, min(max_y - self.radius, self.y))

    def try_shoot_primary(self, target_x, target_y):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 12
            return Projectile(self.x, self.y, target_x, target_y, speed=12.0, damage=self.attack_power, is_player=True, p_type="blaster")
        return None

    def try_shoot_secondary(self, target_x, target_y):
        if self.current_tier >= 2 and self.plasma_cooldown == 0:
            self.plasma_cooldown = 40
            return Projectile(self.x, self.y, target_x, target_y, speed=9.0, damage=self.attack_power * 2.2, is_player=True, p_type="plasma")
        return None

    def draw(self, surface, mouse_pos):
        pos = (int(self.x), int(self.y))
        tier_color = self.get_tier_info()["theme_color"]

        # Aim rotation angle towards mouse
        angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)

        # Draw Shield Aura if active
        if self.shield > 0:
            shield_radius = int(self.radius + 6)
            pygame.draw.circle(surface, COLOR_META_BLUE, pos, shield_radius, 2)

        # Draw Dash Ghost / Trail
        if self.is_dashing:
            pygame.draw.circle(surface, (255, 255, 255), pos, int(self.radius + 4), 1)

        # Player Base Body (Cyber-Guardian Hex/Circle)
        pygame.draw.circle(surface, (15, 23, 42), pos, self.radius)
        pygame.draw.circle(surface, tier_color, pos, self.radius, 3)

        # Player Visor / Directional Pointer
        barrel_x = self.x + math.cos(angle) * (self.radius + 6)
        barrel_y = self.y + math.sin(angle) * (self.radius + 6)
        pygame.draw.line(surface, COLOR_CYAN, pos, (int(barrel_x), int(barrel_y)), 4)
        pygame.draw.circle(surface, (255, 255, 255), (int(barrel_x), int(barrel_y)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
