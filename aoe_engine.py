# AOE Engine & Gameplay JavaScript Generator
def get_aoe_engine_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES RTS GAMEPLAY ENGINE & SIMULATION
    // =========================================================================

    // Global Game State
    window.aoeState = {
      age: 'Dark Age',
      civ: 'Britons',
      resources: { wood: 200, food: 200, gold: 100, stone: 200 },
      pop: 4,
      maxPop: 10,
      selectedEntities: [],
      selectedEntity: null,
      idleVillagers: [],
      townBellRinging: false,
      relicsHeld: 0,
      wonderActive: false,
      wonderTimer: 200,
      buildCategory: 'eco', // 'eco', 'mil', 'cmd'
      activePlacementType: null,
      placementGhost: null,
      controlGroups: {},
      projectiles: [],
      particles: [],
      gameWon: false,
      gameLost: false
    };

    // Entity Collections
    const friendlyUnits = [];
    const enemyUnits = [];
    const friendlyBuildings = [];
    const enemyBuildings = [];
    const naturalResources = []; // Trees, Gold mines, Stone mines, Berry bushes, Sheep, Boars
    const holyRelics = [];
    const allSelectable = [];

    let nextEntityId = 1;

    // Unit & Building Prototypes & Costs
    const UNIT_TYPES = {
      villager: { name: 'Villager', hp: 25, attack: 3, armor: 0, range: 1.5, speed: 0.16, cost: { food: 50 }, trainTime: 8, age: 'Dark Age' },
      scout: { name: 'Scout Cavalry', hp: 45, attack: 5, armor: 1, range: 1.8, speed: 0.28, cost: { food: 80 }, trainTime: 10, age: 'Dark Age' },
      militia: { name: 'Militia', hp: 40, attack: 4, armor: 1, range: 1.5, speed: 0.18, cost: { food: 60, gold: 20 }, trainTime: 9, age: 'Dark Age' },
      man_at_arms: { name: 'Man-at-Arms', hp: 50, attack: 7, armor: 2, range: 1.5, speed: 0.18, cost: { food: 60, gold: 20 }, trainTime: 10, age: 'Feudal Age' },
      spearman: { name: 'Spearman', hp: 45, attack: 4, armor: 0, range: 2.2, speed: 0.19, cost: { food: 35, wood: 25 }, trainTime: 8, age: 'Feudal Age' },
      archer: { name: 'Archer', hp: 30, attack: 4, armor: 0, range: 14, speed: 0.17, cost: { wood: 25, gold: 45 }, trainTime: 11, age: 'Feudal Age' },
      knight: { name: 'Knight', hp: 100, attack: 10, armor: 2, range: 2.0, speed: 0.25, cost: { food: 60, gold: 75 }, trainTime: 14, age: 'Castle Age' },
      monk: { name: 'Monk', hp: 30, attack: 0, armor: 0, range: 8, speed: 0.15, cost: { gold: 100 }, trainTime: 15, age: 'Castle Age' },
      trebuchet: { name: 'Trebuchet', hp: 150, attack: 150, armor: 2, range: 35, speed: 0.08, cost: { wood: 200, gold: 200 }, trainTime: 20, age: 'Imperial Age' }
    };

    const BUILDING_TYPES = {
      town_center: { name: 'Town Center', hp: 2400, cost: { wood: 275, stone: 100 }, size: 14, age: 'Dark Age', providesPop: 5 },
      house: { name: 'House', hp: 550, cost: { wood: 25 }, size: 6, age: 'Dark Age', providesPop: 5 },
      mill: { name: 'Mill', hp: 600, cost: { wood: 100 }, size: 7, age: 'Dark Age' },
      lumber_camp: { name: 'Lumber Camp', hp: 600, cost: { wood: 100 }, size: 7, age: 'Dark Age' },
      mining_camp: { name: 'Mining Camp', hp: 600, cost: { wood: 100 }, size: 7, age: 'Dark Age' },
      farm: { name: 'Farm', hp: 480, cost: { wood: 60 }, size: 9, age: 'Dark Age' },
      barracks: { name: 'Barracks', hp: 1200, cost: { wood: 175 }, size: 11, age: 'Dark Age' },
      archery_range: { name: 'Archery Range', hp: 1200, cost: { wood: 175 }, size: 10, age: 'Feudal Age' },
      stable: { name: 'Stable', hp: 1500, cost: { wood: 175 }, size: 12, age: 'Feudal Age' },
      blacksmith: { name: 'Blacksmith', hp: 1200, cost: { wood: 150 }, size: 7, age: 'Feudal Age' },
      monastery: { name: 'Monastery', hp: 1400, cost: { wood: 175 }, size: 12, age: 'Castle Age' },
      castle: { name: 'Castle', hp: 4800, cost: { stone: 650 }, size: 22, age: 'Castle Age' },
      wonder: { name: 'Wonder of the World', hp: 6000, cost: { wood: 1000, gold: 1000, stone: 1000 }, size: 28, age: 'Imperial Age' },
      watchtower: { name: 'Watchtower', hp: 1020, cost: { wood: 50, stone: 125 }, size: 5, age: 'Feudal Age' },
      wall: { name: 'Stone Wall', hp: 1800, cost: { stone: 5 }, size: 6, age: 'Feudal Age' }
    };

    // UI Toast Notification
    window.showAoENotice = function(msg, duration = 3000) {
      const banner = document.getElementById('aoe-notice');
      if (!banner) return;
      banner.textContent = msg;
      banner.style.display = 'block';
      clearTimeout(banner._timer);
      banner._timer = setTimeout(() => {
        banner.style.display = 'none';
      }, duration);
    };

    // Update Top Resource Counters & Population
    window.updateResourceUI = function() {
      document.getElementById('aoe-wood').textContent = Math.floor(aoeState.resources.wood);
      document.getElementById('aoe-food').textContent = Math.floor(aoeState.resources.food);
      document.getElementById('aoe-gold').textContent = Math.floor(aoeState.resources.gold);
      document.getElementById('aoe-stone').textContent = Math.floor(aoeState.resources.stone);
      document.getElementById('aoe-pop').textContent = aoeState.pop;
      document.getElementById('aoe-maxpop').textContent = aoeState.maxPop;
      document.getElementById('current-age-name').textContent = aoeState.age.toUpperCase();

      // Check if eligible to advance age
      const advBtn = document.getElementById('btn-advance-age');
      const advLbl = document.getElementById('advance-age-label');
      if (aoeState.age === 'Dark Age') {
        advBtn.style.display = 'flex';
        advLbl.textContent = 'Feudal Age (500 Food)';
        advBtn.disabled = aoeState.resources.food < 500;
        advBtn.style.opacity = aoeState.resources.food >= 500 ? '1' : '0.6';
      } else if (aoeState.age === 'Feudal Age') {
        advBtn.style.display = 'flex';
        advLbl.textContent = 'Castle Age (800F, 200G)';
        const canAdv = aoeState.resources.food >= 800 && aoeState.resources.gold >= 200;
        advBtn.disabled = !canAdv;
        advBtn.style.opacity = canAdv ? '1' : '0.6';
      } else if (aoeState.age === 'Castle Age') {
        advBtn.style.display = 'flex';
        advLbl.textContent = 'Imperial Age (1000F, 800G)';
        const canAdv = aoeState.resources.food >= 1000 && aoeState.resources.gold >= 800;
        advBtn.disabled = !canAdv;
        advBtn.style.opacity = canAdv ? '1' : '0.6';
      } else {
        advBtn.style.display = 'none';
      }

      // Idle villager count
      const idleCount = friendlyUnits.filter(u => u.type === 'villager' && u.state === 'idle').length;
      document.getElementById('idle-count').textContent = idleCount;
    };

    // Age Advancement Logic
    window.advanceCurrentAge = function() {
      initAudio();
      if (aoeState.age === 'Dark Age') {
        if (aoeState.resources.food < 500) {
          showAoENotice('[INSUFFICIENT FOOD] Advance to Feudal Age requires 500 Food.');
          return;
        }
        aoeState.resources.food -= 500;
        aoeState.age = 'Feudal Age';
        playAdvanceAgeFanfare();
        showAoENotice('[RESEARCH COMPLETE: FEUDAL AGE REACHED!] New military structures and technologies unlocked!');
        refreshBuildingVisuals();
      } else if (aoeState.age === 'Feudal Age') {
        if (aoeState.resources.food < 800 || aoeState.resources.gold < 200) {
          showAoENotice('[INSUFFICIENT RESOURCES] Castle Age requires 800 Food and 200 Gold.');
          return;
        }
        aoeState.resources.food -= 800;
        aoeState.resources.gold -= 200;
        aoeState.age = 'Castle Age';
        playAdvanceAgeFanfare();
        showAoENotice('[RESEARCH COMPLETE: CASTLE AGE REACHED!] Fortified stone castles, knights, and holy relics unlocked!');
        refreshBuildingVisuals();
      } else if (aoeState.age === 'Castle Age') {
        if (aoeState.resources.food < 1000 || aoeState.resources.gold < 800) {
          showAoENotice('[INSUFFICIENT RESOURCES] Imperial Age requires 1000 Food and 800 Gold.');
          return;
        }
        aoeState.resources.food -= 1000;
        aoeState.resources.gold -= 800;
        aoeState.age = 'Imperial Age';
        playAdvanceAgeFanfare();
        showAoENotice('[RESEARCH COMPLETE: IMPERIAL AGE REACHED!] Paladins, trebuchets, and the Wonder of the World unlocked!');
        refreshBuildingVisuals();
      }
      updateResourceUI();
      updateActionGrid();
    };

    // Town Bell Garrison Mechanism
    window.toggleTownBell = function() {
      initAudio();
      playTownBellSound();
      aoeState.townBellRinging = !aoeState.townBellRinging;
      const bellBtn = document.getElementById('btn-town-bell');

      const townCenter = friendlyBuildings.find(b => b.type === 'town_center');
      if (!townCenter) return;

      if (aoeState.townBellRinging) {
        bellBtn.style.background = 'linear-gradient(180deg, #dc2626 0%, #7f1d1d 100%)';
        showAoENotice('[TOWN BELL SOUNDED] All villagers retreat to garrison inside the Town Center!');
        friendlyUnits.filter(u => u.type === 'villager').forEach(v => {
          v.state = 'garrisoned';
          v.mesh.visible = false;
        });
      } else {
        bellBtn.style.background = 'linear-gradient(180deg, #991b1b 0%, #580c0c 100%)';
        showAoENotice('[TOWN BELL RUNG] Villagers emerge from the Town Center and resume work!');
        friendlyUnits.filter(u => u.type === 'villager').forEach(v => {
          v.state = 'idle';
          v.mesh.visible = true;
          v.mesh.position.set(townCenter.mesh.position.x + (Math.random() - 0.5) * 12, 0, townCenter.mesh.position.z + 8 + Math.random() * 4);
        });
      }
      updateResourceUI();
    };

    // Cycle Next Idle Villager
    let lastIdleIndex = 0;
    window.cycleIdleVillager = function() {
      const idles = friendlyUnits.filter(u => u.type === 'villager' && u.state === 'idle');
      if (idles.length === 0) {
        showAoENotice('[ALL VILLAGERS OCCUPIED] No idle villagers in realm.');
        return;
      }
      lastIdleIndex = (lastIdleIndex + 1) % idles.length;
      const target = idles[lastIdleIndex];
      selectSingleEntity(target);
      // Pan camera to unit
      cameraTargetPos.set(target.mesh.position.x, target.mesh.position.y, target.mesh.position.z);
      playVoiceBark('select');
    };
    """
