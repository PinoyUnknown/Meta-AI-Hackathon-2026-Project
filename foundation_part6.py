part6 = r"""
    // =========================================================================
    // 3D BUILDINGS & ORGANIC GRID-LESS PLACEMENT SYSTEM
    // =========================================================================
    const buildings = [];
    let activeBuildType = null;
    let ghostBuilding = null;
    let ghostRotation = 0;

    const buildingCosts = {
      center:   { gold: 0,   wood: 0,  stone: 0 },
      lumber:   { gold: 0,   wood: 15, stone: 0 },
      quarry:   { gold: 0,   wood: 20, stone: 0 },
      well:     { gold: 0,   wood: 0,  stone: 10 },
      cottage:  { gold: 0,   wood: 12, stone: 5 },
      market:   { gold: 5,   wood: 15, stone: 0 },
      windmill: { gold: 0,   wood: 25, stone: 10 },
      church:   { gold: 0,   wood: 20, stone: 40 },
      keep:     { gold: 20,  wood: 40, stone: 60 }
    };

    function selectBuildType(type) {
      initAudio();
      if (activeBuildType === type) {
        cancelBuildingPlacement();
        return;
      }
      activeBuildType = type;
      if (ghostBuilding) scene.remove(ghostBuilding);

      ghostBuilding = createBuildingMesh(type, true);
      scene.add(ghostBuilding);

      // Highlight dock button
      document.querySelectorAll('.b-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.b-btn')).find(b => b.onclick && b.onclick.toString().includes(`'${type}'`));
      if (activeBtn) activeBtn.classList.add('active');
    }

    function cancelBuildingPlacement() {
      activeBuildType = null;
      if (ghostBuilding) {
        scene.remove(ghostBuilding);
        ghostBuilding = null;
      }
      document.querySelectorAll('.b-btn').forEach(btn => btn.classList.remove('active'));
    }

    // Procedural 3D Modular Architecture Construction
    function createBuildingMesh(type, isGhost = false) {
      const group = new THREE.Group();

      const stoneMat = new THREE.MeshStandardMaterial({
        map: generateCobbleTexture(),
        roughness: 0.85,
        transparent: isGhost,
        opacity: isGhost ? 0.6 : 1.0
      });

      const woodMat = new THREE.MeshStandardMaterial({
        map: generateWoodTexture(),
        roughness: 0.75,
        transparent: isGhost,
        opacity: isGhost ? 0.6 : 1.0
      });

      const thatchMat = new THREE.MeshStandardMaterial({
        map: generateThatchTexture(),
        roughness: 0.9,
        transparent: isGhost,
        opacity: isGhost ? 0.6 : 1.0
      });

      const tileMat = new THREE.MeshStandardMaterial({
        map: generateClayTileTexture(),
        roughness: 0.7,
        transparent: isGhost,
        opacity: isGhost ? 0.6 : 1.0
      });

      const canopyMat = new THREE.MeshStandardMaterial({
        map: generateCanopyTexture(),
        roughness: 0.5,
        side: THREE.DoubleSide,
        transparent: isGhost,
        opacity: isGhost ? 0.6 : 1.0
      });

      if (type === 'center') {
        // Town Hall / Manor
        const base = new THREE.Mesh(new THREE.BoxGeometry(10, 4, 8), stoneMat);
        base.position.y = 2; base.castShadow = !isGhost; base.receiveShadow = !isGhost;
        group.add(base);

        const upper = new THREE.Mesh(new THREE.BoxGeometry(9.6, 3.5, 7.6), woodMat);
        upper.position.y = 5.75; upper.castShadow = !isGhost;
        group.add(upper);

        const roof = new THREE.Mesh(new THREE.ConeGeometry(7, 4, 4), tileMat);
        roof.position.y = 9.5; roof.rotation.y = Math.PI * 0.25; roof.castShadow = !isGhost;
        group.add(roof);

        // Banner Flagpole
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 6, 6), woodMat);
        pole.position.set(0, 12, 0); group.add(pole);
        const banner = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.2), canopyMat);
        banner.position.set(0.9, 13.5, 0); group.add(banner);

      } else if (type === 'lumber') {
        // Lumber Camp
        const cabin = new THREE.Mesh(new THREE.BoxGeometry(7, 3.2, 5), woodMat);
        cabin.position.y = 1.6; cabin.castShadow = !isGhost; group.add(cabin);

        const roof = new THREE.Mesh(new THREE.ConeGeometry(5, 2.5, 4), thatchMat);
        roof.position.y = 4.2; roof.rotation.y = Math.PI * 0.25; group.add(roof);

        // Stacked Logs
        for (let l = 0; l < 5; l++) {
          const log = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 4, 6), woodMat);
          log.rotation.z = Math.PI * 0.5;
          log.position.set(4.5, 0.3 + (l % 2) * 0.5, (l - 2) * 0.6);
          group.add(log);
        }

      } else if (type === 'quarry') {
        // Stonecutter Quarry
        const yard = new THREE.Mesh(new THREE.BoxGeometry(8, 0.6, 8), stoneMat);
        yard.position.y = 0.3; group.add(yard);

        // Wooden Hoist Crane
        const cranePost = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.25, 6, 6), woodMat);
        cranePost.position.set(-2.5, 3, -2.5); group.add(cranePost);
        const craneArm = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 5, 6), woodMat);
        craneArm.position.set(-1, 5.8, -1); craneArm.rotation.z = Math.PI * 0.35; group.add(craneArm);

        // Chiseled Blocks
        for (let b = 0; b < 4; b++) {
          const block = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.0, 1.2), stoneMat);
          block.position.set(1.5 + (b % 2) * 1.5, 0.6, -1 + Math.floor(b / 2) * 1.5);
          group.add(block);
        }

      } else if (type === 'well') {
        // Town Well
        const ring = new THREE.Mesh(new THREE.CylinderGeometry(1.8, 1.9, 1.5, 12, 1, true), stoneMat);
        ring.position.y = 0.75; group.add(ring);

        [-1.2, 1.2].forEach(x => {
          const post = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 3.2, 6), woodMat);
          post.position.set(x, 1.6, 0); group.add(post);
        });

        const canopy = new THREE.Mesh(new THREE.ConeGeometry(2.4, 1.6, 4), tileMat);
        canopy.position.y = 3.6; canopy.rotation.y = Math.PI * 0.25; group.add(canopy);

      } else if (type === 'cottage') {
        // Thatched Serf Cottage
        const walls = new THREE.Mesh(new THREE.BoxGeometry(5.5, 3.2, 4.5), stoneMat);
        walls.position.y = 1.6; walls.castShadow = !isGhost; group.add(walls);

        const thatch = new THREE.Mesh(new THREE.ConeGeometry(4.6, 3.2, 4), thatchMat);
        thatch.position.y = 4.4; thatch.rotation.y = Math.PI * 0.25; thatch.castShadow = !isGhost; group.add(thatch);

        // Chimney
        const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.9, 4.5, 0.9), stoneMat);
        chimney.position.set(1.8, 3.5, 1.2); group.add(chimney);

      } else if (type === 'market') {
        // Market Stall with Striped Canopy
        const table = new THREE.Mesh(new THREE.BoxGeometry(4.5, 1.2, 2.5), woodMat);
        table.position.y = 0.6; group.add(table);

        const awning = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 3.5), canopyMat);
        awning.position.y = 3.2; awning.rotation.x = Math.PI * 0.35; group.add(awning);

        // Crates of Food
        const crateMat = new THREE.MeshStandardMaterial({ color: 0xb45309 });
        const crate1 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.0), crateMat);
        crate1.position.set(-1.2, 1.4, 0); group.add(crate1);
        const crate2 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.0), crateMat);
        crate2.position.set(1.2, 1.4, 0); group.add(crate2);

      } else if (type === 'windmill') {
        // Windmill
        const tower = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 3.5, 9, 8), stoneMat);
        tower.position.y = 4.5; tower.castShadow = !isGhost; group.add(tower);

        const cap = new THREE.Mesh(new THREE.ConeGeometry(2.8, 2.2, 8), thatchMat);
        cap.position.y = 9.8; group.add(cap);

        // 4 Rotating Canvas Sails
        const sailsGroup = new THREE.Group();
        sailsGroup.position.set(0, 8.5, 2.4);
        for (let s = 0; s < 4; s++) {
          const sail = new THREE.Mesh(new THREE.BoxGeometry(0.3, 7.5, 0.8), woodMat);
          sail.rotation.z = (s * Math.PI) / 2;
          sailsGroup.add(sail);
        }
        group.add(sailsGroup);
        group.sails = sailsGroup;

      } else if (type === 'church') {
        // Rustic Church
        const nave = new THREE.Mesh(new THREE.BoxGeometry(14, 6.5, 8), stoneMat);
        nave.position.y = 3.25; nave.castShadow = !isGhost; group.add(nave);

        const roof = new THREE.Mesh(new THREE.ConeGeometry(8.5, 4.5, 4), tileMat);
        roof.position.y = 8.2; roof.rotation.y = Math.PI * 0.25; group.add(roof);

        // Belfry Spire Tower
        const belfry = new THREE.Mesh(new THREE.BoxGeometry(5, 14, 5), stoneMat);
        belfry.position.set(-8, 7, 0); belfry.castShadow = !isGhost; group.add(belfry);

        const spire = new THREE.Mesh(new THREE.ConeGeometry(3.6, 7, 8), tileMat);
        spire.position.set(-8, 17.5, 0); spire.castShadow = !isGhost; group.add(spire);

      } else if (type === 'keep') {
        // Lord's Keep Citadel
        const citadel = new THREE.Mesh(new THREE.BoxGeometry(16, 10, 14), stoneMat);
        citadel.position.y = 5; citadel.castShadow = !isGhost; group.add(citadel);

        // 4 Corner Towers with Crenellations
        [[-8, -7], [8, -7], [-8, 7], [8, 7]].forEach(([tx, tz]) => {
          const tower = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.8, 14, 8), stoneMat);
          tower.position.set(tx, 7, tz); tower.castShadow = !isGhost; group.add(tower);
          const roof = new THREE.Mesh(new THREE.ConeGeometry(3.2, 3.5, 8), tileMat);
          roof.position.set(tx, 15.5, tz); group.add(roof);
        });
      }

      return group;
    }

    // Place building on terrain
    function tryPlaceBuilding(worldX, worldZ) {
      if (!activeBuildType) return;
      const cost = buildingCosts[activeBuildType];

      // Check costs
      if (gameState.gold < cost.gold || gameState.wood < cost.wood || gameState.stone < cost.stone) {
        alert(`[INSUFFICIENT RESOURCES] Requires ${cost.gold} Gold, ${cost.wood} Wood, ${cost.stone} Stone.`);
        return;
      }

      // Deduct resources
      gameState.gold -= cost.gold;
      gameState.wood -= cost.wood;
      gameState.stone -= cost.stone;
      updateResourceLedger();

      const building = createBuildingMesh(activeBuildType, false);
      const groundY = getTerrainHeight(worldX, worldZ);
      building.position.set(worldX, groundY, worldZ);
      building.rotation.y = ghostRotation;
      scene.add(building);

      playBuildHammerSound();

      buildings.push({
        type: activeBuildType,
        mesh: building,
        x: worldX,
        z: worldZ,
        workers: []
      });

      checkQuestMilestone(activeBuildType);
      cancelBuildingPlacement();
    }
"""
