# AOE Engine & Gameplay JavaScript Generator
def get_aoe_engine_js():
    return """
    // =========================================================================
    // AGE OF EMPIRES RTS GAMEPLAY ENGINE, MISSIONS & CRAFTING
    // =========================================================================

    // Global Game State
    window.aoeState = {
      age: 'Dark Age',
      civ: 'Britons',
      resources: { wood: 200, food: 200, gold: 100, stone: 200 },
      pop: 4,
      maxPop: 10,
      score: 150,
      level: 1,
      levelTitle: 'Hamlet',
      weather: 'Sunny Noon',
      miningBonus: 1.0,
      archerBonus: false,
      passiveGold: 0,
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
      craftedItems: {},
      missions: [
        { id: 'm1', title: '1. Lay the Foundation', desc: 'Construct a Lumber Camp and a Town House to secure supplies for your realm.', goalType: 'build_house_lumber', target: 2, current: 0, rewardXp: 100, rewardWood: 50, completed: false },
        { id: 'm2', title: '2. Hunt Wild Beasts', desc: 'Command your villagers into the jungle to hunt a Wild Boar or Deer for survival food.', goalType: 'hunt_wild', target: 1, current: 0, rewardXp: 150, rewardFood: 100, completed: false },
        { id: 'm3', title: '3. Stockpile the Granary', desc: 'Amass 500 Food and advance your civilization to the Feudal Age.', goalType: 'advance_feudal', target: 1, current: 0, rewardXp: 250, rewardGold: 50, completed: false },
        { id: 'm4', title: '4. Muster the Vanguard', desc: 'Erect a Barracks and muster 3 Spearmen or Archers for defense.', goalType: 'train_military', target: 3, current: 0, rewardXp: 350, rewardFood: 100, completed: false },
        { id: 'm5', title: '5. Raze the Rival Fortress', desc: 'March across the stone bridge and destroy the Rival Red Town Center!', goalType: 'destroy_enemy_tc', target: 1, current: 0, rewardXp: 1000, rewardGold: 500, completed: false }
      ],
      gameWon: false,
      gameLost: false
    };

    // Entity Collections
    const friendlyUnits = [];
    const enemyUnits = [];
    const friendlyBuildings = [];
    const enemyBuildings = [];
    const naturalResources = []; // Trees, Gold mines, Stone mines, Berry bushes, Sheep, Wild Boars, Wild Deer
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

    // Crafting Recipes Palette
    const CRAFTING_RECIPES = [
      { id: 'pickaxe', name: 'Masterwork Pickaxe', cost: { wood: 10, gold: 20 }, desc: '+25% Mining Gathering Rate', icon: '[TOOL]' },
      { id: 'bow', name: 'Recurve Yew Bow', cost: { wood: 15, gold: 25 }, desc: '+3 Archer Range & +2 Attack', icon: '[WEAPON]' },
      { id: 'stained_glass', name: 'Stained Glass Rosette', cost: { stone: 10, gold: 30 }, desc: '+150 Prestige & +10 Pop Cap', icon: '[FAITH]' },
      { id: 'sovereign_relic', name: 'Gilded Sovereign Relic', cost: { stone: 20, gold: 50 }, desc: '+200 XP & +1 Gold/sec Income', icon: '[CROWN]' }
    ];

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

    // Point & Level Progression System
    window.addPoints = function(pts, reason) {
      aoeState.score += pts;
      checkLevelProgression();
      updateResourceUI();
      if (reason) showAoENotice(`[+${pts} PTS] ${reason}`);
    };

    function checkLevelProgression() {
      const tiers = [
        { lvl: 1, min: 0, title: 'Hamlet' },
        { lvl: 2, min: 250, title: 'Village' },
        { lvl: 3, min: 600, title: 'Barony' },
        { lvl: 4, min: 1200, title: 'Duchy' },
        { lvl: 5, min: 2500, title: 'Sovereign Empire' }
      ];
      let currentTier = tiers[0];
      for (let t of tiers) {
        if (aoeState.score >= t.min) currentTier = t;
      }
      if (currentTier.lvl > aoeState.level) {
        aoeState.level = currentTier.lvl;
        aoeState.levelTitle = currentTier.title;
        playAdvanceAgeFanfare();
        showAoENotice(`[LEVEL UP!] Sovereign title promoted to Level ${aoeState.level}: ${aoeState.levelTitle}!`);
      }
    }

    // Check Mission Progress
    window.triggerMissionProgress = function(goalType, delta = 1) {
      let updated = false;
      aoeState.missions.forEach(m => {
        if (!m.completed && m.goalType === goalType) {
          m.current += delta;
          if (m.current >= m.target) {
            m.completed = true;
            updated = true;
            playAdvanceAgeFanfare();
            showAoENotice(`[TASK COMPLETED!] ${m.title}`);
            addPoints(m.rewardXp, `Completed ${m.title}`);
            if (m.rewardWood) aoeState.resources.wood += m.rewardWood;
            if (m.rewardFood) aoeState.resources.food += m.rewardFood;
            if (m.rewardGold) aoeState.resources.gold += m.rewardGold;
          }
        }
      });
      updateMissionHUD();
      updateResourceUI();
    };

    function updateMissionHUD() {
      const hudStep = document.getElementById('mission-step-count');
      const hudTitle = document.getElementById('mission-current-title');
      const hudDesc = document.getElementById('mission-current-desc');
      const hudReward = document.getElementById('mission-reward-tag');

      const activeMission = aoeState.missions.find(m => !m.completed);
      const completedCount = aoeState.missions.filter(m => m.completed).length;

      if (hudStep) hudStep.textContent = `${completedCount + 1} / ${aoeState.missions.length}`;

      if (activeMission) {
        if (hudTitle) hudTitle.textContent = activeMission.title;
        if (hudDesc) hudDesc.textContent = `${activeMission.desc} (${activeMission.current}/${activeMission.target})`;
        if (hudReward) {
          let rewText = `[REWARD: +${activeMission.rewardXp} XP`;
          if (activeMission.rewardWood) rewText += ` / ${activeMission.rewardWood} WOOD`;
          if (activeMission.rewardFood) rewText += ` / ${activeMission.rewardFood} FOOD`;
          if (activeMission.rewardGold) rewText += ` / ${activeMission.rewardGold} GOLD`;
          rewText += ']';
          hudReward.textContent = rewText;
        }
      } else {
        if (hudTitle) hudTitle.textContent = '[ALL TASKS COMPLETED]';
        if (hudDesc) hudDesc.textContent = 'Your sovereign realm has attained historic supremacy!';
        if (hudReward) hudReward.textContent = '[VICTORY IMMINENT]';
      }
    }

    // Update Top Resource Counters & Population
    window.updateResourceUI = function() {
      document.getElementById('aoe-wood').textContent = Math.floor(aoeState.resources.wood);
      document.getElementById('aoe-food').textContent = Math.floor(aoeState.resources.food);
      document.getElementById('aoe-gold').textContent = Math.floor(aoeState.resources.gold);
      document.getElementById('aoe-stone').textContent = Math.floor(aoeState.resources.stone);
      document.getElementById('aoe-pop').textContent = aoeState.pop;
      document.getElementById('aoe-maxpop').textContent = aoeState.maxPop;
      document.getElementById('current-age-name').textContent = aoeState.age.toUpperCase();

      const lvlTitleEl = document.getElementById('aoe-level-title');
      const scoreEl = document.getElementById('aoe-score');
      if (lvlTitleEl) lvlTitleEl.textContent = `LVL ${aoeState.level}: ${aoeState.levelTitle.toUpperCase()}`;
      if (scoreEl) scoreEl.textContent = `${aoeState.score} PTS`;

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
        addPoints(250, 'Reached the Feudal Age');
        triggerMissionProgress('advance_feudal', 1);
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
        addPoints(500, 'Reached the Castle Age');
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
        addPoints(1000, 'Reached the Imperial Age');
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
      cameraTargetPos.set(target.mesh.position.x, 0, target.mesh.position.z);
    };

    // Crafting Atelier UI & Logic
    window.toggleCraftingModal = function() {
      const modal = document.getElementById('crafting-modal');
      const isVisible = modal.style.display === 'flex';
      modal.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) renderCraftingCards();
    };

    function renderCraftingCards() {
      const container = document.getElementById('craft-recipes-container');
      if (!container) return;
      container.innerHTML = '';

      CRAFTING_RECIPES.forEach(recipe => {
        const isCrafted = aoeState.craftedItems[recipe.id];
        let canAfford = true;
        let costStrs = [];
        if (recipe.cost.wood) {
          costStrs.push(`${recipe.cost.wood} Wood`);
          if (aoeState.resources.wood < recipe.cost.wood) canAfford = false;
        }
        if (recipe.cost.food) {
          costStrs.push(`${recipe.cost.food} Food`);
          if (aoeState.resources.food < recipe.cost.food) canAfford = false;
        }
        if (recipe.cost.gold) {
          costStrs.push(`${recipe.cost.gold} Gold`);
          if (aoeState.resources.gold < recipe.cost.gold) canAfford = false;
        }
        if (recipe.cost.stone) {
          costStrs.push(`${recipe.cost.stone} Stone`);
          if (aoeState.resources.stone < recipe.cost.stone) canAfford = false;
        }

        const card = document.createElement('div');
        card.className = 'craft-card';
        card.innerHTML = `
          <div>
            <div class="craft-card-title">${recipe.icon} ${recipe.name}</div>
            <div class="craft-card-desc">${recipe.desc}</div>
          </div>
          <div class="craft-card-footer">
            <span class="craft-cost">Cost: ${costStrs.join(', ')}</span>
            <button class="top-btn" ${isCrafted ? 'disabled' : (canAfford ? '' : 'disabled')} onclick="window.executeCraftItem('${recipe.id}')">
              ${isCrafted ? '[CRAFTED]' : '[CRAFT ITEM]'}
            </button>
          </div>
        `;
        container.appendChild(card);
      });
    }

    window.executeCraftItem = function(recipeId) {
      initAudio();
      const recipe = CRAFTING_RECIPES.find(r => r.id === recipeId);
      if (!recipe || aoeState.craftedItems[recipeId]) return;

      if (recipe.cost.wood && aoeState.resources.wood < recipe.cost.wood) return;
      if (recipe.cost.food && aoeState.resources.food < recipe.cost.food) return;
      if (recipe.cost.gold && aoeState.resources.gold < recipe.cost.gold) return;
      if (recipe.cost.stone && aoeState.resources.stone < recipe.cost.stone) return;

      if (recipe.cost.wood) aoeState.resources.wood -= recipe.cost.wood;
      if (recipe.cost.food) aoeState.resources.food -= recipe.cost.food;
      if (recipe.cost.gold) aoeState.resources.gold -= recipe.cost.gold;
      if (recipe.cost.stone) aoeState.resources.stone -= recipe.cost.stone;

      aoeState.craftedItems[recipeId] = true;

      // Apply bonuses
      if (recipeId === 'pickaxe') {
        aoeState.miningBonus = 1.25;
        showAoENotice('[CRAFTED] Masterwork Pickaxe! +25% Mining Rate.');
      } else if (recipeId === 'bow') {
        aoeState.archerBonus = true;
        showAoENotice('[CRAFTED] Recurve Yew Bow! Archers gain +3 range.');
      } else if (recipeId === 'stained_glass') {
        aoeState.maxPop += 10;
        addPoints(150, 'Crafted Stained Glass Rosette');
        showAoENotice('[CRAFTED] Stained Glass Rosette! +150 Prestige & +10 Pop Cap.');
      } else if (recipeId === 'sovereign_relic') {
        aoeState.passiveGold += 1;
        addPoints(200, 'Crafted Sovereign Relic');
        showAoENotice('[CRAFTED] Gilded Sovereign Relic! +1 Gold/sec passive income.');
      }

      playVoiceBark('build');
      updateResourceUI();
      renderCraftingCards();
    };

    // Modal Toggles
    window.toggleObjectivesModal = function() {
      const modal = document.getElementById('objectives-modal');
      const isVisible = modal.style.display === 'flex';
      modal.style.display = isVisible ? 'none' : 'flex';

      if (!isVisible) {
        const listEl = document.getElementById('modal-missions-list');
        if (listEl) {
          listEl.innerHTML = aoeState.missions.map(m => `
            <div style="background: #190f07; border: 1px solid #5a3e20; border-radius: 4px; padding: 8px 12px; margin-bottom: 6px;">
              <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 800; color: ${m.completed ? '#4ade80' : '#ffd700'};">${m.completed ? '[COMPLETED] ' : ''}${m.title}</span>
                <span style="color: #4ade80; font-size: 11px;">+${m.rewardXp} XP</span>
              </div>
              <div style="font-size: 11px; color: #c4b5a0; margin-top: 2px;">${m.desc} (${m.current}/${m.target})</div>
            </div>
          `).join('');
        }
      }
    };

    window.toggleMenuModal = function() {
      const modal = document.getElementById('menu-modal');
      modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
    };

    // Save & Load Functions
    window.saveAoEGame = function() {
      const saveObj = {
        age: aoeState.age,
        score: aoeState.score,
        level: aoeState.level,
        levelTitle: aoeState.levelTitle,
        resources: aoeState.resources,
        pop: aoeState.pop,
        maxPop: aoeState.maxPop,
        craftedItems: aoeState.craftedItems,
        missions: aoeState.missions.map(m => ({ id: m.id, current: m.current, completed: m.completed })),
        camPos: { x: cameraTargetPos.x, z: cameraTargetPos.z },
        timestamp: Date.now()
      };
      localStorage.setItem('aoe_empire_save', JSON.stringify(saveObj));
      playAdvanceAgeFanfare();
      showAoENotice('[EMPIRE SAVED] Game state stored successfully in local memory!');
    };

    window.loadAoEGame = function() {
      const raw = localStorage.getItem('aoe_empire_save');
      if (!raw) {
        showAoENotice('[NO SAVE FOUND] No saved empire state detected.');
        return;
      }
      try {
        const data = JSON.parse(raw);
        aoeState.age = data.age || 'Dark Age';
        aoeState.score = data.score || 150;
        aoeState.level = data.level || 1;
        aoeState.levelTitle = data.levelTitle || 'Hamlet';
        aoeState.resources = data.resources || { wood: 200, food: 200, gold: 100, stone: 200 };
        aoeState.pop = data.pop || 4;
        aoeState.maxPop = data.maxPop || 10;
        aoeState.craftedItems = data.craftedItems || {};
        if (data.missions) {
          data.missions.forEach(sm => {
            const m = aoeState.missions.find(x => x.id === sm.id);
            if (m) {
              m.current = sm.current;
              m.completed = sm.completed;
            }
          });
        }
        if (data.camPos) {
          cameraTargetPos.set(data.camPos.x, 0, data.camPos.z);
        }
        playAdvanceAgeFanfare();
        showAoENotice('[EMPIRE RESTORED] Sovereign state loaded successfully!');
        updateResourceUI();
        updateMissionHUD();
        refreshBuildingVisuals();
      } catch (err) {
        showAoENotice('[LOAD FAILED] Could not parse save file.');
      }
    };
    """
