def get_aoe_pathfinding_fsm_js():
    return """
    // =========================================================================
    // PHASE 1: ENGINE INITIALIZATION, CAMERA & WORLD GRID SYSTEM
    // =========================================================================

    // Grid: 100x100 tiles, each 2x2m (Exact 200x200m World Grid: -100m to +100m)
    const GRID_SIZE = 100;
    const TILE_SIZE = 2;
    const GRID_OFFSET = 100; // grid(0,0) is world(-100, -100)

    // Tile Classifications
    const TILE_WALKABLE = 0;       // Open grass/meadow: Walkable & Buildable
    const TILE_WATER = 1;          // River/Lake: Unwalkable, Non-buildable
    const TILE_CLIFF = 2;          // Steep rocks/Cliffs: Unwalkable, Non-buildable
    const TILE_OCCUPIED = 3;       // Building, wall, or tree: Unwalkable, Non-buildable

    // 100x100 Tilemap Classification Array
    const tilemapGrid = new Uint8Array(GRID_SIZE * GRID_SIZE);

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
      for (let dx = -Math.floor(sizeX / 2); dx <= Math.floor(sizeX / 2); dx++) {
        for (let dz = -Math.floor(sizeZ / 2); dz <= Math.floor(sizeZ / 2); dz++) {
          const nx = gx + dx;
          const nz = gz + dz;
          if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) return false;
          if (tilemapGrid[nz * GRID_SIZE + nx] !== TILE_WALKABLE) return false;
        }
      }
      return true;
    }

    // Dynamic Grid Obstacle Occupy & Free Methods
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

    // Dynamic A* Pathfinding with 8-directional navigation & diagonal smoothing
    function findAStarPath(startX, startZ, endX, endZ) {
      const start = worldToGrid(startX, startZ);
      const goal = worldToGrid(endX, endZ);

      if (start.x === goal.x && start.z === goal.z) {
        return [new THREE.Vector3(endX, 0, endZ)];
      }

      // Priority queue simulation
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
      const maxIterations = 400; // High speed safeguard

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
            path.unshift(new THREE.Vector3(w.x, 0, w.z));
            curr = cameFrom[curr];
          }
          path[path.length - 1].set(endX, 0, endZ);
          return path;
        }

        const cz = Math.floor(current / GRID_SIZE);
        const cx = current % GRID_SIZE;

        for (const n of neighbors) {
          const nx = cx + n.dx;
          const nz = cz + n.dz;
          if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
            // Check walkable
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

      // Direct fallback if path obstructed or timeout
      return [new THREE.Vector3(endX, 0, endZ)];
    }

    // Instantly reroute moving units when NavMesh changes
    function onNavMeshUpdated() {
      friendlyUnits.concat(enemyUnits).forEach(u => {
        if (u.state === 'moving' && u.path && u.path.length > 0) {
          const dest = u.path[u.path.length - 1];
          const newPath = findAStarPath(u.mesh.position.x, u.mesh.position.z, dest.x, dest.z);
          u.path = newPath;
          u.dest = newPath.length > 0 ? newPath[0] : dest;
        }
      });
    }

    // Formation Flocking Calculator
    function calculateFormationPositions(targetPos, count, spacing = 2.4) {
      const positions = [];
      const cols = Math.ceil(Math.sqrt(count));
      for (let i = 0; i < count; i++) {
        const row = Math.floor(i / cols);
        const col = i % cols;
        const offsetX = (col - (cols - 1) * 0.5) * spacing;
        const offsetZ = row * spacing;
        positions.push(new THREE.Vector3(targetPos.x + offsetX, targetPos.y, targetPos.z + offsetZ));
      }
      return positions;
    }

    // =========================================================================
    // FOG OF WAR & LINE OF SIGHT (EXPLORATION VISIBILITY SYSTEM)
    // =========================================================================
    // 0 = Unexplored (Black), 1 = Explored (Dim/Grey), 2 = Visible (Full Sight)
    const fogOfWarGrid = new Uint8Array(GRID_SIZE * GRID_SIZE);

    function updateFogOfWar() {
      for (let i = 0; i < fogOfWarGrid.length; i++) {
        if (fogOfWarGrid[i] === 2) fogOfWarGrid[i] = 1;
      }

      const visionEntities = friendlyUnits.concat(friendlyBuildings);
      visionEntities.forEach(ent => {
        if (ent.hp <= 0 || ent.state === 'garrisoned') return;
        const g = worldToGrid(ent.mesh.position.x, ent.mesh.position.z);
        const radius = ent.type === 'scout' ? 8 : (ent.type === 'town_center' || ent.type === 'castle' ? 10 : 5);

        for (let dx = -radius; dx <= radius; dx++) {
          for (let dz = -radius; dz <= radius; dz++) {
            if (dx * dx + dz * dz <= radius * radius) {
              const nx = g.x + dx;
              const nz = g.z + dz;
              if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
                fogOfWarGrid[nz * GRID_SIZE + nx] = 2;
              }
            }
          }
        }
      });

      enemyUnits.forEach(u => {
        if (!u.mesh) return;
        const g = worldToGrid(u.mesh.position.x, u.mesh.position.z);
        const isVisible = fogOfWarGrid[g.z * GRID_SIZE + g.x] === 2;
        u.mesh.visible = isVisible;
      });
    }

    // Damage & Rock-Paper-Scissors Multiplier
    function calculateDamage(attacker, defender) {
      let baseDmg = Math.max(1, attacker.attack - (defender.armor || 0));

      // Rock-Paper-Scissors:
      // Spearman / Pikeman deals +15 bonus damage vs Cavalry (Scout, Knight)
      if (attacker.type === 'spearman' && (defender.type === 'scout' || defender.type === 'knight')) {
        baseDmg += 15;
      }
      // Skirmisher deals bonus vs Archers
      if (attacker.type === 'skirmisher' && defender.type === 'archer') {
        baseDmg += 5;
      }
      // Trebuchet deals massive x3 bonus vs Buildings
      if (attacker.type === 'trebuchet' && defender.isBuilding) {
        baseDmg *= 3;
      }

      return Math.round(baseDmg);
    }
    """
