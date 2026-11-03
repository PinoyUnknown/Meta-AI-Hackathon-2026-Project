def get_aoe_audio_textures_js():
    return """
    // =========================================================================
    // PROCEDURAL TEXTURE GENERATION (HIGH FIDELITY VIBRANT AGE OF EMPIRES)
    // =========================================================================
    function createProceduralCanvas(width, height) {
      const c = document.createElement('canvas');
      c.width = width;
      c.height = height;
      return c;
    }

    function generateGrassTexture() {
      const c = createProceduralCanvas(512, 512);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#559933';
      ctx.fillRect(0, 0, 512, 512);

      // Grass blades
      for (let i = 0; i < 2000; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        ctx.strokeStyle = Math.random() > 0.5 ? '#6eb53e' : '#468028';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 5, y - 4 - Math.random() * 5);
        ctx.stroke();
      }

      // Small wildflowers
      for (let i = 0; i < 150; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        ctx.fillStyle = Math.random() > 0.4 ? '#fef08a' : '#ffffff';
        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fill();
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(40, 40);
      return tex;
    }

    function generateWoodTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#8b5a2b';
      ctx.fillRect(0, 0, 256, 256);

      ctx.fillStyle = '#6d421d';
      for (let i = 0; i < 256; i += 16) {
        ctx.fillRect(0, i, 256, 2);
      }
      for (let i = 0; i < 50; i++) {
        ctx.strokeStyle = 'rgba(60, 35, 15, 0.4)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(Math.random() * 256, Math.random() * 256, Math.random() * 20, 0, Math.PI * 2);
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function generateStoneTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#7a7a7a';
      ctx.fillRect(0, 0, 256, 256);

      // Ashlar stone brick joints
      ctx.strokeStyle = '#4a4a4a';
      ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 32) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(256, y);
        ctx.stroke();

        const offset = (y / 32) % 2 === 0 ? 0 : 32;
        for (let x = offset; x < 256; x += 64) {
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x, y + 32);
          ctx.stroke();
        }
      }

      for (let i = 0; i < 1000; i++) {
        const x = Math.random() * 256;
        const y = Math.random() * 256;
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.12)';
        ctx.fillRect(x, y, 2, 2);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function generateThatchTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#c89d55';
      ctx.fillRect(0, 0, 256, 256);

      ctx.strokeStyle = '#9e7330';
      ctx.lineWidth = 1.5;
      for (let i = 0; i < 600; i++) {
        const x = Math.random() * 256;
        const y = Math.random() * 256;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 4, y + 8 + Math.random() * 8);
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function generateTileTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#a8432a';
      ctx.fillRect(0, 0, 256, 256);

      ctx.strokeStyle = '#6e2716';
      ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 16) {
        ctx.strokeRect(0, y, 256, 16);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function generatePlasterTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#eae2cf';
      ctx.fillRect(0, 0, 256, 256);

      // Timber framing cross-beams
      ctx.fillStyle = '#5c3818';
      ctx.fillRect(0, 0, 256, 12);
      ctx.fillRect(0, 244, 256, 12);
      ctx.fillRect(0, 0, 12, 256);
      ctx.fillRect(244, 0, 12, 256);
      ctx.fillRect(122, 0, 12, 256);
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function generateIronTexture() {
      const c = createProceduralCanvas(128, 128);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#4a5568';
      ctx.fillRect(0, 0, 128, 128);
      for (let i = 0; i < 400; i++) {
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.15)';
        ctx.fillRect(Math.random() * 128, Math.random() * 128, 2, 2);
      }
      return new THREE.CanvasTexture(c);
    }

    function generateWaterTexture() {
      const c = createProceduralCanvas(256, 256);
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#1e6f9f';
      ctx.fillRect(0, 0, 256, 256);

      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 1.8;
      for (let i = 0; i < 60; i++) {
        const y = Math.random() * 256;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.bezierCurveTo(64, y + 8, 192, y - 8, 256, y);
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(6, 60);
      return tex;
    }

    // =========================================================================
    // WEB AUDIO SYNTHESIZER (PROCEDURAL VOICE BARKS, FANFARE & SFX)
    // =========================================================================
    let audioCtx = null;
    let masterGain = null;

    function initAudio() {
      if (!audioCtx) {
        const AudioClass = window.AudioContext || window.webkitAudioContext;
        if (AudioClass) {
          audioCtx = new AudioClass();
          masterGain = audioCtx.createGain();
          masterGain.gain.setValueAtTime(0.7, audioCtx.currentTime);
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
        // "Mandatum?" - Rising question inflection
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, t);
        osc.frequency.exponentialRampToValueAtTime(220, t + 0.18);
        filter.frequency.setValueAtTime(750, t);
        filter.frequency.exponentialRampToValueAtTime(1400, t + 0.18);
        gain.gain.setValueAtTime(0.18, t);
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
        gain.gain.setValueAtTime(0.16, t);
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
        gain.gain.setValueAtTime(0.16, t);
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
        gain.gain.setValueAtTime(0.16, t);
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
        gain.gain.setValueAtTime(0.22, t);
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

      // Two-step harmonic formant frequency transition
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
        o1.stop(t + tone.start + tone.dur);
        o2.start(t + tone.start);
        o2.stop(t + tone.start + tone.dur);
      });
    }

    // Town Bell Alarm
    function playTownBellSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const freqs = [440, 880, 1320, 1760];
      freqs.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.2 / (idx + 1), t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 2.2);
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(t);
        osc.stop(t + 2.2);
      });
    }

    // Age Advancement Fanfare
    function playAdvanceAgeFanfare() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const notes = [
        { f: 261.63, start: 0.0, dur: 0.25 }, // C4
        { f: 329.63, start: 0.22, dur: 0.25 }, // E4
        { f: 392.00, start: 0.44, dur: 0.35 }, // G4
        { f: 523.25, start: 0.75, dur: 0.80 }  // C5
      ];
      notes.forEach(n => {
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(n.f, t + n.start);
        g.gain.setValueAtTime(0.2, t + n.start);
        g.gain.exponentialRampToValueAtTime(0.001, t + n.start + n.dur);
        osc.connect(g);
        g.connect(masterGain);
        osc.start(t + n.start);
        osc.stop(t + n.start + n.dur);
      });
    }

    // Combat Sounds
    function playSwordClashSound() {
      if (!audioCtx) return;
      initAudio();
      const t = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(1800, t);
      osc.frequency.exponentialRampToValueAtTime(200, t + 0.12);
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
    """
