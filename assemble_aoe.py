import os
import re
import subprocess
from aoe_css import get_aoe_css
from aoe_html import get_aoe_html
from aoe_audio_textures import get_aoe_audio_textures_js
from aoe_models import get_aoe_models_js
from aoe_units_combat import get_aoe_units_combat_js
from aoe_pathfinding_fsm import get_aoe_pathfinding_fsm_js
from aoe_engine import get_aoe_engine_js
from aoe_sim_loop import get_aoe_sim_loop_js
from aoe_world_director import get_aoe_world_director_js

def build():
    css = get_aoe_css()
    html_body = get_aoe_html()

    js_parts = [
        "import * as THREE from './lib/three.module.min.js';",
        """
    // =========================================================================
    // THREE.JS SETUP, ACES FILMIC TONE MAPPING & ATMOSPHERIC LIGHTING
    // =========================================================================
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0xc2daf0, 0.0028);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 28, 38);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.22;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Atmospheric Sky Dome with Horizon Gradient & Clouds
    const skyGeom = new THREE.SphereGeometry(450, 32, 16);
    const skyCanvas = document.createElement('canvas');
    skyCanvas.width = 512;
    skyCanvas.height = 512;
    const skyCtx = skyCanvas.getContext('2d');
    const skyGrad = skyCtx.createLinearGradient(0, 0, 0, 512);
    skyGrad.addColorStop(0, '#1e40af');    // Deep royal blue zenith
    skyGrad.addColorStop(0.45, '#3b82f6'); // Mid-sky
    skyGrad.addColorStop(0.82, '#93c5fd'); // Atmospheric haze
    skyGrad.addColorStop(1, '#ffedd5');    // Warm golden horizon
    skyCtx.fillStyle = skyGrad;
    skyCtx.fillRect(0, 0, 512, 512);

    // Soft cumulus cloud wisps
    for (let c = 0; c < 30; c++) {
      const cx = Math.random() * 512;
      const cy = 180 + Math.random() * 220;
      const cr = 35 + Math.random() * 65;
      const cloudGrad = skyCtx.createRadialGradient(cx, cy, 4, cx, cy, cr);
      cloudGrad.addColorStop(0, 'rgba(255, 255, 255, 0.42)');
      cloudGrad.addColorStop(0.6, 'rgba(255, 255, 255, 0.18)');
      cloudGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
      skyCtx.fillStyle = cloudGrad;
      skyCtx.beginPath();
      skyCtx.arc(cx, cy, cr, 0, Math.PI * 2);
      skyCtx.fill();
    }

    const skyTex = new THREE.CanvasTexture(skyCanvas);
    const skyMat = new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide });
    const skyDome = new THREE.Mesh(skyGeom, skyMat);
    scene.add(skyDome);

    // Realistic Sun & Atmospheric Bounce Lighting
    const hemiLight = new THREE.HemisphereLight(0xdbeafe, 0x3f3528, 0.85);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfff7ed, 1.95);
    sunLight.position.set(70, 95, 60);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 300;
    sunLight.shadow.camera.left = -115;
    sunLight.shadow.camera.right = 115;
    sunLight.shadow.camera.top = 115;
    sunLight.shadow.camera.bottom = -115;
    sunLight.shadow.bias = -0.0004;
    sunLight.shadow.normalBias = 0.02;
    scene.add(sunLight);

    const ambientLight = new THREE.AmbientLight(0xffeedd, 0.35);
    scene.add(ambientLight);

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
        """,
        get_aoe_audio_textures_js(),
        """
    // Initialize Procedural Textures
    const grassTex = generateGrassTexture();
    const woodTex = generateWoodTexture();
    const stoneTex = generateStoneTexture();
    const thatchTex = generateThatchTexture();
    const tileTex = generateTileTexture();
    const plasterTex = generatePlasterTexture();
    const ironTex = generateIronTexture();
    const waterTex = generateWaterTexture();
    const cliffTex = generateCliffTexture();
        """,
        get_aoe_models_js(),
        get_aoe_units_combat_js(),
        get_aoe_pathfinding_fsm_js(),
        get_aoe_engine_js(),
        get_aoe_sim_loop_js(),
        get_aoe_world_director_js(),
        """
    // =========================================================================
    // INITIALIZATION & RENDER ANIMATION LOOP
    // =========================================================================
    initAoEWorld();

    function animate() {
      requestAnimationFrame(animate);
      updateSimulation();
      renderer.render(scene, camera);
    }
    animate();
        """
    ]

    full_js = "\n".join(js_parts)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AGE OF EMPIRES // OFFICIAL HISTORICAL RTS PROTOTYPE</title>
  <style>
{css}
  </style>
</head>
<body>
{html_body}
  <script type="module">
{full_js}
  </script>
</body>
</html>
"""

    # Check for exact word boundary \bAI\b
    ai_matches = re.findall(r'\bAI\b', full_html)
    print(f"Occurrences of exact word boundary \\bAI\\b: {len(ai_matches)}")
    if ai_matches:
        print("WARNING: Found AI word matches! Must eliminate.")
        for m in re.finditer(r'\bAI\b', full_html):
            start = max(0, m.start() - 30)
            end = min(len(full_html), m.end() + 30)
            print(f"Context: {full_html[start:end]}")

    out_path = os.path.join('game_3d', 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Successfully wrote {out_path} ({len(full_html)} bytes).")

    # Extract and check script with node
    with open('test_aoe_script.js', 'w', encoding='utf-8') as f:
        f.write(full_js)

    res = subprocess.run(['node', '--check', 'test_aoe_script.js'], capture_output=True, text=True)
    print("Node check exit code:", res.returncode)
    if res.returncode != 0:
        print("Node check stderr:\n", res.stderr)
    else:
        print("Node check PASSED with 0 syntax errors!")

    if os.path.exists('test_aoe_script.js'):
        os.remove('test_aoe_script.js')

if __name__ == '__main__':
    build()
