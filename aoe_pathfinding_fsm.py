def get_aoe_pathfinding_fsm_js():
    return """
    // =========================================================================
    // PHASE 1, 2, 3 & 5: MAP GRID, A* PATHFINDING, FSM & FOG OF WAR
    // =========================================================================

    // Grid Dimensions: 100x100 tiles, each 4x4m (World: -200 to +200)
    const GRID_SIZE = 100;
    const TILE_SIZE = 4;
    const GRID_OFFSET = 200; // grid(0,0) is world(-200, -200)

    // Pathfinding Grid: 0 = Walkable, 1 = Blocked
    const pathGrid = new Uint8Array(GRID_SIZE * GRID_SIZE);

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

    function setGridBlocked(worldX, worldZ, radiusTiles = 1, blocked = true) {
      const g = worldToGrid(worldX, worldZ);
      for (let dx = -radiusTiles; dx <= radiusTiles; dx++) {
        for (let dz = -radiusTiles; dz <= radiusTiles; dz++) {
          const nx = g.x + dx;
          const nz = g.z + dz;
          if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
            pathGrid[nz * GRID_SIZE + nx] = blocked ? 1 : 0;
          }
        }
      }
    }

    function isGridWalkable(gx, gz) {
      if (gx < 0 || gx >= GRID_SIZE || gz < 0 || gz >= GRID_SIZE) return false;
      return pathGrid[gz * GRID_SIZE + gx] === 0;
    }

    // A* Pathfinding Algorithm (Fast 4-directional / 8-directional search)
    function findAStarPath(startX, startZ, endX, endZ) {
      const start = worldToGrid(startX, startZ);
      const goal = worldToGrid(endX, endZ);

      if (start.x === goal.x && start.z === goal.z) {
        return [new THREE.Vector3(endX, 0, endZ)];
      }

      // Priority Queue simulation
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
        { dx: 1, dz: 0, cost: 1 },
        { dx: -1, dz: 0, cost: 1 },
        { dx: 0, dz: 1, cost: 1 },
        { dx: 0, dz: -1, cost: 1 },
        { dx: 1, dz: 1, cost: 1.414 },
        { dx: -1, dz: 1, cost: 1.414 },
        { dx: 1, dz: -1, cost: 1.414 },
        { dx: -1, dz: -1, cost: 1.414 }
      ];

      let iterations = 0;
      const maxIterations = 350; // Performance safeguard

      while (openSet.length > 0 && iterations++ < maxIterations) {
        // Find lowest f
        let bestIdx = 0;
        for (let i = 1; i < openSet.length; i++) {
          if (openSet[i].f < openSet[bestIdx].f) bestIdx = i;
        }
        const current = openSet.splice(bestIdx, 1)[0].index;

        if (current === goalIndex) {
          // Reconstruct path
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
            if (pathGrid[nz * GRID_SIZE + nx] === 1 && (nx !== goal.x || nz !== goal.z)) {
              continue; // Blocked obstacle
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

      // Direct fallback if path is clear or timeout
      return [new THREE.Vector3(endX, 0, endZ)];
    }

    // Formation Calculator (Flocking grid offset so units fan out)
    function calculateFormationPositions(targetPos, count, spacing = 2.2) {
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
      // Degrade visible (2) to explored (1)
      for (let i = 0; i < fogOfWarGrid.length; i++) {
        if (fogOfWarGrid[i] === 2) fogOfWarGrid[i] = 1;
      }

      // Units and buildings emit vision radius (2)
      const visionEntities = friendlyUnits.concat(friendlyBuildings);
      visionEntities.forEach(ent => {
        if (ent.hp <= 0 || ent.state === 'garrisoned') return;
        const g = worldToGrid(ent.mesh.position.x, ent.mesh.position.z);
        const radius = ent.type === 'scout' ? 6 : (ent.type === 'town_center' || ent.type === 'castle' ? 8 : 4);

        for (let dx = -radius; dx <= radius; dx++) {
          for (let dz = -radius; dz <= radius; dz++) {
            if (dx * dx + dz * dz <= radius * radius) {
              const nx = g.x + dx;
              const nz = g.z + dz;
              if (nx >= 0 && nx < GRID_SIZE && nz >= 0 && nz < GRID_SIZE) {
                fogOfWarGrid[nz * GRID_SIZE + nx] = 2; // In direct vision!
              }
            }
          }
        }
      });

      // Update Enemy Unit Visibility (Only visible if inside a vision tile!)
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

      // Rock-Paper-Scissors Bonuses:
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
