def get_aoe_sim_loop_js():
    return """
    // =========================================================================
    // RTS CAMERA CONTROLLER, SCREEN-EDGE PANNING & INTERACTION LOOP
    // =========================================================================

    let raycaster = new THREE.Raycaster();
    let mouse = new THREE.Vector2();
    let isMouseDown = false;
    let mouseDownScreen = { x: 0, y: 0 };
    let lastMouseScreen = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    let dragThreshold = 6;
    let isDragging = false;
    let selectionBoxEl = document.getElementById('selection-box');

    // RTS Camera Controller (Isometric Top-Down Perspective)
    // Constrained strictly to the 200x200 world grid (-100m to +100m)
    let cameraTargetPos = new THREE.Vector3(0, 0, 0);
    let cameraZoom = 36; // Clamped height: 16m min, 65m max
    const keysPressed = {};

    window.addEventListener('keydown', e => {
      keysPressed[e.code] = true;
      if (e.code === 'KeyZ' || e.code === 'Period') {
        window.cycleIdleVillager();
      } else if (e.code === 'KeyB') {
        window.toggleTownBell();
      } else if (e.code === 'KeyQ') {
        window.setBuildCategory('eco');
      } else if (e.code === 'KeyW') {
        window.setBuildCategory('mil');
      } else if (e.code === 'Escape') {
        if (aoeState.activePlacementType) {
          cancelBuildingPlacement();
        } else {
          window.toggleMenuModal();
        }
      } else if (e.code === 'F5') {
        e.preventDefault();
        window.saveAoEGame();
      } else if (e.code === 'F9') {
        e.preventDefault();
        window.loadAoEGame();
      }
    });

    window.addEventListener('keyup', e => {
      keysPressed[e.code] = false;
    });

    // Scroll-Wheel Zooming Clamped between Min (16m) and Max (65m) Heights
    window.addEventListener('wheel', e => {
      cameraZoom = Math.max(16, Math.min(65, cameraZoom + e.deltaY * 0.04));
    }, { passive: true });

    // Track Screen Coordinates for Screen-Edge Mouse Panning
    window.addEventListener('mousemove', e => {
      lastMouseScreen.x = e.clientX;
      lastMouseScreen.y = e.clientY;
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      // Selection Box Dragging
      if (isMouseDown) {
        const dx = Math.abs(e.clientX - mouseDownScreen.x);
        const dy = Math.abs(e.clientY - mouseDownScreen.y);
        if (dx > dragThreshold || dy > dragThreshold) {
          isDragging = true;
          selectionBoxEl.style.display = 'block';
          const left = Math.min(e.clientX, mouseDownScreen.x);
          const top = Math.min(e.clientY, mouseDownScreen.y);
          const width = Math.abs(e.clientX - mouseDownScreen.x);
          const height = Math.abs(e.clientY - mouseDownScreen.y);
          selectionBoxEl.style.left = left + 'px';
          selectionBoxEl.style.top = top + 'px';
          selectionBoxEl.style.width = width + 'px';
          selectionBoxEl.style.height = height + 'px';
        }
      }

      // Blueprint Ghost Snapping & Real-time Collision Check
      if (aoeState.placementGhost) {
        raycaster.setFromCamera(mouse, camera);
        const hits = raycaster.intersectObject(terrainMesh);
        if (hits.length > 0) {
          const pt = hits[0].point;
          const snapX = Math.round(pt.x / TILE_SIZE) * TILE_SIZE;
          const snapZ = Math.round(pt.z / TILE_SIZE) * TILE_SIZE;
          aoeState.placementGhost.position.set(snapX, 0, snapZ);

          const g = worldToGrid(snapX, snapZ);
          const bDef = BUILDING_TYPES[aoeState.activePlacementType];
          const sizeTiles = Math.max(1, Math.round((bDef ? bDef.size : 4) / TILE_SIZE));
          const isClear = isTileBuildable(g.x, g.z, sizeTiles, sizeTiles);

          aoeState.placementGhost.traverse(c => {
            if (c.isMesh && c.material) {
              c.material.color.setHex(isClear ? 0x22c55e : 0xef4444);
            }
          });
        }
      }

      updateHoverTooltip(e);
    });

    window.addEventListener('mousedown', e => {
      if (e.target.closest('#aoe-top-bar') || e.target.closest('#aoe-bottom-bar') || e.target.closest('.aoe-modal')) {
        return;
      }
      initAudio();

      if (e.button === 0) { // Left Click
        if (aoeState.activePlacementType) {
          confirmBuildingPlacement();
          return;
        }
        isMouseDown = true;
        mouseDownScreen.x = e.clientX;
        mouseDownScreen.y = e.clientY;
        isDragging = false;
      } else if (e.button === 2) { // Right Click - Smart Action
        e.preventDefault();
        if (aoeState.activePlacementType) {
          cancelBuildingPlacement();
          return;
        }
        handleSmartRightClick(e);
      }
    });

    window.addEventListener('contextmenu', e => e.preventDefault());

    // Mouse Up (Complete Drag Selection)
    window.addEventListener('mouseup', e => {
      if (e.button === 0 && isMouseDown) {
        isMouseDown = false;
        selectionBoxEl.style.display = 'none';

        if (isDragging) {
          isDragging = false;
          // Box Selection
          const minX = Math.min(e.clientX, mouseDownScreen.x);
          const maxX = Math.max(e.clientX, mouseDownScreen.x);
          const minY = Math.min(e.clientY, mouseDownScreen.y);
          const maxY = Math.max(e.clientY, mouseDownScreen.y);

          const selected = [];
          friendlyUnits.forEach(u => {
            if (u.state === 'garrisoned') return;
            const screenPos = u.mesh.position.clone().project(camera);
            const sx = (screenPos.x * 0.5 + 0.5) * window.innerWidth;
            const sy = (-(screenPos.y * 0.5) + 0.5) * window.innerHeight;
            if (sx >= minX && sx <= maxX && sy >= minY && sy <= maxY) {
              selected.push(u);
            }
          });

          if (selected.length > 0) {
            const military = selected.filter(u => u.type !== 'villager');
            selectEntities(military.length > 0 ? military : selected);
            playVoiceBark(military.length > 0 ? 'attack' : 'select');
          } else {
            clearSelection();
          }
        } else {
          // Single Click Selection
          raycaster.setFromCamera(mouse, camera);
          const selectableMeshes = [];
          allSelectable.forEach(item => {
            if (item.mesh && item.mesh.visible) {
              selectableMeshes.push(item.mesh);
            }
          });
          const intersects = raycaster.intersectObjects(selectableMeshes, true);
          if (intersects.length > 0) {
            let hitObj = intersects[0].object;
            while (hitObj.parent && !hitObj.userData.entityRef) {
              hitObj = hitObj.parent;
            }
            if (hitObj.userData.entityRef) {
              selectSingleEntity(hitObj.userData.entityRef);
              if (hitObj.userData.entityRef.team === 'player') {
                playVoiceBark(hitObj.userData.entityRef.type === 'villager' ? 'select' : 'attack');
              }
            }
          } else {
            clearSelection();
          }
        }
      }
    });

    // Smart Right Click: Move, Attack, Harvest, Repair, Garrison
    function handleSmartRightClick(e) {
      if (aoeState.selectedEntities.length === 0) return;

      raycaster.setFromCamera(mouse, camera);
      const selectableMeshes = allSelectable.map(item => item.mesh).filter(Boolean);
      const intersects = raycaster.intersectObjects(selectableMeshes, true);

      let targetEntity = null;
      if (intersects.length > 0) {
        let hitObj = intersects[0].object;
        while (hitObj.parent && !hitObj.userData.entityRef) {
          hitObj = hitObj.parent;
        }
        targetEntity = hitObj.userData.entityRef;
      }

      const terrainHits = raycaster.intersectObject(terrainMesh);
      const targetPos = terrainHits.length > 0 ? terrainHits[0].point : null;

      if (targetEntity) {
        if (targetEntity.team === 'enemy') {
          // ATTACK COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.state !== 'garrisoned') {
              unit.target = targetEntity;
              unit.state = 'attacking';
            }
          });
          spawnAttackMarker(targetEntity.mesh.position);
          playVoiceBark('attack');
          showAoENotice('[ATTACK COMMAND] Targeting ' + targetEntity.name + '!');
        } else if (targetEntity.isResource) {
          // GATHER RESOURCE COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager' && unit.state !== 'garrisoned') {
              unit.target = targetEntity;
              unit.state = 'gathering';
              updateVillagerToolVisual(unit, targetEntity.resType);
            }
          });
          spawnMoveMarker(targetEntity.mesh.position);
          playVoiceBark(targetEntity.resType === 'wood' ? 'wood' : (targetEntity.resType === 'gold' || targetEntity.resType === 'stone' ? 'mine' : 'select'));
          showAoENotice('[GATHERING] Harvesting ' + targetEntity.name);
        } else if (targetEntity.team === 'player' && targetEntity.isFoundation) {
          // BUILD FOUNDATION COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager') {
              unit.target = targetEntity;
              unit.state = 'building';
              updateVillagerToolVisual(unit, 'build');
            }
          });
          spawnMoveMarker(targetEntity.mesh.position);
          playVoiceBark('build');
          showAoENotice('[CONSTRUCTING] Constructing ' + targetEntity.name);
        } else if (targetEntity.team === 'player' && targetEntity.type === 'town_center') {
          // GARRISON COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager') {
              unit.state = 'garrisoned';
              unit.mesh.visible = false;
            }
          });
          showAoENotice('[GARRISON] Units sheltered inside Town Center.');
          updateResourceUI();
        } else if (targetEntity.team === 'player' && targetEntity.hp < targetEntity.maxHp) {
          // REPAIR COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager') {
              unit.target = targetEntity;
              unit.state = 'repairing';
              updateVillagerToolVisual(unit, 'build');
            }
          });
          spawnMoveMarker(targetEntity.mesh.position);
          playVoiceBark('build');
        }
      } else if (targetPos) {
        // FORMATION MOVEMENT (Flocking grid offsets)
        const formationSlots = calculateFormationPositions(targetPos, aoeState.selectedEntities.length);
        aoeState.selectedEntities.forEach((unit, idx) => {
          if (unit.state !== 'garrisoned') {
            const dest = formationSlots[idx] || targetPos;
            const path = findAStarPath(unit.mesh.position.x, unit.mesh.position.z, dest.x, dest.z);
            unit.path = path;
            unit.dest = path.length > 0 ? path[0] : dest;
            unit.state = 'moving';
            unit.target = null;
          }
        });
        spawnMoveMarker(targetPos);
        playVoiceBark('move');
      }
    }

    // Waypoint Visual Markers
    function spawnMoveMarker(pos) {
      const geom = new THREE.RingGeometry(0.8, 1.2, 16);
      geom.rotateX(-Math.PI / 2);
      const mat = new THREE.MeshBasicMaterial({ color: 0x4ade80, side: THREE.DoubleSide });
      const m = new THREE.Mesh(geom, mat);
      m.position.set(pos.x, pos.y + 0.15, pos.z);
      scene.add(m);
      let scale = 1.0;
      const anim = setInterval(() => {
        scale += 0.12;
        m.scale.set(scale, scale, scale);
        mat.opacity -= 0.1;
        if (mat.opacity <= 0) {
          clearInterval(anim);
          scene.remove(m);
        }
      }, 30);
    }

    function spawnAttackMarker(pos) {
      const geom = new THREE.RingGeometry(1.0, 1.5, 16);
      geom.rotateX(-Math.PI / 2);
      const mat = new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide });
      const m = new THREE.Mesh(geom, mat);
      m.position.set(pos.x, pos.y + 0.2, pos.z);
      scene.add(m);
      let scale = 1.0;
      const anim = setInterval(() => {
        scale += 0.15;
        m.scale.set(scale, scale, scale);
        mat.opacity -= 0.1;
        if (mat.opacity <= 0) {
          clearInterval(anim);
          scene.remove(m);
        }
      }, 30);
    }

    // Selection Handlers
    function selectEntities(entities) {
      clearSelection();
      aoeState.selectedEntities = entities;
      entities.forEach(e => {
        if (e.mesh && e.mesh.userData && e.mesh.userData.ring) {
          e.mesh.userData.ring.visible = true;
        }
      });
      aoeState.selectedEntity = entities[0];
      updateConsoleUI(entities[0]);
    }

    function selectSingleEntity(entity) {
      clearSelection();
      aoeState.selectedEntities = [entity];
      aoeState.selectedEntity = entity;
      if (entity.mesh && entity.mesh.userData && entity.mesh.userData.ring) {
        entity.mesh.userData.ring.visible = true;
      }
      updateConsoleUI(entity);
    }

    function clearSelection() {
      aoeState.selectedEntities.forEach(e => {
        if (e.mesh && e.mesh.userData && e.mesh.userData.ring) {
          e.mesh.userData.ring.visible = false;
        }
      });
      aoeState.selectedEntities = [];
      aoeState.selectedEntity = null;
      updateConsoleUI(null);
    }

    // Dynamic Tool Visuals on Villager
    function updateVillagerToolVisual(unit, type) {
      if (!unit.mesh.userData.axeGroup) return;
      unit.mesh.userData.axeGroup.visible = (type === 'wood');
      unit.mesh.userData.pickGroup.visible = (type === 'gold' || type === 'stone');
      unit.mesh.userData.hammerGroup.visible = (type === 'build');
    }

    // Update Console UI (Left portrait + Stats + Action Grid)
    function updateConsoleUI(entity) {
      const nameEl = document.getElementById('entity-name');
      const typeEl = document.getElementById('entity-type');
      const hpFill = document.getElementById('hp-bar-inner');
      const statHp = document.getElementById('stat-hp');
      const statAtk = document.getElementById('stat-atk');
      const statArm = document.getElementById('stat-arm');
      const statRng = document.getElementById('stat-rng');
      const tabsBar = document.getElementById('grid-tabs-bar');
      const grid = document.getElementById('action-grid');

      if (!entity) {
        nameEl.textContent = 'No Selection';
        typeEl.textContent = 'Select units or buildings';
        hpFill.style.width = '0%';
        statHp.textContent = '-';
        statAtk.textContent = '-';
        statArm.textContent = '-';
        statRng.textContent = '-';
        tabsBar.style.display = 'none';
        grid.innerHTML = '<div style="grid-column: 1/-1; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #8e6834;">Left-click units or drag box to issue commands.</div>';
        renderPortraitCanvas(null);
        return;
      }

      nameEl.textContent = entity.name;
      typeEl.textContent = (entity.team === 'player' ? '[BRITONS] ' : '[RIVAL RED] ') + (entity.isBuilding ? 'Structure' : 'Unit');

      const hpPct = Math.max(0, Math.min(100, (entity.hp / entity.maxHp) * 100));
      hpFill.style.width = hpPct + '%';
      hpFill.style.background = hpPct > 50 ? '#22c55e' : (hpPct > 25 ? '#eab308' : '#ef4444');

      statHp.textContent = `${Math.floor(entity.hp)} / ${entity.maxHp}`;
      statAtk.textContent = entity.attack || '0';
      statArm.textContent = `${entity.armor || 0} / ${entity.armor || 0}`;
      statRng.textContent = entity.range || '1';

      renderPortraitCanvas(entity);
      updateActionGrid();
    }

    // Render 2D Canvas Portrait
    function renderPortraitCanvas(entity) {
      const cvs = document.getElementById('portrait-canvas');
      const ctx = cvs.getContext('2d');
      ctx.fillStyle = '#1a1008';
      ctx.fillRect(0, 0, 64, 64);
      if (!entity) return;

      // Draw Heraldic Crest or Icon
      ctx.fillStyle = entity.team === 'enemy' ? '#dc2626' : '#2563eb';
      ctx.beginPath();
      ctx.arc(32, 28, 18, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffd700';
      ctx.font = 'bold 16px Georgia, serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const initial = entity.name ? entity.name[0] : 'U';
      ctx.fillText(initial, 32, 28);

      ctx.strokeStyle = '#c9933b';
      ctx.lineWidth = 2;
      ctx.strokeRect(1, 1, 62, 62);
    }

    // Switch Build Categories (Q: Eco, W: Mil)
    window.setBuildCategory = function(cat) {
      aoeState.buildCategory = cat;
      document.querySelectorAll('.grid-tab-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('tab-build-' + cat) || document.getElementById('tab-commands');
      if (activeBtn) activeBtn.classList.add('active');
      updateActionGrid();
    };

    // Update Action Grid Buttons Based on Selection
    function updateActionGrid() {
      const grid = document.getElementById('action-grid');
      const tabsBar = document.getElementById('grid-tabs-bar');
      grid.innerHTML = '';

      const entity = aoeState.selectedEntity;
      if (!entity || entity.team !== 'player') {
        tabsBar.style.display = 'none';
        return;
      }

      if (entity.type === 'villager') {
        tabsBar.style.display = 'flex';
        if (aoeState.buildCategory === 'eco') {
          // Economic Buildings
          renderActionButton(grid, 'House', '25W', () => startBuildingPlacement('house'), 'Q', aoeState.resources.wood >= 25);
          renderActionButton(grid, 'Mill', '100W', () => startBuildingPlacement('mill'), 'W', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Lumber Camp', '100W', () => startBuildingPlacement('lumber_camp'), 'E', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Mining Camp', '100W', () => startBuildingPlacement('mining_camp'), 'R', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Farm', '60W', () => startBuildingPlacement('farm'), 'T', aoeState.resources.wood >= 60);
          renderActionButton(grid, 'Town Center', '275W 100S', () => startBuildingPlacement('town_center'), 'A', aoeState.resources.wood >= 275 && aoeState.resources.stone >= 100 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
        } else if (aoeState.buildCategory === 'mil') {
          // Military Buildings
          renderActionButton(grid, 'Barracks', '175W', () => startBuildingPlacement('barracks'), 'Q', aoeState.resources.wood >= 175);
          renderActionButton(grid, 'Archery Range', '175W', () => startBuildingPlacement('archery_range'), 'W', aoeState.resources.wood >= 175 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Stable', '175W', () => startBuildingPlacement('stable'), 'E', aoeState.resources.wood >= 175 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Blacksmith', '150W', () => startBuildingPlacement('blacksmith'), 'R', aoeState.resources.wood >= 150 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Monastery', '175W', () => startBuildingPlacement('monastery'), 'T', aoeState.resources.wood >= 175 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
          renderActionButton(grid, 'Castle', '650S', () => startBuildingPlacement('castle'), 'A', aoeState.resources.stone >= 650 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
          renderActionButton(grid, 'Wonder', '1000W 1000G', () => startBuildingPlacement('wonder'), 'S', aoeState.resources.wood >= 1000 && aoeState.resources.gold >= 1000 && aoeState.resources.stone >= 1000 && aoeState.age === 'Imperial Age');
          renderActionButton(grid, 'Watchtower', '50W 125S', () => startBuildingPlacement('watchtower'), 'D', aoeState.resources.wood >= 50 && aoeState.resources.stone >= 125 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Stone Wall', '5S', () => startBuildingPlacement('wall'), 'F', aoeState.resources.stone >= 5 && aoeState.age !== 'Dark Age');
        } else {
          // Commands
          renderActionButton(grid, 'Stop', '', () => stopSelectedUnits(), 'S', true);
        }
      } else if (entity.type === 'town_center') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Create Villager', '50 Food', () => queueUnitProduction('villager', entity), 'Q', aoeState.resources.food >= 50 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Research Loom', '50 Gold', () => researchLoom(), 'W', aoeState.resources.gold >= 50 && !aoeState.loomResearched);
        renderActionButton(grid, 'Ring Town Bell', '', () => window.toggleTownBell(), 'B', true);
      } else if (entity.type === 'barracks') {
        tabsBar.style.display = 'none';
        const swordsmanType = aoeState.age === 'Dark Age' ? 'militia' : 'man_at_arms';
        renderActionButton(grid, 'Train ' + (swordsmanType === 'militia' ? 'Militia' : 'Man-at-Arms'), '60F 20G', () => queueUnitProduction(swordsmanType, entity), 'Q', aoeState.resources.food >= 60 && aoeState.resources.gold >= 20 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Train Spearman', '35F 25W', () => queueUnitProduction('spearman', entity), 'W', aoeState.resources.food >= 35 && aoeState.resources.wood >= 25 && aoeState.pop < aoeState.maxPop && aoeState.age !== 'Dark Age');
      } else if (entity.type === 'archery_range') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Archer', '25W 45G', () => queueUnitProduction('archer', entity), 'Q', aoeState.resources.wood >= 25 && aoeState.resources.gold >= 45 && aoeState.pop < aoeState.maxPop);
      } else if (entity.type === 'stable') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Scout', '80 Food', () => queueUnitProduction('scout', entity), 'Q', aoeState.resources.food >= 80 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Train Knight', '60F 75G', () => queueUnitProduction('knight', entity), 'W', aoeState.resources.food >= 60 && aoeState.resources.gold >= 75 && aoeState.pop < aoeState.maxPop && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
      } else if (entity.type === 'monastery') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Monk', '100 Gold', () => queueUnitProduction('monk', entity), 'Q', aoeState.resources.gold >= 100 && aoeState.pop < aoeState.maxPop);
      } else if (entity.type === 'castle') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Knight', '60F 75G', () => queueUnitProduction('knight', entity), 'Q', aoeState.resources.food >= 60 && aoeState.resources.gold >= 75 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Build Trebuchet', '200W 200G', () => queueUnitProduction('trebuchet', entity), 'W', aoeState.resources.wood >= 200 && aoeState.resources.gold >= 200 && aoeState.pop < aoeState.maxPop && aoeState.age === 'Imperial Age');
      } else {
        // Military Unit Stances
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Aggressive Stance', '', () => setUnitStance('aggressive'), 'A', true);
        renderActionButton(grid, 'Defensive Stance', '', () => setUnitStance('defensive'), 'D', true);
        renderActionButton(grid, 'Stand Ground', '', () => setUnitStance('stand_ground'), 'S', true);
        renderActionButton(grid, 'Stop', '', () => stopSelectedUnits(), 'Space', true);
      }
    }

    function renderActionButton(parent, name, cost, onClick, hotkey, enabled) {
      const btn = document.createElement('button');
      btn.className = 'action-btn';
      if (!enabled) btn.disabled = true;
      btn.onclick = () => {
        initAudio();
        onClick();
        updateResourceUI();
        updateActionGrid();
      };

      if (hotkey) {
        const hk = document.createElement('span');
        hk.className = 'btn-hotkey';
        hk.textContent = hotkey;
        btn.appendChild(hk);
      }

      const nm = document.createElement('span');
      nm.className = 'btn-name';
      nm.textContent = name;
      btn.appendChild(nm);

      if (cost) {
        const cs = document.createElement('span');
        cs.className = 'btn-cost';
        cs.textContent = cost;
        btn.appendChild(cs);
      }

      parent.appendChild(btn);
    }

    function stopSelectedUnits() {
      aoeState.selectedEntities.forEach(u => {
        u.dest = null;
        u.path = null;
        u.target = null;
        u.state = 'idle';
      });
      showAoENotice('[COMMAND] Halt.');
    }

    function setUnitStance(stance) {
      aoeState.selectedEntities.forEach(u => {
        u.stance = stance;
      });
      showAoENotice(`[STANCE] Set to ${stance.toUpperCase()}`);
    }

    function researchLoom() {
      if (aoeState.resources.gold < 50) return;
      aoeState.resources.gold -= 50;
      aoeState.loomResearched = true;
      friendlyUnits.filter(u => u.type === 'villager').forEach(v => {
        v.maxHp += 15;
        v.hp += 15;
        v.armor += 1;
      });
      playAdvanceAgeFanfare();
      showAoENotice('[RESEARCH COMPLETE: LOOM] Villagers gained +15 HP and +1 Armor!');
    }

    function queueUnitProduction(unitType, building) {
      const proto = UNIT_TYPES[unitType];
      if (!proto) return;

      if (aoeState.pop >= aoeState.maxPop) {
        showAoENotice('[HOUSES NEEDED] Build additional houses to support more population!');
        return;
      }

      for (const [res, amt] of Object.entries(proto.cost)) {
        if (aoeState.resources[res] < amt) {
          showAoENotice(`[INSUFFICIENT ${res.toUpperCase()}] Requires ${amt} ${res}.`);
          return;
        }
      }
      for (const [res, amt] of Object.entries(proto.cost)) {
        aoeState.resources[res] -= amt;
      }
      aoeState.pop++;

      if (!building.queue) building.queue = [];
      building.queue.push({
        type: unitType,
        proto,
        progress: 0,
        totalTime: proto.trainTime
      });

      playBuildingHammerSound();
      showAoENotice(`[TRAINING] ${proto.name} ordered.`);
      updateResourceUI();
    }

    // Building Placement Logic
    function startBuildingPlacement(bType) {
      const bDef = BUILDING_TYPES[bType];
      if (!bDef) return;

      cancelBuildingPlacement();
      aoeState.activePlacementType = bType;

      let ghost = null;
      if (bType === 'town_center') ghost = createTownCenterMesh(aoeState.age, false);
      else if (bType === 'house') ghost = createHouseMesh(aoeState.age, false);
      else if (bType === 'mill') ghost = createMillMesh();
      else if (bType === 'lumber_camp') ghost = createLumberCampMesh();
      else if (bType === 'mining_camp') ghost = createMiningCampMesh();
      else if (bType === 'farm') ghost = createFarmMesh();
      else if (bType === 'barracks') ghost = createBarracksMesh(false);
      else if (bType === 'archery_range') ghost = createArcheryRangeMesh(false);
      else if (bType === 'stable') ghost = createStableMesh(false);
      else if (bType === 'blacksmith') ghost = createBlacksmithMesh();
      else if (bType === 'monastery') ghost = createMonasteryMesh(false);
      else if (bType === 'castle') ghost = createCastleMesh(false);
      else if (bType === 'wonder') ghost = createWonderMesh();
      else if (bType === 'watchtower') ghost = createWatchtowerMesh(aoeState.age, false);
      else if (bType === 'wall') ghost = createWallMesh();

      if (ghost) {
        ghost.traverse(c => {
          if (c.isMesh) {
            c.material = c.material.clone();
            c.material.transparent = true;
            c.material.opacity = 0.55;
          }
        });
        scene.add(ghost);
        aoeState.placementGhost = ghost;
      }
      showAoENotice(`[CONSTRUCTION] Left-click ground to place ${bDef.name}. ESC to cancel.`);
    }

    function confirmBuildingPlacement() {
      const bType = aoeState.activePlacementType;
      const bDef = BUILDING_TYPES[bType];
      const ghost = aoeState.placementGhost;
      if (!bType || !bDef || !ghost) return;

      // Coordinate check & buildable test
      const snapX = ghost.position.x;
      const snapZ = ghost.position.z;
      const g = worldToGrid(snapX, snapZ);
      const sizeTiles = Math.max(1, Math.round(bDef.size / TILE_SIZE));

      if (!isTileBuildable(g.x, g.z, sizeTiles, sizeTiles)) {
        showAoENotice('[OBSTRUCTED] Cannot place structure on occupied, water, or cliff ground.');
        return;
      }

      for (const [res, amt] of Object.entries(bDef.cost)) {
        if (aoeState.resources[res] < amt) {
          showAoENotice(`[INSUFFICIENT ${res.toUpperCase()}] Requires ${amt} ${res}.`);
          return;
        }
      }
      for (const [res, amt] of Object.entries(bDef.cost)) {
        aoeState.resources[res] -= amt;
      }

      const pos = ghost.position.clone();
      cancelBuildingPlacement();

      // Spawn Building and mark grid blocked
      spawnBuilding(bType, pos.x, pos.z, 'player');
      occupyGridArea(pos.x, pos.z, sizeTiles, sizeTiles);

      playBuildingHammerSound();
      showAoENotice(`[CONSTRUCTED] ${bDef.name} placed!`);

      if (bDef.providesPop) {
        aoeState.maxPop = Math.min(200, aoeState.maxPop + bDef.providesPop);
      }

      if (bType === 'wonder') {
        aoeState.wonderActive = true;
        aoeState.wonderTimer = 200;
        document.getElementById('wonder-banner').style.display = 'flex';
        showAoENotice('[WONDER COMPLETED!] Imperial countdown initiated: Defend for 200 seconds!');
      }

      updateResourceUI();
      updateActionGrid();
    }

    function cancelBuildingPlacement() {
      if (aoeState.placementGhost) {
        scene.remove(aoeState.placementGhost);
        aoeState.placementGhost = null;
      }
      aoeState.activePlacementType = null;
    }
    """
