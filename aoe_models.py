def get_aoe_models_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES 3D MODELS & ARCHITECTURE ACROSS THE 4 AGES
    // =========================================================================

    // Dynamic Team Colors
    const COLOR_PLAYER_PRIMARY = 0x2563eb;   // Team Blue
    const COLOR_PLAYER_SECONDARY = 0x1d4ed8;
    const COLOR_ENEMY_PRIMARY = 0xdc2626;    // Team Red
    const COLOR_ENEMY_SECONDARY = 0x991b1b;

    // Materials Palette
    const timberMat = new THREE.MeshLambertMaterial({ map: woodTex });
    const stoneMat = new THREE.MeshLambertMaterial({ map: stoneTex });
    const plasterMat = new THREE.MeshLambertMaterial({ map: plasterTex });
    const thatchMat = new THREE.MeshLambertMaterial({ map: thatchTex });
    const tileMat = new THREE.MeshLambertMaterial({ map: tileTex });
    const ironMat = new THREE.MeshStandardMaterial({ map: ironTex, roughness: 0.4, metalness: 0.7 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xffd700, roughness: 0.3, metalness: 0.8 });
    const whiteMarbleMat = new THREE.MeshLambertMaterial({ color: 0xf5f3ee });

    // 1. TOWN CENTER (Upgrades through Dark -> Feudal -> Castle -> Imperial)
    function createTownCenterMesh(age, isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      if (age === 'Dark Age') {
        // Dark Age: Heavy timber pillars, open gathering hall, thatched roof, central bell
        const baseGeom = new THREE.BoxGeometry(14, 0.8, 14);
        const base = new THREE.Mesh(baseGeom, stoneMat);
        base.position.y = 0.4;
        base.receiveShadow = true;
        group.add(base);

        // 4 Timber Pillars
        const pillarGeom = new THREE.CylinderGeometry(0.6, 0.7, 7, 8);
        const pOffsets = [[-5, -5], [5, -5], [-5, 5], [5, 5]];
        pOffsets.forEach(pos => {
          const p = new THREE.Mesh(pillarGeom, timberMat);
          p.position.set(pos[0], 3.9, pos[1]);
          p.castShadow = true;
          group.add(p);
        });

        // Thatched Pyramid Roof
        const roofGeom = new THREE.ConeGeometry(11, 6, 4);
        const roof = new THREE.Mesh(roofGeom, thatchMat);
        roof.position.y = 10.4;
        roof.rotation.y = Math.PI / 4;
        roof.castShadow = true;
        group.add(roof);

        // Bell Turret on Apex
        const turretGeom = new THREE.CylinderGeometry(0.8, 0.8, 2.5, 6);
        const turret = new THREE.Mesh(turretGeom, timberMat);
        turret.position.y = 14;
        group.add(turret);

        // Bronze Bell
        const bellGeom = new THREE.ConeGeometry(0.5, 0.9, 8);
        const bell = new THREE.Mesh(bellGeom, goldMat);
        bell.position.y = 13.6;
        group.add(bell);

        // Team Flag
        const flagGeom = new THREE.PlaneGeometry(1.8, 1.2);
        const flag = new THREE.Mesh(flagGeom, teamMat);
        flag.position.set(0, 15.5, 0.9);
        group.add(flag);

        // Center Campfire & Supplies
        const firePitGeom = new THREE.CylinderGeometry(1.5, 1.8, 0.4, 8);
        const firePit = new THREE.Mesh(firePitGeom, stoneMat);
        firePit.position.set(0, 0.8, 0);
        group.add(firePit);
      } else if (age === 'Feudal Age') {
        // Feudal Age: Timber-framed walls, tiled gabled roof, wooden battlements
        const hallGeom = new THREE.BoxGeometry(16, 7, 14);
        const hall = new THREE.Mesh(hallGeom, plasterMat);
        hall.position.y = 3.9;
        hall.castShadow = true;
        group.add(hall);

        // Tiled Roof
        const roofGeom = new THREE.ConeGeometry(13, 6, 4);
        const roof = new THREE.Mesh(roofGeom, tileMat);
        roof.position.y = 10.4;
        roof.rotation.y = Math.PI / 4;
        roof.castShadow = true;
        group.add(roof);

        // Wooden Watchtower corner
        const twGeom = new THREE.CylinderGeometry(1.8, 2.2, 13, 8);
        const tw = new THREE.Mesh(twGeom, timberMat);
        tw.position.set(6, 6.5, 5);
        tw.castShadow = true;
        group.add(tw);

        // Team Banners
        const bannerGeom = new THREE.BoxGeometry(0.3, 3, 1.5);
        const b = new THREE.Mesh(bannerGeom, teamMat);
        b.position.set(6, 11, 6);
        group.add(b);
      } else {
        // Castle / Imperial Age: Imposing stone ashlar citadel with corner bastions
        const keepGeom = new THREE.BoxGeometry(18, 9, 16);
        const keep = new THREE.Mesh(keepGeom, stoneMat);
        keep.position.y = 4.9;
        keep.castShadow = true;
        group.add(keep);

        // 4 Corner Stone Turrets
        const tGeom = new THREE.CylinderGeometry(2, 2.4, 14, 8);
        const tPositions = [[-8, -7], [8, -7], [-8, 7], [8, 7]];
        tPositions.forEach(pos => {
          const t = new THREE.Mesh(tGeom, stoneMat);
          t.position.set(pos[0], 7, pos[1]);
          t.castShadow = true;
          group.add(t);

          // Turret Conical Roof
          const crGeom = new THREE.ConeGeometry(2.4, 4, 8);
          const cr = new THREE.Mesh(crGeom, tileMat);
          cr.position.set(pos[0], 16, pos[1]);
          group.add(cr);
        });

        // Iron Portcullis Arch
        const gateGeom = new THREE.BoxGeometry(4.5, 5.5, 1);
        const gate = new THREE.Mesh(gateGeom, ironMat);
        gate.position.set(0, 3, 8.2);
        group.add(gate);

        // Royal Crest Banner
        const bannerGeom = new THREE.BoxGeometry(3, 4.5, 0.2);
        const banner = new THREE.Mesh(bannerGeom, teamMat);
        banner.position.set(0, 8.5, 8.2);
        group.add(banner);
      }

      return group;
    }

    // 2. HOUSE (Provides +5 Pop Cap)
    function createHouseMesh(age, isEnemy) {
      const group = new THREE.Group();
      const bGeom = new THREE.BoxGeometry(6, 4, 5);
      const bMat = age === 'Dark Age' ? timberMat : plasterMat;
      const b = new THREE.Mesh(bGeom, bMat);
      b.position.y = 2.4;
      b.castShadow = true;
      group.add(b);

      const rGeom = new THREE.ConeGeometry(5, 3.2, 4);
      const rMat = age === 'Dark Age' ? thatchMat : tileMat;
      const r = new THREE.Mesh(rGeom, rMat);
      r.position.y = 6;
      r.rotation.y = Math.PI / 4;
      r.castShadow = true;
      group.add(r);

      // Chimney
      const chGeom = new THREE.BoxGeometry(0.8, 3, 0.8);
      const ch = new THREE.Mesh(chGeom, stoneMat);
      ch.position.set(1.8, 6.2, 1.2);
      group.add(ch);

      return group;
    }

    // 3. MILL (Resource drop-off for Food with rotating 4-blade windmill)
    function createMillMesh() {
      const group = new THREE.Group();
      const bodyGeom = new THREE.CylinderGeometry(3.5, 4.5, 8, 8);
      const body = new THREE.Mesh(bodyGeom, stoneMat);
      body.position.y = 4.4;
      body.castShadow = true;
      group.add(body);

      const capGeom = new THREE.ConeGeometry(4.5, 3.5, 8);
      const cap = new THREE.Mesh(capGeom, thatchMat);
      cap.position.y = 10;
      cap.castShadow = true;
      group.add(cap);

      // Rotating Windmill Rotor
      const rotorGroup = new THREE.Group();
      rotorGroup.position.set(0, 8.2, 3.8);

      const hubGeom = new THREE.CylinderGeometry(0.5, 0.5, 0.8, 8);
      const hub = new THREE.Mesh(hubGeom, timberMat);
      hub.rotation.x = Math.PI / 2;
      rotorGroup.add(hub);

      // 4 Sails
      const bladeGeom = new THREE.BoxGeometry(0.6, 9, 0.1);
      for (let i = 0; i < 4; i++) {
        const blade = new THREE.Mesh(bladeGeom, timberMat);
        blade.rotation.z = (Math.PI / 2) * i;
        rotorGroup.add(blade);
      }
      group.add(rotorGroup);
      group.userData.rotor = rotorGroup; // Animated in render loop

      return group;
    }

    // 4. LUMBER CAMP & MINING CAMP
    function createLumberCampMesh() {
      const group = new THREE.Group();
      const shedGeom = new THREE.BoxGeometry(7, 4.5, 6);
      const shed = new THREE.Mesh(shedGeom, timberMat);
      shed.position.y = 2.65;
      shed.castShadow = true;
      group.add(shed);

      // Stacked Cut Logs
      const logGeom = new THREE.CylinderGeometry(0.4, 0.4, 4, 8);
      for (let i = 0; i < 6; i++) {
        const log = new THREE.Mesh(logGeom, timberMat);
        log.rotation.z = Math.PI / 2;
        log.position.set(4, 0.5 + (i % 3) * 0.7, -1 + Math.floor(i / 3) * 1);
        group.add(log);
      }
      return group;
    }

    function createMiningCampMesh() {
      const group = new THREE.Group();
      const shedGeom = new THREE.BoxGeometry(7, 4.5, 6);
      const shed = new THREE.Mesh(shedGeom, stoneMat);
      shed.position.y = 2.65;
      shed.castShadow = true;
      group.add(shed);

      // Ore Cart & Bins
      const cartGeom = new THREE.BoxGeometry(2.5, 1.6, 1.8);
      const cart = new THREE.Mesh(cartGeom, ironMat);
      cart.position.set(4.2, 1, 0);
      group.add(cart);

      // Gold Nuggets in Cart
      const nuggetGeom = new THREE.DodecahedronGeometry(0.4);
      const n = new THREE.Mesh(nuggetGeom, goldMat);
      n.position.set(4.2, 1.8, 0);
      group.add(n);

      return group;
    }

    // 5. FARM (3x3 furrowed field with wheat crops)
    function createFarmMesh() {
      const group = new THREE.Group();
      const soilGeom = new THREE.BoxGeometry(9, 0.3, 9);
      const soilMat = new THREE.MeshLambertMaterial({ color: 0x4a2e12 });
      const soil = new THREE.Mesh(soilGeom, soilMat);
      soil.position.y = 0.15;
      soil.receiveShadow = true;
      group.add(soil);

      // Growing Wheat Bundles
      const wheatGeom = new THREE.CylinderGeometry(0.2, 0.2, 1.4, 4);
      const wheatMat = new THREE.MeshLambertMaterial({ color: 0xd4a34b });
      for (let x = -3; x <= 3; x += 1.5) {
        for (let z = -3; z <= 3; z += 1.5) {
          const w = new THREE.Mesh(wheatGeom, wheatMat);
          w.position.set(x + (Math.random()-0.5)*0.3, 0.8, z + (Math.random()-0.5)*0.3);
          group.add(w);
        }
      }

      // Wooden Split-Rail Perimeter
      const fenceGeom = new THREE.BoxGeometry(9.4, 0.6, 0.2);
      const f1 = new THREE.Mesh(fenceGeom, timberMat);
      f1.position.set(0, 0.4, 4.6);
      group.add(f1);
      const f2 = f1.clone();
      f2.position.set(0, 0.4, -4.6);
      group.add(f2);

      return group;
    }

    // 6. BARRACKS (Trains Infantry: Militia, Man-at-Arms, Spearmen)
    function createBarracksMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const hallGeom = new THREE.BoxGeometry(11, 5.5, 9);
      const hall = new THREE.Mesh(hallGeom, timberMat);
      hall.position.y = 3.15;
      hall.castShadow = true;
      group.add(hall);

      const roofGeom = new THREE.ConeGeometry(8.5, 4, 4);
      const roof = new THREE.Mesh(roofGeom, tileMat);
      roof.position.y = 7.9;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Straw Training Dummy
      const dummyPost = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 2.5, 6), timberMat);
      dummyPost.position.set(5.5, 1.25, 2);
      group.add(dummyPost);

      const dummyHead = new THREE.Mesh(new THREE.SphereGeometry(0.5, 6, 6), thatchMat);
      dummyHead.position.set(5.5, 2.5, 2);
      group.add(dummyHead);

      // Team Shield on Wall
      const shield = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.2, 8), teamMat);
      shield.rotation.x = Math.PI / 2;
      shield.position.set(0, 4.5, 4.6);
      group.add(shield);

      return group;
    }

    // 7. ARCHERY RANGE (Trains Archers & Crossbowmen)
    function createArcheryRangeMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Pavilion Shelter
      const shelterGeom = new THREE.BoxGeometry(10, 4.5, 6);
      const shelter = new THREE.Mesh(shelterGeom, plasterMat);
      shelter.position.y = 2.65;
      shelter.castShadow = true;
      group.add(shelter);

      const roofGeom = new THREE.ConeGeometry(7.5, 3.2, 4);
      const roof = new THREE.Mesh(roofGeom, tileMat);
      roof.position.y = 6.4;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // 3 Bullseye Targets
      for (let i = -1; i <= 1; i++) {
        const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 2, 6), timberMat);
        stand.position.set(i * 2.2, 1, 6);
        group.add(stand);

        const target = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.2, 12), thatchMat);
        target.rotation.x = Math.PI / 2;
        target.position.set(i * 2.2, 2.2, 6);
        group.add(target);

        // Bullseye Red Ring
        const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.22, 12), teamMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.set(i * 2.2, 2.2, 6.02);
        group.add(ring);
      }

      return group;
    }

    // 8. STABLE (Trains Scout Cavalry & Knights)
    function createStableMesh(isEnemy) {
      const group = new THREE.Group();
      const barnGeom = new THREE.BoxGeometry(12, 5.5, 8);
      const barn = new THREE.Mesh(barnGeom, timberMat);
      barn.position.y = 3.15;
      barn.castShadow = true;
      group.add(barn);

      const roofGeom = new THREE.ConeGeometry(9, 4, 4);
      const roof = new THREE.Mesh(roofGeom, thatchMat);
      roof.position.y = 7.9;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Horse Stalls Enclosure
      const fenceGeom = new THREE.BoxGeometry(11, 1.2, 4);
      const fence = new THREE.Mesh(fenceGeom, timberMat);
      fence.position.set(0, 0.6, 5.5);
      group.add(fence);

      return group;
    }

    // 9. BLACKSMITH (Researches Weapon & Armor Technologies)
    function createBlacksmithMesh() {
      const group = new THREE.Group();
      const forgeGeom = new THREE.BoxGeometry(7, 4.5, 6);
      const forge = new THREE.Mesh(forgeGeom, stoneMat);
      forge.position.y = 2.65;
      forge.castShadow = true;
      group.add(forge);

      // Chimney with Glowing Fire
      const chGeom = new THREE.BoxGeometry(1.4, 4, 1.4);
      const ch = new THREE.Mesh(chGeom, stoneMat);
      ch.position.set(2, 6, 1.5);
      group.add(ch);

      const fireGeom = new THREE.BoxGeometry(1, 0.8, 1);
      const fireMat = new THREE.MeshBasicMaterial({ color: 0xff4500 });
      const fire = new THREE.Mesh(fireGeom, fireMat);
      fire.position.set(2, 4.5, 1.5);
      group.add(fire);

      // Anvil Outside
      const anvilGeom = new THREE.BoxGeometry(1, 1.2, 0.6);
      const anvil = new THREE.Mesh(anvilGeom, ironMat);
      anvil.position.set(0, 0.6, 4);
      group.add(anvil);

      return group;
    }

    // 10. MONASTERY (Trains Monks, Stores Holy Relics)
    function createMonasteryMesh(isEnemy) {
      const group = new THREE.Group();
      const naveGeom = new THREE.BoxGeometry(12, 7, 8);
      const nave = new THREE.Mesh(naveGeom, stoneMat);
      nave.position.y = 3.9;
      nave.castShadow = true;
      group.add(nave);

      const roofGeom = new THREE.ConeGeometry(9, 4.5, 4);
      const roof = new THREE.Mesh(roofGeom, tileMat);
      roof.position.y = 9.5;
      roof.rotation.y = Math.PI / 4;
      roof.castShadow = true;
      group.add(roof);

      // Bell Tower Spire
      const towerGeom = new THREE.BoxGeometry(3, 13, 3);
      const tower = new THREE.Mesh(towerGeom, stoneMat);
      tower.position.set(4.5, 6.5, 0);
      tower.castShadow = true;
      group.add(tower);

      const spireGeom = new THREE.ConeGeometry(2.4, 6, 8);
      const spire = new THREE.Mesh(spireGeom, tileMat);
      spire.position.set(4.5, 16, 0);
      group.add(spire);

      // Holy Cross on Top
      const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.3, 2, 0.3), goldMat);
      crossV.position.set(4.5, 19.5, 0);
      group.add(crossV);
      const crossH = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.3, 0.3), goldMat);
      crossH.position.set(4.5, 19.8, 0);
      group.add(crossH);

      return group;
    }

    // 11. CASTLE (Colossal 4-Tower Stone Fortress)
    function createCastleMesh(isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      // Central Stone Keep
      const keepGeom = new THREE.BoxGeometry(22, 14, 18);
      const keep = new THREE.Mesh(keepGeom, stoneMat);
      keep.position.y = 7.4;
      keep.castShadow = true;
      group.add(keep);

      // 4 Massive Corner Bastions
      const bastGeom = new THREE.CylinderGeometry(3.5, 4.2, 20, 10);
      const bOffsets = [[-11, -9], [11, -9], [-11, 9], [11, 9]];
      bOffsets.forEach(pos => {
        const b = new THREE.Mesh(bastGeom, stoneMat);
        b.position.set(pos[0], 10, pos[1]);
        b.castShadow = true;
        group.add(b);

        // Crenellations / Battlements
        const crGeom = new THREE.CylinderGeometry(4.2, 3.8, 2, 10);
        const cr = new THREE.Mesh(crGeom, stoneMat);
        cr.position.set(pos[0], 21, pos[1]);
        group.add(cr);

        // Tower Royal Standard
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 4, 6), timberMat);
        pole.position.set(pos[0], 24, pos[1]);
        group.add(pole);

        const banner = new THREE.Mesh(new THREE.PlaneGeometry(2, 1.4), teamMat);
        banner.position.set(pos[0] + 1, 24.5, pos[1]);
        group.add(banner);
      });

      // Iron Portcullis & Drawbridge Gate
      const gateGeom = new THREE.BoxGeometry(6, 7, 1);
      const gate = new THREE.Mesh(gateGeom, ironMat);
      gate.position.set(0, 3.5, 9.2);
      group.add(gate);

      return group;
    }

    // 12. WONDER OF THE WORLD (Imperial Age Colossal Cathedral)
    function createWonderMesh() {
      const group = new THREE.Group();

      // Colossal Marble Basilica Base
      const baseGeom = new THREE.BoxGeometry(28, 12, 22);
      const base = new THREE.Mesh(baseGeom, whiteMarbleMat);
      base.position.y = 6.4;
      base.castShadow = true;
      group.add(base);

      // Soaring Central Dome
      const domeGeom = new THREE.SphereGeometry(7, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2);
      const dome = new THREE.Mesh(domeGeom, goldMat);
      dome.position.y = 12.4;
      dome.castShadow = true;
      group.add(dome);

      // Gilded Cupola & Cross
      const cupolaGeom = new THREE.CylinderGeometry(1.5, 1.5, 3, 8);
      const cupola = new THREE.Mesh(cupolaGeom, whiteMarbleMat);
      cupola.position.y = 20;
      group.add(cupola);

      const cross = new THREE.Mesh(new THREE.BoxGeometry(0.4, 2.5, 0.4), goldMat);
      cross.position.y = 22.5;
      group.add(cross);

      // Colonnade Pillars
      const pGeom = new THREE.CylinderGeometry(0.7, 0.8, 10, 8);
      for (let x = -11; x <= 11; x += 3.6) {
        const pFront = new THREE.Mesh(pGeom, whiteMarbleMat);
        pFront.position.set(x, 5.4, 11.8);
        pFront.castShadow = true;
        group.add(pFront);
      }

      return group;
    }

    // 13. WATCHTOWER
    function createWatchtowerMesh(age, isEnemy) {
      const group = new THREE.Group();
      const teamMat = new THREE.MeshLambertMaterial({ color: isEnemy ? COLOR_ENEMY_PRIMARY : COLOR_PLAYER_PRIMARY });

      const towerMat = age === 'Dark Age' ? timberMat : stoneMat;
      const shaftGeom = new THREE.CylinderGeometry(1.8, 2.4, 14, 8);
      const shaft = new THREE.Mesh(shaftGeom, towerMat);
      shaft.position.y = 7.4;
      shaft.castShadow = true;
      group.add(shaft);

      // Guard Balustrade
      const balGeom = new THREE.CylinderGeometry(2.8, 2.2, 2.5, 8);
      const bal = new THREE.Mesh(balGeom, towerMat);
      bal.position.y = 15;
      group.add(bal);

      // Team Pennant
      const flag = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1), teamMat);
      flag.position.set(0, 17.5, 0);
      group.add(flag);

      return group;
    }

    // 14. STONE WALL
    function createWallMesh() {
      const group = new THREE.Group();
      const wallGeom = new THREE.BoxGeometry(6, 4, 1.8);
      const wall = new THREE.Mesh(wallGeom, stoneMat);
      wall.position.y = 2.4;
      wall.castShadow = true;
      group.add(wall);
      return group;
    }
    """
