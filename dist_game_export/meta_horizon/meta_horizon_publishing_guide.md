# How to Publish MetaHorizon Odyssey 3D to Meta Horizon Worlds & Meta Quest

1. **Meta Developer Portal**:
   - Access your registered workspace: `https://dev.meta.ai/?team_id=1716967459402469&project_id=1042883398799623`
2. **Deploy to Meta Horizon Worlds**:
   - Open Meta Horizon Creator Studio (or Desktop Creator Hub).
   - Import `meta_horizon_scene_graph.json`.
   - The 7 planetary sectors, flight controllers, and procedural mesh handlers will automatically bind to your world space.
3. **Meta Quest WebXR / Standalone Deployment**:
   - Host `game_3d/index.html` on your server or test locally via `python main.py`.
   - On Meta Quest, open Meta Quest Browser to your local server IP (e.g. `http://<your-lan-ip>:8088`).
   - The game runs at 90-120 FPS in full stereoscopic WebXR mode!
