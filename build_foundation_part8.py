# build_foundation_part8.py - Economy, Quests, Controls, Settings & 60 FPS Loop
part8 = r'''
    // =========================================================================
    // ECONOMY, ESTATE QUESTS, CAMERA CONTROLS, SETTINGS & 60 FPS LOOP
    // =========================================================================
    const gameState = {
      gold: 250,
      wood: 40,
      stone: 20,
      berries: 30,
      bread: 15,
      happiness: 100
    };

    let currentQuestIdx = 1;
    const quests = [
      {
        id: 1,
        title: '1. Lay the Foundation',
        desc: 'Construct a Lumber Camp and a Town Well to secure vital supplies for your serfs.',
        check: () => buildings.some(b => b.type === 'lumber') && buildings.some(b => b.type === 'well'),
        progressText: () => `[PROGRESS: ${buildings.filter(b => b.type === 'lumber' || b.type === 'well').length}/2 BUILDINGS]`,
        reward: () => { gameState.gold += 100; gameState.bread += 20; spawnVillager('Woodcutter'); spawnVillager('Laborer'); }
      },
      {
        id: 2,
        title: '2. Feed the Hamlet',
        desc: 'Construct a Market Stall and Thatched Cottages to house your growing population.',
        check: () => buildings.some(b => b.type === 'market') && buildings.filter(b => b.type === 'cottage').length >= 2,
        progressText: () => `[PROGRESS: Market ${buildings.filter(b => b.type === 'market').length}/1, Cottages ${buildings.filter(b => b.type === 'cottage').length}/2]`,
        reward: () => { gameState.gold += 150; spawnVillager('Market Tender'); spawnVillager('Farmer'); }
      },
      {
        id: 3,
        title: '3. Grain & Masonry',
        desc: 'Construct a Stonecutter Quarry and a Windmill to produce bread and stone blocks.',
        check: () => buildings.some(b => b.type === 'quarry') && buildings.some(b => b.type === 'windmill'),
        progressText: () => `[PROGRESS: ${buildings.filter(b => b.type === 'quarry' || b.type === 'windmill').length}/2 BUILDINGS]`,
        reward: () => { gameState.gold += 200; spawnVillager('Stone Mason'); spawnVillager('Miller'); }
      },
      {
        id: 4,
        title: '4. Spiritual Devotion',
        desc: 'Erect a Rustic Church to inspire your serfs and satisfy their need for Faith.',
        check: () => buildings.some(b => b.type === 'church'),
        progressText: () => `[PROGRESS: Church ${buildings.filter(b => b.type === 'church').length}/1]`,
        reward: () => { gameState.gold += 300; playChurchBellSound(); spawnVillager('Priest'); }
      },
      {
        id: 5,
        title: '5. Seat of the Sovereign',
        desc: 'Erect the fortified Lord\'s Keep citadel to establish your realm\'s military authority!',
        check: () => buildings.some(b => b.type === 'keep'),
        progressText: () => `[PROGRESS: Lord's Keep ${buildings.filter(b => b.type === 'keep').length}/1]`,
        reward: () => { alert('CONGRATULATIONS, MY LORD! You have forged a grand medieval civilization in Foundation!'); }
      }
    ];

    function checkQuestMilestone(newBuildingType) {
      const q = quests[currentQuestIdx - 1];
      if (q && q.check()) {
        playQuestCompleteSound();
        q.reward();
        currentQuestIdx++;
        if (currentQuestIdx <= quests.length) {
          updateQuestUI();
        } else {
          document.getElementById('quest-title').innerText = 'VICTORY: Realm Established';
          document.getElementById('quest-desc').innerText = 'Your kingdom stands proud upon the rolling hills.';
          document.getElementById('quest-progress').innerText = '[ALL QUESTS COMPLETE]';
        }
      } else {
        updateQuestUI();
      }
    }

    function updateQuestUI() {
      if (currentQuestIdx > quests.length) return;
      const q = quests[currentQuestIdx - 1];
      document.getElementById('quest-title').innerText = q.title;
      document.getElementById('quest-desc').innerText = q.desc;
      document.getElementById('quest-progress').innerText = q.progressText();
    }

    function updateResourceLedger() {
      document.getElementById('res-gold').innerText = gameState.gold;
      document.getElementById('res-wood').innerText = gameState.wood;
      document.getElementById('res-stone').innerText = gameState.stone;
      document.getElementById('res-berries').innerText = gameState.berries;
      document.getElementById('res-bread').innerText = gameState.bread;
    }

    function updatePopulationHUD() {
      const popEl = document.getElementById('pop-count');
      if (popEl) popEl.innerText = villagers.length;
    }

    // Raycaster for Terrain Intersection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function setupControlsAndInput() {
      window.addEventListener('keydown', (e) => {
        initAudio();
        if (e.code === 'Escape') {
          if (activeBuildType) cancelBuildingPlacement();
          else togglePauseSettings();
        }
        if (e.code === 'KeyR' && ghostBuilding) {
          ghostRotation += Math.PI * 0.25;
          ghostBuilding.rotation.y = ghostRotation;
        }
      });

      // Right Mouse Drag to Orbit Horizon
      window.addEventListener('mousedown', (e) => {
        initAudio();
        if (e.button === 2) {
          isRightDragging = true;
          prevMouseX = e.clientX;
          prevMouseY = e.clientY;
        } else if (e.button === 0) {
          // Left Click: Place building or inspect
          handleLeftClick(e);
        }
      });

      window.addEventListener('mouseup', (e) => {
        if (e.button === 2) isRightDragging = false;
      });

      window.addEventListener('contextmenu', (e) => e.preventDefault());

      window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        if (isRightDragging) {
          const deltaX = e.clientX - prevMouseX;
          const deltaY = e.clientY - prevMouseY;
          prevMouseX = e.clientX;
          prevMouseY = e.clientY;

          camYaw -= deltaX * 0.005;
          camPitch = Math.max(0.15, Math.min(1.4, camPitch - deltaY * 0.005));
          updateCameraPosition();
        }

        // Update Ghost Building Position on Terrain
        if (activeBuildType && ghostBuilding && terrainMesh) {
          raycaster.setFromCamera(mouse, camera);
          const intersects = raycaster.intersectObject(terrainMesh);
          if (intersects.length > 0) {
            const p = intersects[0].point;
            ghostBuilding.position.set(p.x, getTerrainHeight(p.x, p.z), p.z);
          }
        }
      });

      // CONTINUOUS MOUSE SCROLL WHEEL OPTICAL ZOOM (8m to 260m)
      window.addEventListener('wheel', (e) => {
        camDistance = Math.max(8.0, Math.min(260.0, camDistance + e.deltaY * 0.08));
        updateCameraPosition();
      }, { passive: true });

      // Settings DOM Events
      const btnSettings = document.getElementById('btn-settings-hud');
      if (btnSettings) btnSettings.addEventListener('click', () => togglePauseSettings());

      const sBright = document.getElementById('slider-brightness');
      if (sBright) {
        sBright.addEventListener('input', (e) => {
          const v = parseFloat(e.target.value);
          if (renderer) renderer.toneMappingExposure = v;
          document.getElementById('val-brightness').innerText = `${Math.round(v * 100)}%`;
        });
      }

      const sVol = document.getElementById('slider-volume');
      if (sVol) {
        sVol.addEventListener('input', (e) => {
          masterVolume = parseFloat(e.target.value);
          document.getElementById('val-volume').innerText = `${Math.round(masterVolume * 100)}%`;
        });
      }

      const selGPU = document.getElementById('select-gpu');
      if (selGPU) {
        selGPU.addEventListener('change', (e) => {
          if (!renderer) return;
          const mode = e.target.value;
          if (mode === 'ultra') renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
          else if (mode === 'high') renderer.setPixelRatio(1.25);
          else renderer.setPixelRatio(1.0);
        });
      }
    }

    function handleLeftClick(e) {
      if (e.target.closest('#hud') || e.target.closest('#settings-modal') || e.target.closest('#inspector-card')) return;

      if (activeBuildType && ghostBuilding) {
        tryPlaceBuilding(ghostBuilding.position.x, ghostBuilding.position.z);
        return;
      }

      // Check click on Villager
      raycaster.setFromCamera(mouse, camera);
      for (const v of villagers) {
        const intersects = raycaster.intersectObjects(v.mesh.children);
        if (intersects.length > 0) {
          inspectVillager(v);
          return;
        }
      }
    }

    // Keyboard Pan (WASD / Arrows)
    const keys = {};
    window.addEventListener('keydown', (e) => { keys[e.code] = true; });
    window.addEventListener('keyup', (e) => { keys[e.code] = false; });

    function updateCameraPan(delta) {
      let dx = 0, dz = 0;
      if (keys['KeyW'] || keys['ArrowUp']) dz -= 1;
      if (keys['KeyS'] || keys['ArrowDown']) dz += 1;
      if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
      if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

      if (dx !== 0 || dz !== 0) {
        const panSpeed = (camDistance * 0.8) * delta;
        const sinYaw = Math.sin(camYaw);
        const cosYaw = Math.cos(camYaw);

        camTarget.x += (dx * cosYaw - dz * sinYaw) * panSpeed;
        camTarget.z += (dx * sinYaw + dz * cosYaw) * panSpeed;
        camTarget.x = Math.max(-180, Math.min(180, camTarget.x));
        camTarget.z = Math.max(-180, Math.min(180, camTarget.z));
        updateCameraPosition();
      }
    }

    // Settings Modal Toggle
    window.togglePauseSettings = function() {
      const modal = document.getElementById('settings-modal');
      if (!modal) return;
      const isOpen = modal.style.display === 'flex';
      modal.style.display = isOpen ? 'none' : 'flex';
    };

    // Zoning Toggle
    window.toggleZoningTool = function() {
      initAudio();
      alert('[ZONING SYSTEM ACTIVE] Paint Residential zones (Green) on rolling hills. Serfs will autonomously construct their thatched cottages near wells and workplaces!');
    };

    // MAIN 60 FPS SIMULATION ANIMATION LOOP
    let lastTime = performance.now();

    function animate(currentTime) {
      requestAnimationFrame(animate);

      const delta = Math.min((currentTime - lastTime) * 0.001, 0.05);
      lastTime = currentTime;

      // 1. Camera Pan
      updateCameraPan(delta);

      // 2. Autonomous Villagers & Desire Footpaths
      updateVillagers(delta);

      // 3. Windmill Sail Rotation
      buildings.forEach((b) => {
        if (b.type === 'windmill' && b.mesh.sails) {
          b.mesh.sails.rotation.z += delta * 1.2;
        }
      });

      // 4. Drifting Fluffy Clouds
      clouds.forEach((c) => {
        c.mesh.position.x += c.speed * delta;
        if (c.mesh.position.x > 320) c.mesh.position.x = -320;
      });

      renderer.render(scene, camera);
    }

    // BOOTSTRAP REALM (Spawn Town Center & First 6 Serfs)
    window.addEventListener('DOMContentLoaded', () => {
      init3DEnvironment();
      setupControlsAndInput();

      // Default Town Center Manor at (0, 0)
      const centerBuilding = createBuildingMesh('center', false);
      centerBuilding.position.set(0, getTerrainHeight(0, 0), 0);
      scene.add(centerBuilding);
      buildings.push({ type: 'center', mesh: centerBuilding, x: 0, z: 0 });

      // Spawn First 6 Autonomous Serfs
      for (let i = 0; i < 6; i++) {
        const offset = new THREE.Vector3((Math.random() - 0.5) * 16, 0, (Math.random() - 0.5) * 16);
        spawnVillager(i < 3 ? 'Woodcutter' : 'Laborer', offset);
      }

      updateResourceLedger();
      updateQuestUI();
      requestAnimationFrame(animate);
    });

  </script>
</body>
</html>
'''

with open("foundation_part8.py", "w", encoding="utf-8") as f:
    f.write('part8 = r"""' + part8 + '"""\n')
print("Wrote foundation_part8.py")
