def get_aoe_units_combat_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES 3D UNITS, ANIMATED TOOLS, CARGO & SELECTION
    // =========================================================================

    const ringGeom = new THREE.RingGeometry(1.2, 1.45, 24);
    ringGeom.rotateX(-Math.PI / 2);
    const friendlyRingMat = new THREE.MeshBasicMaterial({ color: 0x22c55e, side: THREE.DoubleSide });
    const enemyRingMat = new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide });

    function createSelectionRing(isEnemy) {
      const ring = new THREE.Mesh(ringGeom, isEnemy ? enemyRingMat : friendlyRingMat);
      ring.position.y = 0.08;
      ring.visible = false;
      return ring;
    }

    function addUnitHitbox(group, radius = 1.3, height = 2.8) {
      const hitboxGeom = new THREE.CylinderGeometry(radius, radius, height, 8);
      const hitboxMat = new THREE.MeshBasicMaterial({ visible: false });
      const hitbox = new THREE.Mesh(hitboxGeom, hitboxMat);
      hitbox.position.y = height * 0.5;
      group.add(hitbox);
      return hitbox;
    }

    // 1. VILLAGER (Animated Walking Legs, Dynamic Tool & Cargo)
    function createVillagerMesh(isEnemy) {
      const group = new THREE.Group();
      const teamColor = isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY;
      const tunicMat = new THREE.MeshLambertMaterial({ color: teamColor });
      const skinMat = new THREE.MeshLambertMaterial({ color: 0xdfab76 });
      const pantsMat = new THREE.MeshLambertMaterial({ color: 0x3d2b1f });

      // Legs (For Walking Animation)
      const legGeom = new THREE.BoxGeometry(0.3, 1.0, 0.3);
      const legL = new THREE.Mesh(legGeom, pantsMat);
      legL.position.set(-0.22, 0.5, 0);
      group.add(legL);
      const legR = new THREE.Mesh(legGeom, pantsMat);
      legR.position.set(0.22, 0.5, 0);
      group.add(legR);

      // Torso / Tunic
      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.0, 0.5), tunicMat);
      torso.position.y = 1.4;
      torso.castShadow = true;
      group.add(torso);

      // Head
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 8, 8), skinMat);
      head.position.y = 2.1;
      group.add(head);

      // Straw Cap
      const hat = new THREE.Mesh(new THREE.ConeGeometry(0.48, 0.32, 8), thatchMat);
      hat.position.y = 2.35;
      group.add(hat);

      // Right Arm & Dynamic Tool Mount
      const armR = new THREE.Group();
      armR.position.set(0.5, 1.6, 0);
      const armMesh = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.7, 0.2), tunicMat);
      armMesh.position.y = -0.3;
      armR.add(armMesh);

      // Tool 1: Iron Woodcutter Axe
      const axeGroup = new THREE.Group();
      axeGroup.position.set(0, -0.6, 0.2);
      const axeHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.1, 6), timberMat);
      axeGroup.add(axeHandle);
      const axeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.22, 0.06), ironMat);
      axeBlade.position.set(0.12, 0.45, 0);
      axeGroup.add(axeBlade);
      armR.add(axeGroup);

      // Tool 2: Miner Pickaxe
      const pickGroup = new THREE.Group();
      pickGroup.position.set(0, -0.6, 0.2);
      const pickHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.2, 6), timberMat);
      pickGroup.add(pickHandle);
      const pickHead = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.1, 0.06), ironMat);
      pickHead.position.set(0, 0.5, 0);
      pickGroup.add(pickHead);
      pickGroup.visible = false;
      armR.add(pickGroup);

      // Tool 3: Carpenter Hammer
      const hammerGroup = new THREE.Group();
      hammerGroup.position.set(0, -0.6, 0.2);
      const hammerHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.8, 6), timberMat);
      hammerGroup.add(hammerHandle);
      const hammerHead = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.16, 0.16), ironMat);
      hammerHead.position.set(0, 0.35, 0);
      hammerGroup.add(hammerHead);
      hammerGroup.visible = false;
      armR.add(hammerGroup);

      // Tool 4: Hunter Spear / Bow
      const spearGroup = new THREE.Group();
      spearGroup.position.set(0, -0.6, 0.2);
      const spearShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.6, 6), timberMat);
      spearGroup.add(spearShaft);
      const spearTip = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.35, 6), ironMat);
      spearTip.position.y = 0.8;
      spearGroup.add(spearTip);
      spearGroup.visible = false;
      armR.add(spearGroup);

      group.add(armR);

      // Carried Resource Cargo (Back / Hip)
      const cargoGroup = new THREE.Group();
      cargoGroup.position.set(0, 1.3, -0.35);

      const logCargo = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 1.3, 6), timberMat);
      logCargo.rotation.z = Math.PI / 2;
      cargoGroup.add(logCargo);

      const oreCargo = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.45, 0.45), goldMat);
      oreCargo.visible = false;
      cargoGroup.add(oreCargo);

      const meatCargo = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.45, 0.45), new THREE.MeshLambertMaterial({ color: 0x991b1b }));
      meatCargo.visible = false;
      cargoGroup.add(meatCargo);

      cargoGroup.visible = false;
      group.add(cargoGroup);

      // Selection Ring Decal & Hitbox
      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.8);

      group.userData = {
        legL, legR, armR, axeGroup, pickGroup, hammerGroup, spearGroup,
        cargoGroup, logCargo, oreCargo, meatCargo, ring
      };

      return group;
    }

    // 2. SCOUT CAVALRY
    function createScoutMesh(isEnemy) {
      const group = new THREE.Group();
      const horseMat = new THREE.MeshLambertMaterial({ color: 0x5c3a21 });
      const riderMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Horse Torso
      const horseBody = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.1, 2.4), horseMat);
      horseBody.position.y = 1.4;
      horseBody.castShadow = true;
      group.add(horseBody);

      // Horse Neck & Head
      const neck = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.2, 0.8), horseMat);
      neck.position.set(0, 2.2, 1.1);
      neck.rotation.x = -Math.PI / 6;
      group.add(neck);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.8), horseMat);
      head.position.set(0, 2.7, 1.5);
      group.add(head);

      // 4 Horse Legs
      for (let x of [-0.45, 0.45]) {
        for (let z of [-0.8, 0.8]) {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.25, 1.2, 0.25), horseMat);
          leg.position.set(x, 0.6, z);
          leg.castShadow = true;
          group.add(leg);
        }
      }

      // Mounted Scout Rider
      const rider = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.9, 0.45), riderMat);
      rider.position.set(0, 2.3, 0.1);
      rider.castShadow = true;
      group.add(rider);

      const riderHead = new THREE.Mesh(new THREE.SphereGeometry(0.28, 6, 6), new THREE.MeshLambertMaterial({ color: 0xdfab76 }));
      riderHead.position.set(0, 2.9, 0.1);
      group.add(riderHead);

      const scoutSword = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.2, 0.04), ironMat);
      scoutSword.position.set(0.55, 2.4, 0.4);
      scoutSword.rotation.x = Math.PI / 4;
      group.add(scoutSword);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.6, 3.2);
      group.userData = { ring };

      return group;
    }

    // 3. SWORDSMAN (Militia & Man-at-Arms)
    function createSwordsmanMesh(isEnemy, tier = 1) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const legGeom = new THREE.BoxGeometry(0.3, 1.0, 0.3);
      const legL = new THREE.Mesh(legGeom, timberMat);
      legL.position.set(-0.22, 0.5, 0);
      group.add(legL);
      const legR = new THREE.Mesh(legGeom, timberMat);
      legR.position.set(0.22, 0.5, 0);
      group.add(legR);

      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.1, 0.55), tier > 1 ? ironMat : teamMat);
      torso.position.y = 1.45;
      torso.castShadow = true;
      group.add(torso);

      const helm = new THREE.Mesh(new THREE.SphereGeometry(0.32, 8, 8), ironMat);
      helm.position.y = 2.15;
      group.add(helm);

      // Sword
      const sword = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.3, 0.05), ironMat);
      sword.position.set(0.6, 1.4, 0.3);
      sword.rotation.x = Math.PI / 5;
      group.add(sword);

      // Shield
      const shield = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.85, 0.08), teamMat);
      shield.position.set(-0.55, 1.4, 0.2);
      group.add(shield);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.8);
      group.userData = { legL, legR, ring };
      return group;
    }

    // 4. SPEARMAN
    function createSpearmanMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const legL = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.0, 0.3), timberMat);
      legL.position.set(-0.22, 0.5, 0);
      group.add(legL);
      const legR = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.0, 0.3), timberMat);
      legR.position.set(0.22, 0.5, 0);
      group.add(legR);

      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.0, 0.5), teamMat);
      torso.position.y = 1.4;
      torso.castShadow = true;
      group.add(torso);

      const head = new THREE.Mesh(new THREE.SphereGeometry(0.3, 8, 8), ironMat);
      head.position.y = 2.1;
      group.add(head);

      // Long Pike / Spear (2.8m)
      const pike = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 2.8, 6), timberMat);
      pike.position.set(0.5, 1.8, 0.3);
      pike.rotation.x = Math.PI / 8;
      group.add(pike);

      const pikeTip = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.4, 6), ironMat);
      pikeTip.position.set(0.5, 3.2, 0.9);
      pikeTip.rotation.x = Math.PI / 8;
      group.add(pikeTip);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.8);
      group.userData = { legL, legR, ring };
      return group;
    }

    // 5. ARCHER
    function createArcherMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const legL = new THREE.Mesh(new THREE.BoxGeometry(0.28, 1.0, 0.28), timberMat);
      legL.position.set(-0.22, 0.5, 0);
      group.add(legL);
      const legR = new THREE.Mesh(new THREE.BoxGeometry(0.28, 1.0, 0.28), timberMat);
      legR.position.set(0.22, 0.5, 0);
      group.add(legR);

      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.75, 1.0, 0.5), teamMat);
      torso.position.y = 1.4;
      torso.castShadow = true;
      group.add(torso);

      const cap = new THREE.Mesh(new THREE.ConeGeometry(0.4, 0.35, 6), new THREE.MeshLambertMaterial({ color: 0x1e3a1e }));
      cap.position.y = 2.25;
      group.add(cap);

      // Longbow
      const bow = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.035, 6, 12, Math.PI), timberMat);
      bow.position.set(0.5, 1.5, 0.3);
      bow.rotation.y = Math.PI / 2;
      group.add(bow);

      // Quiver
      const quiver = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.9, 6), timberMat);
      quiver.position.set(-0.35, 1.5, -0.3);
      quiver.rotation.z = Math.PI / 6;
      group.add(quiver);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.8);
      group.userData = { legL, legR, ring };
      return group;
    }

    // 6. KNIGHT
    function createKnightMesh(isEnemy) {
      const group = new THREE.Group();
      const horseMat = new THREE.MeshLambertMaterial({ color: 0x222222 });
      const bardingMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const horseBody = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.2, 2.5), bardingMat);
      horseBody.position.y = 1.45;
      horseBody.castShadow = true;
      group.add(horseBody);

      const neck = new THREE.Mesh(new THREE.BoxGeometry(0.65, 1.3, 0.85), horseMat);
      neck.position.set(0, 2.3, 1.15);
      neck.rotation.x = -Math.PI / 6;
      group.add(neck);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.55, 0.85), ironMat);
      head.position.set(0, 2.8, 1.55);
      group.add(head);

      for (let x of [-0.48, 0.48]) {
        for (let z of [-0.85, 0.85]) {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.28, 1.2, 0.28), ironMat);
          leg.position.set(x, 0.6, z);
          group.add(leg);
        }
      }

      // Armored Knight in Plate Mail
      const knight = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.0, 0.55), ironMat);
      knight.position.set(0, 2.45, 0.1);
      group.add(knight);

      const greatHelm = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.65, 0.55), ironMat);
      greatHelm.position.set(0, 3.1, 0.1);
      group.add(greatHelm);

      // Heavy Lance
      const lance = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.12, 3.6, 6), ironMat);
      lance.position.set(0.65, 2.6, 1.2);
      lance.rotation.x = Math.PI / 3;
      group.add(lance);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.8, 3.4);
      group.userData = { ring };
      return group;
    }

    // 7. MONK
    function createMonkMesh(isEnemy) {
      const group = new THREE.Group();
      const robeMat = new THREE.MeshLambertMaterial({ color: 0x78350f });

      const robe = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.55, 1.6, 8), robeMat);
      robe.position.y = 0.85;
      robe.castShadow = true;
      group.add(robe);

      const hood = new THREE.Mesh(new THREE.SphereGeometry(0.35, 8, 8), robeMat);
      hood.position.y = 1.9;
      group.add(hood);

      const staff = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 2.2, 6), timberMat);
      staff.position.set(0.45, 1.1, 0.2);
      group.add(staff);

      const cross = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.06), goldMat);
      cross.position.set(0.45, 2.1, 0.2);
      group.add(cross);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.8);
      group.userData = { ring };
      return group;
    }

    // 8. TREBUCHET
    function createTrebuchetMesh(isEnemy) {
      const group = new THREE.Group();
      const chassis = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.5, 5.5), timberMat);
      chassis.position.y = 0.75;
      chassis.castShadow = true;
      group.add(chassis);

      // 4 Wheels
      for (let x of [-2.2, 2.2]) {
        for (let z of [-2.0, 2.0]) {
          const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.35, 10), timberMat);
          wheel.rotation.z = Math.PI / 2;
          wheel.position.set(x, 0.65, z);
          group.add(wheel);
        }
      }

      // A-Frame
      const frameL = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 4.6, 6), timberMat);
      frameL.position.set(-1.6, 2.9, 0);
      group.add(frameL);
      const frameR = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 4.6, 6), timberMat);
      frameR.position.set(1.6, 2.9, 0);
      group.add(frameR);

      // Throwing Arm & Counterweight
      const armGroup = new THREE.Group();
      armGroup.position.set(0, 5.0, 0);
      const arm = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.35, 8.5), timberMat);
      arm.position.set(0, 0, 1.4);
      armGroup.add(arm);

      const counterWeight = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 1.6), stoneMat);
      counterWeight.position.set(0, -1.0, -2.4);
      armGroup.add(counterWeight);
      group.add(armGroup);

      const ring = createSelectionRing(isEnemy);
      group.add(ring);
      addUnitHitbox(group, 3.0, 6.0);
      group.userData = { ring, armGroup };
      return group;
    }

    // 9. WILD ANIMALS & SHEEP
    function createSheepMesh() {
      const group = new THREE.Group();
      const wool = new THREE.Mesh(new THREE.SphereGeometry(0.7, 8, 8), new THREE.MeshLambertMaterial({ color: 0xedebe4 }));
      wool.scale.set(1, 0.85, 1.25);
      wool.position.y = 0.75;
      wool.castShadow = true;
      group.add(wool);

      const head = new THREE.Mesh(new THREE.SphereGeometry(0.28, 6, 6), new THREE.MeshLambertMaterial({ color: 0x1a1a1a }));
      head.position.set(0, 0.9, 0.8);
      group.add(head);

      for (let x of [-0.3, 0.3]) {
        for (let z of [-0.35, 0.35]) {
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.55, 6), new THREE.MeshLambertMaterial({ color: 0x1a1a1a }));
          leg.position.set(x, 0.28, z);
          group.add(leg);
        }
      }
      const ring = createSelectionRing(false);
      group.add(ring);
      addUnitHitbox(group, 1.2, 1.8);
      group.userData = { ring };
      return group;
    }

    function createBoarMesh() {
      const group = new THREE.Group();
      const boarMat = new THREE.MeshLambertMaterial({ color: 0x3d2314 });

      const body = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.95, 1.8), boarMat);
      body.position.y = 0.75;
      body.castShadow = true;
      group.add(body);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.85), boarMat);
      head.position.set(0, 0.75, 1.1);
      group.add(head);

      const snout = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.35, 0.4), new THREE.MeshLambertMaterial({ color: 0x241208 }));
      snout.position.set(0, 0.65, 1.6);
      group.add(snout);

      // Curved Tusks
      for (let x of [-0.28, 0.28]) {
        const tusk = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.4, 6), new THREE.MeshLambertMaterial({ color: 0xfafafa }));
        tusk.position.set(x, 0.75, 1.5);
        tusk.rotation.x = -Math.PI / 4;
        group.add(tusk);
      }

      // 4 Legs
      for (let x of [-0.4, 0.4]) {
        for (let z of [-0.6, 0.6]) {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.7, 0.22), boarMat);
          leg.position.set(x, 0.35, z);
          group.add(leg);
        }
      }

      const ring = createSelectionRing(false);
      group.add(ring);
      addUnitHitbox(group, 1.4, 2.0);
      group.userData = { ring };
      return group;
    }

    function createDeerMesh() {
      const group = new THREE.Group();
      const tanMat = new THREE.MeshLambertMaterial({ color: 0x9c6644 });
      const hornMat = new THREE.MeshLambertMaterial({ color: 0xd4a373 });
      const darkMat = new THREE.MeshLambertMaterial({ color: 0x3d2b1f });

      // Body
      const body = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.85, 1.6), tanMat);
      body.position.y = 1.2;
      body.castShadow = true;
      group.add(body);

      // Neck & Head
      const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.25, 0.9, 6), tanMat);
      neck.position.set(0, 1.8, 0.7);
      neck.rotation.x = -Math.PI / 6;
      group.add(neck);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.6), tanMat);
      head.position.set(0, 2.2, 0.95);
      group.add(head);

      // Antlers
      for (let x of [-0.2, 0.2]) {
        const antler = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.7, 5), hornMat);
        antler.position.set(x, 2.6, 0.9);
        antler.rotation.z = x > 0 ? 0.3 : -0.3;
        group.add(antler);
      }

      // 4 Slender Legs
      for (let x of [-0.3, 0.3]) {
        for (let z of [-0.5, 0.5]) {
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1.2, 6), darkMat);
          leg.position.set(x, 0.6, z);
          group.add(leg);
        }
      }

      const ring = createSelectionRing(false);
      group.add(ring);
      addUnitHitbox(group, 1.3, 2.5);
      group.userData = { ring };
      return group;
    }

    function createRelicMesh() {
      const group = new THREE.Group();
      const plinth = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.3, 0.5, 8), stoneMat);
      plinth.position.y = 0.25;
      group.add(plinth);

      const chest = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.65, 0.65), goldMat);
      chest.position.y = 0.8;
      chest.castShadow = true;
      group.add(chest);

      const ray = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.7, 7, 8), new THREE.MeshBasicMaterial({ color: 0xffe066, transparent: true, opacity: 0.35 }));
      ray.position.y = 4.0;
      group.add(ray);

      const ring = createSelectionRing(false);
      group.add(ring);
      addUnitHitbox(group, 1.4, 2.5);
      group.userData = { ring };
      return group;
    }
    """
