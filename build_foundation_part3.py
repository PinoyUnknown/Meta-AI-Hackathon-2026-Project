# build_foundation_part3.py - Three.js Imports & Procedural Medieval Textures
part3 = r'''
  <script type="module">
    import * as THREE from './lib/three.module.min.js';

    // =========================================================================
    // PROCEDURAL TEXTURE GENERATION (OFFLINE PAINTERLY MEDIEVAL REALISM)
    // =========================================================================
    function createProceduralCanvas(width, height) {
      const c = document.createElement('canvas');
      c.width = width;
      c.height = height;
      return c;
    }

    // Lush Emerald Meadow with Clover & Wildflowers
    function generateGrassTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#568239';
      ctx.fillRect(0, 0, 512, 512);

      // Grass blade noise
      for (let i = 0; i < 1200; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        ctx.strokeStyle = Math.random() > 0.5 ? '#679b44' : '#456a2c';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 6, y - 4 - Math.random() * 6);
        ctx.stroke();
      }

      // Wildflowers (Buttercups & Daisies)
      for (let i = 0; i < 90; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        ctx.fillStyle = Math.random() > 0.4 ? '#fef08a' : '#ffffff';
        ctx.beginPath();
        ctx.arc(x, y, 2 + Math.random() * 2, 0, Math.PI * 2);
        ctx.fill();
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(16, 16);
      return tex;
    }

    // Cobblestone Paving for Roads & Foundations
    function generateCobbleTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#6b6357';
      ctx.fillRect(0, 0, 512, 512);

      const step = 32;
      for (let x = 0; x < 512; x += step) {
        for (let y = 0; y < 512; y += step) {
          ctx.fillStyle = (x + y) % 64 === 0 ? '#8a8070' : '#7a7061';
          ctx.beginPath();
          ctx.roundRect(x + 2, y + 2, step - 4, step - 4, 6);
          ctx.fill();
        }
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // Aged Oak Wood Beam Grain
    function generateWoodTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#6e4722';
      ctx.fillRect(0, 0, 512, 512);

      for (let y = 0; y < 512; y += 48) {
        ctx.strokeStyle = '#422810';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(512, y);
        ctx.stroke();

        ctx.strokeStyle = '#85562a';
        ctx.lineWidth = 1;
        for (let j = 0; j < 6; j++) {
          ctx.beginPath();
          ctx.moveTo(0, y + j * 8);
          ctx.lineTo(512, y + j * 8 + Math.sin(j) * 4);
          ctx.stroke();
        }
      }
      return new THREE.CanvasTexture(c);
    }

    // Golden Straw Thatch Roof
    function generateThatchTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#bfa052';
      ctx.fillRect(0, 0, 512, 512);

      for (let y = 0; y < 512; y += 24) {
        for (let x = 0; x < 512; x += 12) {
          ctx.strokeStyle = Math.random() > 0.5 ? '#d9b764' : '#9e8139';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x + (Math.random() - 0.5) * 4, y + 22);
          ctx.stroke();
        }
      }
      return new THREE.CanvasTexture(c);
    }

    // Terracotta Clay Tiles
    function generateClayTileTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#a84e31';
      ctx.fillRect(0, 0, 512, 512);

      for (let y = 0; y < 512; y += 28) {
        const offset = (y / 28) % 2 === 0 ? 0 : 16;
        for (let x = -16; x < 528; x += 32) {
          ctx.fillStyle = '#ba5736';
          ctx.beginPath();
          ctx.arc(x + offset + 16, y + 14, 14, 0, Math.PI);
          ctx.fill();
          ctx.strokeStyle = '#7c3520';
          ctx.lineWidth = 2;
          ctx.stroke();
        }
      }
      return new THREE.CanvasTexture(c);
    }

    // Striped Medieval Market Stall Canopy
    function generateCanopyTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(0, 0, 256, 256);

      ctx.fillStyle = '#b91c1c'; // Crimson red stripes
      for (let x = 0; x < 256; x += 64) {
        ctx.fillRect(x, 0, 32, 256);
      }
      return new THREE.CanvasTexture(c);
    }

    // Water Surface with Gentle Wave Ripples
    function generateWaterTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      const g = ctx.createLinearGradient(0, 0, 512, 512);
      g.addColorStop(0, '#0284c7');
      g.addColorStop(0.5, '#38bdf8');
      g.addColorStop(1, '#0369a1');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, 512, 512);

      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 2;
      for (let i = 0; i < 40; i++) {
        const y = Math.random() * 512;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.bezierCurveTo(150, y + 20, 350, y - 20, 512, y);
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(8, 8);
      return tex;
    }
'''

with open("foundation_part3.py", "w", encoding="utf-8") as f:
    f.write('part3 = r"""' + part3 + '"""\n')
print("Wrote foundation_part3.py")
