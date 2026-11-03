def get_aoe_pathfinding_fsm_js():
    return """
    // =========================================================================
    // PHASE 1: MATHEMATICAL GRID, ELEVATION, A* PATHFINDING & FSM
    // =========================================================================

    const GRID_SIZE = 100;
    const TILE_SIZE = 2;
    const GRID_OFFSET = 100;

    const TILE_WALKABLE = 0;
    const TILE_WATER = 1;
    const TILE_CLIFF = 2;
    const TILE_OCCUPIED = 3;

    const tilemapGrid = new Uint8Array(GRID_SIZE * GRID_SIZE);

    // Exact Mathematical Terrain Elevation Function (Mountains, Rivers, Valleys)
    function getTerrainHeight(x, z) {
      // 1. Eastern Rocky Mountains (x > 52)
      if (x > 52) {
        const mDist = (x - 52) / 48; // 0 to 1
        let mh = Math.pow(mDist, 1.3) * 12.0;
        mh += Math.sin(x * 0.15) * Math.cos(z * 0.15) * 2.5;
        // Mountain Spring / Waterfall notch at (x: 58 to 68, z: -38 to -28)
        if (x >= 58 && x <= 68 && Math.abs(z + 33) < 5) {
          mh = Math.min(mh, 5.0);
        }
        return mh;
      }

      // 2. Mountain Creek Bed flowing from waterfall (x: -16 to 55, z around -33)
      if (x >= -16 && x <= 55 && Math.abs(z + 33 + (x - 20) * 0.05) < 3.2) {
        return -1.5;
      }

      // 3. Central River (x: -34 to -16)
      if (x > -34 && x < -16) {
        if (Math.abs(z) <= 4.0) {
          return 0.2; // Bridge roadway elevation
        }
        return -2.0; // River water surface
      }

      // 4. Woodland Lake at (x: -20, z: 60)
      const lakeDist = Math.hypot(x + 20, z - 60);
      if (lakeDist < 14) {
        return -2.0; // Lake bed
      }

      // 5. Rolling Hills across meadows & open terrain
      return Math.sin(x * 0.04) * Math.cos(z * 0.04) * 1.5 + Math.sin(z * 0.08) * 0.6;
    }

    function worldToGrid(x, z) {
      const gx = Math.floor((x + GRID_OFFSET) / TILE_SIZE);
      const gz = Math.floor((z + GRID_OFFSET) / TILE_SIZE);
      return {
        x: Math.max(0, Math.min(GRID_SIZE - 1, gx)),
        z: Math.max(0, Math.min(GRID_SIZE - 1, gz))
      };
    }

    function gridToWorld(gx, gz) {
      return {
        x: gx * TILE_SIZE - GRID_OFFSET + TILE_SIZE * 0.5,
        z: gz * TILE_SIZE - GRID_OFFSET + TILE_SIZE * 0.5
      };
    }

    function getTileType(gx, gz) {
      if (gx < 0 || gx >= GRID_SIZE || gz < 0 || gz >= GRID_SIZE) return TILE_CLIFF;
      return tilemapGrid[gz * GRID_SIZE + gx];
    }

    function isTileWalkable(gx, gz) {
      return getTileType(gx, gz) === TILE_WALKABLE;
    }

    function isTileBuildable(gx, gz, sizeX = 1, sizeZ = 1) {
      const hx = Math.floor(sizeX / 2);
      const hz = Math.floor(sizeZ / 2);
      for (let dx = -hx; dx <= hx; dx++) {
        for (let dz = -hz; dz <= hz; dz++) {
          const nx = gx + dx;
          const nz = gz + dz;
          if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) return false;
          if (tilemapGrid[nz * GRID_SIZE + nx] !== TILE_WALKABLE) return false;
        }
      }
      return true;
    }

    function occupyGridArea(worldX, worldZ, sizeTilesX = 1, sizeTilesZ = 1) {
      const g = worldToGrid(worldX, worldZ);
      const hx = Math.floor(sizeTilesX / 2);
      const hz = Math.floor(sizeTilesZ / 2);
      for (let dx = -hx; dx <= hx; dx++) {
        for (let dz = -hz; dz <= hz; dz++) {
          const nx = g.x + dx;
          const nz = g.z + dz;
          if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
            tilemapGrid[nz * GRID_SIZE + nx] = TILE_OCCUPIED;
          }
        }
      }
      onNavMeshUpdated();
    }

    function freeGridArea(worldX, worldZ, sizeTilesX = 1, sizeTilesZ = 1) {
      const g = worldToGrid(worldX, worldZ);
      const hx = Math.floor(sizeTilesX / 2);
      const hz = Math.floor(sizeTilesZ / 2);
      for (let dx = -hx; dx <= hx; dx++) {
        for (let dz = -hz; dz <= hz; dz++) {
          const nx = g.x + dx;
          const nz = g.z + dz;
          if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
            tilemapGrid[nz * GRID_SIZE + nx] = TILE_WALKABLE;
          }
        }
      }
      onNavMeshUpdated();
    }

    // Dynamic A* Pathfinding with 8-directional search
    function findAStarPath(startX, startZ, endX, endZ) {
      const start = worldToGrid(startX, startZ);
      const goal = worldToGrid(endX, endZ);

      if (start.x === goal.x && start.z === goal.z) {
        return [new THREE.Vector3(endX, getTerrainHeight(endX, endZ), endZ)];
      }

      const openSet = [];
      const cameFrom = new Int32Array(GRID_SIZE * GRID_SIZE).fill(-1);
      const gScore = new Float32Array(GRID_SIZE * GRID_SIZE).fill(Infinity);
      const fScore = new Float32Array(GRID_SIZE * GRID_SIZE).fill(Infinity);

      const startIndex = start.z * GRID_SIZE + start.x;
      const goalIndex = goal.z * GRID_SIZE + goal.x;

      gScore[startIndex] = 0;
      fScore[startIndex] = Math.hypot(goal.x - start.x, goal.z - start.z);
      openSet.push({ index: startIndex, f: fScore[startIndex] });

      const neighbors = [
        { dx: 1, dz: 0, cost: 1.0 },
        { dx: -1, dz: 0, cost: 1.0 },
        { dx: 0, dz: 1, cost: 1.0 },
        { dx: 0, dz: -1, cost: 1.0 },
        { dx: 1, dz: 1, cost: 1.414 },
        { dx: -1, dz: 1, cost: 1.414 },
        { dx: 1, dz: -1, cost: 1.414 },
        { dx: -1, dz: -1, cost: 1.414 }
      ];

      let iterations = 0;
      const maxIterations = 500;

      while (openSet.length > 0 && iterations++ < maxIterations) {
        let bestIdx = 0;
        for (let i = 1; i < openSet.length; i++) {
          if (openSet[i].f < openSet[bestIdx].f) bestIdx = i;
        }
        const current = openSet.splice(bestIdx, 1)[0].index;

        if (current === goalIndex) {
          const path = [];
          let curr = current;
          while (curr !== -1) {
            const cz = Math.floor(curr / GRID_SIZE);
            const cx = curr % GRID_SIZE;
            const w = gridToWorld(cx, cz);
            path.unshift(new THREE.Vector3(w.x, getTerrainHeight(w.x, w.z), w.z));
            curr = cameFrom[curr];
          }
          path[path.length - 1].set(endX, getTerrainHeight(endX, endZ), endZ);
          return path;
        }

        const cz = Math.floor(current / GRID_SIZE);
        const cx = current % GRID_SIZE;

        for (const n of neighbors) {
          const nx = cx + n.dx;
          const nz = cz + n.dz;
          if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
            if (tilemapGrid[nz * GRID_SIZE + nx] !== TILE_WALKABLE && (nx !== goal.x || nz !== goal.z)) {
              continue;
            }
            const neighborIdx = nz * GRID_SIZE + nx;
            const tentativeG = gScore[current] + n.cost;

            if (tentativeG < gScore[neighborIdx]) {
              cameFrom[neighborIdx] = current;
              gScore[neighborIdx] = tentativeG;
              const h = Math.hypot(goal.x - nx, goal.z - nz);
              fScore[neighborIdx] = tentativeG + h;
              if (!openSet.some(o => o.index === neighborIdx)) {
                openSet.push({ index: neighborIdx, f: fScore[neighborIdx] });
              }
            }
          }
        }
      }

      // Straight-line fallback if target within range
      return [new THREE.Vector3(endX, getTerrainHeight(endX, endZ), endZ)];
    }

    function onNavMeshUpdated() {
      friendlyUnits.concat(enemyUnits).forEach(u => {
        if (u.state === 'moving' && u.path && u.path.length > 0) {
          const dest = u.path[u.path.length - 1];
          const newPath = findAStarPath(u.mesh.position.x, u.mesh.position.z, dest.x, dest.z);
          u.path = newPath;
          u.dest = newPath.length > 1 ? newPath[1] : (newPath[0] || dest);
        }
      });
    }

    function calculateFormationPositions(targetPos, count, spacing = 2.4) {
      const positions = [];
      const cols = Math.ceil(Math.sqrt(count));
      for (let i = 0; i < count; i++) {
        const row = Math.floor(i / cols);
        const col = i % cols;
        const offsetX = (col - (cols - 1) / 2) * spacing;
        const offsetZ = (row - (Math.ceil(count / cols) - 1) / 2) * spacing;
        const posX = targetPos.x + offsetX;
        const posZ = targetPos.z + offsetZ;
        positions.push(new THREE.Vector3(posX, getTerrainHeight(posX, posZ), posZ));
      }
      return positions;
    }

    // Fog of War Visibility Tracking (0: Hidden, 1: Explored, 2: Active Visible)
    const fogOfWarGrid = new Uint8Array(GRID_SIZE * GRID_SIZE);

    function updateFogOfWar() {
      // Degrade active visible to explored
      for (let i = 0; i < fogOfWarGrid.length; i++) {
        if (fogOfWarGrid[i] === 2) fogOfWarGrid[i] = 1;
      }

      // Friendly units & buildings cast line-of-sight
      const visionEntities = friendlyUnits.concat(friendlyBuildings);
      visionEntities.forEach(ent => {
        if (ent.hp <= 0 || ent.state === 'garrisoned') return;
        const g = worldToGrid(ent.mesh.position.x, ent.mesh.position.z);
        const sightRadius = Math.ceil((ent.range || 8) / TILE_SIZE) + 2;

        for (let dx = -sightRadius; dx <= sightRadius; dx++) {
          for (let dz = -sightRadius; dz <= sightRadius; dz++) {
            if (dx * dx + dz * dz <= sightRadius * sightRadius) {
              const nx = g.x + dx;
              const nz = g.z + dz;
              if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
                fogOfWarGrid[nz * GRID_SIZE + nx] = 2; // Active Sight
              }
            }
          }
        }
      });

      // Update visibility of enemy units based on FoW
      enemyUnits.forEach(u => {
        if (u.hp <= 0) return;
        const g = worldToGrid(u.mesh.position.x, u.mesh.position.z);
        const isVisible = fogOfWarGrid[g.z * GRID_SIZE + g.x] === 2;
        u.mesh.visible = isVisible;
      });
    }
    """
