"""
MetaHorizon Odyssey - Autonomous AI Game Engine & Multi-Tier RPG
Built for Meta Global AI Developer Hackathon 2026.
Track: Push the Frontier (Gaming, Simulation, and Autonomous Game Dev)
Meta Developer Portal:
  Team ID: 1716967459402469
  Project ID: 1042883398799623
  Workspace: https://dev.meta.ai/?team_id=1716967459402469&project_id=1042883398799623
"""

__title__ = "MetaHorizon Odyssey"
__version__ = "2.0.0"
__team_id__ = "1716967459402469"
__project_id__ = "1042883398799623"
__author__ = "Meta Global AI Hackathon Game Developer"

from .engine import GameEngine, launch_game

__all__ = ["GameEngine", "launch_game", "__title__", "__version__", "__team_id__", "__project_id__"]
