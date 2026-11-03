def get_aoe_world_director_js():
    return """
    // =========================================================================
    // PHASE 1 WORLD INITIALIZATION, HIGH REALISM SCENE, BIOMES & 60 FPS ENGINE
    // =========================================================================

    let terrainMesh = null;
    let waterMesh = null;
    let creekMesh = null;
    let lakeMesh = null;
    let waterfallMesh = null;
    let waterfallMistGroup = null;
    let rainGroup = null;
    let globalSimTime = 0;

    function initAoEWorld() {
      // 1. Grassy Rolling Mountain Terrain (200x200 World Grid: -100m to +100m)
      const terrainGeom = new THREE.PlaneGeometry(200, 200, 96, 96);
      terrainGeom.rotateX(-Math.PI / 2);
      const posAttr = terrainGeom.attributes.position;
      for (let i = 0; i < posAttr.count; i++) {
        const x = posAttr.getX(i);
        const z = posAttr.getZ(i);
        posAttr.setY(i, getTerrainHeight(x, z));
      }
      terrainGeom.computeVertexNormals();

      const terrainMat = new THREE.MeshLambertMaterial({ map: grassTex });
      terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
      terrainMesh.receiveShadow = true;
      scene.add(terrainMesh);

      // 2. Classify River Water & Obstacles into 100x100 Tilemap
      for (let gx = 0; gx < GRID_SIZE; gx++) {
        for (let gz = 0; gz < GRID_SIZE; gz++) {
          const w = gridToWorld(gx, gz);
          // Central River (-34m to -16m)
          if (w.x >= -34 && w.x <= -16) {
            tilemapGrid[gz * GRID_SIZE + gx] = TILE_WATER;
          }
          // Woodland Lake (-20, 60, radius 13)
          if (Math.hypot(w.x + 20, w.z - 60) < 13) {
            tilemapGrid[gz * GRID_SIZE + gx] = TILE_WATER;
          }
          // Eastern Rocky Cliffs (x > 62)
          if (w.x > 62 && Math.abs(w.z + 33) > 5) {
            tilemapGrid[gz * GRID_SIZE + gx] = TILE_CLIFF;
          }
        }
      }

      // 3. Shimmering River Water Ribbon at x = -25
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

      // 4. Mountain Creek Water flowing from Waterfall
      const creekGeom = new THREE.PlaneGeometry(72, 6.5);
      creekGeom.rotateX(-Math.PI / 2);
      creekMesh = new THREE.Mesh(creekGeom, waterMat);
      creekMesh.position.set(20, -1.35, -33);
      scene.add(creekMesh);

      // 5. Woodland Lake Water Surface at (-20, 60)
      const lakeGeom = new THREE.CircleGeometry(13.5, 32);
      lakeGeom.rotateX(-Math.PI / 2);
      lakeMesh = new THREE.Mesh(lakeGeom, waterMat);
      lakeMesh.position.set(-20, -1.75, 60);
      scene.add(lakeMesh);

      // 6. Roaring Mountain Waterfall (Descending from x = 60, y = 5.0, z = -33)
      const wfGeom = new THREE.PlaneGeometry(7.5, 7.2);
      const wfMat = new THREE.MeshStandardMaterial({
        map: waterTex,
        roughness: 0.2,
        metalness: 0.4,
        transparent: true,
        opacity: 0.92,
        side: THREE.DoubleSide
      });
      waterfallMesh = new THREE.Mesh(wfGeom, wfMat);
      waterfallMesh.position.set(58, 1.8, -33);
      waterfallMesh.rotation.y = -Math.PI / 2;
      waterfallMesh.rotation.x = -0.15;
      scene.add(waterfallMesh);

      // Waterfall Splash Mist Particles at Foot
      waterfallMistGroup = new THREE.Group();
      for (let i = 0; i < 18; i++) {
        const mist = new THREE.Mesh(
          new THREE.SphereGeometry(0.5 + Math.random() * 0.4, 6, 6),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.35 })
        );
        mist.position.set(55 + (Math.random() - 0.5) * 4, -1.0 + Math.random() * 0.8, -33 + (Math.random() - 0.5) * 6);
        waterfallMistGroup.add(mist);
      }
      scene.add(waterfallMistGroup);

      // 7. Arched Cobblestone River Bridge at (x: -25, z: 0)
      const bridgeGroup = new THREE.Group();
      bridgeGroup.position.set(-25, -0.4, 0);

      const spanGeom = new THREE.BoxGeometry(22, 1.0, 7.5);
      const span = new THREE.Mesh(spanGeom, stoneMat);
      span.castShadow = true;
      span.receiveShadow = true;
      bridgeGroup.add(span);

      // Stone Balustrades with Lantern Posts
      for (let z of [-3.6, 3.6]) {
        const rail = new THREE.Mesh(new THREE.BoxGeometry(22, 0.8, 0.35), stoneMat);
        rail.position.set(0, 0.8, z);
        bridgeGroup.add(rail);

        for (let x of [-10, 0, 10]) {
          const post = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.4, 0.6), stoneMat);
          post.position.set(x, 1.0, z);
          bridgeGroup.add(post);

          const lantern = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.3), new THREE.MeshBasicMaterial({ color: 0xffe066 }));
          lantern.position.set(x, 1.7, z);
          bridgeGroup.add(lantern);
        }
      }
      scene.add(bridgeGroup);

      // Bridge tiles Walkable
      for (let x = -35; x <= -15; x += 2) {
        for (let z = -4; z <= 4; z += 2) {
          const g = worldToGrid(x, z);
          tilemapGrid[g.z * GRID_SIZE + g.x] = TILE_WALKABLE;
        }
      }

      // 8. Natural Forests (Oak Groves, Pine Jungles & Birch Trees)
      spawnForestGrove(24, 18, 14);
      spawnForestGrove(-6, -28, 12);
      spawnForestGrove(35, -16, 15);
      spawnForestGrove(-68, 25, 14);
      spawnForestGrove(45, 35, 12);

      // 9. Mineral Deposits (Gold Veins & Stone Quarries)
      spawnMineralDeposit('gold', 18, -10, 4);
      spawnMineralDeposit('stone', 26, 12, 4);
      spawnMineralDeposit('gold', -55, -12, 4);
      spawnMineralDeposit('stone', -75, -35, 4);
      spawnMineralDeposit('gold', 42, -26, 3);

      // 10. Forage Berry Bushes
      spawnForageBushes(10, 20, 5);
      spawnForageBushes(-52, -25, 4);
      spawnForageBushes(28, 40, 4);

      // 11. Domestic Sheep & Wild Game (Huntable Boars & Deer)
      spawnSheepFlock(-10, -8, 4);
      spawnWildBoar(35, 25);
      spawnWildBoar(-50, 35);
      spawnWildDeer(38, -20);
      spawnWildDeer(-15, 50);

      // 12. Holy Relics
      spawnRelic(0, 45);
      spawnRelic(-25, -45);
      spawnRelic(62, -10);

      // 13. Initial Player Town Base (Team Blue)
      // Town Center at (0, 0)
      spawnBuilding('town_center', 0, 0, 'player');
      occupyGridArea(0, 0, 7, 7);

      spawnBuilding('house', -16, 12, 'player');
      occupyGridArea(-16, 12, 3, 3);

      // Start Units OPEN IN THE MEADOW (Never inside Town Center)
      spawnUnit('scout', -10, 10, 'player');
      spawnUnit('villager', 14, 10, 'player'); // Near woodcutter trees
      spawnUnit('villager', 8, 18, 'player');  // Near berry bushes & deer
      spawnUnit('villager', 16, -8, 'player'); // Near gold vein

      // 14. Initial Rival Red Base Across the River (Automated Opponent)
      spawnBuilding('town_center', -65, -15, 'enemy');
      occupyGridArea(-65, -15, 7, 7);
      spawnBuilding('barracks', -55, -5, 'enemy');
      occupyGridArea(-55, -5, 5, 5);
      spawnBuilding('archery_range', -58, -25, 'enemy');
      occupyGridArea(-58, -25, 5, 5);
      spawnBuilding('watchtower', -42, 2, 'enemy');
      occupyGridArea(-42, 2, 3, 3);

      spawnUnit('scout', -52, -12, 'enemy');
      spawnUnit('villager', -60, -8, 'enemy');
      spawnUnit('villager', -68, -20, 'enemy');
      spawnUnit('militia', -48, -4, 'enemy');

      // 15. Setup Rain Particle System for Overcast Weather
      rainGroup = new THREE.Group();
      const rainGeom = new THREE.BufferGeometry();
      const rainCount = 1200;
      const rainPositions = new Float32Array(rainCount * 3);
      for (let i = 0; i < rainCount * 3; i += 3) {
        rainPositions[i] = (Math.random() - 0.5) * 200;
        rainPositions[i + 1] = Math.random() * 40;
        rainPositions[i + 2] = (Math.random() - 0.5) * 200;
      }
      rainGeom.setAttribute('position', new THREE.BufferAttribute(rainPositions, 3));
      const rainMat = new THREE.PointsMaterial({
        color: 0x93c5fd,
        size: 0.35,
        transparent: true,
        opacity: 0.6
      });
      const rainPoints = new THREE.Points(rainGeom, rainMat);
      rainGroup.add(rainPoints);
      rainGroup.visible = false;
      scene.add(rainGroup);

      updateResourceUI();
      updateMissionHUD();
      showAoENotice('[EMPIRE FOUNDED] Britons civilization established. Lead your people to glory!');
    }

    // Spawners with Selection Footprints
    function createResourceSelectionRing(radius = 1.8) {
      const geom = new THREE.RingGeometry(radius * 0.85, radius, 20);
      geom.rotateX(-Math.PI / 2);
      const mat = new THREE.MeshBasicMaterial({ color: 0xfacc15, side: THREE.DoubleSide });
      const ring = new THREE.Mesh(geom, mat);
      ring.position.y = 0.1;
      ring.visible = false;
      return ring;
    }

    function spawnForestGrove(cx, cz, count) {
      for (let i = 0; i < count; i++) {
        const ox = cx + (Math.random() - 0.5) * 16;
        const oz = cz + (Math.random() - 0.5) * 16;
        const h = getTerrainHeight(ox, oz);
        if (h < -1.0) continue;

        const group = new THREE.Group();
        const trunkH = 2.8 + Math.random() * 1.5;
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.45, trunkH, 7), timberMat);
        trunk.position.y = trunkH / 2;
        trunk.castShadow = true;
        group.add(trunk);

        // Multi-tier lush foliage canopy
        const leafMat = new THREE.MeshLambertMaterial({ color: Math.random() > 0.4 ? 0x2e6930 : 0x1e4620 });
        for (let t = 0; t < 3; t++) {
          const cone = new THREE.Mesh(new THREE.ConeGeometry(2.4 - t * 0.55, 2.8, 7), leafMat);
          cone.position.y = trunkH + 0.8 + t * 1.5;
          cone.castShadow = true;
          group.add(cone);
        }

        const ring = createResourceSelectionRing(2.0);
        group.add(ring);
        group.position.set(ox, h, oz);
        scene.add(group);

        const resObj = {
          id: nextEntityId++,
          type: 'tree',
          name: 'Oak Tree',
          resType: 'wood',
          amount: 100,
          maxAmount: 100,
          isResource: true,
          mesh: group
        };
        group.userData.entityRef = resObj;
        group.userData.ring = ring;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnMineralDeposit(type, cx, cz, count) {
      const isGold = (type === 'gold');
      const oreMat = isGold ? goldMat : stoneMat;
      const oreName = isGold ? 'Gold Vein' : 'Stone Quarry';

      for (let i = 0; i < count; i++) {
        const ox = cx + (Math.random() - 0.5) * 8;
        const oz = cz + (Math.random() - 0.5) * 8;
        const h = getTerrainHeight(ox, oz);
        if (h < -1.0) continue;

        const group = new THREE.Group();
        const mainRock = new THREE.Mesh(new THREE.DodecahedronGeometry(1.6 + Math.random() * 0.4), oreMat);
        mainRock.position.y = 1.1;
        mainRock.castShadow = true;
        group.add(mainRock);

        for (let j = 0; j < 3; j++) {
          const sm = new THREE.Mesh(new THREE.DodecahedronGeometry(0.6 + Math.random() * 0.3), oreMat);
          sm.position.set((Math.random() - 0.5) * 2.2, 0.4, (Math.random() - 0.5) * 2.2);
          group.add(sm);
        }

        const ring = createResourceSelectionRing(2.2);
        group.add(ring);
        group.position.set(ox, h, oz);
        scene.add(group);

        const resObj = {
          id: nextEntityId++,
          type: isGold ? 'gold_mine' : 'stone_mine',
          name: oreName,
          resType: isGold ? 'gold' : 'stone',
          amount: 800,
          maxAmount: 800,
          isResource: true,
          mesh: group
        };
        group.userData.entityRef = resObj;
        group.userData.ring = ring;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnForageBushes(cx, cz, count) {
      for (let i = 0; i < count; i++) {
        const ox = cx + (Math.random() - 0.5) * 7;
        const oz = cz + (Math.random() - 0.5) * 7;
        const h = getTerrainHeight(ox, oz);
        if (h < -1.0) continue;

        const group = new THREE.Group();
        const bushMat = new THREE.MeshLambertMaterial({ color: 0x3d7a36 });
        const bush = new THREE.Mesh(new THREE.SphereGeometry(1.1, 7, 7), bushMat);
        bush.position.y = 0.9;
        bush.castShadow = true;
        group.add(bush);

        // Red/Purple Berries
        const berryMat = new THREE.MeshBasicMaterial({ color: 0xbe123c });
        for (let b = 0; b < 10; b++) {
          const berry = new THREE.Mesh(new THREE.SphereGeometry(0.14, 5, 5), berryMat);
          berry.position.set((Math.random() - 0.5) * 1.6, 0.6 + Math.random() * 0.9, (Math.random() - 0.5) * 1.6);
          group.add(berry);
        }

        const ring = createResourceSelectionRing(1.5);
        group.add(ring);
        group.position.set(ox, h, oz);
        scene.add(group);

        const resObj = {
          id: nextEntityId++,
          type: 'forage_bush',
          name: 'Forage Berry Bush',
          resType: 'food',
          amount: 150,
          maxAmount: 150,
          isResource: true,
          mesh: group
        };
        group.userData.entityRef = resObj;
        group.userData.ring = ring;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnSheepFlock(cx, cz, count) {
      for (let i = 0; i < count; i++) {
        const ox = cx + (Math.random() - 0.5) * 5;
        const oz = cz + (Math.random() - 0.5) * 5;
        const h = getTerrainHeight(ox, oz);

        const mesh = createSheepMesh();
        mesh.position.set(ox, h, oz);
        scene.add(mesh);

        const resObj = {
          id: nextEntityId++,
          type: 'sheep',
          name: 'Domestic Sheep',
          resType: 'food',
          amount: 100,
          maxAmount: 100,
          isResource: true,
          mesh
        };
        mesh.userData.entityRef = resObj;
        naturalResources.push(resObj);
        allSelectable.push(resObj);
      }
    }

    function spawnWildBoar(x, z) {
      const h = getTerrainHeight(x, z);
      const mesh = createBoarMesh();
      mesh.position.set(x, h, z);
      scene.add(mesh);

      const resObj = {
        id: nextEntityId++,
        type: 'boar',
        name: 'Wild Jungle Boar',
        resType: 'food',
        hp: 100,
        maxHp: 100,
        amount: 250,
        maxAmount: 250,
        isWildAnimal: true,
        isResource: true,
        mesh
      };
      mesh.userData.entityRef = resObj;
      naturalResources.push(resObj);
      allSelectable.push(resObj);
      return resObj;
    }

    function spawnWildDeer(x, z) {
      const h = getTerrainHeight(x, z);
      const mesh = createDeerMesh();
      mesh.position.set(x, h, z);
      scene.add(mesh);

      const resObj = {
        id: nextEntityId++,
        type: 'deer',
        name: 'Wild Creek Deer',
        resType: 'food',
        hp: 80,
        maxHp: 80,
        amount: 200,
        maxAmount: 200,
        isWildAnimal: true,
        isResource: true,
        mesh
      };
      mesh.userData.entityRef = resObj;
      naturalResources.push(resObj);
      allSelectable.push(resObj);
      return resObj;
    }

    function spawnRelic(x, z) {
      const h = getTerrainHeight(x, z);
      const mesh = createRelicMesh();
      mesh.position.set(x, h, z);
      scene.add(mesh);

      const relicObj = {
        id: nextEntityId++,
        type: 'relic',
        name: 'Holy Relic',
        isRelic: true,
        heldBy: null,
        mesh
      };
      mesh.userData.entityRef = relicObj;
      holyRelics.push(relicObj);
      allSelectable.push(relicObj);
      return relicObj;
    }

    function spawnBuilding(type, x, z, team) {
      const def = BUILDING_TYPES[type] || BUILDING_TYPES.house;
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
      mesh.position.set(x, getTerrainHeight(x, z), z);
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
      mesh.position.set(x, getTerrainHeight(x, z), z);
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
      if (team === 'player') {
        friendlyUnits.push(uObj);
        if (type !== 'villager') {
          triggerMissionProgress('train_military', 1);
        }
      } else {
        enemyUnits.push(uObj);
      }
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

    // Rival Automated Wave Director
    let rivalGameTime = 0;
    let lastWaveIndex = 0;

    function updateRivalDirector(dt) {
      rivalGameTime += dt;

      if (rivalGameTime > 120 && lastWaveIndex < 1) {
        lastWaveIndex = 1;
        showAoENotice('[ALERT] Rival Clan raiding party spotted crossing the river bridge!');
        const r1 = spawnUnit('militia', -25, 4, 'enemy');
        const r2 = spawnUnit('militia', -23, 2, 'enemy');
        if (r1) { r1.state = 'moving'; r1.dest = new THREE.Vector3(0, 0, 0); }
        if (r2) { r2.state = 'moving'; r2.dest = new THREE.Vector3(0, 0, 0); }
      } else if (rivalGameTime > 300 && lastWaveIndex < 2) {
        lastWaveIndex = 2;
        showAoENotice('[ALERT] Rival Clan cavalry force advancing across the ford!');
        const k1 = spawnUnit('scout', -25, -2, 'enemy');
        const k2 = spawnUnit('scout', -24, 0, 'enemy');
        const a1 = spawnUnit('archer', -27, 2, 'enemy');
        [k1, k2, a1].forEach(u => {
          if (u) { u.state = 'moving'; u.dest = new THREE.Vector3(0, 0, 0); }
        });
      }
    }

    // Main 60 FPS Engine Simulation Loop
    let lastTime = performance.now();

    function updateSimulation() {
      const now = performance.now();
      const dt = Math.min(0.1, (now - lastTime) / 1000);
      lastTime = now;
      globalSimTime += dt;

      // Animate Water Currents & Waterfall
      if (waterMesh && waterMesh.material.map) {
        waterMesh.material.map.offset.y = (globalSimTime * 0.12) % 1.0;
      }
      if (waterfallMesh && waterfallMesh.material.map) {
        waterfallMesh.material.map.offset.y = -(globalSimTime * 0.75) % 1.0;
      }
      if (waterfallMistGroup) {
        waterfallMistGroup.children.forEach((m, idx) => {
          m.position.y = -1.0 + Math.sin(globalSimTime * 4 + idx) * 0.4;
        });
      }

      // Animate Rain Particles
      if (rainGroup && rainGroup.visible) {
        const positions = rainGroup.children[0].geometry.attributes.position.array;
        for (let i = 1; i < positions.length; i += 3) {
          positions[i] -= dt * 35;
          if (positions[i] < 0) positions[i] = 40;
        }
        rainGroup.children[0].geometry.attributes.position.needsUpdate = true;
      }

      // Passive Gold Income from Relics & Crafts
      if (aoeState.passiveGold > 0) {
        aoeState.resources.gold += aoeState.passiveGold * dt;
        updateResourceUI();
      }

      // 1. Screen-Edge Mouse Panning & WASD Camera Navigation
      const panSpeed = 38 * dt;
      let panX = 0;
      let panZ = 0;

      if (keysPressed['KeyA'] || keysPressed['ArrowLeft']) panX -= panSpeed;
      if (keysPressed['KeyD'] || keysPressed['ArrowRight']) panX += panSpeed;
      if (keysPressed['KeyW'] || keysPressed['ArrowUp']) panZ -= panSpeed;
      if (keysPressed['KeyS'] || keysPressed['ArrowDown']) panZ += panSpeed;

      // Screen-Edge Viewport Triggers
      const edgeThreshold = 24;
      if (lastMouseScreen.x <= edgeThreshold) panX -= panSpeed;
      else if (lastMouseScreen.x >= window.innerWidth - edgeThreshold) panX += panSpeed;
      if (lastMouseScreen.y <= edgeThreshold) panZ -= panSpeed;
      else if (lastMouseScreen.y >= window.innerHeight - edgeThreshold) panZ += panSpeed;

      cameraTargetPos.x += panX;
      cameraTargetPos.z += panZ;

      // Constrain Camera to 200x200 World Grid
      cameraTargetPos.x = Math.max(-85, Math.min(85, cameraTargetPos.x));
      cameraTargetPos.z = Math.max(-85, Math.min(85, cameraTargetPos.z));

      // Isometric Top-Down Perspective
      camera.position.x = cameraTargetPos.x;
      camera.position.y = cameraZoom * 0.75;
      camera.position.z = cameraTargetPos.z + cameraZoom;
      camera.lookAt(cameraTargetPos.x, 0, cameraTargetPos.z);

      // 2. Animate Mill Rotor Blades
      friendlyBuildings.concat(enemyBuildings).forEach(b => {
        if (b.type === 'mill' && b.mesh.userData && b.mesh.userData.rotorGroup) {
          b.mesh.userData.rotorGroup.rotation.z += dt * 1.6;
        }
      });

      // 3. Process Building Training Queues
      friendlyBuildings.forEach(b => {
        if (b.queue && b.queue.length > 0) {
          const item = b.queue[0];
          item.timeRemaining -= dt;
          if (aoeState.selectedEntity === b) {
            const queueBar = document.getElementById('train-queue-bar');
            queueBar.style.display = 'flex';
            const pct = Math.max(0, Math.min(100, ((item.totalTime - item.timeRemaining) / item.totalTime) * 100));
            document.getElementById('queue-fill').style.width = pct + '%';
            document.getElementById('queue-slots').innerHTML = b.queue.map(q => `<div class="queue-slot">${q.type[0].toUpperCase()}</div>`).join('');
          }
          if (item.timeRemaining <= 0) {
            b.queue.shift();
            spawnUnit(item.type, b.mesh.position.x + (Math.random() - 0.5) * 6, b.mesh.position.z + 5, 'player');
            playVoiceBark('move');
            showAoENotice(`[TRAINED] ${UNIT_TYPES[item.type].name} mustered for duty!`);
            if (b.queue.length === 0 && aoeState.selectedEntity === b) {
              document.getElementById('train-queue-bar').style.display = 'none';
            }
          }
        }
      });

      // 4. Update Friendly & Enemy Units (FSM & Terrain Elevation)
      const allActiveUnits = friendlyUnits.concat(enemyUnits);
      allActiveUnits.forEach(u => {
        if (u.hp <= 0 || u.state === 'garrisoned') return;

        // Animate legs when moving
        if (u.state === 'moving' && u.mesh.userData && u.mesh.userData.legL) {
          u.mesh.userData.legL.rotation.x = Math.sin(globalSimTime * 12) * 0.6;
          u.mesh.userData.legR.rotation.x = -Math.sin(globalSimTime * 12) * 0.6;
        } else if (u.mesh.userData && u.mesh.userData.legL) {
          u.mesh.userData.legL.rotation.x = 0;
          u.mesh.userData.legR.rotation.x = 0;
        }

        // Animate arm when gathering, hunting or building
        if ((u.state === 'gathering' || u.state === 'hunting' || u.state === 'building' || u.state === 'repairing') && u.mesh.userData && u.mesh.userData.armR) {
          u.mesh.userData.armR.rotation.x = Math.sin(globalSimTime * 9) * 0.7;
        } else if (u.mesh.userData && u.mesh.userData.armR) {
          u.mesh.userData.armR.rotation.x = 0;
        }

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

        // Constrain Unit Y to Exact Terrain Height
        u.mesh.position.y = getTerrainHeight(u.mesh.position.x, u.mesh.position.z);

        // Aggro Radius (14m)
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

        // Villager HUNTING Routine
        if (u.type === 'villager' && u.state === 'hunting' && u.target) {
          const tgt = u.target;
          if (tgt.hp <= 0) {
            u.state = 'gathering';
            updateVillagerToolVisual(u, 'food');
            return;
          }
          const dist = u.mesh.position.distanceTo(tgt.mesh.position);
          if (dist > 3.8) {
            const dir = new THREE.Vector3().subVectors(tgt.mesh.position, u.mesh.position).normalize();
            dir.y = 0;
            u.mesh.position.addScaledVector(dir, u.speed * 60 * dt);
            u.mesh.rotation.y = Math.atan2(dir.x, dir.z);
          } else {
            u.attackCooldown = (u.attackCooldown || 0) + dt;
            if (u.attackCooldown >= 1.0) {
              u.attackCooldown = 0;
              tgt.hp -= 25;
              playSwordClashSound();

              // Retaliation: Wild Boar charges!
              if (tgt.type === 'boar' && dist > 1.2) {
                const chargeDir = new THREE.Vector3().subVectors(u.mesh.position, tgt.mesh.position).normalize();
                chargeDir.y = 0;
                tgt.mesh.position.addScaledVector(chargeDir, 0.2 * 60 * dt);
              }

              if (tgt.hp <= 0) {
                tgt.name = `Downed ${tgt.type === 'boar' ? 'Boar' : 'Deer'} Carcass (250 Food)`;
                tgt.mesh.rotation.z = Math.PI / 2;
                tgt.mesh.position.y = getTerrainHeight(tgt.mesh.position.x, tgt.mesh.position.z) + 0.3;
                tgt.isWildAnimal = false;
                tgt.isResource = true;
                showAoENotice(`[HUNT COMPLETE] Wild ${tgt.type} harvested for 250 Food!`);
                addPoints(50, `Hunted Wild ${tgt.type}`);
                triggerMissionProgress('hunt_wild', 1);
                u.state = 'gathering';
                updateVillagerToolVisual(u, 'food');
              }
            }
          }
        }

        // Villager Gathering Routine
        if (u.type === 'villager' && u.state === 'gathering' && u.target) {
          const tgtPos = u.target.mesh.position;
          const dist = u.mesh.position.distanceTo(tgtPos);
          if (dist > 2.5) {
            const dir = new THREE.Vector3().subVectors(tgtPos, u.mesh.position).normalize();
            dir.y = 0;
            u.mesh.position.addScaledVector(dir, u.speed * 60 * dt);
            u.mesh.rotation.y = Math.atan2(dir.x, dir.z);
          } else {
            let rate = 2.5;
            if ((u.target.resType === 'gold' || u.target.resType === 'stone') && aoeState.miningBonus) {
              rate *= aoeState.miningBonus;
            }
            u.carryAmount += rate * dt;
            u.carryType = u.target.resType;

            if (u.mesh.userData.cargoGroup) {
              u.mesh.userData.cargoGroup.visible = true;
              if (u.mesh.userData.logCargo) u.mesh.userData.logCargo.visible = (u.carryType === 'wood');
              if (u.mesh.userData.oreCargo) u.mesh.userData.oreCargo.visible = (u.carryType === 'gold' || u.carryType === 'stone');
              if (u.mesh.userData.meatCargo) u.mesh.userData.meatCargo.visible = (u.carryType === 'food');
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

        // Villager Depositing Routine
        if (u.type === 'villager' && u.state === 'depositing' && u.dest) {
          const dist = u.mesh.position.distanceTo(u.dest);
          if (dist <= 3.5) {
            if (u.team === 'player' && u.carryType) {
              aoeState.resources[u.carryType] += u.carryAmount;
              addPoints(Math.floor(u.carryAmount), `Deposited ${u.carryType}`);
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
          let combatRange = u.range;
          if (u.type === 'archer' && aoeState.archerBonus && u.team === 'player') {
            combatRange += 3;
          }

          if (dist > combatRange) {
            const dir = new THREE.Vector3().subVectors(tgt.mesh.position, u.mesh.position).normalize();
            dir.y = 0;
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

    function calculateDamage(attacker, defender) {
      let base = attacker.attack || 4;
      if (attacker.type === 'spearman' && defender.type === 'scout') {
        base += 15; // Anti-Cavalry Pike Bonus!
      } else if (attacker.type === 'archer' && defender.type === 'spearman') {
        base += 3; // Archers counter light spearmen
      } else if (attacker.type === 'knight' && defender.type === 'archer') {
        base += 6; // Heavy cavalry tramples archers
      }
      const armor = defender.armor || 0;
      return Math.max(1, base - armor);
    }

    function findNearestDropOff(unit) {
      const candidates = friendlyBuildings.filter(b => {
        if (unit.carryType === 'wood') return b.type === 'town_center' || b.type === 'lumber_camp';
        if (unit.carryType === 'food') return b.type === 'town_center' || b.type === 'mill';
        if (unit.carryType === 'gold' || unit.carryType === 'stone') return b.type === 'town_center' || b.type === 'mining_camp';
        return b.type === 'town_center';
      });
      if (candidates.length === 0) return friendlyBuildings.find(b => b.type === 'town_center');

      let nearest = null;
      let minDist = Infinity;
      candidates.forEach(c => {
        const d = unit.mesh.position.distanceTo(c.mesh.position);
        if (d < minDist) {
          minDist = d;
          nearest = c;
        }
      });
      return nearest;
    }

    function triggerGameVictory(msg) {
      if (aoeState.gameWon) return;
      aoeState.gameWon = true;
      playAdvanceAgeFanfare();
      showAoENotice('[VICTORY ACHIEVED] ' + msg, 10000);
      addPoints(1000, 'Imperial Conquest Victory');
    }

    function destroyEntity(entity) {
      if (entity.mesh) scene.remove(entity.mesh);
      showAoENotice(`[FALLEN] ${entity.name} destroyed!`);
      if (entity.isBuilding) {
        const bDef = BUILDING_TYPES[entity.type];
        const sizeTiles = Math.max(1, Math.round((bDef ? bDef.size : 4) / TILE_SIZE));
        freeGridArea(entity.mesh.position.x, entity.mesh.position.z, sizeTiles, sizeTiles);

        // Check if Enemy Town Center destroyed -> Conquest Victory!
        if (entity.type === 'town_center' && entity.team === 'enemy') {
          triggerGameVictory('Conquest Victory! The Rival Red Civilization has fallen!');
          triggerMissionProgress('destroy_enemy_tc', 1);
        }
      }
      const rem = arr => {
        const idx = arr.indexOf(entity);
        if (idx !== -1) arr.splice(idx, 1);
      };
      rem(friendlyUnits);
      rem(enemyUnits);
      rem(friendlyBuildings);
      rem(enemyBuildings);
      rem(naturalResources);
      rem(allSelectable);

      if (aoeState.selectedEntities.includes(entity)) {
        clearSelection();
      }
    }

    // 3D Hover Tooltip
    function updateHoverTooltip(e) {
      const tip = document.getElementById('hover-tooltip');
      const title = document.getElementById('tip-title');
      const sub = document.getElementById('tip-sub');
      if (!tip || !title || !sub) return;

      raycaster.setFromCamera(mouse, camera);
      const selectableMeshes = allSelectable.map(item => item.mesh).filter(Boolean);
      const intersects = raycaster.intersectObjects(selectableMeshes, true);

      if (intersects.length > 0) {
        let obj = intersects[0].object;
        while (obj.parent && !obj.userData.entityRef) {
          obj = obj.parent;
        }
        const ent = obj.userData.entityRef;
        if (ent) {
          title.textContent = `[${ent.name.toUpperCase()}]`;
          if (ent.isUnit) {
            sub.textContent = `Team: ${ent.team === 'player' ? 'Britons' : 'Rival Red'} | HP: ${Math.ceil(ent.hp)}/${ent.maxHp} | State: ${ent.state.toUpperCase()}`;
          } else if (ent.isWildAnimal) {
            sub.textContent = `Wild Game | HP: ${Math.ceil(ent.hp)}/${ent.maxHp} | Food: ${ent.amount} (Huntable)`;
          } else if (ent.isResource) {
            sub.textContent = `Natural Resource: ${ent.resType.toUpperCase()} | Stock: ${Math.ceil(ent.amount)}`;
          } else if (ent.isBuilding) {
            sub.textContent = `Team: ${ent.team === 'player' ? 'Britons' : 'Rival Red'} | HP: ${Math.ceil(ent.hp)}/${ent.maxHp}`;
          }
          tip.style.display = 'block';
          tip.style.left = e.clientX + 'px';
          tip.style.top = (e.clientY - 24) + 'px';
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
      const riverX = ((-25 + 100) / 200) * w;
      ctx.fillRect(riverX - 5, 0, 10, h);

      // Bridge
      ctx.fillStyle = '#7a7a7a';
      ctx.fillRect(riverX - 7, h / 2 - 4, 14, 8);

      // Resources
      naturalResources.forEach(r => {
        if (!r.mesh) return;
        const rx = ((r.mesh.position.x + 100) / 200) * w;
        const rz = ((r.mesh.position.z + 100) / 200) * h;
        ctx.fillStyle = r.resType === 'wood' ? '#14532d' : (r.resType === 'gold' ? '#eab308' : (r.isWildAnimal ? '#ea580c' : '#94a3b8'));
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
    """
