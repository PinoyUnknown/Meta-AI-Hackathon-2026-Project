def get_aoe_world_director_js():
    return """
    // =========================================================================
    // PHASE 1 WORLD INITIALIZATION, SCREEN-EDGE PANNING & 60 FPS ENGINE LOOP
    // =========================================================================

    let terrainMesh = null;
    let waterMesh = null;

    function initAoEWorld() {
      // 1. Grassy Terrain (200x200 World Grid: -100m to +100m)
      const terrainGeom = new THREE.PlaneGeometry(200, 200, 64, 64);
      terrainGeom.rotateX(-Math.PI / 2);
      const posAttr = terrainGeom.attributes.position;
      for (let i = 0; i < posAttr.count; i++) {
        const x = posAttr.getX(i);
        const z = posAttr.getZ(i);
        let h = Math.sin(x * 0.03) * Math.cos(z * 0.03) * 1.8;
        // River gorge around x = -25
        if (x > -35 && x < -15) {
          h -= 3.5 * (1 - Math.abs(x + 25) / 10);
        }
        posAttr.setY(i, h);
      }
      terrainGeom.computeVertexNormals();

      const terrainMat = new THREE.MeshLambertMaterial({ map: grassTex });
      terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
      terrainMesh.receiveShadow = true;
      scene.add(terrainMesh);

      // 2. Classify River Water into Tilemap (-32 to -18)
      for (let gx = 0; gx < GRID_SIZE; gx++) {
        for (let gz = 0; gz < GRID_SIZE; gz++) {
          const w = gridToWorld(gx, gz);
          if (w.x >= -34 && w.x <= -16) {
            tilemapGrid[gz * GRID_SIZE + gx] = TILE_WATER;
          }
        }
      }

      // 3. River Water Mesh at x = -25
      const waterGeom = new THREE.PlaneGeometry(18, 200);
      waterGeom.rotateX(-Math.PI / 2);
      const waterMat = new THREE.MeshStandardMaterial({
        map: waterTex,
        roughness: 0.1,
        metalness: 0.8,
        transparent: true,
        opacity: 0.88
      });
      waterMesh = new THREE.Mesh(waterGeom, waterMat);
      waterMesh.position.set(-25, -1.8, 0);
      scene.add(waterMesh);

      // 4. Arched Cobblestone River Bridge at (x: -25, z: 0)
      const bridgeGroup = new THREE.Group();
      bridgeGroup.position.set(-25, -0.4, 0);
      const spanGeom = new THREE.BoxGeometry(22, 1.0, 7);
      const span = new THREE.Mesh(spanGeom, stoneMat);
      span.castShadow = true;
      span.receiveShadow = true;
      bridgeGroup.add(span);
      for (let z of [-3.4, 3.4]) {
        const rail = new THREE.Mesh(new THREE.BoxGeometry(22, 0.8, 0.35), stoneMat);
        rail.position.set(0, 0.8, z);
        bridgeGroup.add(rail);
      }
      scene.add(bridgeGroup);

      // Mark bridge tiles as Walkable across the river!
      for (let x = -35; x <= -15; x += 2) {
        for (let z = -4; z <= 4; z += 2) {
          const g = worldToGrid(x, z);
          tilemapGrid[g.z * GRID_SIZE + g.x] = TILE_WALKABLE;
        }
      }

      // 5. Forests (Oak & Pine clumps)
      spawnForestGrove(18, 16, 12);
      spawnForestGrove(-5, -28, 10);
      spawnForestGrove(30, -18, 14);
      spawnForestGrove(-65, 25, 12);

      // 6. Mineral Veins (Gold & Stone Outcrops)
      spawnMineralDeposit('gold', 15, -8, 4);
      spawnMineralDeposit('stone', 22, 10, 4);
      spawnMineralDeposit('gold', -55, -12, 4);
      spawnMineralDeposit('stone', -75, -35, 4);

      // 7. Forage Berry Bushes
      spawnForageBushes(8, 12, 5);
      spawnForageBushes(-50, -25, 4);

      // 8. Wildlife & Domestic Sheep
      spawnSheepFlock(4, 3, 4);
      spawnWildBoar(32, 20);
      spawnWildBoar(-45, 30);

      // 9. Holy Relics
      spawnRelic(0, 45);
      spawnRelic(-25, -45);
      spawnRelic(-15, -65);

      // 10. Initial Player Town Base (Team Blue)
      spawnBuilding('town_center', 0, 0, 'player');
      occupyGridArea(0, 0, 7, 7);
      spawnBuilding('house', -10, 8, 'player');
      occupyGridArea(-10, 8, 3, 3);

      spawnUnit('scout', 6, 4, 'player');
      spawnUnit('villager', 2, 6, 'player');
      spawnUnit('villager', -4, 4, 'player');
      spawnUnit('villager', 0, 8, 'player');

      // 11. Initial Rival Red Base Across the River (Automated Opponent)
      spawnBuilding('town_center', -65, -15, 'enemy');
      occupyGridArea(-65, -15, 7, 7);
      spawnBuilding('barracks', -55, -5, 'enemy');
      occupyGridArea(-55, -5, 5, 5);
      spawnBuilding('archery_range', -58, -25, 'enemy');
      occupyGridArea(-58, -25, 5, 5);
      spawnBuilding('castle', -80, -15, 'enemy');
      occupyGridArea(-80, -15, 10, 10);
      spawnBuilding('watchtower', -42, -5, 'enemy');
      occupyGridArea(-42, -5, 3, 3);

      spawnUnit('scout', -50, -12, 'enemy');
      spawnUnit('villager', -62, -10, 'enemy');
      spawnUnit('villager', -68, -20, 'enemy');
      spawnUnit('militia', -52, 0, 'enemy');
      spawnUnit('archer', -54, -8, 'enemy');

      updateFogOfWar();
      updateResourceUI();
    }

    // Spawners
    function spawnForestGrove(cx, cz, count) {
      for (let i = 0; i < count; i++) {
        const x = cx + (Math.random() - 0.5) * 18;
        const z = cz + (Math.random() - 0.5) * 18;
        const trunkGeom = new THREE.CylinderGeometry(0.35, 0.5, 4.5, 6);
        const trunk = new THREE.Mesh(trunkGeom, timberMat);
        trunk.position.set(x, 2.25, z);
        trunk.castShadow = true;

        const canopyGeom = new THREE.ConeGeometry(2.4, 6, 7);
        const canopyMat = new THREE.MeshLambertMaterial({ color: Math.random() > 0.5 ? 0x2d5a27 : 0x1e4620 });
        const canopy = new THREE.Mesh(canopyGeom, canopyMat);
        canopy.position.set(x, 6.5, z);
        canopy.castShadow = true;

        const treeGroup = new THREE.Group();
        treeGroup.add(trunk);
        treeGroup.add(canopy);
        scene.add(treeGroup);

        occupyGridArea(x, z, 1, 1);

        const resObj = {
          id: nextEntityId++,
          name: 'Oak Tree',
          isResource: true,
          resType: 'wood',
          amount: 200,
          mesh: treeGroup
        };
        treeGroup.userData.entityRef = resObj;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnMineralDeposit(type, cx, cz, count) {
      const isGold = type === 'gold';
      const col = isGold ? 0xd4af37 : 0x808080;
      const mat = new THREE.MeshLambertMaterial({ color: col });

      for (let i = 0; i < count; i++) {
        const x = cx + (Math.random() - 0.5) * 8;
        const z = cz + (Math.random() - 0.5) * 8;
        const geom = new THREE.DodecahedronGeometry(1.4 + Math.random() * 0.4);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.set(x, 1.2, z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        scene.add(mesh);

        occupyGridArea(x, z, 1, 1);

        const resObj = {
          id: nextEntityId++,
          name: isGold ? 'Gold Vein' : 'Stone Outcropping',
          isResource: true,
          resType: type,
          amount: 800,
          mesh: mesh
        };
        mesh.userData.entityRef = resObj;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnForageBushes(cx, cz, count) {
      const bushMat = new THREE.MeshLambertMaterial({ color: 0x3d702d });
      const berryMat = new THREE.MeshLambertMaterial({ color: 0xd92626 });

      for (let i = 0; i < count; i++) {
        const x = cx + (Math.random() - 0.5) * 6;
        const z = cz + (Math.random() - 0.5) * 6;
        const group = new THREE.Group();
        const b = new THREE.Mesh(new THREE.SphereGeometry(1.1, 7, 7), bushMat);
        b.position.set(x, 0.9, z);
        group.add(b);

        for (let j = 0; j < 6; j++) {
          const berry = new THREE.Mesh(new THREE.SphereGeometry(0.2, 5, 5), berryMat);
          berry.position.set(x + (Math.random() - 0.5) * 1.4, 1.2 + Math.random() * 0.4, z + (Math.random() - 0.5) * 1.4);
          group.add(berry);
        }
        scene.add(group);

        const resObj = {
          id: nextEntityId++,
          name: 'Berry Bush',
          isResource: true,
          resType: 'food',
          amount: 150,
          mesh: group
        };
        group.userData.entityRef = resObj;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnSheepFlock(cx, cz, count) {
      for (let i = 0; i < count; i++) {
        const mesh = createSheepMesh();
        const x = cx + (Math.random() - 0.5) * 6;
        const z = cz + (Math.random() - 0.5) * 6;
        mesh.position.set(x, 0, z);
        scene.add(mesh);

        const resObj = {
          id: nextEntityId++,
          name: 'Sheep',
          isResource: true,
          resType: 'food',
          amount: 100,
          mesh: mesh
        };
        mesh.userData.entityRef = resObj;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnWildBoar(x, z) {
      const mesh = createBoarMesh();
      mesh.position.set(x, 0, z);
      scene.add(mesh);

      const resObj = {
        id: nextEntityId++,
        name: 'Wild Boar',
        isResource: true,
        resType: 'food',
        amount: 350,
        mesh: mesh
      };
      mesh.userData.entityRef = resObj;
      naturalResources.push(resObj);
      allSelectable.push(resObj);
    }

    function spawnRelic(x, z) {
      const mesh = createRelicMesh();
      mesh.position.set(x, 0, z);
      scene.add(mesh);

      const relicObj = {
        id: nextEntityId++,
        name: 'Holy Relic',
        isRelic: true,
        carriedBy: null,
        mesh: mesh
      };
      mesh.userData.entityRef = relicObj;
      holyRelics.push(relicObj);
      allSelectable.push(relicObj);
    }

    function spawnBuilding(type, x, z, team) {
      const def = BUILDING_TYPES[type];
      const isEnemy = (team === 'enemy');
      let mesh = null;

      if (type === 'town_center') mesh = createTownCenterMesh(aoeState.age, isEnemy);
      else if (type === 'house') mesh = createHouseMesh(aoeState.age, isEnemy);
      else if (type === 'mill') mesh = createMillMesh();
      else if (type === 'lumber_camp') mesh = createLumberCampMesh();
      else if (type === 'mining_camp') mesh = createMiningCampMesh();
      else if (type === 'farm') mesh = createFarmMesh();
      else if (type === 'barracks') mesh = createBarracksMesh(isEnemy);
      else if (type === 'archery_range') mesh = createArcheryRangeMesh(isEnemy);
      else if (type === 'stable') mesh = createStableMesh(isEnemy);
      else if (type === 'blacksmith') mesh = createBlacksmithMesh();
      else if (type === 'monastery') mesh = createMonasteryMesh(isEnemy);
      else if (type === 'castle') mesh = createCastleMesh(isEnemy);
      else if (type === 'wonder') mesh = createWonderMesh();
      else if (type === 'watchtower') mesh = createWatchtowerMesh(aoeState.age, isEnemy);
      else if (type === 'wall') mesh = createWallMesh();

      if (!mesh) return null;
      mesh.position.set(x, 0, z);
      scene.add(mesh);

      const bObj = {
        id: nextEntityId++,
        type,
        name: def.name,
        team,
        isBuilding: true,
        hp: def.hp,
        maxHp: def.hp,
        attack: (type === 'town_center' ? 5 : (type === 'castle' ? 11 : (type === 'watchtower' ? 5 : 0))),
        armor: (type === 'castle' ? 8 : 3),
        range: (type === 'castle' ? 18 : (type === 'watchtower' ? 14 : 6)),
        mesh,
        queue: []
      };

      mesh.userData.entityRef = bObj;
      if (team === 'player') friendlyBuildings.push(bObj);
      else enemyBuildings.push(bObj);
      allSelectable.push(bObj);

      return bObj;
    }

    function spawnUnit(type, x, z, team) {
      const def = UNIT_TYPES[type] || UNIT_TYPES.villager;
      const isEnemy = (team === 'enemy');
      let mesh = null;

      if (type === 'villager') mesh = createVillagerMesh(isEnemy);
      else if (type === 'scout') mesh = createScoutMesh(isEnemy);
      else if (type === 'militia' || type === 'man_at_arms') mesh = createSwordsmanMesh(isEnemy, 1);
      else if (type === 'spearman') mesh = createSpearmanMesh(isEnemy);
      else if (type === 'archer') mesh = createArcherMesh(isEnemy);
      else if (type === 'knight') mesh = createKnightMesh(isEnemy);
      else if (type === 'monk') mesh = createMonkMesh(isEnemy);
      else if (type === 'trebuchet') mesh = createTrebuchetMesh(isEnemy);

      if (!mesh) return null;
      mesh.position.set(x, 0, z);
      scene.add(mesh);

      const uObj = {
        id: nextEntityId++,
        type,
        name: def.name,
        team,
        isUnit: true,
        hp: def.hp,
        maxHp: def.hp,
        attack: def.attack,
        armor: def.armor,
        range: def.range,
        speed: def.speed,
        state: 'idle',
        stance: 'aggressive',
        path: null,
        dest: null,
        target: null,
        carryType: null,
        carryAmount: 0,
        mesh
      };

      mesh.userData.entityRef = uObj;
      if (team === 'player') friendlyUnits.push(uObj);
      else enemyUnits.push(uObj);
      allSelectable.push(uObj);

      return uObj;
    }

    function refreshBuildingVisuals() {
      friendlyBuildings.forEach(b => {
        if (b.type === 'town_center' || b.type === 'house' || b.type === 'watchtower') {
          const oldPos = b.mesh.position.clone();
          scene.remove(b.mesh);
          let newMesh = null;
          if (b.type === 'town_center') newMesh = createTownCenterMesh(aoeState.age, false);
          else if (b.type === 'house') newMesh = createHouseMesh(aoeState.age, false);
          else if (b.type === 'watchtower') newMesh = createWatchtowerMesh(aoeState.age, false);
          if (newMesh) {
            newMesh.position.copy(oldPos);
            scene.add(newMesh);
            b.mesh = newMesh;
            newMesh.userData.entityRef = b;
          }
        }
      });
    }

    // Rival Automated Opponent Director
    let rivalGameTime = 0;
    let lastWaveIndex = 0;

    function updateRivalDirector(dt) {
      rivalGameTime += dt;

      // Wave 1 at 120s (2m): 2 Militia
      if (rivalGameTime > 120 && lastWaveIndex < 1) {
        lastWaveIndex = 1;
        showAoENotice('[ALERT] Rival Clan raiding party spotted crossing the river bridge!');
        const r1 = spawnUnit('militia', -25, 4, 'enemy');
        const r2 = spawnUnit('militia', -25, -4, 'enemy');
        r1.dest = new THREE.Vector3(0, 0, 0);
        r1.state = 'attacking';
        r2.dest = new THREE.Vector3(0, 0, 0);
        r2.state = 'attacking';
      }

      // Wave 2 at 300s (5m): 3 Archers, 2 Spearmen
      if (rivalGameTime > 300 && lastWaveIndex < 2) {
        lastWaveIndex = 2;
        showAoENotice('[WAR ALERT] Rival Feudal Army advancing toward your settlement!');
        for (let i = 0; i < 3; i++) {
          const a = spawnUnit('archer', -25, (i - 1) * 3, 'enemy');
          a.dest = new THREE.Vector3(0, 0, 0);
          a.state = 'attacking';
        }
        for (let i = 0; i < 2; i++) {
          const s = spawnUnit('spearman', -25, (i - 0.5) * 4, 'enemy');
          s.dest = new THREE.Vector3(0, 0, 0);
          s.state = 'attacking';
        }
      }

      // Wave 3 at 540s (9m): 4 Knights, 4 Archers, 1 Trebuchet
      if (rivalGameTime > 540 && lastWaveIndex < 3) {
        lastWaveIndex = 3;
        showAoENotice('[IMPERIAL SIEGE] Rival Knights and Trebuchet assault incoming!');
        for (let i = 0; i < 4; i++) {
          const k = spawnUnit('knight', -25, (i - 1.5) * 3, 'enemy');
          k.dest = new THREE.Vector3(0, 0, 0);
          k.state = 'attacking';
        }
        const treb = spawnUnit('trebuchet', -25, 0, 'enemy');
        treb.dest = new THREE.Vector3(-5, 0, 0);
        treb.state = 'attacking';
      }
    }

    // =========================================================================
    // MAIN SIMULATION UPDATE (PHASE 1 CAMERA & MOVEMENT CONSTRAINTS)
    // =========================================================================
    let lastTime = performance.now();

    function updateSimulation() {
      const now = performance.now();
      const dt = Math.min(0.1, (now - lastTime) / 1000);
      lastTime = now;

      // 1. WASD Panning & Screen-Edge Mouse Panning
      const panSpeed = 35 * dt;
      if (keysPressed['KeyA'] || keysPressed['ArrowLeft']) cameraTargetPos.x -= panSpeed;
      if (keysPressed['KeyD'] || keysPressed['ArrowRight']) cameraTargetPos.x += panSpeed;
      if (keysPressed['KeyW'] || keysPressed['ArrowUp']) cameraTargetPos.z -= panSpeed;
      if (keysPressed['KeyS'] || keysPressed['ArrowDown']) cameraTargetPos.z += panSpeed;

      // Screen-Edge Mouse Panning (when cursor hits within 25px of viewport edge)
      const edgeMargin = 25;
      const edgeSpeed = 38 * dt;
      if (lastMouseScreen.x < edgeMargin && lastMouseScreen.x >= 0) cameraTargetPos.x -= edgeSpeed;
      if (lastMouseScreen.x > window.innerWidth - edgeMargin && lastMouseScreen.x <= window.innerWidth) cameraTargetPos.x += edgeSpeed;
      if (lastMouseScreen.y < edgeMargin && lastMouseScreen.y >= 0) cameraTargetPos.z -= edgeSpeed;
      if (lastMouseScreen.y > window.innerHeight - edgeMargin && lastMouseScreen.y <= window.innerHeight) cameraTargetPos.z += edgeSpeed;

      // Constrain Camera to 200x200 World Grid (-85m to +85m target bounds)
      cameraTargetPos.x = Math.max(-85, Math.min(85, cameraTargetPos.x));
      cameraTargetPos.z = Math.max(-85, Math.min(85, cameraTargetPos.z));

      // Isometric Top-Down Camera Perspective
      camera.position.x = cameraTargetPos.x;
      camera.position.y = cameraZoom * 0.75;
      camera.position.z = cameraTargetPos.z + cameraZoom;
      camera.lookAt(cameraTargetPos.x, 0, cameraTargetPos.z);

      // 2. Animate Mill Rotors
      friendlyBuildings.concat(enemyBuildings).forEach(b => {
        if (b.type === 'mill' && b.mesh && b.mesh.userData && b.mesh.userData.rotor) {
          b.mesh.userData.rotor.rotation.z += 1.5 * dt;
        }
      });

      // 3. Update Building Training Queues
      friendlyBuildings.forEach(b => {
        if (b.queue && b.queue.length > 0) {
          const item = b.queue[0];
          item.progress += dt;
          if (aoeState.selectedEntity === b) {
            document.getElementById('train-queue-bar').style.display = 'flex';
            const pct = Math.min(100, (item.progress / item.totalTime) * 100);
            document.getElementById('queue-fill').style.width = pct + '%';
            document.getElementById('queue-slots').textContent = `Queue: ${b.queue.length}`;
          }
          if (item.progress >= item.totalTime) {
            b.queue.shift();
            spawnUnit(item.type, b.mesh.position.x + (Math.random() - 0.5) * 6, b.mesh.position.z + 5, 'player');
            playBuildingHammerSound();
            showAoENotice(`[UNIT READY] ${item.proto.name} trained!`);
            if (b.queue.length === 0 && aoeState.selectedEntity === b) {
              document.getElementById('train-queue-bar').style.display = 'none';
            }
          }
        }
      });

      // 4. Update Friendly & Enemy Units (FSM & A* Navigation)
      const allActiveUnits = friendlyUnits.concat(enemyUnits);
      allActiveUnits.forEach(u => {
        if (u.hp <= 0 || u.state === 'garrisoned') return;

        // Move along A* waypoint path
        if (u.dest) {
          const dir = new THREE.Vector3().subVectors(u.dest, u.mesh.position);
          dir.y = 0;
          const dist = dir.length();
          if (dist > 0.6) {
            dir.normalize();
            u.mesh.position.addScaledVector(dir, u.speed * 60 * dt);
            u.mesh.rotation.y = Math.atan2(dir.x, dir.z);
          } else {
            if (u.path && u.path.length > 1) {
              u.path.shift();
              u.dest = u.path[0];
            } else {
              u.dest = null;
              u.path = null;
              if (u.state === 'moving') u.state = 'idle';
            }
          }
        }

        // AGGRO RADIUS & COMBAT FSM (14m Aggro Sphere)
        if (u.stance === 'aggressive' && u.state === 'idle' && u.type !== 'villager') {
          const opponents = (u.team === 'player' ? enemyUnits : friendlyUnits);
          let closestOpponent = null;
          let closestDist = 14;
          opponents.forEach(opp => {
            if (opp.hp > 0 && opp.state !== 'garrisoned') {
              const d = u.mesh.position.distanceTo(opp.mesh.position);
              if (d < closestDist) {
                closestDist = d;
                closestOpponent = opp;
              }
            }
          });
          if (closestOpponent) {
            u.target = closestOpponent;
            u.state = 'attacking';
          }
        }

        // Villager Gathering Routine (FSM)
        if (u.type === 'villager' && u.state === 'gathering' && u.target) {
          const tgtPos = u.target.mesh.position;
          const dist = u.mesh.position.distanceTo(tgtPos);
          if (dist > 2.5) {
            const dir = new THREE.Vector3().subVectors(tgtPos, u.mesh.position).normalize();
            u.mesh.position.addScaledVector(dir, u.speed * 60 * dt);
            u.mesh.rotation.y = Math.atan2(dir.x, dir.z);
          } else {
            u.carryAmount += 2.5 * dt;
            u.carryType = u.target.resType;
            if (u.mesh.userData.cargoGroup) {
              u.mesh.userData.cargoGroup.visible = true;
            }
            if (u.carryAmount >= 10) {
              const dropOff = findNearestDropOff(u);
              if (dropOff) {
                u.state = 'depositing';
                u.dest = dropOff.mesh.position.clone();
              }
            }
          }
        }

        // Villager Depositing Routine (FSM)
        if (u.type === 'villager' && u.state === 'depositing' && u.dest) {
          const dist = u.mesh.position.distanceTo(u.dest);
          if (dist <= 3.5) {
            if (u.team === 'player' && u.carryType) {
              aoeState.resources[u.carryType] += u.carryAmount;
            }
            u.carryAmount = 0;
            if (u.mesh.userData.cargoGroup) u.mesh.userData.cargoGroup.visible = false;
            updateResourceUI();
            if (u.target && u.target.amount > 0) {
              u.state = 'gathering';
              u.dest = null;
            } else {
              u.state = 'idle';
            }
          }
        }

        // Combat Routine with Rock-Paper-Scissors Damage
        if (u.state === 'attacking' && u.target) {
          const tgt = u.target;
          if (tgt.hp <= 0) {
            u.target = null;
            u.state = 'idle';
            return;
          }
          const dist = u.mesh.position.distanceTo(tgt.mesh.position);
          if (dist > u.range) {
            const dir = new THREE.Vector3().subVectors(tgt.mesh.position, u.mesh.position).normalize();
            u.mesh.position.addScaledVector(dir, u.speed * 60 * dt);
            u.mesh.rotation.y = Math.atan2(dir.x, dir.z);
          } else {
            u.attackCooldown = (u.attackCooldown || 0) + dt;
            if (u.attackCooldown >= 1.2) {
              u.attackCooldown = 0;
              const dmg = calculateDamage(u, tgt);
              tgt.hp -= dmg;
              if (u.type === 'archer') {
                playArrowReleaseSound();
                spawnArrowProjectile(u.mesh.position, tgt.mesh.position);
              } else {
                playSwordClashSound();
              }
              if (tgt.hp <= 0) {
                destroyEntity(tgt);
                u.target = null;
                u.state = 'idle';
              }
            }
          }
        }
      });

      // 5. Update Flying Arrow Projectiles
      for (let i = aoeState.projectiles.length - 1; i >= 0; i--) {
        const p = aoeState.projectiles[i];
        p.progress += dt * 3.5;
        p.mesh.position.lerpVectors(p.start, p.end, p.progress);
        p.mesh.position.y += Math.sin(p.progress * Math.PI) * 2.5;
        if (p.progress >= 1.0) {
          scene.remove(p.mesh);
          aoeState.projectiles.splice(i, 1);
        }
      }

      // 6. Update Wonder Victory Countdown
      if (aoeState.wonderActive && !aoeState.gameWon) {
        aoeState.wonderTimer -= dt;
        const wTimerEl = document.getElementById('wonder-timer');
        if (wTimerEl) wTimerEl.textContent = Math.ceil(aoeState.wonderTimer) + 's';
        if (aoeState.wonderTimer <= 0) {
          triggerGameVictory('Wonder of the World Defended! Imperial Reign Eternal!');
        }
      }

      // 7. Update Rival Wave Director & Fog of War
      updateRivalDirector(dt);
      updateFogOfWar();

      // 8. Render Minimap
      renderMinimapCanvas();
    }

    function spawnArrowProjectile(start, end) {
      const geom = new THREE.CylinderGeometry(0.04, 0.04, 1.2, 4);
      const mat = new THREE.MeshBasicMaterial({ color: 0x1f1f1f });
      const arrow = new THREE.Mesh(geom, mat);
      arrow.position.copy(start);
      arrow.position.y += 1.5;
      scene.add(arrow);
      aoeState.projectiles.push({
        mesh: arrow,
        start: arrow.position.clone(),
        end: end.clone(),
        progress: 0
      });
    }

    function findNearestDropOff(unit) {
      const buildings = unit.team === 'player' ? friendlyBuildings : enemyBuildings;
      let nearest = null;
      let minDist = 9999;
      buildings.forEach(b => {
        if (b.type === 'town_center' || (unit.carryType === 'food' && b.type === 'mill') || (unit.carryType === 'wood' && b.type === 'lumber_camp') || ((unit.carryType === 'gold' || unit.carryType === 'stone') && b.type === 'mining_camp')) {
          const d = unit.mesh.position.distanceTo(b.mesh.position);
          if (d < minDist) {
            minDist = d;
            nearest = b;
          }
        }
      });
      return nearest;
    }

    function destroyEntity(entity) {
      if (entity.mesh) scene.remove(entity.mesh);
      showAoENotice(`[FALLEN] ${entity.name} destroyed!`);
      // Free grid area if building
      if (entity.isBuilding) {
        const bDef = BUILDING_TYPES[entity.type];
        const sizeTiles = Math.max(1, Math.round((bDef ? bDef.size : 4) / TILE_SIZE));
        freeGridArea(entity.mesh.position.x, entity.mesh.position.z, sizeTiles, sizeTiles);
      }
      if (entity.team === 'enemy' && (entity.type === 'town_center' || entity.type === 'castle')) {
        const remainingDef = enemyBuildings.filter(b => (b.type === 'town_center' || b.type === 'castle') && b.hp > 0);
        if (remainingDef.length === 0) {
          triggerGameVictory('Conquest Complete! All rival fortifications razed!');
        }
      }
    }

    function triggerGameVictory(msg) {
      aoeState.gameWon = true;
      playAdvanceAgeFanfare();
      showAoENotice('[VICTORY ACHIEVED!] ' + msg, 10000);
      alert('[VICTORY!] ' + msg);
    }

    function updateHoverTooltip(e) {
      const tip = document.getElementById('hover-tooltip');
      const title = document.getElementById('tip-title');
      const sub = document.getElementById('tip-sub');

      raycaster.setFromCamera(mouse, camera);
      const selectableMeshes = allSelectable.map(item => item.mesh).filter(Boolean);
      const intersects = raycaster.intersectObjects(selectableMeshes, true);

      if (intersects.length > 0) {
        let hitObj = intersects[0].object;
        while (hitObj.parent && !hitObj.userData.entityRef) {
          hitObj = hitObj.parent;
        }
        const ref = hitObj.userData.entityRef;
        if (ref) {
          tip.style.display = 'block';
          tip.style.left = e.clientX + 'px';
          tip.style.top = e.clientY + 'px';
          title.textContent = ref.name;
          if (ref.isResource) {
            sub.textContent = `Resource: ${ref.resType.toUpperCase()} (${ref.amount} remaining)`;
          } else if (ref.isBuilding) {
            sub.textContent = `[${ref.team.toUpperCase()}] HP: ${Math.floor(ref.hp)}/${ref.maxHp}`;
          } else {
            sub.textContent = `[${ref.team.toUpperCase()}] HP: ${Math.floor(ref.hp)}/${ref.maxHp} &bull; State: ${ref.state}`;
          }
          return;
        }
      }
      tip.style.display = 'none';
    }

    // Render Minimap Radar (200x200 World Grid)
    function renderMinimapCanvas() {
      const cvs = document.getElementById('minimap-canvas');
      const ctx = cvs.getContext('2d');
      const w = cvs.width;
      const h = cvs.height;

      ctx.fillStyle = '#223816';
      ctx.fillRect(0, 0, w, h);

      // River Ribbon around x = -25
      ctx.fillStyle = '#1e5f8f';
      const riverX = (( -25 + 100 ) / 200) * w;
      ctx.fillRect(riverX - 5, 0, 10, h);

      // Bridge
      ctx.fillStyle = '#7a7a7a';
      ctx.fillRect(riverX - 7, h / 2 - 4, 14, 8);

      // Resources
      naturalResources.forEach(r => {
        if (!r.mesh) return;
        const rx = ((r.mesh.position.x + 100) / 200) * w;
        const rz = ((r.mesh.position.z + 100) / 200) * h;
        ctx.fillStyle = r.resType === 'wood' ? '#14532d' : (r.resType === 'gold' ? '#eab308' : '#94a3b8');
        ctx.fillRect(rx - 1, rz - 1, 2, 2);
      });

      // Player Buildings (Blue) & Units (Cyan)
      ctx.fillStyle = '#2563eb';
      friendlyBuildings.forEach(b => {
        if (b.hp <= 0) return;
        const bx = ((b.mesh.position.x + 100) / 200) * w;
        const bz = ((b.mesh.position.z + 100) / 200) * h;
        ctx.fillRect(bx - 3, bz - 3, 6, 6);
      });

      ctx.fillStyle = '#38bdf8';
      friendlyUnits.forEach(u => {
        if (u.hp <= 0 || u.state === 'garrisoned') return;
        const ux = ((u.mesh.position.x + 100) / 200) * w;
        const uz = ((u.mesh.position.z + 100) / 200) * h;
        ctx.fillRect(ux - 1.5, uz - 1.5, 3, 3);
      });

      // Enemy Buildings (Red) & Units (Crimson)
      ctx.fillStyle = '#dc2626';
      enemyBuildings.forEach(b => {
        if (b.hp <= 0) return;
        const g = worldToGrid(b.mesh.position.x, b.mesh.position.z);
        if (fogOfWarGrid[g.z * GRID_SIZE + g.x] > 0) {
          const bx = ((b.mesh.position.x + 100) / 200) * w;
          const bz = ((b.mesh.position.z + 100) / 200) * h;
          ctx.fillRect(bx - 3, bz - 3, 6, 6);
        }
      });

      ctx.fillStyle = '#f87171';
      enemyUnits.forEach(u => {
        if (u.hp <= 0 || !u.mesh.visible) return;
        const ux = ((u.mesh.position.x + 100) / 200) * w;
        const uz = ((u.mesh.position.z + 100) / 200) * h;
        ctx.fillRect(ux - 1.5, uz - 1.5, 3, 3);
      });

      // Camera Frustum Box
      const camX = ((cameraTargetPos.x + 100) / 200) * w;
      const camZ = ((cameraTargetPos.z + 100) / 200) * h;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(camX - 16, camZ - 12, 32, 24);
    }

    // Minimap Click-to-Pan (200x200 World Grid)
    const minimapWrapper = document.getElementById('minimap-wrapper');
    minimapWrapper.addEventListener('click', e => {
      const rect = minimapWrapper.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;
      const worldX = (clickX / rect.width) * 200 - 100;
      const worldZ = (clickY / rect.height) * 200 - 100;
      cameraTargetPos.set(worldX, 0, worldZ);
    });

    // Save & Load Functions
    window.saveAoEGame = function() {
      const saveObj = {
        age: aoeState.age,
        resources: aoeState.resources,
        pop: aoeState.pop,
        maxPop: aoeState.maxPop,
        rivalGameTime,
        friendlyUnits: friendlyUnits.map(u => ({ type: u.type, x: u.mesh.position.x, z: u.mesh.position.z, hp: u.hp })),
        friendlyBuildings: friendlyBuildings.map(b => ({ type: b.type, x: b.mesh.position.x, z: b.mesh.position.z, hp: b.hp }))
      };
      localStorage.setItem('aoe_empire_save', JSON.stringify(saveObj));
      playAdvanceAgeFanfare();
      showAoENotice('[EMPIRE RECORDED] Game status saved to browser memory (F5).');
    };

    window.loadAoEGame = function() {
      const saved = localStorage.getItem('aoe_empire_save');
      if (!saved) {
        showAoENotice('[NO SAVE DETECTED] No prior saved empire found.');
        return;
      }
      const data = JSON.parse(saved);
      aoeState.age = data.age;
      aoeState.resources = data.resources;
      aoeState.pop = data.pop;
      aoeState.maxPop = data.maxPop;
      rivalGameTime = data.rivalGameTime || 0;
      updateResourceUI();
      refreshBuildingVisuals();
      playAdvanceAgeFanfare();
      showAoENotice('[EMPIRE RESTORED] Loaded saved empire status successfully!');
    };

    window.toggleObjectivesModal = function() {
      const m = document.getElementById('objectives-modal');
      m.style.display = m.style.display === 'flex' ? 'none' : 'flex';
    };

    window.toggleMenuModal = function() {
      const m = document.getElementById('menu-modal');
      m.style.display = m.style.display === 'flex' ? 'none' : 'flex';
    };
    """
