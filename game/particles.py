"""
MetaHorizon Odyssey - Particle Effects & Floating Text Engine
"""

import math
import random
import pygame

class Particle:
    def __init__(self, x, y, color, size=4, speed=2.0, angle=None, life=30):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.size = size
        self.initial_life = life
        self.life = life
        
        if angle is None:
            angle = random.uniform(0, math.tau)
        self.vx = math.cos(angle) * speed * random.uniform(0.6, 1.4)
        self.vy = math.sin(angle) * speed * random.uniform(0.6, 1.4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size * 0.95)

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, min(255, int(255 * (self.life / self.initial_life))))
            # Draw glowing circle
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class FloatingText:
    def __init__(self, x, y, text, color, font, duration=45):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color
        self.font = font
        self.duration = duration
        self.life = duration
        self.vy = -1.2

    def update(self):
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            surf = self.font.render(self.text, True, self.color)
            surface.blit(surf, (int(self.x - surf.get_width() / 2), int(self.y)))

class ParticleManager:
    def __init__(self):
        self.particles = []
        self.floating_texts = []

    def spawn_burst(self, x, y, color, count=16, speed=3.5, size=4):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, size=size, speed=speed, life=random.randint(20, 40)))

    def spawn_hit(self, x, y, color=(0, 240, 255)):
        self.spawn_burst(x, y, color, count=8, speed=2.5, size=3)

    def spawn_level_up(self, x, y):
        # Spectacular gold/cyan expansion ring
        for i in range(36):
            angle = (i / 36) * math.tau
            self.particles.append(Particle(x, y, (251, 191, 36), size=6, speed=4.5, angle=angle, life=45))
            self.particles.append(Particle(x, y, (0, 240, 255), size=4, speed=3.0, angle=angle, life=35))

    def add_floating_text(self, x, y, text, color, font):
        self.floating_texts.append(FloatingText(x, y, text, color, font))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        for ft in self.floating_texts:
            ft.update()
        self.floating_texts = [ft for ft in self.floating_texts if ft.life > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
        for ft in self.floating_texts:
            ft.draw(surface)
