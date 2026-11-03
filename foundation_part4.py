part4 = r"""
    // =========================================================================
    // PROCEDURAL WEB AUDIO SYNTHESIZER (ZERO EXTERNAL MP3 DEPENDENCIES)
    // =========================================================================
    let audioCtx = null;
    let masterVolume = 0.75;

    function initAudio() {
      if (audioCtx) return;
      try {
        const AudioClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioClass();
        startPastoralAmbiance();
      } catch (e) {
        console.warn('AudioContext unavailable:', e);
      }
    }

    // Peaceful Countryside Ambiance (Soft Wind & Bird Song)
    function startPastoralAmbiance() {
      if (!audioCtx) return;
      try {
        // Continuous soft wind noise
        const bufSize = audioCtx.sampleRate * 2;
        const buf = audioCtx.createBuffer(1, bufSize, audioCtx.sampleRate);
        const data = buf.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = (Math.random() * 2 - 1) * 0.08;

        const noise = audioCtx.createBufferSource();
        noise.buffer = buf;
        noise.loop = true;

        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(320, audioCtx.currentTime);

        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.04 * masterVolume, audioCtx.currentTime);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        noise.start();

        // Periodic bird chirps
        setInterval(() => {
          if (audioCtx && Math.random() > 0.4) playBirdChirp();
        }, 3800);
      } catch (e) {}
    }

    function playBirdChirp() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      const baseFreq = 2200 + Math.random() * 800;
      osc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(baseFreq + 600, audioCtx.currentTime + 0.08);
      osc.frequency.exponentialRampToValueAtTime(baseFreq - 200, audioCtx.currentTime + 0.16);

      gain.gain.setValueAtTime(0.02 * masterVolume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.16);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.18);
    }

    // Construction Hammer Strike
    function playBuildHammerSound() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(180, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(60, audioCtx.currentTime + 0.1);

      gain.gain.setValueAtTime(0.25 * masterVolume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.11);
    }

    // Woodcutter Axe Thud
    function playWoodChopSound() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(120, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);

      gain.gain.setValueAtTime(0.2 * masterVolume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.12);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.13);
    }

    // Stone Quarry Pickaxe Clink
    function playStoneChiselSound() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(450, audioCtx.currentTime + 0.08);

      gain.gain.setValueAtTime(0.18 * masterVolume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.09);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.1);
    }

    // Resonant Church Belfry Bell
    function playChurchBellSound() {
      if (!audioCtx) return;
      [440, 880, 1320].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime((0.15 / (i + 1)) * masterVolume, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 2.5);

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 2.6);
      });
    }

    // Gold Coins Clink
    function playCoinSound() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(987, audioCtx.currentTime);
      osc.frequency.setValueAtTime(1318, audioCtx.currentTime + 0.06);

      gain.gain.setValueAtTime(0.12 * masterVolume, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.18);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.19);
    }

    // Quest Complete Royal Horn Fanfare
    function playQuestCompleteSound() {
      if (!audioCtx) return;
      const notes = [392, 523, 659, 784]; // G4, C5, E5, G5
      notes.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.12);

        gain.gain.setValueAtTime(0.0, audioCtx.currentTime + idx * 0.12);
        gain.gain.linearRampToValueAtTime(0.15 * masterVolume, audioCtx.currentTime + idx * 0.12 + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + idx * 0.12 + 0.35);

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(audioCtx.currentTime + idx * 0.12);
        osc.stop(audioCtx.currentTime + idx * 0.12 + 0.38);
      });
    }
"""
