# build_foundation_part7.py - Villager Simulation, Autonomous Needs & Desire Footpaths
part7 = r'''
    // =========================================================================
    // AUTONOMOUS VILLAGER SIMULATION, NEEDS & DESIRE FOOTPATHS
    // =========================================================================
    const villagers = [];
    const villagerNames = [
      'Godwin', 'Elsbeth', 'Cedric', 'Rosalind', 'Wulfric', 'Morwenna',
      'Aldous', 'Beatrice', 'Osric', 'Gisela', 'Dunstan', 'Rowena'
    ];

    function createVillagerMesh(color = 0x3b82f6) {
      const group = new THREE.Group();

      // Body / Tunic
      const bodyMat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.8 });
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.45, 1.2, 8), bodyMat);
      body.position.y = 1.0; body.castShadow = true;
      group.add(body);

      // Head
      const headMat = new THREE.MeshStandardMaterial({ color: 0xfbd2a9, roughness: 0.6 });
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 8, 8), headMat);
      head.position.y = 1.85; head.castShadow = true;
      group.add(head);

      // Limbs for walking animation
      const limbMat = new THREE.MeshStandardMaterial({ color: 0x422810 });
      const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.65, 0.18), limbMat);
      leftLeg.position.set(-0.2, 0.35, 0); group.add(leftLeg);

      const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.65, 0.18), limbMat);
      rightLeg.position.set(0.2, 0.35, 0); group.add(rightLeg);

      group.leftLeg = leftLeg;
      group.rightLeg = rightLeg;

      return group;
    }

    function spawnVillager(profession = 'Laborer', startPos = null) {
      const name = villagerNames[villagers.length % villagerNames.length];
      const colors = [0x3b82f6, 0xb45309, 0x15803d, 0xca8a04, 0xb91c1c];
      const col = colors[villagers.length % colors.length];

      const mesh = createVillagerMesh(col);
      const pos = startPos || new THREE.Vector3((Math.random() - 0.5) * 15, 0, (Math.random() - 0.5) * 15);
      pos.y = getTerrainHeight(pos.x, pos.z);
      mesh.position.copy(pos);
      scene.add(mesh);

      const villager = {
        name: name,
        mesh: mesh,
        x: pos.x,
        z: pos.z,
        profession: profession,
        state: 'idle',
        targetPos: null,
        targetObj: null,
        workTimer: 0,
        hunger: 100,
        thirst: 100,
        faith: 100,
        walkAnim: 0
      };

      villagers.push(villager);
      updatePopulationHUD();
      return villager;
    }

    // Villager Autonomous AI Decision & Navigation Loop
    function updateVillagers(delta) {
      villagers.forEach((v) => {
        // Needs depletion
        v.hunger = Math.max(0, v.hunger - delta * 0.4);
        v.thirst = Math.max(0, v.thirst - delta * 0.6);

        // State Machine Decision
        if (!v.targetPos || v.state === 'idle') {
          decideVillagerAction(v);
        }

        // Move towards target
        if (v.targetPos) {
          const dx = v.targetPos.x - v.x;
          const dz = v.targetPos.z - v.z;
          const dist = Math.hypot(dx, dz);

          if (dist > 1.2) {
            const speed = 4.2;
            v.x += (dx / dist) * speed * delta;
            v.z += (dz / dist) * speed * delta;
            const y = getTerrainHeight(v.x, v.z);
            v.mesh.position.set(v.x, y, v.z);

            // Orient towards motion
            v.mesh.rotation.y = Math.atan2(dx, dz);

            // Walking limb swing animation
            v.walkAnim += delta * 12;
            v.mesh.leftLeg.rotation.x = Math.sin(v.walkAnim) * 0.6;
            v.mesh.rightLeg.rotation.x = -Math.sin(v.walkAnim) * 0.6;

            // STAMP DESIRE PATH FOOTSTEP
            stampVillagerFootstep(v.x, v.z);

          } else {
            // Reached Destination
            v.mesh.leftLeg.rotation.x = 0;
            v.mesh.rightLeg.rotation.x = 0;
            handleDestinationArrival(v, delta);
          }
        }
      });
    }

    function decideVillagerAction(v) {
      // 1. Thirst Check -> Find Well
      if (v.thirst < 40) {
        const well = buildings.find(b => b.type === 'well');
        if (well) {
          v.state = 'drinking';
          v.targetPos = new THREE.Vector3(well.x, 0, well.z);
          return;
        }
      }

      // 2. Hunger Check -> Find Market
      if (v.hunger < 40) {
        const market = buildings.find(b => b.type === 'market');
        if (market) {
          v.state = 'eating';
          v.targetPos = new THREE.Vector3(market.x, 0, market.z);
          return;
        }
      }

      // 3. Work Duty
      const lumberCamp = buildings.find(b => b.type === 'lumber');
      if (lumberCamp && trees.length > 0) {
        // Find closest tree
        let closestTree = trees[0];
        let minDist = 9999;
        trees.forEach(t => {
          const d = Math.hypot(t.x - lumberCamp.x, t.z - lumberCamp.z);
          if (d < minDist) { minDist = d; closestTree = t; }
        });

        v.state = 'chopping';
        v.targetObj = closestTree;
        v.targetPos = new THREE.Vector3(closestTree.x, 0, closestTree.z);
        return;
      }

      const quarry = buildings.find(b => b.type === 'quarry');
      if (quarry && stoneRocks.length > 0) {
        const closestRock = stoneRocks[0];
        v.state = 'quarrying';
        v.targetObj = closestRock;
        v.targetPos = new THREE.Vector3(closestRock.x, 0, closestRock.z);
        return;
      }

      // 4. Stroll Village Center
      v.state = 'strolling';
      v.targetPos = new THREE.Vector3((Math.random() - 0.5) * 30, 0, (Math.random() - 0.5) * 30);
    }

    function handleDestinationArrival(v, delta) {
      v.workTimer += delta;

      if (v.state === 'chopping' && v.targetObj) {
        if (v.workTimer > 3.0) {
          playWoodChopSound();
          v.workTimer = 0;
          v.targetObj.hp--;
          gameState.wood += 2;
          updateResourceLedger();

          if (v.targetObj.hp <= 0) {
            scene.remove(v.targetObj.mesh);
            const idx = trees.indexOf(v.targetObj);
            if (idx !== -1) trees.splice(idx, 1);
          }
          v.state = 'idle';
          v.targetPos = null;
        }
      } else if (v.state === 'quarrying' && v.targetObj) {
        if (v.workTimer > 3.5) {
          playStoneChiselSound();
          v.workTimer = 0;
          v.targetObj.hp--;
          gameState.stone += 2;
          updateResourceLedger();

          if (v.targetObj.hp <= 0) {
            scene.remove(v.targetObj.mesh);
            const idx = stoneRocks.indexOf(v.targetObj);
            if (idx !== -1) stoneRocks.splice(idx, 1);
          }
          v.state = 'idle';
          v.targetPos = null;
        }
      } else if (v.state === 'drinking') {
        v.thirst = 100;
        v.state = 'idle';
        v.targetPos = null;
      } else if (v.state === 'eating') {
        v.hunger = 100;
        if (gameState.berries > 0) gameState.berries--;
        else if (gameState.bread > 0) gameState.bread--;
        updateResourceLedger();
        v.state = 'idle';
        v.targetPos = null;
      } else {
        if (v.workTimer > 2.0) {
          v.workTimer = 0;
          v.state = 'idle';
          v.targetPos = null;
        }
      }
    }

    // Villager & Building Inspector Click
    function inspectVillager(v) {
      const card = document.getElementById('inspector-card');
      if (!card) return;
      document.getElementById('insp-title').innerText = `${v.name} the ${v.profession}`;
      document.getElementById('insp-status').innerText = 'Serf';
      document.getElementById('insp-job').innerText = v.profession;
      document.getElementById('insp-task').innerText = v.state.toUpperCase();
      document.getElementById('insp-hunger').innerText = v.hunger > 50 ? 'Satisfied' : 'Hungry';
      document.getElementById('insp-thirst').innerText = v.thirst > 50 ? 'Quenched' : 'Thirsty';
      card.style.display = 'block';
    }

    window.closeInspector = function() {
      const card = document.getElementById('inspector-card');
      if (card) card.style.display = 'none';
    };
'''

with open("foundation_part7.py", "w", encoding="utf-8") as f:
    f.write('part7 = r"""' + part7 + '"""\n')
print("Wrote foundation_part7.py")
