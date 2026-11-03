"""
MetaHorizon Odyssey - In-Game HUD, Level-Up Card System & Game Dev Drawer
"""

import pygame
from game.settings import (
    COLOR_BG, COLOR_TEXT, COLOR_TEXT_DIM, COLOR_META_BLUE, 
    COLOR_CYAN, COLOR_NEON_GREEN, COLOR_PURPLE, COLOR_AMBER, 
    COLOR_RED, COLOR_GOLD, LEVELING_TIERS, SCREEN_WIDTH, SCREEN_HEIGHT
)

class GameUI:
    def __init__(self):
        pygame.font.init()
        # Initialize standard fonts
        self.font_title = pygame.font.SysFont("Consolas", 24, bold=True)
        self.font_main = pygame.font.SysFont("Consolas", 15, bold=True)
        self.font_sm = pygame.font.SysFont("Consolas", 12)
        self.font_badge = pygame.font.SysFont("Consolas", 13, bold=True)

        self.show_ai_drawer = False
        self.ai_drawer_tab = 0 # 0=Muse Code, 1=SAM 3.1, 2=Quest Lore

    def draw_hud(self, surface, player, current_wave, enemy_count, boss=None):
        tier_info = player.get_tier_info()
        theme_col = tier_info["theme_color"]

        # 1. Top-Left Player Status Bar
        hud_box = pygame.Rect(16, 16, 320, 100)
        pygame.draw.rect(surface, (15, 23, 42), hud_box, border_radius=8)
        pygame.draw.rect(surface, (30, 41, 59), hud_box, 1, border_radius=8)

        # Player Level & Tier Badge
        tier_text = f"TIER {player.current_tier}: {tier_info['name'].upper()}"
        lbl_tier = self.font_badge.render(tier_text, True, theme_col)
        surface.blit(lbl_tier, (28, 24))

        lvl_text = f"LVL {player.level}"
        lbl_lvl = self.font_title.render(lvl_text, True, COLOR_TEXT)
        surface.blit(lbl_lvl, (250, 20))

        # Health Bar
        bar_w = 200
        hp_pct = max(0.0, min(1.0, player.hp / player.max_hp))
        pygame.draw.rect(surface, (30, 41, 59), (28, 52, bar_w, 10), border_radius=4)
        pygame.draw.rect(surface, COLOR_NEON_GREEN if hp_pct > 0.3 else COLOR_RED, (28, 52, int(bar_w * hp_pct), 10), border_radius=4)
        lbl_hp = self.font_sm.render(f"HP: {int(player.hp)}/{int(player.max_hp)}", True, COLOR_TEXT)
        surface.blit(lbl_hp, (235, 50))

        # Shield Bar
        shield_pct = max(0.0, min(1.0, player.shield / player.max_shield))
        pygame.draw.rect(surface, (30, 41, 59), (28, 68, bar_w, 8), border_radius=4)
        pygame.draw.rect(surface, COLOR_CYAN, (28, 68, int(bar_w * shield_pct), 8), border_radius=4)
        lbl_shield = self.font_sm.render(f"SHIELD: {int(player.shield)}/{int(player.max_shield)}", True, COLOR_TEXT_DIM)
        surface.blit(lbl_shield, (235, 66))

        # XP Bar (Bottom of HUD)
        xp_pct = max(0.0, min(1.0, player.xp / player.xp_to_next))
        pygame.draw.rect(surface, (30, 41, 59), (28, 86, 280, 6), border_radius=3)
        pygame.draw.rect(surface, COLOR_GOLD, (28, 86, int(280 * xp_pct), 6), border_radius=3)

        # 2. Top-Center Wave & Meta Shards Info
        info_box = pygame.Rect(SCREEN_WIDTH // 2 - 140, 16, 280, 50)
        pygame.draw.rect(surface, (15, 23, 42), info_box, border_radius=8)
        pygame.draw.rect(surface, (30, 41, 59), info_box, 1, border_radius=8)

        shards_text = f"◆ SHARDS: {player.meta_shards}  |  ENEMIES: {enemy_count}"
        lbl_shards = self.font_main.render(shards_text, True, COLOR_GOLD)
        surface.blit(lbl_shards, (info_box.x + 20, info_box.y + 16))

        # 3. Top-Right Meta AI Studio Button Prompt
        btn_box = pygame.Rect(SCREEN_WIDTH - 240, 16, 224, 40)
        pygame.draw.rect(surface, (30, 27, 75) if self.show_ai_drawer else (15, 23, 42), btn_box, border_radius=8)
        pygame.draw.rect(surface, COLOR_PURPLE, btn_box, 1, border_radius=8)
        btn_text = "[TAB] META AI STUDIO"
        lbl_btn = self.font_badge.render(btn_text, True, COLOR_PURPLE)
        surface.blit(lbl_btn, (btn_box.x + 24, btn_box.y + 12))

        # 4. Boss Health Bar (if active)
        if boss and boss.alive:
            boss_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 60, 500, 36)
            pygame.draw.rect(surface, (15, 23, 42), boss_box, border_radius=6)
            pygame.draw.rect(surface, COLOR_RED, boss_box, 1, border_radius=6)

            boss_pct = max(0.0, min(1.0, boss.hp / boss.max_hp))
            pygame.draw.rect(surface, (239, 68, 68), (boss_box.x + 6, boss_box.y + 18, int(488 * boss_pct), 12), border_radius=4)

            lbl_boss = self.font_badge.render(f"BOSS: {boss.archetype.upper()} ({int(boss.hp)}/{int(boss.max_hp)})", True, COLOR_GOLD)
            surface.blit(lbl_boss, (boss_box.x + 12, boss_box.y + 3))

        # 5. Draw AI Drawer if toggled
        if self.show_ai_drawer:
            self._draw_ai_drawer(surface, player)

    def _draw_ai_drawer(self, surface, player):
        drawer = pygame.Rect(SCREEN_WIDTH - 420, 70, 400, 480)
        pygame.draw.rect(surface, (11, 15, 23), drawer, border_radius=10)
        pygame.draw.rect(surface, COLOR_PURPLE, drawer, 2, border_radius=10)

        # Drawer Title
        title_surf = self.font_main.render("META AI GAME DEV STUDIO", True, COLOR_CYAN)
        surface.blit(title_surf, (drawer.x + 20, drawer.y + 16))

        sub_surf = self.font_sm.render("Autonomous In-Game Level & Asset Forge", True, COLOR_TEXT_DIM)
        surface.blit(sub_surf, (drawer.x + 20, drawer.y + 40))

        # Content Cards
        card1 = pygame.Rect(drawer.x + 16, drawer.y + 70, 368, 110)
        pygame.draw.rect(surface, (15, 23, 42), card1, border_radius=6)
        c1_t = self.font_badge.render("1. Meta Muse Code Engine (v1.4)", True, COLOR_PURPLE)
        surface.blit(c1_t, (card1.x + 12, card1.y + 10))
        c1_desc = self.font_sm.render(f"Generating Tier {player.current_tier} wave curves & loot tables.", True, COLOR_TEXT_DIM)
        surface.blit(c1_desc, (card1.x + 12, card1.y + 32))
        c1_stat = self.font_sm.render("CLI Status: CONNECTED (muse.cmd)", True, COLOR_NEON_GREEN)
        surface.blit(c1_stat, (card1.x + 12, card1.y + 54))
        c1_key = self.font_sm.render("Press [G] to re-roll procedural level with Muse Code", True, COLOR_GOLD)
        surface.blit(c1_key, (card1.x + 12, card1.y + 76))

        card2 = pygame.Rect(drawer.x + 16, drawer.y + 195, 368, 100)
        pygame.draw.rect(surface, (15, 23, 42), card2, border_radius=6)
        c2_t = self.font_badge.render("2. Meta SAM 3.1 Sprite Collider", True, COLOR_CYAN)
        surface.blit(c2_t, (card2.x + 12, card2.y + 10))
        c2_desc = self.font_sm.render("Zero-shot polygon hitboxes extracted for enemies.", True, COLOR_TEXT_DIM)
        surface.blit(c2_desc, (card2.x + 12, card2.y + 32))
        c2_stat = self.font_sm.render("Collision Precision: 98.8% IoU (Watertight)", True, COLOR_NEON_GREEN)
        surface.blit(c2_stat, (card2.x + 12, card2.y + 54))

        card3 = pygame.Rect(drawer.x + 16, drawer.y + 310, 368, 100)
        pygame.draw.rect(surface, (15, 23, 42), card3, border_radius=6)
        c3_t = self.font_badge.render("3. Meta Llama 3.2 Vision / Lore", True, COLOR_META_BLUE)
        surface.blit(c3_t, (card3.x + 12, card3.y + 10))
        c3_desc = self.font_sm.render(f"Current Quest: {player.get_tier_info()['description'][:40]}...", True, COLOR_TEXT_DIM)
        surface.blit(c3_desc, (card3.x + 12, card3.y + 32))
        c3_stat = self.font_sm.render(f"Unlocked Ability: {player.get_tier_info()['unlocked_ability']}", True, COLOR_GOLD)
        surface.blit(c3_stat, (card3.x + 12, card3.y + 54))

        close_hint = self.font_sm.render("Press [TAB] or [ESC] to close drawer", True, COLOR_TEXT_DIM)
        surface.blit(close_hint, (drawer.x + 80, drawer.y + 440))

    def draw_game_over(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((11, 15, 23, 210))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("SYSTEM CRITICAL: GUARDIAN DEFEATED", True, COLOR_RED)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        sub = self.font_main.render("Press [R] to Respawn  |  Press [ESC] for Menu", True, COLOR_TEXT)
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    def draw_victory(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((11, 15, 23, 220))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("VICTORY! OMNI-FORGE SUPERINTELLIGENCE RESTORED!", True, COLOR_GOLD)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        sub = self.font_main.render("You completed all 4 Leveling Tiers! Horizon is saved.", True, COLOR_NEON_GREEN)
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2))

        restart = self.font_sm.render("Press [R] to Play Endless Mode  |  Press [ESC] for Menu", True, COLOR_TEXT)
        surface.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 45))
