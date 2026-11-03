def get_aoe_sim_loop_js():
    return """
    // =========================================================================
    // RTS SELECTION, UI, COMMAND MOVEMENT, HUNTING & BUILDING PLACEMENT
    // =========================================================================

    let raycaster = new THREE.Raycaster();
    let mouse = new THREE.Vector2();
    let isMouseDown = false;
    let mouseDownScreen = { x: 0, y: 0 };
    let lastMouseScreen = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    let dragThreshold = 6;
    let isDragging = false;
    let selectionBoxEl = document.getElementById('selection-box');

    let cameraTargetPos = new THREE.Vector3(0, 0, 0);
    let cameraZoom = 36;
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

    window.addEventListener('wheel', e => {
      cameraZoom = Math.max(16, Math.min(65, cameraZoom + e.deltaY * 0.04));
    }, { passive: true });

    window.addEventListener('mousemove', e => {
      lastMouseScreen.x = e.clientX;
      lastMouseScreen.y = e.clientY;
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

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

      if (aoeState.placementGhost) {
        raycaster.setFromCamera(mouse, camera);
        const hits = raycaster.intersectObject(terrainMesh);
        if (hits.length > 0) {
          const pt = hits[0].point;
          const snapX = Math.round(pt.x / TILE_SIZE) * TILE_SIZE;
          const snapZ = Math.round(pt.z / TILE_SIZE) * TILE_SIZE;
          aoeState.placementGhost.position.set(snapX, getTerrainHeight(snapX, snapZ), snapZ);

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
      if (e.target.closest('#aoe-top-bar') || e.target.closest('#aoe-bottom-bar') || e.target.closest('.aoe-modal') || e.target.closest('#mission-hud')) {
        return;
      }
      initAudio();

      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      if (e.button === 0) { // Left Click
        if (aoeState.activePlacementType) {
          confirmBuildingPlacement();
          return;
        }
        isMouseDown = true;
        mouseDownScreen.x = e.clientX;
        mouseDownScreen.y = e.clientY;
        isDragging = false;
      } else if (e.button === 2) { // Right Click - Smart Command
        e.preventDefault();
        if (aoeState.activePlacementType) {
          cancelBuildingPlacement();
          return;
        }
        handleSmartRightClick(e);
      }
    });

    window.addEventListener('contextmenu', e => e.preventDefault());

    // Complete Left Click or Drag Selection
    window.addEventListener('mouseup', e => {
      if (e.button === 0 && isMouseDown) {
        isMouseDown = false;
        selectionBoxEl.style.display = 'none';

        if (isDragging) {
          // Box Selection
          const minX = Math.min(mouseDownScreen.x, e.clientX);
          const maxX = Math.max(mouseDownScreen.x, e.clientX);
          const minY = Math.min(mouseDownScreen.y, e.clientY);
          const maxY = Math.max(mouseDownScreen.y, e.clientY);

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
          // Single Click Selection with Prioritized Unit Raycasting
          raycaster.setFromCamera(mouse, camera);
          const selectableMeshes = [];
          allSelectable.forEach(item => {
            if (item.mesh && item.mesh.visible) {
              selectableMeshes.push(item.mesh);
            }
          });
          const intersects = raycaster.intersectObjects(selectableMeshes, true);
          if (intersects.length > 0) {
            // Find all hit entities
            const hitEntities = [];
            for (let hit of intersects) {
              let obj = hit.object;
              while (obj.parent && !obj.userData.entityRef) {
                obj = obj.parent;
              }
              if (obj.userData.entityRef && !hitEntities.includes(obj.userData.entityRef)) {
                hitEntities.push(obj.userData.entityRef);
              }
            }

            // Priority: Friendly Units > Enemy Units > Resources / Animals > Buildings
            const friendlyHit = hitEntities.find(ent => ent.isUnit && ent.team === 'player');
            const enemyHit = hitEntities.find(ent => ent.isUnit && ent.team === 'enemy');
            const resHit = hitEntities.find(ent => ent.isResource || ent.isWildAnimal);
            const target = friendlyHit || enemyHit || resHit || hitEntities[0];

            if (target) {
              selectSingleEntity(target);
              if (target.team === 'player') {
                playVoiceBark(target.type === 'villager' ? 'select' : 'attack');
              }
            }
          } else {
            clearSelection();
          }
        }
      }
    });

    // Smart Right Click: Move, Attack, Harvest, Hunt, Repair, Deposit, Garrison
    function handleSmartRightClick(e) {
      if (aoeState.selectedEntities.length === 0) return;

      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const selectableMeshes = allSelectable.map(item => item.mesh).filter(Boolean);
      const intersects = raycaster.intersectObjects(selectableMeshes, true);

      let targetEntity = null;
      if (intersects.length > 0) {
        const hitEntities = [];
        for (let hit of intersects) {
          let obj = hit.object;
          while (obj.parent && !obj.userData.entityRef) {
            obj = obj.parent;
          }
          if (obj.userData.entityRef && !hitEntities.includes(obj.userData.entityRef)) {
            hitEntities.push(obj.userData.entityRef);
          }
        }

        // Prioritize interactive targets: Enemy > Wild Animal > Resource > Damaged Building
        targetEntity = hitEntities.find(ent => ent.team === 'enemy') ||
                       hitEntities.find(ent => ent.isWildAnimal) ||
                       hitEntities.find(ent => ent.isResource) ||
                       hitEntities.find(ent => ent.isBuilding && ent.team === 'player' && (ent.hp < ent.maxHp || ent.type === 'town_center' || ent.type === 'mill' || ent.type === 'lumber_camp' || ent.type === 'mining_camp'));
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
        } else if (targetEntity.isWildAnimal) {
          // HUNT WILD ANIMAL COMMAND!
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager' && unit.state !== 'garrisoned') {
              unit.target = targetEntity;
              unit.state = 'hunting';
              updateVillagerToolVisual(unit, 'hunt');
            }
          });
          spawnMoveMarker(targetEntity.mesh.position);
          playVoiceBark('wood');
          showAoENotice('[HUNTING COMMAND] Stalking ' + targetEntity.name + ' for sustenance!');
        } else if (targetEntity.isResource) {
          // GATHER NATURAL RESOURCE COMMAND!
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
        } else if (targetEntity.isBuilding && targetEntity.team === 'player' && (targetEntity.type === 'town_center' || targetEntity.type === 'mill' || targetEntity.type === 'lumber_camp' || targetEntity.type === 'mining_camp')) {
          // DEPOSIT CARGO OR GARRISON
          let anyDeposited = false;
          aoeState.selectedEntities.forEach(unit => {
            if (unit.type === 'villager' && unit.carryAmount > 0 && unit.carryType) {
              aoeState.resources[unit.carryType] += unit.carryAmount;
              addPoints(Math.floor(unit.carryAmount), `Deposited ${unit.carryType}`);
              unit.carryAmount = 0;
              unit.carryType = null;
              if (unit.mesh.userData && unit.mesh.userData.cargoGroup) {
                unit.mesh.userData.cargoGroup.visible = false;
              }
              anyDeposited = true;
            }
          });
          if (anyDeposited) {
            playVoiceBark('move');
            showAoENotice('[RESOURCES DEPOSITED] Supplies safely stockpiled in storage.');
            updateResourceUI();
          } else if (targetEntity.type === 'town_center') {
            // Garrison
            aoeState.selectedEntities.forEach(unit => {
              if (unit.type === 'villager') {
                unit.state = 'garrisoned';
                unit.mesh.visible = false;
              }
            });
            showAoENotice('[GARRISON] Villagers sheltered inside Town Center.');
            updateResourceUI();
          }
        } else if (targetEntity.isBuilding && targetEntity.team === 'player' && targetEntity.hp < targetEntity.maxHp) {
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
        } else if (targetPos) {
          executeMoveCommand(targetPos);
        }
      } else if (targetPos) {
        executeMoveCommand(targetPos);
      }
    }

    function executeMoveCommand(targetPos) {
      const formationSlots = calculateFormationPositions(targetPos, aoeState.selectedEntities.length);
      aoeState.selectedEntities.forEach((unit, idx) => {
        if (unit.state !== 'garrisoned') {
          const dest = formationSlots[idx] || targetPos;
          const path = findAStarPath(unit.mesh.position.x, unit.mesh.position.z, dest.x, dest.z);
          unit.path = path;
          // Step towards next node immediately
          if (path && path.length > 1) {
            unit.path = path.slice(1);
            unit.dest = unit.path[0];
          } else {
            unit.path = [dest];
            unit.dest = dest;
          }
          unit.state = 'moving';
          unit.target = null;
        }
      });
      spawnMoveMarker(targetPos);
      playVoiceBark('move');
    }

    // Expanding Waypoint Rings
    function spawnMoveMarker(pos) {
      const geom = new THREE.RingGeometry(0.8, 1.25, 16);
      geom.rotateX(-Math.PI / 2);
      const mat = new THREE.MeshBasicMaterial({ color: 0x4ade80, side: THREE.DoubleSide, transparent: true, opacity: 1.0 });
      const m = new THREE.Mesh(geom, mat);
      m.position.set(pos.x, getTerrainHeight(pos.x, pos.z) + 0.15, pos.z);
      scene.add(m);
      let scale = 1.0;
      const anim = setInterval(() => {
        scale += 0.14;
        m.scale.set(scale, scale, scale);
        mat.opacity -= 0.12;
        if (mat.opacity <= 0) {
          clearInterval(anim);
          scene.remove(m);
        }
      }, 30);
    }

    function spawnAttackMarker(pos) {
      const geom = new THREE.RingGeometry(1.0, 1.55, 16);
      geom.rotateX(-Math.PI / 2);
      const mat = new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 1.0 });
      const m = new THREE.Mesh(geom, mat);
      m.position.set(pos.x, getTerrainHeight(pos.x, pos.z) + 0.2, pos.z);
      scene.add(m);
      let scale = 1.0;
      const anim = setInterval(() => {
        scale += 0.15;
        m.scale.set(scale, scale, scale);
        mat.opacity -= 0.12;
        if (mat.opacity <= 0) {
          clearInterval(anim);
          scene.remove(m);
        }
      }, 30);
    }

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

    function updateVillagerToolVisual(unit, type) {
      if (!unit.mesh.userData.axeGroup) return;
      unit.mesh.userData.axeGroup.visible = (type === 'wood');
      unit.mesh.userData.pickGroup.visible = (type === 'gold' || type === 'stone');
      unit.mesh.userData.hammerGroup.visible = (type === 'build');
      if (unit.mesh.userData.spearGroup) {
        unit.mesh.userData.spearGroup.visible = (type === 'hunt');
      }
    }

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
      const trainQueueBar = document.getElementById('train-queue-bar');

      if (!entity) {
        nameEl.textContent = 'No Selection';
        typeEl.textContent = 'Select units or buildings';
        hpFill.style.width = '0%';
        statHp.textContent = '-';
        statAtk.textContent = '-';
        statArm.textContent = '-';
        statRng.textContent = '-';
        tabsBar.style.display = 'none';
        trainQueueBar.style.display = 'none';
        grid.innerHTML = '<div style="grid-column: 1/-1; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #8e6834;">Left-click units or drag box to issue commands.</div>';
        renderPortraitCanvas(null);
        return;
      }

      nameEl.textContent = entity.name;
      typeEl.textContent = (entity.team === 'player' ? '[BRITONS] ' : '[RIVAL RED] ') + (entity.isBuilding ? 'Structure' : (entity.isWildAnimal ? 'Wild Game' : 'Unit'));

      const hpPct = Math.max(0, Math.min(100, (entity.hp / entity.maxHp) * 100));
      hpFill.style.width = hpPct + '%';
      hpFill.style.background = hpPct > 50 ? '#22c55e' : (hpPct > 25 ? '#eab308' : '#ef4444');

      statHp.textContent = `${Math.ceil(entity.hp)} / ${entity.maxHp}`;
      statAtk.textContent = entity.attack !== undefined ? entity.attack : '-';
      statArm.textContent = entity.armor !== undefined ? `${entity.armor}` : '-';
      statRng.textContent = entity.range !== undefined ? `${entity.range}m` : '-';

      renderPortraitCanvas(entity);
      updateActionGrid();
    }

    function renderPortraitCanvas(entity) {
      const cvs = document.getElementById('portrait-canvas');
      const ctx = cvs.getContext('2d');
      ctx.fillStyle = '#1c130c';
      ctx.fillRect(0, 0, 68, 68);
      if (!entity) return;

      ctx.fillStyle = entity.team === 'enemy' ? '#dc2626' : (entity.isWildAnimal ? '#78350f' : '#2563eb');
      ctx.beginPath();
      ctx.arc(34, 30, 20, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      const initials = entity.name.split(' ').map(s => s[0]).join('').slice(0, 3);
      ctx.fillText(initials, 34, 34);

      ctx.strokeStyle = '#c9933b';
      ctx.lineWidth = 2;
      ctx.strokeRect(1, 1, 66, 66);
    }

    window.setBuildCategory = function(cat) {
      aoeState.buildCategory = cat;
      document.querySelectorAll('.grid-tab-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById(`tab-build-${cat}`);
      if (activeBtn) activeBtn.classList.add('active');
      updateActionGrid();
    };

    function updateActionGrid() {
      const grid = document.getElementById('action-grid');
      const tabsBar = document.getElementById('grid-tabs-bar');
      const trainQueueBar = document.getElementById('train-queue-bar');
      grid.innerHTML = '';

      const entity = aoeState.selectedEntity;
      if (!entity) return;

      if (entity.type === 'villager') {
        tabsBar.style.display = 'flex';
        if (aoeState.buildCategory === 'eco') {
          renderActionButton(grid, 'House', '25W', () => startBuildingPlacement('house'), 'Q', aoeState.resources.wood >= 25);
          renderActionButton(grid, 'Mill', '100W', () => startBuildingPlacement('mill'), 'W', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Lumber Camp', '100W', () => startBuildingPlacement('lumber_camp'), 'E', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Mining Camp', '100W', () => startBuildingPlacement('mining_camp'), 'R', aoeState.resources.wood >= 100);
          renderActionButton(grid, 'Farm', '60W', () => startBuildingPlacement('farm'), 'T', aoeState.resources.wood >= 60);
          renderActionButton(grid, 'Town Center', '275W 100S', () => startBuildingPlacement('town_center'), 'A', aoeState.resources.wood >= 275 && aoeState.resources.stone >= 100 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
        } else if (aoeState.buildCategory === 'mil') {
          renderActionButton(grid, 'Barracks', '175W', () => startBuildingPlacement('barracks'), 'Q', aoeState.resources.wood >= 175);
          renderActionButton(grid, 'Archery Range', '175W', () => startBuildingPlacement('archery_range'), 'W', aoeState.resources.wood >= 175 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Stable', '175W', () => startBuildingPlacement('stable'), 'E', aoeState.resources.wood >= 175 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Blacksmith', '150W', () => startBuildingPlacement('blacksmith'), 'R', aoeState.resources.wood >= 150 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Monastery', '175W', () => startBuildingPlacement('monastery'), 'T', aoeState.resources.wood >= 175 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
          renderActionButton(grid, 'Castle', '650S', () => startBuildingPlacement('castle'), 'A', aoeState.resources.stone >= 650 && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
          renderActionButton(grid, 'Wonder', '1000WGS', () => startBuildingPlacement('wonder'), 'S', aoeState.resources.wood >= 1000 && aoeState.resources.gold >= 1000 && aoeState.resources.stone >= 1000 && aoeState.age === 'Imperial Age');
          renderActionButton(grid, 'Watchtower', '50W 125S', () => startBuildingPlacement('watchtower'), 'D', aoeState.resources.wood >= 50 && aoeState.resources.stone >= 125 && aoeState.age !== 'Dark Age');
          renderActionButton(grid, 'Stone Wall', '5S', () => startBuildingPlacement('wall'), 'F', aoeState.resources.stone >= 5 && aoeState.age !== 'Dark Age');
        } else {
          renderActionButton(grid, 'Stop', '', () => stopSelectedUnits(), 'S', true);
        }
      } else if (entity.type === 'town_center') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Villager', '50F', () => queueUnitProduction('villager', entity), 'Q', aoeState.resources.food >= 50 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Town Bell', '', () => window.toggleTownBell(), 'B', true);
      } else if (entity.type === 'barracks') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Militia', '60F 20G', () => queueUnitProduction('militia', entity), 'Q', aoeState.resources.food >= 60 && aoeState.resources.gold >= 20 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Train Spearman', '35F 25W', () => queueUnitProduction('spearman', entity), 'W', aoeState.resources.food >= 35 && aoeState.resources.wood >= 25 && aoeState.pop < aoeState.maxPop && aoeState.age !== 'Dark Age');
      } else if (entity.type === 'archery_range') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Archer', '25W 45G', () => queueUnitProduction('archer', entity), 'Q', aoeState.resources.wood >= 25 && aoeState.resources.gold >= 45 && aoeState.pop < aoeState.maxPop);
      } else if (entity.type === 'stable') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Scout', '80F', () => queueUnitProduction('scout', entity), 'Q', aoeState.resources.food >= 80 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Train Knight', '60F 75G', () => queueUnitProduction('knight', entity), 'W', aoeState.resources.food >= 60 && aoeState.resources.gold >= 75 && aoeState.pop < aoeState.maxPop && (aoeState.age === 'Castle Age' || aoeState.age === 'Imperial Age'));
      } else if (entity.type === 'castle') {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Train Knight', '60F 75G', () => queueUnitProduction('knight', entity), 'Q', aoeState.resources.food >= 60 && aoeState.resources.gold >= 75 && aoeState.pop < aoeState.maxPop);
        renderActionButton(grid, 'Build Trebuchet', '200W 200G', () => queueUnitProduction('trebuchet', entity), 'W', aoeState.resources.wood >= 200 && aoeState.resources.gold >= 200 && aoeState.pop < aoeState.maxPop && aoeState.age === 'Imperial Age');
      } else {
        tabsBar.style.display = 'none';
        renderActionButton(grid, 'Aggressive Stance', '', () => setUnitStance('aggressive'), 'A', true);
        renderActionButton(grid, 'Defensive Stance', '', () => setUnitStance('defensive'), 'D', true);
        renderActionButton(grid, 'Stand Ground', '', () => setUnitStance('stand'), 'S', true);
        renderActionButton(grid, 'Halt / Stop', '', () => stopSelectedUnits(), 'H', true);
      }
    }

    function renderActionButton(parent, label, cost, onClick, hotkey, isEnabled) {
      const btn = document.createElement('button');
      btn.className = 'action-btn';
      if (!isEnabled) btn.disabled = true;

      btn.innerHTML = `
        <span class="btn-hotkey">${hotkey}</span>
        <span class="btn-label">${label}</span>
        ${cost ? `<span class="btn-cost">${cost}</span>` : ''}
      `;
      btn.onclick = () => {
        if (isEnabled) {
          initAudio();
          onClick();
        }
      };
      parent.appendChild(btn);
    }

    function setUnitStance(stance) {
      aoeState.selectedEntities.forEach(u => {
        if (u.isUnit) u.stance = stance;
      });
      showAoENotice('[STANCE SET] ' + stance.toUpperCase());
    }

    function stopSelectedUnits() {
      aoeState.selectedEntities.forEach(u => {
        if (u.isUnit) {
          u.state = 'idle';
          u.path = null;
          u.dest = null;
          u.target = null;
        }
      });
      playVoiceBark('move');
    }

    function queueUnitProduction(unitType, building) {
      const uDef = UNIT_TYPES[unitType];
      if (!uDef) return;

      if (uDef.cost.food && aoeState.resources.food < uDef.cost.food) return;
      if (uDef.cost.wood && aoeState.resources.wood < uDef.cost.wood) return;
      if (uDef.cost.gold && aoeState.resources.gold < uDef.cost.gold) return;

      if (uDef.cost.food) aoeState.resources.food -= uDef.cost.food;
      if (uDef.cost.wood) aoeState.resources.wood -= uDef.cost.wood;
      if (uDef.cost.gold) aoeState.resources.gold -= uDef.cost.gold;

      aoeState.pop += 1;
      building.queue.push({
        type: unitType,
        timeRemaining: uDef.trainTime,
        totalTime: uDef.trainTime
      });

      playVoiceBark('build');
      showAoENotice('[QUEUE] ' + uDef.name + ' training commenced.');
      updateResourceUI();
    }

    function startBuildingPlacement(bType) {
      const bDef = BUILDING_TYPES[bType];
      if (!bDef) return;

      if (bDef.cost.wood && aoeState.resources.wood < bDef.cost.wood) {
        showAoENotice('[INSUFFICIENT WOOD] Requires ' + bDef.cost.wood + ' Wood.');
        return;
      }
      if (bDef.cost.stone && aoeState.resources.stone < bDef.cost.stone) {
        showAoENotice('[INSUFFICIENT STONE] Requires ' + bDef.cost.stone + ' Stone.');
        return;
      }

      cancelBuildingPlacement();

      aoeState.activePlacementType = bType;
      const ghostGeom = new THREE.BoxGeometry(bDef.size, 4, bDef.size);
      const ghostMat = new THREE.MeshBasicMaterial({ color: 0x22c55e, wireframe: true });
      const ghost = new THREE.Mesh(ghostGeom, ghostMat);
      ghost.position.set(0, 0, 0);
      scene.add(ghost);
      aoeState.placementGhost = ghost;

      showAoENotice('[BLUEPRINT ACTIVE] Left-click to place ' + bDef.name + ', Right-click to cancel.');
    }

    function cancelBuildingPlacement() {
      if (aoeState.placementGhost) {
        scene.remove(aoeState.placementGhost);
        aoeState.placementGhost = null;
      }
      aoeState.activePlacementType = null;
    }

    function confirmBuildingPlacement() {
      const bType = aoeState.activePlacementType;
      const bDef = BUILDING_TYPES[bType];
      const ghost = aoeState.placementGhost;
      if (!bType || !bDef || !ghost) return;

      const snapX = ghost.position.x;
      const snapZ = ghost.position.z;
      const g = worldToGrid(snapX, snapZ);
      const sizeTiles = Math.max(1, Math.round(bDef.size / TILE_SIZE));

      if (!isTileBuildable(g.x, g.z, sizeTiles, sizeTiles)) {
        showAoENotice('[CANNOT BUILD HERE] Terrain obstructed or uneven!');
        playVoiceBark('select');
        return;
      }

      if (bDef.cost.wood) aoeState.resources.wood -= bDef.cost.wood;
      if (bDef.cost.stone) aoeState.resources.stone -= bDef.cost.stone;

      const pos = ghost.position.clone();
      cancelBuildingPlacement();

      spawnBuilding(bType, pos.x, pos.z, 'player');
      occupyGridArea(pos.x, pos.z, sizeTiles, sizeTiles);

      if (bDef.providesPop) {
        aoeState.maxPop += bDef.providesPop;
      }

      addPoints(50, `Constructed ${bDef.name}`);
      triggerMissionProgress('build_house_lumber', 1);

      playVoiceBark('build');
      showAoENotice('[CONSTRUCTED] ' + bDef.name + ' foundation laid!');
      updateResourceUI();
    }

    // Dynamic Weather Controller
    window.cycleWeather = function() {
      const weathers = ['Sunny Noon', 'Misty Rain', 'Sunset Glow'];
      const nextIdx = (weathers.indexOf(aoeState.weather) + 1) % weathers.length;
      applyWeather(weathers[nextIdx]);
    };

    function applyWeather(mode) {
      aoeState.weather = mode;
      const btn = document.getElementById('btn-weather');
      if (btn) btn.textContent = `[WEATHER: ${mode.toUpperCase()}]`;

      if (mode === 'Sunny Noon') {
        scene.background.setHex(0x87ceeb);
        scene.fog.color.setHex(0xb0d8f0);
        sunLight.color.setHex(0xfffaed);
        sunLight.intensity = 1.45;
        showAoENotice('[WEATHER] Clear skies & radiant medieval sun.');
      } else if (mode === 'Misty Rain') {
        scene.background.setHex(0x5a6e7c);
        scene.fog.color.setHex(0x607380);
        sunLight.color.setHex(0xd0d8e0);
        sunLight.intensity = 0.85;
        playRainSound();
        showAoENotice('[WEATHER] Overcast skies & cool rainfall.');
      } else if (mode === 'Sunset Glow') {
        scene.background.setHex(0xb45309);
        scene.fog.color.setHex(0xd97706);
        sunLight.color.setHex(0xffaa44);
        sunLight.intensity = 1.6;
        showAoENotice('[WEATHER] Amber dusk & long evening shadows.');
      }
    }
    """
