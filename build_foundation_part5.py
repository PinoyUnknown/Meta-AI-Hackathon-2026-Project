# build_foundation_part5.py - 3D Landscape, Rolling Hills, River, Foliage & Desire Path System
part5 = r'''
    // =========================================================================
    // 3D LANDSCAPE, ROLLING HILLS, RIVER, FOLIAGE & DESIRE PATH SYSTEM
    // =========================================================================
    let scene, camera, renderer;
    let ambientLight, sunLight;
    let terrainMesh, riverMesh;
    let pathCanvas, pathCtx, pathTexture;

    const trees = [];
    const stoneRocks = [];
    const clouds = [];

    // Camera Orbit & Pan State
    let camTarget = new THREE.Vector3(0, 0, 0);
    let camDistance = 75; // Mouse scroll wheel scales 8m to 260m
    let camPitch = 0.75;
    let camYaw = 0.5;
    let isRightDragging = false;
    let prevMouseX = 0, prevMouseY = 0;

    function init3DEnvironment() {
      const container = document.getElementById('canvas-container');
      scene = new THREE.Scene();

      // BRIGHT DAYLIGHT SKY (Lush pastoral summer afternoon)
      scene.background = new THREE.Color(0x93c5fd);
      scene.fog = new THREE.FogExp2(0xbae6fd, 0.0022);

      camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
      updateCameraPosition();

      renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.35;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      container.appendChild(renderer.domElement);

      // SUNLIGHT & SKY LIGHTING (Vibrant & Warm)
      ambientLight = new THREE.AmbientLight(0xfffbeb, 1.4);
      scene.add(ambientLight);

      const hemi = new THREE.HemisphereLight(0xbae6fd, 0x4d7c0f, 1.25);
      scene.add(hemi);

      sunLight = new THREE.DirectionalLight(0xfff6db, 2.8);
      sunLight.position.set(120, 180, 80);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 2048;
      sunLight.shadow.mapSize.height = 2048;
      sunLight.shadow.camera.near = 10;
      sunLight.shadow.camera.far = 450;
      sunLight.shadow.camera.left = -160;
      sunLight.shadow.camera.right = 160;
      sunLight.shadow.camera.top = 160;
      sunLight.shadow.camera.bottom = -160;
      scene.add(sunLight);

      setupDesirePathCanvas();
      setupRollingTerrain();
      setupWindingRiver();
      setupFoliageAndRocks();
      setupSkyClouds();

      window.addEventListener('resize', onWindowResize);
    }

    function onWindowResize() {
      if (!camera || !renderer) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // Emergent Footpath Texture System (Villagers footsteps carve dynamic dirt paths)
    function setupDesirePathCanvas() {
      pathCanvas = createProceduralCanvas(512, 512);
      pathCtx = pathCanvas.getContext('2d');
      // Transparent base
      pathCtx.clearRect(0, 0, 512, 512);

      pathTexture = new THREE.CanvasTexture(pathCanvas);
    }

    function stampVillagerFootstep(worldX, worldZ) {
      // Map world coords (-200 to +200) into canvas pixels (0 to 512)
      const u = ((worldX + 200) / 400) * 512;
      const v = ((worldZ + 200) / 400) * 512;

      pathCtx.fillStyle = 'rgba(107, 71, 34, 0.06)';
      pathCtx.beginPath();
      pathCtx.arc(u, v, 4.5, 0, Math.PI * 2);
      pathCtx.fill();

      pathTexture.needsUpdate = true;
    }

    // Procedural Elevation for Rolling Hills
    function getTerrainHeight(x, z) {
      // Flatter village center, gentle hills outward
      const distFromCenter = Math.hypot(x, z);
      const centerDamp = Math.min(1.0, distFromCenter / 50);

      const h1 = Math.sin(x * 0.02) * Math.cos(z * 0.02) * 8;
      const h2 = Math.sin(x * 0.045 + 1.2) * Math.sin(z * 0.035) * 4;
      const h3 = Math.cos(x * 0.01 - z * 0.015) * 6;

      // River valley cut (-35 < x < -10)
      let riverDepth = 0;
      const riverCenter = -22 + Math.sin(z * 0.03) * 14;
      const distToRiver = Math.abs(x - riverCenter);
      if (distToRiver < 16) {
        riverDepth = (1 - distToRiver / 16) * 5.5;
      }

      return (h1 + h2 + h3) * centerDamp - riverDepth;
    }

    // 400x400 Organic Meadow Terrain Mesh
    function setupRollingTerrain() {
      const geo = new THREE.PlaneGeometry(400, 400, 96, 96);
      geo.rotateX(-Math.PI * 0.5);

      const pos = geo.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const z = pos.getZ(i);
        pos.setY(i, getTerrainHeight(x, z));
      }
      geo.computeVertexNormals();

      const grassTex = generateGrassTexture();
      const mat = new THREE.MeshStandardMaterial({
        map: grassTex,
        roughness: 0.85,
        metalness: 0.05
      });

      terrainMesh = new THREE.Mesh(geo, mat);
      terrainMesh.receiveShadow = true;
      scene.add(terrainMesh);

      // Overlay Desire Path Mesh
      const pathMat = new THREE.MeshStandardMaterial({
        map: pathTexture,
        transparent: true,
        opacity: 0.9,
        roughness: 0.95,
        polygonOffset: true,
        polygonOffsetFactor: -1
      });
      const pathMesh = new THREE.Mesh(geo.clone(), pathMat);
      scene.add(pathMesh);
    }

    // Winding Sparkling Blue River
    function setupWindingRiver() {
      const riverGeo = new THREE.PlaneGeometry(28, 400, 16, 64);
      riverGeo.rotateX(-Math.PI * 0.5);

      const pos = riverGeo.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        const z = pos.getZ(i);
        const riverCenter = -22 + Math.sin(z * 0.03) * 14;
        const x = pos.getX(i);
        pos.setX(i, x + riverCenter);
        pos.setY(i, -2.4);
      }
      riverGeo.computeVertexNormals();

      const waterTex = generateWaterTexture();
      const riverMat = new THREE.MeshStandardMaterial({
        map: waterTex,
        roughness: 0.15,
        metalness: 0.2,
        transparent: true,
        opacity: 0.88
      });
      riverMesh = new THREE.Mesh(riverGeo, riverMat);
      scene.add(riverMesh);
    }

    // Harvestable Oak Trees, Pines & Granite Boulders
    function setupFoliageAndRocks() {
      const trunkMat = new THREE.MeshStandardMaterial({ color: 0x5c3818, roughness: 0.9 });
      const pineLeavesMat = new THREE.MeshStandardMaterial({ color: 0x22542a, roughness: 0.8 });
      const oakLeavesMat = new THREE.MeshStandardMaterial({ color: 0x4d7c0f, roughness: 0.8 });
      const stoneMat = new THREE.MeshStandardMaterial({ map: generateCobbleTexture(), roughness: 0.85 });

      // Spawn 140 Trees across the countryside
      for (let i = 0; i < 140; i++) {
        const x = (Math.random() - 0.5) * 340;
        const z = (Math.random() - 0.5) * 340;
        if (Math.hypot(x, z) < 30 || Math.abs(x - (-22)) < 24) continue; // Keep village center & river clear

        const y = getTerrainHeight(x, z);
        const treeGroup = new THREE.Group();

        // Trunk
        const trunkGeo = new THREE.CylinderGeometry(0.35, 0.5, 3.5, 6);
        const trunk = new THREE.Mesh(trunkGeo, trunkMat);
        trunk.position.y = 1.75;
        trunk.castShadow = true;
        treeGroup.add(trunk);

        // Canopy (Oak or Pine)
        const isPine = Math.random() > 0.4;
        if (isPine) {
          for (let l = 0; l < 3; l++) {
            const coneGeo = new THREE.ConeGeometry(2.4 - l * 0.5, 2.5, 7);
            const cone = new THREE.Mesh(coneGeo, pineLeavesMat);
            cone.position.y = 3.2 + l * 1.5;
            cone.castShadow = true;
            treeGroup.add(cone);
          }
        } else {
          const sphereGeo = new THREE.SphereGeometry(2.2, 8, 8);
          const sphere = new THREE.Mesh(sphereGeo, oakLeavesMat);
          sphere.position.y = 4.2;
          sphere.scale.set(1.1, 1.3, 1.1);
          sphere.castShadow = true;
          treeGroup.add(sphere);
        }

        treeGroup.position.set(x, y, z);
        scene.add(treeGroup);
        trees.push({ mesh: treeGroup, x: x, z: z, hp: 4 });
      }

      // Spawn 35 Granite Boulders
      for (let i = 0; i < 35; i++) {
        const x = (Math.random() - 0.5) * 320;
        const z = (Math.random() - 0.5) * 320;
        if (Math.hypot(x, z) < 25) continue;
        const y = getTerrainHeight(x, z);

        const rockRad = 1.8 + Math.random() * 2.2;
        const rockGeo = new THREE.DodecahedronGeometry(rockRad, 1);
        const rock = new THREE.Mesh(rockGeo, stoneMat);
        rock.position.set(x, y + rockRad * 0.6, z);
        rock.rotation.set(Math.random(), Math.random(), Math.random());
        rock.castShadow = true;
        scene.add(rock);
        stoneRocks.push({ mesh: rock, x: x, z: z, hp: 6 });
      }
    }

    // Fluffy Drifting Cumulus Clouds
    function setupSkyClouds() {
      const cloudMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        roughness: 0.95,
        transparent: true,
        opacity: 0.85
      });

      for (let i = 0; i < 18; i++) {
        const cloudGroup = new THREE.Group();
        const pCount = 5 + Math.floor(Math.random() * 5);
        for (let p = 0; p < pCount; p++) {
          const rad = 12 + Math.random() * 15;
          const puff = new THREE.Mesh(new THREE.SphereGeometry(rad, 7, 7), cloudMat);
          puff.position.set((Math.random() - 0.5) * 35, (Math.random() - 0.5) * 10, (Math.random() - 0.5) * 25);
          cloudGroup.add(puff);
        }
        cloudGroup.position.set(
          (Math.random() - 0.5) * 600,
          90 + Math.random() * 40,
          (Math.random() - 0.5) * 600
        );
        scene.add(cloudGroup);
        clouds.push({ mesh: cloudGroup, speed: 1.5 + Math.random() * 2.5 });
      }
    }

    function updateCameraPosition() {
      const x = camTarget.x + camDistance * Math.sin(camYaw) * Math.cos(camPitch);
      const y = camTarget.y + camDistance * Math.sin(camPitch);
      const z = camTarget.z + camDistance * Math.cos(camYaw) * Math.cos(camPitch);
      camera.position.set(x, Math.max(4, y), z);
      camera.lookAt(camTarget);
    }
'''

with open("foundation_part5.py", "w", encoding="utf-8") as f:
    f.write('part5 = r"""' + part5 + '"""\n')
print("Wrote foundation_part5.py")
