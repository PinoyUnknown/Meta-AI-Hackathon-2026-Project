def get_aoe_units_combat_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES 3D UNITS, COMBAT, HARVESTING & SELECTION ENGINE
    // =========================================================================

    // Selection Ring Indicator Decal
    const ringGeom = new THREE.RingGeometry(1.2, 1.4, 24);
    ringGeom.rotateX(-Math.PI / 2);
    const friendlyRingMat = new THREE.MeshBasicMaterial({ color: 0x22c55e, side: THREE.DoubleSide });
    const enemyRingMat = new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide });

    function createSelectionRing(isEnemy) {
      const ring = new THREE.Mesh(ringGeom, isEnemy ? enemyRingMat : friendlyRingMat);
      ring.position.y = 0.08;
      ring.visible = false;
      return ring;
    }

    // 1. VILLAGER MESH (Male & Female with Tool & Cargo Switching)
    function createVillagerMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const tunicMat = new THREE.MeshLambertMaterial({ color: teamColor });
      const skinMat = new THREE.MeshLambertMaterial({ color: 0xe0ac69 });
      const pantsMat = new THREE.MeshLambertMaterial({ color: 0x4a3728 });

      // Legs
      const legGeom = new THREE.BoxGeometry(0.35, 1.1, 0.35);
      const legL = new THREE.Mesh(legGeom, pantsMat);
      legL.position.set(-0.25, 0.55, 0);
      group.add(legL);
      const legR = new THREE.Mesh(legGeom, pantsMat);
      legR.position.set(0.25, 0.55, 0);
      group.add(legR);

      // Torso / Tunic
      const torsoGeom = new THREE.BoxGeometry(0.85, 1.1, 0.55);
      const torso = new THREE.Mesh(torsoGeom, tunicMat);
      torso.position.y = 1.45;
      torso.castShadow = true;
      group.add(torso);

      // Head
      const headGeom = new THREE.SphereGeometry(0.32, 8, 8);
      const head = new THREE.Mesh(headGeom, skinMat);
      head.position.y = 2.2;
      group.add(head);

      // Hat / Straw Cap
      const hatGeom = new THREE.ConeGeometry(0.5, 0.35, 8);
      const hat = new THREE.Mesh(hatGeom, thatchMat);
      hat.position.y = 2.45;
      group.add(hat);

      // Dynamic Tool Mount (Right Hand)
      const toolMount = new THREE.Group();
      toolMount.position.set(0.55, 1.4, 0.2);

      // Tool 1: Wood Axe
      const axeGroup = new THREE.Group();
      const axeHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.2, 6), timberMat);
      axeHandle.position.y = 0.2;
      axeGroup.add(axeHandle);
      const axeHead = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.25, 0.08), ironMat);
      axeHead.position.set(0.12, 0.6, 0);
      axeGroup.add(axeHead);
      toolMount.add(axeGroup);

      // Tool 2: Pickaxe
      const pickGroup = new THREE.Group();
      const pickHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.3, 6), timberMat);
      pickHandle.position.y = 0.2;
      pickGroup.add(pickHandle);
      const pickHead = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.12, 0.08), ironMat);
      pickHead.position.set(0, 0.65, 0);
      pickGroup.add(pickHead);
      pickGroup.visible = false;
      toolMount.add(pickGroup);

      // Tool 3: Hammer
      const hammerGroup = new THREE.Group();
      const hammerHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.9, 6), timberMat);
      hammerGroup.add(hammerHandle);
      const hammerHead = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.2, 0.2), ironMat);
      hammerHead.position.set(0, 0.45, 0);
      hammerGroup.add(hammerHead);
      hammerGroup.visible = false;
      toolMount.add(hammerGroup);

      group.add(toolMount);

      // Carried Resource Cargo (Back / Hip)
      const cargoGroup = new THREE.Group();
      cargoGroup.position.set(0, 1.4, -0.4);

      // Log Cargo
      const logCargo = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 1.4, 6), timberMat);
      logCargo.rotation.z = Math.PI / 2;
      cargoGroup.add(logCargo);

      // Ore Basket Cargo
      const oreCargo = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.5, 0.5), goldMat);
      oreCargo.visible = false;
      cargoGroup.add(oreCargo);

      cargoGroup.visible = false;
      group.add(cargoGroup);

      // Selection Ring
      const ring = createSelectionRing(isEnemy);
      group.add(ring);

      group.userData = {
        legL, legR, toolMount, axeGroup, pickGroup, hammerGroup,
        cargoGroup, logCargo, oreCargo, ring
      };

      return group;
    }

    // 2. SCOUT CAVALRY MESH
    function createScoutMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const teamMat = new THREE.MeshLambertMaterial({ color: teamColor });
      const horseMat = new THREE.MeshLambertMaterial({ color: 0x6e3d16 });

      // Horse Body
      const bodyGeom = new THREE.BoxGeometry(1.2, 1.1, 2.2);
      const body = new THREE.Mesh(bodyGeom, horseMat);
      body.position.y = 1.4;
      body.castShadow = true;
      group.add(body);

      // Horse Neck & Head
      const neckGeom = new THREE.BoxGeometry(0.6, 1.1, 0.9);
      const neck = new THREE.Mesh(neckGeom, horseMat);
      neck.position.set(0, 2.1, 0.9);
      neck.rotation.x = -Math.PI / 6;
      group.add(neck);

      // Horse 4 Legs
      const legGeom = new THREE.BoxGeometry(0.25, 1.2, 0.25);
      const legPositions = [[-0.45, 0.6, -0.8], [0.45, 0.6, -0.8], [-0.45, 0.6, 0.8], [0.45, 0.6, 0.8]];
      legPositions.forEach(p => {
        const leg = new THREE.Mesh(legGeom, horseMat);
        leg.position.set(p[0], p[1], p[2]);
        group.add(leg);
      });

      // Rider in Saddle
      const riderGeom = new THREE.BoxGeometry(0.8, 1.1, 0.6);
      const rider = new THREE.Mesh(riderGeom, teamMat);
      rider.position.set(0, 2.3, 0);
      group.add(rider);

      // Rider Spear
      const spearGeom = new THREE.CylinderGeometry(0.04, 0.04, 2.8, 6);
      const spear = new THREE.Mesh(spearGeom, timberMat);
      spear.rotation.x = Math.PI / 4;
      spear.position.set(0.5, 2.4, 0.5);
      group.add(spear);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring };
      return group;
    }

    // 3. SWORDSMAN MESH (Militia, Man-at-Arms, Longswordsman)
    function createSwordsmanMesh(isEnemy, tier = 1) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const teamMat = new THREE.MeshLambertMaterial({ color: teamColor });

      // Armored Body
      const bodyGeom = new THREE.BoxGeometry(0.9, 1.2, 0.6);
      const body = new THREE.Mesh(bodyGeom, ironMat);
      body.position.y = 1.45;
      body.castShadow = true;
      group.add(body);

      // Steel Kettle Helmet
      const helmGeom = new THREE.SphereGeometry(0.38, 8, 8);
      const helm = new THREE.Mesh(helmGeom, ironMat);
      helm.position.y = 2.25;
      group.add(helm);

      // Broadsword (Right Hand)
      const swordBlade = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.4, 0.06), ironMat);
      swordBlade.position.set(0.65, 1.7, 0.3);
      group.add(swordBlade);

      // Team Shield (Left Hand)
      const shieldGeom = new THREE.BoxGeometry(0.1, 1.1, 0.7);
      const shield = new THREE.Mesh(shieldGeom, teamMat);
      shield.position.set(-0.6, 1.45, 0.2);
      group.add(shield);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring, swordBlade };
      return group;
    }

    // 4. SPEARMAN MESH (Anti-Cavalry Pike)
    function createSpearmanMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const teamMat = new THREE.MeshLambertMaterial({ color: teamColor });

      const body = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.1, 0.55), teamMat);
      body.position.y = 1.45;
      group.add(body);

      // 3.5m Long Pike
      const pike = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 3.8, 6), timberMat);
      pike.rotation.x = Math.PI / 6;
      pike.position.set(0.4, 1.8, 0.8);
      group.add(pike);

      const pikeTip = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.5, 6), ironMat);
      pikeTip.rotation.x = Math.PI / 6;
      pikeTip.position.set(0.4, 3.5, 1.8);
      group.add(pikeTip);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring };
      return group;
    }

    // 5. ARCHER MESH (Recurve Bow & Arrow)
    function createArcherMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const teamMat = new THREE.MeshLambertMaterial({ color: teamColor });

      const body = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.1, 0.5), teamMat);
      body.position.y = 1.4;
      group.add(body);

      // Feathered Archer Cap
      const cap = new THREE.Mesh(new THREE.ConeGeometry(0.45, 0.4, 6), timberMat);
      cap.position.y = 2.3;
      group.add(cap);

      // Recurve Bow (Left Hand)
      const bowGeom = new THREE.TorusGeometry(0.5, 0.04, 6, 12, Math.PI);
      const bow = new THREE.Mesh(bowGeom, timberMat);
      bow.position.set(-0.55, 1.4, 0.3);
      bow.rotation.y = Math.PI / 2;
      group.add(bow);

      // Back Quiver
      const quiver = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.1, 0.9, 6), timberMat);
      quiver.rotation.z = Math.PI / 6;
      quiver.position.set(0.2, 1.5, -0.35);
      group.add(quiver);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring };
      return group;
    }

    // 6. KNIGHT / PALADIN MESH (Armored Warhorse & Tilting Lance)
    function createKnightMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const teamMat = new THREE.MeshLambertMaterial({ color: teamColor });

      // Warhorse with Team Caparison Barding
      const bodyGeom = new THREE.BoxGeometry(1.4, 1.3, 2.6);
      const body = new THREE.Mesh(bodyGeom, teamMat);
      body.position.y = 1.6;
      body.castShadow = true;
      group.add(body);

      // Armored Great Helm Knight
      const rider = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.3, 0.7), ironMat);
      rider.position.set(0, 2.6, 0);
      group.add(rider);

      // Tilting Heavy Lance
      const lance = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.15, 3.5, 8), timberMat);
      lance.rotation.x = Math.PI / 3;
      lance.position.set(0.7, 2.4, 1.0);
      group.add(lance);

      // Knight Heater Shield
      const shield = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.3, 0.8), teamMat);
      shield.position.set(-0.7, 2.3, 0.2);
      group.add(shield);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring };
      return group;
    }

    // 7. MONK MESH (Brown Habit, Holy Relic Aura)
    function createMonkMesh(isEnemy) {
      const group = new THREE.Group();
      const monkRobeMat = new THREE.MeshLambertMaterial({ color: 0x5a3d28 });

      // Robe Cylinder
      const robe = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.8, 1.8, 8), monkRobeMat);
      robe.position.y = 0.9;
      group.add(robe);

      // Cowl Hood
      const hood = new THREE.Mesh(new THREE.SphereGeometry(0.42, 8, 8), monkRobeMat);
      hood.position.y = 2.0;
      group.add(hood);

      // Wooden Staff
      const staff = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.4, 6), timberMat);
      staff.position.set(0.5, 1.2, 0.2);
      group.add(staff);

      // Golden Holy Aura Ring
      const aura = new THREE.Mesh(new THREE.RingGeometry(0.8, 1.0, 16), goldMat);
      aura.rotation.x = -Math.PI / 2;
      aura.position.y = 0.1;
      group.add(aura);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring, aura };
      return group;
    }

    // 8. TREBUCHET MESH (Rolling Siege Engine with Throwing Arm)
    function createTrebuchetMesh(isEnemy) {
      const group = new THREE.Group();

      // Rolling Timber Chassis with 4 Wheels
      const chassis = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.6, 6), timberMat);
      chassis.position.y = 0.8;
      chassis.castShadow = true;
      group.add(chassis);

      // 4 Wheels
      for (let x of [-2.4, 2.4]) {
        for (let z of [-2.2, 2.2]) {
          const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.4, 10), timberMat);
          wheel.rotation.z = Math.PI / 2;
          wheel.position.set(x, 0.7, z);
          group.add(wheel);
        }
      }

      // Triangular A-Frame
      const frameL = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, 5, 6), timberMat);
      frameL.position.set(-1.8, 3.2, 0);
      group.add(frameL);
      const frameR = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, 5, 6), timberMat);
      frameR.position.set(1.8, 3.2, 0);
      group.add(frameR);

      // Swinging Throwing Arm
      const armGroup = new THREE.Group();
      armGroup.position.set(0, 5.5, 0);

      const arm = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 9), timberMat);
      arm.position.set(0, 0, 1.5);
      armGroup.add(arm);

      // Heavy Counterweight Box
      const counterWeight = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.8, 1.8), stoneMat);
      counterWeight.position.set(0, -1.2, -2.5);
      armGroup.add(counterWeight);

      group.add(armGroup);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      group.userData = { ring, armGroup };
      return group;
    }

    // 9. WILD ANIMALS & SHEEP
    function createSheepMesh() {
      const group = new THREE.Group();
      const woolMat = new THREE.MeshLambertMaterial({ color: 0xefede6 });
      const skinMat = new THREE.MeshLambertMaterial({ color: 0x1f1f1f });

      // Fluffy Wool Body
      const body = new THREE.Mesh(new THREE.SphereGeometry(0.75, 8, 8), woolMat);
      body.scale.set(1, 0.85, 1.3);
      body.position.y = 0.8;
      body.castShadow = true;
      group.add(body);

      // Black Face
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 6, 6), skinMat);
      head.position.set(0, 0.95, 0.9);
      group.add(head);

      // 4 Black Legs
      for (let x of [-0.35, 0.35]) {
        for (let z of [-0.4, 0.4]) {
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.6, 6), skinMat);
          leg.position.set(x, 0.3, z);
          group.add(leg);
        }
      }
      return group;
    }

    function createBoarMesh() {
      const group = new THREE.Group();
      const boarMat = new THREE.MeshLambertMaterial({ color: 0x4a2a12 });
      const tuskMat = new THREE.MeshLambertMaterial({ color: 0xffffff });

      // Stocky Bristly Body
      const body = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.0, 1.8), boarMat);
      body.position.y = 0.8;
      body.castShadow = true;
      group.add(body);

      // Head & Snout
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.8), boarMat);
      head.position.set(0, 0.8, 1.1);
      group.add(head);

      // 2 Curved White Tusks
      const tuskL = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.4, 6), tuskMat);
      tuskL.position.set(-0.35, 0.85, 1.4);
      tuskL.rotation.x = -Math.PI / 4;
      group.add(tuskL);
      const tuskR = tuskL.clone();
      tuskR.position.x = 0.35;
      group.add(tuskR);

      return group;
    }

    // 10. HOLY RELIC (Golden Chest on Ancient Stone Plinth)
    function createRelicMesh() {
      const group = new THREE.Group();
      const plinth = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.4, 0.6, 8), stoneMat);
      plinth.position.y = 0.3;
      group.add(plinth);

      const chest = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.7, 0.7), goldMat);
      chest.position.y = 0.9;
      chest.castShadow = true;
      group.add(chest);

      // Golden Holy Ray Light
      const ray = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.8, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffe066, transparent: true, opacity: 0.35 }));
      ray.position.y = 4.5;
      group.add(ray);

      return group;
    }
    """
