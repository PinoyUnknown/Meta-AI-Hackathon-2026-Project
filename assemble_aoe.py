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
    // THREE.JS SETUP & LIGHTING
    // =========================================================================
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87ceeb);
    scene.fog = new THREE.FogExp2(0xb0d8f0, 0.0022);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 28, 38);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Sun & Atmosphere Lights
    const hemiLight = new THREE.HemisphereLight(0xfff7e6, 0x556b2f, 0.65);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfffaed, 1.45);
    sunLight.position.set(60, 90, 50);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 280;
    sunLight.shadow.camera.left = -120;
    sunLight.shadow.camera.right = 120;
    sunLight.shadow.camera.top = 120;
    sunLight.shadow.camera.bottom = -120;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    const ambientLight = new THREE.AmbientLight(0xffeedd, 0.45);
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
