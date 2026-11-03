"""
MetaHorizon Odyssey - Global Game Settings & Leveling Tier Definitions
"""

import pygame

# Window & Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "MetaHorizon Odyssey: Frontier Voyager"

# Cybernetic Theme Colors
COLOR_BG = (11, 15, 23)
COLOR_GRID = (25, 34, 52)
COLOR_TEXT = (248, 250, 252)
COLOR_TEXT_DIM = (148, 163, 184)
COLOR_META_BLUE = (0, 129, 251)
COLOR_CYAN = (0, 240, 255)
COLOR_NEON_GREEN = (16, 185, 129)
COLOR_PURPLE = (139, 92, 246)
COLOR_AMBER = (245, 158, 11)
COLOR_RED = (239, 68, 68)
COLOR_GOLD = (251, 191, 36)

# The 4 Leveling Tiers
LEVELING_TIERS = {
    1: {
        "tier_id": 1,
        "name": "Novice Citadel",
        "level_range": (1, 5),
        "theme_color": COLOR_CYAN,
        "bg_accent": (15, 30, 45),
        "description": "Virtual neon training ground. Master kinetic dash and energy blasters.",
        "enemies": ["Glitch Mite", "Rogue Scout Drone"],
        "boss_name": "Citadel Core Sentry",
        "boss_level": 5,
        "unlocked_ability": "Phase Dash (SPACE)"
    },
    2: {
        "tier_id": 2,
        "name": "Cyber-Grid Outpost",
        "level_range": (6, 10),
        "theme_color": COLOR_META_BLUE,
        "bg_accent": (10, 25, 55),
        "description": "Heavy industrial grid with automated defense turrets and mecha guards.",
        "enemies": ["EMP Stalker", "Armored Enforcer", "Laser Turret"],
        "boss_name": "The Grid Sentinel",
        "boss_level": 10,
        "unlocked_ability": "Plasma Wave Cannon (Right-Click)"
    },
    3: {
        "tier_id": 3,
        "name": "Horizon Frontier",
        "level_range": (11, 15),
        "theme_color": COLOR_PURPLE,
        "bg_accent": (35, 15, 55),
        "description": "Zero-gravity nebula sector with phase-shifting quantum anomalies.",
        "enemies": ["Phase Shifter", "Quantum Worm", "Void Phantom"],
        "boss_name": "Horizon Overlord",
        "boss_level": 15,
        "unlocked_ability": "Quantum Time Dilation (Q)"
    },
    4: {
        "tier_id": 4,
        "name": "Superintelligence Core",
        "level_range": (16, 20),
        "theme_color": COLOR_GOLD,
        "bg_accent": (45, 35, 15),
        "description": "The reality-bending nexus of the Meta Horizon multiverse.",
        "enemies": ["Apex Synthetic", "Invariant Guardian", "Neural Wyrm"],
        "boss_name": "Nexus-Prime: The Rogue Superintelligence",
        "boss_level": 20,
        "unlocked_ability": "Omni-Forge Overdrive (F)"
    }
}

# Meta Hackathon Metadata
META_TEAM_ID = "1716967459402469"
META_PROJECT_ID = "1042883398799623"
META_PORTAL_URL = f"https://dev.meta.ai/?team_id={META_TEAM_ID}&project_id={META_PROJECT_ID}"
