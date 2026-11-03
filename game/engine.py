"""
MetaHorizon Odyssey - Master Game Engine & 60 FPS Loop
"""

import sys
import math
import random
import pygame

from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, COLOR_BG, 
    LEVELING_TIERS, COLOR_GOLD, COLOR_CYAN, COLOR_RED, COLOR_NEON_GREEN
)
from game.player import Player
from game.enemies import Enemy
from game.world import World
from game.particles import ParticleManager
from game.ui import GameUI
from game.ai_forge import MetaAIGameForge

class GameEngine:
    def __init__(self, headless=False):
        pygame.init()
        self.headless = headless
        if not headless:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(TITLE)
        else:
            self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        # Systems
        self.player = Player()
        self.world = World()
        self.particles = ParticleManager()
        self.ui = GameUI()
        self.ai_forge = MetaAIGameForge()

        # Game State
        self.state = "PLAYING" # PLAYING, GAME_OVER, VICTORY
        self.current_wave = 1
        self.enemies = []
        self.player_projectiles = []
        self.enemy_projectiles = []
        self.current_boss = None

        self._spawn_wave()

    def _spawn_wave(self):
        tier = self.player.current_tier
        # Check if boss wave (Levels 5, 10, 15, 20)
        if self.player.level in (5, 10, 15, 20) and not self.current_boss:
            tier_info = LEVELING_TIERS.get(tier, LEVELING_TIERS[1])
            bx = random.choice([200, SCREEN_WIDTH - 200])
            by = random.choice([150, SCREEN_HEIGHT - 150])
            self.current_boss = Enemy(bx, by, tier=tier, is_boss=True)
            self.enemies.append(self.current_boss)
            self.particles.add_floating_text(
                SCREEN_WIDTH // 2, 200, 
                f"WARNING: {tier_info['boss_name'].upper()} APPROACHING!", 
                COLOR_RED, self.ui.font_title
            )
            return

        # Standard Wave
        wave_size = 4 + (tier * 3) + (self.current_wave % 3)
        for _ in range(wave_size):
            # Spawn along perimeter
            side = random.randint(0, 3)
            if side == 0:
                ex, ey = random.randint(50, SCREEN_WIDTH - 50), -30
            elif side == 1:
                ex, ey = random.randint(50, SCREEN_WIDTH - 50), SCREEN_HEIGHT + 30
            elif side == 2:
                ex, ey = -30, random.randint(50, SCREEN_HEIGHT - 50)
            else:
                ex, ey = SCREEN_WIDTH + 30, random.randint(50, SCREEN_HEIGHT - 50)

            # Archetype distribution
            r = random.random()
            if r < 0.4:
                arch = "swarmer"
            elif r < 0.75:
                arch = "ranger"
            else:
                arch = "tank"

            self.enemies.append(Enemy(ex, ey, tier=tier, archetype=arch))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos() if not self.headless else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.ui.show_ai_drawer = not self.ui.show_ai_drawer
                elif event.key == pygame.K_ESCAPE:
                    if self.ui.show_ai_drawer:
                        self.ui.show_ai_drawer = False
                    else:
                        self.running = False
                elif event.key == pygame.K_g:
                    # Procedurally forge new level using Meta Muse Code
                    bp = self.ai_forge.forge_procedural_level(self.player.current_tier)
                    self.particles.add_floating_text(
                        SCREEN_WIDTH // 2, 160, 
                        f"FORGED BY MUSE CODE: {bp.tier_name.upper()} WAVE!", 
                        COLOR_GOLD, self.ui.font_title
                    )
                    self._spawn_wave()
                elif event.key == pygame.K_r:
                    if self.state in ("GAME_OVER", "VICTORY"):
                        self.__init__(headless=self.headless)
                elif event.key == pygame.K_q:
                    # Tier 3 Quantum ability: clear projectiles
                    if self.player.current_tier >= 3 and self.player.special_cooldown == 0:
                        self.player.special_cooldown = 180
                        self.enemy_projectiles.clear()
                        self.particles.spawn_burst(self.player.x, self.player.y, (139, 92, 246), count=30, speed=6.0)

            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "PLAYING":
                if event.button == 1: # Left-Click
                    proj = self.player.try_shoot_primary(mouse_pos[0], mouse_pos[1])
                    if proj:
                        self.player_projectiles.append(proj)
                        self.particles.spawn_burst(self.player.x, self.player.y, COLOR_CYAN, count=3, speed=1.5, size=2)
                elif event.button == 3: # Right-Click
                    plasma = self.player.try_shoot_secondary(mouse_pos[0], mouse_pos[1])
                    if plasma:
                        self.player_projectiles.append(plasma)
                        self.particles.spawn_burst(self.player.x, self.player.y, (0, 129, 251), count=8, speed=3.0, size=4)

    def update(self):
        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos() if not self.headless else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        mouse_pressed = pygame.mouse.get_pressed()

        # Update Player
        self.player.handle_input(keys, mouse_pressed, mouse_pos)
        self.player.update()

        # Continuous fire if holding left click
        if mouse_pressed[0] and not self.ui.show_ai_drawer:
            proj = self.player.try_shoot_primary(mouse_pos[0], mouse_pos[1])
            if proj:
                self.player_projectiles.append(proj)

        # Update Projectiles
        for p in self.player_projectiles:
            p.update()
        self.player_projectiles = [p for p in self.player_projectiles if p.alive]

        for ep in self.enemy_projectiles:
            ep.update()
        self.enemy_projectiles = [ep for ep in self.enemy_projectiles if ep.alive]

        # Update Enemies
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y)
            # Enemy Shoot
            bullets = enemy.try_shoot(self.player.x, self.player.y)
            if bullets:
                self.enemy_projectiles.extend(bullets)

            # Enemy Collision with Player
            if math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < (enemy.radius + self.player.radius):
                dmg = self.player.take_damage(enemy.damage * 0.25)
                if dmg > 0:
                    self.particles.add_floating_text(self.player.x, self.player.y - 15, f"-{int(dmg)}", COLOR_RED, self.ui.font_sm)
                    self.particles.spawn_hit(self.player.x, self.player.y, COLOR_RED)

        # Check Player Projectiles vs Enemies
        for proj in self.player_projectiles:
            p_rect = proj.get_rect()
            for enemy in self.enemies:
                if enemy.alive and p_rect.colliderect(enemy.get_rect()):
                    enemy.take_damage(proj.damage)
                    proj.alive = False
                    self.particles.spawn_hit(enemy.x, enemy.y, proj.color)
                    self.particles.add_floating_text(enemy.x, enemy.y - 12, f"{int(proj.damage)}", COLOR_CYAN, self.ui.font_sm)

                    # Enemy defeated
                    if not enemy.alive:
                        self.player.enemies_defeated += 1
                        self.particles.spawn_burst(enemy.x, enemy.y, enemy.color, count=20, speed=4.0)
                        
                        # Loot Drop
                        self.world.spawn_pickup(enemy.x, enemy.y, "xp")
                        if random.random() < 0.35:
                            self.world.spawn_pickup(enemy.x + random.randint(-15, 15), enemy.y, "shard")
                        if random.random() < 0.15:
                            self.world.spawn_pickup(enemy.x, enemy.y + random.randint(-15, 15), "health")

                        # Boss defeated check
                        if enemy.is_boss:
                            self.current_boss = None
                            if self.player.level >= 20:
                                self.state = "VICTORY"
                            else:
                                self.particles.add_floating_text(
                                    SCREEN_WIDTH // 2, 240, 
                                    "BOSS DEFEATED! ADVANCING TIER!", 
                                    COLOR_GOLD, self.ui.font_title
                                )
                    break

        # Check Enemy Projectiles vs Player
        p_rect = self.player.get_rect()
        for ep in self.enemy_projectiles:
            if ep.alive and p_rect.colliderect(ep.get_rect()):
                ep.alive = False
                dmg = self.player.take_damage(ep.damage)
                if dmg > 0:
                    self.particles.spawn_hit(self.player.x, self.player.y, COLOR_RED)
                    self.particles.add_floating_text(self.player.x, self.player.y - 15, f"-{int(dmg)}", COLOR_RED, self.ui.font_sm)

        # Check Pickups
        for pickup in self.world.pickups:
            if pickup.alive and math.hypot(pickup.x - self.player.x, pickup.y - self.player.y) < (pickup.radius + self.player.radius + 15):
                pickup.alive = False
                if pickup.p_type == "xp":
                    leveled = self.player.gain_xp(pickup.value, self.particles)
                    if leveled:
                        self.particles.add_floating_text(self.player.x, self.player.y - 30, f"LEVEL UP! (LVL {self.player.level})", COLOR_GOLD, self.ui.font_title)
                elif pickup.p_type == "health":
                    self.player.hp = min(self.player.max_hp, self.player.hp + pickup.value)
                    self.particles.add_floating_text(self.player.x, self.player.y - 20, f"+{int(pickup.value)} HP", COLOR_NEON_GREEN, self.ui.font_sm)
                elif pickup.p_type == "shard":
                    self.player.meta_shards += pickup.value
                    self.particles.add_floating_text(self.player.x, self.player.y - 20, "+1 META SHARD", COLOR_GOLD, self.ui.font_sm)

        # Cleanup dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        # Spawn new wave if all enemies cleared
        if len(self.enemies) == 0:
            self.current_wave += 1
            self.particles.add_floating_text(SCREEN_WIDTH // 2, 200, f"WAVE {self.current_wave} CLEARED!", COLOR_NEON_GREEN, self.ui.font_title)
            self._spawn_wave()

        # Update World & Particles
        self.world.update()
        self.particles.update()

        # Check Player Death
        if self.player.hp <= 0:
            self.state = "GAME_OVER"

    def draw(self):
        mouse_pos = pygame.mouse.get_pos() if not self.headless else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # 1. World Grid & Obstacles
        self.world.draw(self.screen, tier=self.player.current_tier)

        # 2. Projectiles
        for p in self.player_projectiles:
            p.draw(self.screen)
        for ep in self.enemy_projectiles:
            ep.draw(self.screen)

        # 3. Enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # 4. Player
        self.player.draw(self.screen, mouse_pos)

        # 5. Particles & Damage Numbers
        self.particles.draw(self.screen)

        # 6. In-Game HUD
        self.ui.draw_hud(self.screen, self.player, self.current_wave, len(self.enemies), boss=self.current_boss)

        # 7. Game Over / Victory Screens
        if self.state == "GAME_OVER":
            self.ui.draw_game_over(self.screen)
        elif self.state == "VICTORY":
            self.ui.draw_victory(self.screen)

        if not self.headless:
            pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

def launch_game():
    engine = GameEngine()
    engine.run()

if __name__ == "__main__":
    launch_game()
