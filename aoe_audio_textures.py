def get_aoe_audio_textures_js():
    return """
    // =========================================================================
    // PROCEDURAL TEXTURE GENERATION (REALISTIC AGE OF EMPIRES VISUALS)
    // =========================================================================
    function createProceduralCanvas(width, height) {
      const c = document.createElement('canvas');
      c.width = width;
      c.height = height;
      return c;
    }

    // 1. Natural Lush Meadow Grass with Dirt Blending
    function generateGrassTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      // Base meadow gradient with organic hue shifts
      const grad = ctx.createLinearGradient(0, 0, 512, 512);
      grad.addColorStop(0, '#3e6b28');
      grad.addColorStop(0.5, '#4a7d32');
      grad.addColorStop(1, '#3b6625');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 512, 512);

      // Subtle rich earth patches
      for (let i = 0; i < 30; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        const r = 15 + Math.random() * 35;
        const earthGrad = ctx.createRadialGradient(x, y, 2, x, y, r);
        earthGrad.addColorStop(0, 'rgba(74, 53, 31, 0.45)');
        earthGrad.addColorStop(1, 'rgba(74, 53, 31, 0)');
        ctx.fillStyle = earthGrad;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }

      // 4000 Individual layered blades of grass
      for (let i = 0; i < 4000; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        const shades = ['#559138', '#63a841', '#427429', '#6ebc48', '#385e23'];
        ctx.strokeStyle = shades[Math.floor(Math.random() * shades.length)];
        ctx.lineWidth = 1.2 + Math.random() * 1.0;
        ctx.beginPath();
        ctx.moveTo(x, y);
        const curve = (Math.random() - 0.5) * 6;
        ctx.quadraticCurveTo(x + curve * 0.5, y - 4, x + curve, y - 7 - Math.random() * 7);
        ctx.stroke();
      }

      // Clover clusters & Meadow wildflowers
      for (let i = 0; i < 80; i++) {
        const cx = Math.random() * 512;
        const cy = Math.random() * 512;
        // 3 clover leaves
        ctx.fillStyle = '#2d531e';
        for (let a = 0; a < 3; a++) {
          const ang = (a * Math.PI * 2) / 3;
          ctx.beginPath();
          ctx.arc(cx + Math.cos(ang) * 2.8, cy + Math.sin(ang) * 2.8, 2.2, 0, Math.PI * 2);
          ctx.fill();
        }
        // Occasional flower center
        if (Math.random() > 0.5) {
          ctx.fillStyle = Math.random() > 0.4 ? '#fef08a' : (Math.random() > 0.5 ? '#ef4444' : '#60a5fa');
          ctx.beginPath();
          ctx.arc(cx, cy, 1.8, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(24, 24);
      return tex;
    }

    // 2. Medieval Ashlar Stone Texture (Hand-Dressed Limestone Blocks)
    function generateStoneTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      // Aged limestone base
      ctx.fillStyle = '#827f78';
      ctx.fillRect(0, 0, 512, 512);

      // Block rows with irregular ashlar courses
      const rowHeights = [36, 44, 40, 48, 38, 42, 46, 38, 42, 44, 40, 48, 46];
      let curY = 0;

      for (let r = 0; r < rowHeights.length; r++) {
        const h = rowHeights[r];
        let curX = (r % 2 === 0 ? 0 : -28);

        while (curX < 512) {
          const w = 55 + Math.random() * 35;
          // Block face with subtle gradient
          const stoneLight = 110 + Math.floor(Math.random() * 35);
          ctx.fillStyle = `rgb(${stoneLight}, ${stoneLight - 4}, ${stoneLight - 8})`;
          ctx.fillRect(curX + 2, curY + 2, w - 4, h - 4);

          // Top highlight bevel
          ctx.fillStyle = 'rgba(255, 255, 255, 0.18)';
          ctx.fillRect(curX + 2, curY + 2, w - 4, 3);
          ctx.fillRect(curX + 2, curY + 2, 3, h - 4);

          // Bottom shadow bevel
          ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
          ctx.fillRect(curX + 2, curY + h - 4, w - 4, 3);
          ctx.fillRect(curX + w - 4, curY + 2, 3, h - 4);

          // Mortar joint
          ctx.fillStyle = '#47443e';
          ctx.fillRect(curX, curY, w, 2);
          ctx.fillRect(curX, curY, 2, h);

          curX += w;
        }
        curY += h;
      }

      // Weathering stains & Chisel marks
      for (let i = 0; i < 1500; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(0,0,0,0.12)' : 'rgba(255,255,255,0.08)';
        ctx.fillRect(x, y, 1 + Math.random() * 2, 1 + Math.random() * 2);
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 3. Rich Oak Timber Texture with Wood Grain & Planks
    function generateWoodTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      // Deep heartwood base
      ctx.fillStyle = '#7a4b22';
      ctx.fillRect(0, 0, 512, 512);

      // Distinct plank grooves
      const plankW = 42;
      for (let x = 0; x < 512; x += plankW) {
        // Plank tone variation
        const varTone = (Math.random() - 0.5) * 18;
        ctx.fillStyle = `rgba(${Math.floor(100 + varTone)}, ${Math.floor(65 + varTone)}, ${Math.floor(30 + varTone)}, 0.4)`;
        ctx.fillRect(x, 0, plankW, 512);

        // Wood grain lines
        for (let g = 0; g < 18; g++) {
          const gx = x + Math.random() * plankW;
          ctx.strokeStyle = 'rgba(55, 30, 12, 0.35)';
          ctx.lineWidth = 1.0 + Math.random() * 1.5;
          ctx.beginPath();
          ctx.moveTo(gx, 0);
          ctx.bezierCurveTo(gx + (Math.random() - 0.5) * 8, 170, gx + (Math.random() - 0.5) * 8, 340, gx, 512);
          ctx.stroke();
        }

        // Dark plank seam
        ctx.fillStyle = '#3a1f0a';
        ctx.fillRect(x, 0, 3, 512);

        // Iron nail studs
        for (let y = 30; y < 512; y += 95) {
          ctx.fillStyle = '#1e1e1e';
          ctx.beginPath();
          ctx.arc(x + plankW * 0.5, y, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 4. Terracotta Clay Roof Tiles (Shaded Curved Barrel Tiles)
    function generateTileTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      ctx.fillStyle = '#8f3518';
      ctx.fillRect(0, 0, 512, 512);

      const tileH = 28;
      const tileW = 38;

      for (let y = 0; y < 512; y += tileH) {
        const offset = (y / tileH) % 2 === 0 ? 0 : tileW * 0.5;
        for (let x = -tileW; x < 512 + tileW; x += tileW) {
          const rx = x + offset;

          // Curved 3D tile shading
          const tileGrad = ctx.createLinearGradient(rx, y, rx + tileW, y);
          tileGrad.addColorStop(0, '#66220e');
          tileGrad.addColorStop(0.3, '#b84d2a');
          tileGrad.addColorStop(0.7, '#cf5e38');
          tileGrad.addColorStop(1, '#5a1d0b');
          ctx.fillStyle = tileGrad;
          ctx.fillRect(rx + 2, y + 2, tileW - 4, tileH - 4);

          // Scalloped bottom rim
          ctx.fillStyle = 'rgba(255, 255, 255, 0.22)';
          ctx.fillRect(rx + 2, y + 2, tileW - 4, 3);

          // Overlap shadow
          ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
          ctx.fillRect(rx, y + tileH - 3, tileW, 3);
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 5. Tudor Half-Timbered Plaster (Fachwerk White Stucco & Dark Oak Framing)
    function generatePlasterTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      // Textured lime plaster base
      ctx.fillStyle = '#f0eae0';
      ctx.fillRect(0, 0, 512, 512);

      // Stucco grain
      for (let i = 0; i < 2000; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)';
        ctx.fillRect(Math.random() * 512, Math.random() * 512, 2, 2);
      }

      // Dark aged timber framing beams
      ctx.fillStyle = '#422814';

      // Perimeter frame
      const bw = 24;
      ctx.fillRect(0, 0, 512, bw);
      ctx.fillRect(0, 512 - bw, 512, bw);
      ctx.fillRect(0, 0, bw, 512);
      ctx.fillRect(512 - bw, 0, bw, 512);
      // Center upright & cross braces
      ctx.fillRect(256 - bw * 0.5, 0, bw, 512);

      // Diagonal cross beams
      ctx.lineWidth = bw;
      ctx.strokeStyle = '#422814';
      ctx.beginPath();
      ctx.moveTo(bw, bw);
      ctx.lineTo(256 - bw * 0.5, 512 - bw);
      ctx.moveTo(512 - bw, bw);
      ctx.lineTo(256 + bw * 0.5, 512 - bw);
      ctx.stroke();

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 6. Thatched Straw Roof Texture
    function generateThatchTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      ctx.fillStyle = '#b88942';
      ctx.fillRect(0, 0, 512, 512);

      // Thousands of individual reed fibers
      for (let i = 0; i < 3000; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        const shades = ['#cca058', '#996e2b', '#e0b56e', '#80591e'];
        ctx.strokeStyle = shades[Math.floor(Math.random() * shades.length)];
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 5, y + 14 + Math.random() * 16);
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 7. Shimmering Water Caustics Texture
    function generateWaterTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');

      // Deep aquatic gradient
      const grad = ctx.createLinearGradient(0, 0, 512, 512);
      grad.addColorStop(0, '#105670');
      grad.addColorStop(0.5, '#196f8c');
      grad.addColorStop(1, '#124d63');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 512, 512);

      // Wave ripple rings
      for (let i = 0; i < 90; i++) {
        const cx = Math.random() * 512;
        const cy = Math.random() * 512;
        const r = 10 + Math.random() * 45;

        ctx.strokeStyle = 'rgba(180, 235, 255, 0.28)';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.ellipse(cx, cy, r, r * 0.45, Math.random() * Math.PI, 0, Math.PI * 2);
        ctx.stroke();

        // Wave crest highlight
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.arc(cx, cy, r * 0.3, 0, Math.PI);
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(4, 18);
      return tex;
    }

    // 8. Hammered Iron Metal Texture
    function generateIronTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#475569';
      ctx.fillRect(0, 0, 256, 256);

      for (let i = 0; i < 800; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.2)';
        ctx.fillRect(Math.random() * 256, Math.random() * 256, 2, 2);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // 9. Rocky Mountain Cliff Texture
    function generateCliffTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#645d54';
      ctx.fillRect(0, 0, 512, 512);

      // Stratified horizontal strata layers
      for (let y = 0; y < 512; y += 18 + Math.random() * 12) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
        ctx.fillRect(0, y, 512, 3);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.fillRect(0, y + 3, 512, 2);
      }
      for (let i = 0; i < 1200; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? '#7a7065' : '#4a443d';
        ctx.fillRect(Math.random() * 512, Math.random() * 512, 3, 3);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    // =========================================================================
    // WEB AUDIO SYNTHESIZER (PROCEDURAL VOICE BARKS, AMBIENCE & COMBAT SFX)
    // =========================================================================
    let audioCtx = null;
    let masterGain = null;

    function initAudio() {
      if (!audioCtx) {
        const AudioClass = window.AudioContext || window.webkitAudioContext;
        if (AudioClass) {
          audioCtx = new AudioClass();
          masterGain = audioCtx.createGain();
          masterGain.gain.setValueAtTime(0.75, audioCtx.currentTime);
          masterGain.connect(audioCtx.destination);
        }
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
    }

    window.setMasterVolume = function(val) {
      if (masterGain && audioCtx) {
        masterGain.gain.setValueAtTime(parseFloat(val), audioCtx.currentTime);
      }
    };

    // Authentic AoE Villager & Military Vocal Formants
    function playVoiceBark(type) {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const filter = audioCtx.createBiquadFilter();

      filter.type = 'bandpass';
      filter.Q.value = 4.0;

      if (type === 'select') {
        // "Mandatum?" - Rising vocal inflection
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, t);
        osc.frequency.exponentialRampToValueAtTime(220, t + 0.18);
        filter.frequency.setValueAtTime(750, t);
        filter.frequency.exponentialRampToValueAtTime(1400, t + 0.18);
        gain.gain.setValueAtTime(0.2, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.22);
      } else if (type === 'wood') {
        // "Chopper!" - Two sharp syllables
        osc.type = 'square';
        osc.frequency.setValueAtTime(180, t);
        osc.frequency.linearRampToValueAtTime(120, t + 0.2);
        filter.frequency.setValueAtTime(950, t);
        gain.gain.setValueAtTime(0.18, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.25);
      } else if (type === 'mine') {
        // "Miner!"
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, t);
        osc.frequency.exponentialRampToValueAtTime(110, t + 0.22);
        filter.frequency.setValueAtTime(1100, t);
        gain.gain.setValueAtTime(0.18, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.24);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.24);
      } else if (type === 'build') {
        // "Buldere!"
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(130, t);
        osc.frequency.linearRampToValueAtTime(170, t + 0.15);
        osc.frequency.linearRampToValueAtTime(120, t + 0.3);
        filter.frequency.setValueAtTime(800, t);
        gain.gain.setValueAtTime(0.18, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.32);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.32);
      } else if (type === 'move') {
        // "Correctus!"
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(150, t);
        osc.frequency.linearRampToValueAtTime(200, t + 0.12);
        osc.frequency.linearRampToValueAtTime(140, t + 0.24);
        filter.frequency.setValueAtTime(1200, t);
        gain.gain.setValueAtTime(0.18, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.26);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.26);
      } else if (type === 'attack') {
        // "Ad arma!" - Aggressive battle cry
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(190, t);
        osc.frequency.exponentialRampToValueAtTime(280, t + 0.14);
        osc.frequency.exponentialRampToValueAtTime(160, t + 0.28);
        filter.frequency.setValueAtTime(1500, t);
        gain.gain.setValueAtTime(0.24, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 0.3);
      }
    }

    // Iconic Monk "WOLOLO" Chant!
    function playWololoSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;

      const tones = [
        { f1: 330, f2: 660, start: 0, dur: 0.24 },
        { f1: 260, f2: 520, start: 0.24, dur: 0.24 },
        { f1: 330, f2: 660, start: 0.48, dur: 0.3 }
      ];

      tones.forEach(tone => {
        const o1 = audioCtx.createOscillator();
        const o2 = audioCtx.createOscillator();
        const g = audioCtx.createGain();

        o1.type = 'sawtooth';
        o1.frequency.setValueAtTime(tone.f1, t + tone.start);
        o2.type = 'sine';
        o2.frequency.setValueAtTime(tone.f2, t + tone.start);

        g.gain.setValueAtTime(0.15, t + tone.start);
        g.gain.exponentialRampToValueAtTime(0.001, t + tone.start + tone.dur);

        o1.connect(g);
        o2.connect(g);
        g.connect(masterGain);

        o1.start(t + tone.start);
        o2.start(t + tone.start);
        o1.stop(t + tone.start + tone.dur);
        o2.stop(t + tone.start + tone.dur);
      });
    }

    // Heavy Bronze Town Bell Toll
    function playTownBellSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;

      [130, 260, 520, 780].forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.25 / (idx + 1), t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 2.4);
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 2.5);
      });
    }

    // Royal Age Advancement Trumpet Fanfare
    function playAdvanceAgeFanfare() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;

      const notes = [
        { f: 293.66, start: 0, dur: 0.18 }, // D4
        { f: 369.99, start: 0.18, dur: 0.18 }, // F#4
        { f: 440.00, start: 0.36, dur: 0.22 }, // A4
        { f: 587.33, start: 0.58, dur: 0.55 }  // D5
      ];

      notes.forEach(note => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(note.f, t + note.start);
        gain.gain.setValueAtTime(0.22, t + note.start);
        gain.gain.exponentialRampToValueAtTime(0.001, t + note.start + note.dur);
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(t + note.start);
        osc.stop(t + note.start + note.dur);
      });
    }

    function playSwordClashSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(800, t);
      osc.frequency.exponentialRampToValueAtTime(180, t + 0.12);
      gain.gain.setValueAtTime(0.25, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.14);
      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(t);
      osc.stop(t + 0.14);
    }

    function playArrowReleaseSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(600, t);
      osc.frequency.exponentialRampToValueAtTime(1200, t + 0.08);
      gain.gain.setValueAtTime(0.18, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(t);
      osc.stop(t + 0.1);
    }

    function playBuildingHammerSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(220, t);
      gain.gain.setValueAtTime(0.15, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(t);
      osc.stop(t + 0.08);
    }

    function playRainSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(65, t);
      osc.frequency.exponentialRampToValueAtTime(45, t + 0.8);
      gain.gain.setValueAtTime(0.12, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.9);
      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(t);
      osc.stop(t + 0.9);
    }
    """
