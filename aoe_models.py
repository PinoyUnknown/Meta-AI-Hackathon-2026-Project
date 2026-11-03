def get_aoe_models_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES HIGH-FIDELITY 3D ARCHITECTURAL MODELS & ASSETS
    // =========================================================================

    const COLOR_PLAYER_PRIMARY = 0x1d4ed8;   // Royal Cobalt Blue
    const COLOR_PLAYER_SECONDARY = 0x2563eb;
    const COLOR_ENEMY_PRIMARY = 0xb91c1c;    // Crimson Red
    const COLOR_ENEMY_SECONDARY = 0xdc2626;

    // Materials Palette with Procedural Textures
    const timberMat = new THREE.MeshLambertMaterial({ map: woodTex });
    const stoneMat = new THREE.MeshLambertMaterial({ map: stoneTex });
    const plasterMat = new THREE.MeshLambertMaterial({ map: plasterTex });
    const thatchMat = new THREE.MeshLambertMaterial({ map: thatchTex });
    const tileMat = new THREE.MeshLambertMaterial({ map: tileTex });
    const ironMat = new THREE.MeshStandardMaterial({ map: ironTex, roughness: 0.35, metalness: 0.75 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xffd700, roughness: 0.25, metalness: 0.85 });
    const whiteMarbleMat = new THREE.MeshLambertMaterial({ color: 0xf5f3ee });

    function createBuildingFootprintRing(sizeX, sizeZ, isEnemy) {
      const geom = new THREE.PlaneGeometry(sizeX + 1.2, sizeZ + 1.2);
      geom.rotateX(-Math.PI / 2);
      const ringMat = new THREE.MeshBasicMaterial({
        color: isEnemy ? 0xef4444 : 0x3b82f6,
        wireframe: true,
        side: THREE.DoubleSide
      });
      const ring = new THREE.Mesh(geom, ringMat);
      ring.position.y = 0.15;
      ring.visible = false;
      return ring;
    }

    // 1. TOWN CENTER (Detailed Medieval Civic Center)
    function createTownCenterMesh(age, isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Raised Cobblestone Apron Base
      const baseGeom = new THREE.BoxGeometry(12, 0.6, 12);
      const base = new THREE.Mesh(baseGeom, stoneMat);
      base.position.y = 0.3;
      base.receiveShadow = true;
      group.add(base);

      // Low Stone Foundation Rim
      const rimGeom = new THREE.BoxGeometry(12.4, 0.4, 12.4);
      const rim = new THREE.Mesh(rimGeom, stoneMat);
      rim.position.y = 0.6;
      group.add(rim);

      // 4 Heavy Dark Timber Corner Pillars with Iron Brackets
      const pillarGeom = new THREE.CylinderGeometry(0.5, 0.6, 6.5, 8);
      const pillarOffsets = [[-4.5, -4.5], [4.5, -4.5], [-4.5, 4.5], [4.5, 4.5]];
      pillarOffsets.forEach(pos => {
        const p = new THREE.Mesh(pillarGeom, timberMat);
        p.position.set(pos[0], 3.5, pos[1]);
        p.castShadow = true;
        group.add(p);

        // Iron Base Bracket
        const br = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.4, 8), ironMat);
        br.position.set(pos[0], 0.8, pos[1]);
        group.add(br);
      });

      // Wooden Deck Flooring
      const deckGeom = new THREE.BoxGeometry(10.5, 0.2, 10.5);
      const deck = new THREE.Mesh(deckGeom, timberMat);
      deck.position.y = 0.7;
      deck.receiveShadow = true;
      group.add(deck);

      // Central Stone Hearth & Fireplace Chimney
      const chimneyGeom = new THREE.BoxGeometry(2.4, 11, 2.4);
      const chimney = new THREE.Mesh(chimneyGeom, stoneMat);
      chimney.position.set(0, 5.5, 0);
      chimney.castShadow = true;
      group.add(chimney);

      // Glowing Hearth Coals
      const hearthFire = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.2), new THREE.MeshBasicMaterial({ color: 0xff5500 }));
      hearthFire.position.set(0, 1.2, 1.0);
      group.add(hearthFire);

      // Authentic Roof Structure (Thatched in Dark Age, Clay Tiled in Feudal/Castle)
      const roofMat = (age === 'Dark Age') ? thatchMat : tileMat;
      const roofGeom = new THREE.ConeGeometry(9.5, 5, 4);
      const roof = new THREE.Mesh(roofGeom, roofMat);
      roof.position.y = 9.2;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Overhanging Timber Eaves
      const eaveGeom = new THREE.BoxGeometry(11, 0.3, 11);
      const eave = new THREE.Mesh(eaveGeom, timberMat);
      eave.position.y = 6.8;
      group.add(eave);

      // Central Bell Turret & Bronze Bell
      const turretGeom = new THREE.BoxGeometry(2.2, 3.2, 2.2);
      const turret = new THREE.Mesh(turretGeom, timberMat);
      turret.position.set(0, 12, 0);
      group.add(turret);

      const bellGeom = new THREE.ConeGeometry(0.6, 0.9, 8);
      const bell = new THREE.Mesh(bellGeom, goldMat);
      bell.position.set(0, 11.5, 0);
      group.add(bell);

      // Flying Royal Pennant
      const flagPole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 3.5, 6), timberMat);
      flagPole.position.set(0, 14.5, 0);
      group.add(flagPole);

      const flagGeom = new THREE.PlaneGeometry(1.8, 1.1);
      const flag = new THREE.Mesh(flagGeom, teamMat);
      flag.position.set(0.9, 14.8, 0);
      group.add(flag);

      // Footprint Decal
      const ring = createBuildingFootprintRing(12, 12, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 2. HOUSE (English Half-Timbered Cottage)
    function createHouseMesh(age, isEnemy) {
      const group = new THREE.Group();
      const roofMat = (age === 'Dark Age') ? thatchMat : tileMat;

      // Foundation Plinth
      const base = new THREE.Mesh(new THREE.BoxGeometry(5.4, 0.4, 5.4), stoneMat);
      base.position.y = 0.2;
      group.add(base);

      // Plaster & Half-Timbered Walls
      const walls = new THREE.Mesh(new THREE.BoxGeometry(4.8, 3.2, 4.8), plasterMat);
      walls.position.y = 1.9;
      walls.castShadow = true;
      group.add(walls);

      // Pitched Gable Roof
      const roofGeom = new THREE.ConeGeometry(4.2, 2.8, 4);
      const roof = new THREE.Mesh(roofGeom, roofMat);
      roof.position.y = 4.8;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Stone Chimney
      const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.8, 4.5, 0.8), stoneMat);
      chimney.position.set(1.8, 2.5, 1.4);
      group.add(chimney);

      // Wooden Plank Door
      const door = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.8, 0.1), timberMat);
      door.position.set(0, 1.3, 2.45);
      group.add(door);

      const ring = createBuildingFootprintRing(5.4, 5.4, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 3. MILL (Lattice Sails & Grain Sacks)
    function createMillMesh() {
      const group = new THREE.Group();

      // Octagonal Stone Base
      const base = new THREE.Mesh(new THREE.CylinderGeometry(3.0, 3.6, 5.5, 8), stoneMat);
      base.position.y = 2.75;
      base.castShadow = true;
      group.add(base);

      // Timber Cap
      const cap = new THREE.Mesh(new THREE.ConeGeometry(3.2, 2.4, 8), thatchMat);
      cap.position.y = 6.6;
      group.add(cap);

      // Windmill Sails Hub & 4 Rotating Lattice Blades
      const rotorGroup = new THREE.Group();
      rotorGroup.position.set(0, 5.5, 2.8);

      const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.6, 8), timberMat);
      hub.rotation.x = Math.PI / 2;
      rotorGroup.add(hub);

      for (let i = 0; i < 4; i++) {
        const bladeGroup = new THREE.Group();
        bladeGroup.rotation.z = (i * Math.PI) / 2;

        const spar = new THREE.Mesh(new THREE.BoxGeometry(0.12, 4.4, 0.12), timberMat);
        spar.position.y = 2.2;
        bladeGroup.add(spar);

        const sailCloth = new THREE.Mesh(new THREE.PlaneGeometry(0.85, 3.4), thatchMat);
        sailCloth.position.set(0.45, 2.4, 0.05);
        bladeGroup.add(sailCloth);

        rotorGroup.add(bladeGroup);
      }
      group.add(rotorGroup);

      const ring = createBuildingFootprintRing(6.5, 6.5, false);
      group.add(ring);
      group.userData = { ring, rotorGroup };

      return group;
    }

    // 4. LUMBER CAMP (Log Piles & Sawbuck)
    function createLumberCampMesh() {
      const group = new THREE.Group();

      // Open Post Shelter
      const floor = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.3, 6.5), timberMat);
      floor.position.y = 0.15;
      group.add(floor);

      for (let x of [-2.6, 2.6]) {
        for (let z of [-2.6, 2.6]) {
          const post = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 3.5, 6), timberMat);
          post.position.set(x, 1.9, z);
          group.add(post);
        }
      }

      // Shed Roof
      const roof = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.3, 7.0), thatchMat);
      roof.position.y = 3.7;
      roof.rotation.x = 0.12;
      group.add(roof);

      // Stacked Timber Logs
      for (let y = 0; y < 3; y++) {
        for (let i = 0; i < 4 - y; i++) {
          const log = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 3.2, 6), timberMat);
          log.rotation.z = Math.PI / 2;
          log.position.set(0, 0.4 + y * 0.45, -1.2 + (i - (3 - y) * 0.5) * 0.65);
          group.add(log);
        }
      }

      const ring = createBuildingFootprintRing(6.5, 6.5, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 5. MINING CAMP (Ore Baskets & Anvil)
    function createMiningCampMesh() {
      const group = new THREE.Group();

      const base = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.3, 6.5), stoneMat);
      base.position.y = 0.15;
      group.add(base);

      // Wooden Lean-To
      const shed = new THREE.Mesh(new THREE.BoxGeometry(5.0, 3.2, 3.0), timberMat);
      shed.position.set(0, 1.8, -1.2);
      group.add(shed);

      // Ore Cart & Gold / Stone Nuggets
      const cart = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.9, 2.2), timberMat);
      cart.position.set(1.4, 0.6, 1.4);
      group.add(cart);

      const orePile = new THREE.Mesh(new THREE.DodecahedronGeometry(0.55), goldMat);
      orePile.position.set(1.4, 1.1, 1.4);
      group.add(orePile);

      const ring = createBuildingFootprintRing(6.5, 6.5, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 6. FARM (Tilled Dark Soil & Golden Crops)
    function createFarmMesh() {
      const group = new THREE.Group();

      // Furrowed Earth Field
      const soilMat = new THREE.MeshLambertMaterial({ color: 0x3d2714 });
      const soil = new THREE.Mesh(new THREE.BoxGeometry(8.5, 0.25, 8.5), soilMat);
      soil.position.y = 0.12;
      soil.receiveShadow = true;
      group.add(soil);

      // Golden Wheat Rows
      const cropMat = new THREE.MeshLambertMaterial({ color: 0xd4a037 });
      for (let z = -3.2; z <= 3.2; z += 1.2) {
        const cropRow = new THREE.Mesh(new THREE.BoxGeometry(7.5, 0.75, 0.55), cropMat);
        cropRow.position.set(0, 0.6, z);
        group.add(cropRow);
      }

      const ring = createBuildingFootprintRing(8.5, 8.5, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 7. BARRACKS (Military Stockade & Training Arena)
    function createBarracksMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Sturdy Ashlar Stone Base
      const stoneBase = new THREE.Mesh(new THREE.BoxGeometry(10.5, 1.5, 8.5), stoneMat);
      stoneBase.position.y = 0.75;
      group.add(stoneBase);

      // Timber Training Hall
      const hall = new THREE.Mesh(new THREE.BoxGeometry(9.5, 3.8, 7.5), timberMat);
      hall.position.y = 3.4;
      hall.castShadow = true;
      group.add(hall);

      // Gabled Roof
      const roof = new THREE.Mesh(new THREE.ConeGeometry(7.2, 3.2, 4), thatchMat);
      roof.position.y = 6.8;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Wall Shields & Heraldry
      for (let x of [-3.5, 3.5]) {
        const shield = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.1, 8), teamMat);
        shield.rotation.x = Math.PI / 2;
        shield.position.set(x, 3.5, 4.3);
        group.add(shield);
      }

      const ring = createBuildingFootprintRing(10.5, 8.5, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 8. ARCHERY RANGE
    function createArcheryRangeMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const lodge = new THREE.Mesh(new THREE.BoxGeometry(8.5, 4.0, 5.5), timberMat);
      lodge.position.set(0, 2.0, -1.8);
      lodge.castShadow = true;
      group.add(lodge);

      const roof = new THREE.Mesh(new THREE.ConeGeometry(6.2, 2.8, 4), thatchMat);
      roof.position.set(0, 5.2, -1.8);
      roof.rotation.y = Math.PI / 4;
      group.add(roof);

      // 3 Straw Target Dummies
      for (let x of [-2.5, 0, 2.5]) {
        const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.2, 6), timberMat);
        stand.position.set(x, 1.1, 2.2);
        group.add(stand);

        const target = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.15, 12), teamMat);
        target.rotation.x = Math.PI / 2;
        target.position.set(x, 1.5, 2.2);
        group.add(target);
      }

      const ring = createBuildingFootprintRing(9.5, 8.5, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 9. STABLE
    function createStableMesh(isEnemy) {
      const group = new THREE.Group();

      const barn = new THREE.Mesh(new THREE.BoxGeometry(11, 4.5, 7.5), timberMat);
      barn.position.y = 2.25;
      barn.castShadow = true;
      group.add(barn);

      const roof = new THREE.Mesh(new THREE.ConeGeometry(8, 3.2, 4), thatchMat);
      roof.position.y = 5.8;
      roof.rotation.y = Math.PI / 4;
      group.add(roof);

      // 3 Horse Stalls with Gates
      for (let x of [-3.2, 0, 3.2]) {
        const stallDoor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.8, 0.15), timberMat);
        stallDoor.position.set(x, 1.0, 3.85);
        group.add(stallDoor);
      }

      const ring = createBuildingFootprintRing(11, 8.5, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 10. BLACKSMITH (Stone Hearth, Bellows & Forge)
    function createBlacksmithMesh() {
      const group = new THREE.Group();

      const base = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.4, 7.0), stoneMat);
      base.position.y = 0.2;
      group.add(base);

      const forge = new THREE.Mesh(new THREE.BoxGeometry(2.8, 5.0, 2.8), stoneMat);
      forge.position.set(1.5, 2.5, -1.2);
      group.add(forge);

      const fire = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.2), new THREE.MeshBasicMaterial({ color: 0xff3300 }));
      fire.position.set(1.5, 1.4, -0.4);
      group.add(fire);

      const anvil = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.85, 0.5), ironMat);
      anvil.position.set(-1.2, 0.6, 0.8);
      group.add(anvil);

      const ring = createBuildingFootprintRing(7.0, 7.0, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 11. MONASTERY (Romanesque Stone Basilica)
    function createMonasteryMesh(isEnemy) {
      const group = new THREE.Group();

      const nave = new THREE.Mesh(new THREE.BoxGeometry(11, 6.5, 7.5), stoneMat);
      nave.position.y = 3.25;
      nave.castShadow = true;
      group.add(nave);

      const roof = new THREE.Mesh(new THREE.ConeGeometry(8, 4, 4), tileMat);
      roof.position.y = 8.8;
      roof.rotation.y = Math.PI / 4;
      group.add(roof);

      // Bell Tower & Gilded Cross
      const tower = new THREE.Mesh(new THREE.BoxGeometry(2.8, 12, 2.8), stoneMat);
      tower.position.set(4.2, 6.0, 0);
      group.add(tower);

      const spire = new THREE.Mesh(new THREE.ConeGeometry(2.2, 5.5, 8), tileMat);
      spire.position.set(4.2, 14.5, 0);
      group.add(spire);

      const cross = new THREE.Mesh(new THREE.BoxGeometry(0.25, 2.2, 0.25), goldMat);
      cross.position.set(4.2, 18, 0);
      group.add(cross);

      const ring = createBuildingFootprintRing(12, 8.5, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 12. CASTLE (Colossal 4-Tower Stone Citadel)
    function createCastleMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Central Stone Keep
      const keep = new THREE.Mesh(new THREE.BoxGeometry(18, 12, 15), stoneMat);
      keep.position.y = 6.3;
      keep.castShadow = true;
      group.add(keep);

      // 4 Massive Round Bastion Towers
      const bOffsets = [[-9, -7.5], [9, -7.5], [-9, 7.5], [9, 7.5]];
      bOffsets.forEach(pos => {
        const tower = new THREE.Mesh(new THREE.CylinderGeometry(2.8, 3.4, 17, 10), stoneMat);
        tower.position.set(pos[0], 8.5, pos[1]);
        tower.castShadow = true;
        group.add(tower);

        // Crenellated Battlement Crown
        const cr = new THREE.Mesh(new THREE.CylinderGeometry(3.5, 3.1, 1.8, 10), stoneMat);
        cr.position.set(pos[0], 17.5, pos[1]);
        group.add(cr);

        // Banner
        const flag = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.2), teamMat);
        flag.position.set(pos[0] + 0.9, 20, pos[1]);
        group.add(flag);
      });

      // Iron Portcullis Gate
      const gate = new THREE.Mesh(new THREE.BoxGeometry(5, 6, 0.8), ironMat);
      gate.position.set(0, 3, 7.6);
      group.add(gate);

      const ring = createBuildingFootprintRing(20, 18, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 13. WONDER OF THE WORLD (Imperial Colossal Cathedral)
    function createWonderMesh() {
      const group = new THREE.Group();
      const base = new THREE.Mesh(new THREE.BoxGeometry(24, 10, 18), whiteMarbleMat);
      base.position.y = 5.3;
      base.castShadow = true;
      group.add(base);

      // Soaring Central Dome
      const dome = new THREE.Mesh(new THREE.SphereGeometry(6, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), goldMat);
      dome.position.y = 10.3;
      dome.castShadow = true;
      group.add(dome);

      // Gilded Spire
      const spire = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 2.5, 8), whiteMarbleMat);
      spire.position.y = 17;
      group.add(spire);

      const cross = new THREE.Mesh(new THREE.BoxGeometry(0.35, 2.2, 0.35), goldMat);
      cross.position.set(0, 19, 0);
      group.add(cross);

      const ring = createBuildingFootprintRing(25, 20, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    // 14. WATCHTOWER & WALL
    function createWatchtowerMesh(age, isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });
      const towerMat = (age === 'Dark Age') ? timberMat : stoneMat;

      const shaft = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 2.0, 12, 8), towerMat);
      shaft.position.y = 6.3;
      shaft.castShadow = true;
      group.add(shaft);

      const bal = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 1.8, 2.2, 8), towerMat);
      bal.position.y = 12.8;
      group.add(bal);

      const flag = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 0.9), teamMat);
      flag.position.set(0, 15, 0);
      group.add(flag);

      const ring = createBuildingFootprintRing(4.5, 4.5, isEnemy);
      group.add(ring);
      group.userData = { ring };

      return group;
    }

    function createWallMesh() {
      const group = new THREE.Group();
      const wall = new THREE.Mesh(new THREE.BoxGeometry(5.5, 3.5, 1.6), stoneMat);
      wall.position.y = 2.05;
      wall.castShadow = true;
      group.add(wall);

      const ring = createBuildingFootprintRing(5.5, 2.0, false);
      group.add(ring);
      group.userData = { ring };

      return group;
    }
    """
