def get_aoe_html():
    return """
  <div id="selection-box"></div>
  <div id="canvas-container"></div>

  <!-- NOTICE TOAST -->
  <div id="aoe-notice"></div>

  <!-- WONDER COUNTDOWN BANNER -->
  <div id="wonder-banner">
    <div class="wonder-title">[IMPERIAL WONDER VICTORY]</div>
    <div id="wonder-timer" class="wonder-timer">200s</div>
  </div>

  <!-- FLOATING 3D HOVER TOOLTIP -->
  <div id="hover-tooltip">
    <div id="tip-title" class="tip-title">[OBJECT NAME]</div>
    <div id="tip-sub" class="tip-sub">Details</div>
  </div>

  <!-- FLOATING ROYAL TASKS & BOUNTIES TRACKER -->
  <div id="mission-hud">
    <div class="mission-hud-header">
      <span class="mission-hud-title">[SOVEREIGN CAMPAIGN]</span>
      <span id="mission-step-count" style="font-size: 10px; color: #ffd700;">1 / 5</span>
    </div>
    <div id="mission-current-title" class="mission-current-title">1. Lay the Foundation</div>
    <div id="mission-current-desc" class="mission-current-desc">Construct a Lumber Camp and a Town House to secure vital supplies for your realm.</div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span id="mission-reward-tag" class="mission-reward-tag">[REWARD: +100 XP / 50 WOOD]</span>
      <button class="top-btn" style="padding: 2px 6px; font-size: 9px;" onclick="window.toggleObjectivesModal()">[ALL]</button>
    </div>
  </div>

  <!-- TOP STATUS & RESOURCE BAR (Classic AoE Wood/Gold Header) -->
  <div id="aoe-top-bar">
    <div class="top-left-sect">
      <div class="civ-shield">
        <span>[CIV]</span>
        <span id="civ-name">BRITONS</span>
      </div>

      <div class="age-badge">
        <span id="current-age-name">DARK AGE</span>
      </div>

      <button id="btn-advance-age" class="age-advance-btn" onclick="window.advanceCurrentAge()" style="display: none;">
        <span>[ADVANCE]</span> <span id="advance-age-label">Feudal Age (500 Food)</span>
      </button>

      <div class="level-pill">
        <span id="aoe-level-title">LVL 1: HAMLET</span>
        <span style="color: #ca8a04;">|</span>
        <span id="aoe-score">150 PTS</span>
      </div>
    </div>

    <!-- 4 Classic AoE Resources & Pop Cap -->
    <div class="resource-row">
      <div class="res-pill res-wood" title="Wood: Lumber for buildings & bows">
        <span class="tag">[WOOD]</span>
        <span id="aoe-wood">200</span>
      </div>
      <div class="res-pill res-food" title="Food: Foraging, farming & hunting">
        <span class="tag">[FOOD]</span>
        <span id="aoe-food">200</span>
      </div>
      <div class="res-pill res-gold" title="Gold: High-tier troops & techs">
        <span class="tag">[GOLD]</span>
        <span id="aoe-gold">100</span>
      </div>
      <div class="res-pill res-stone" title="Stone: Fortresses, walls & castles">
        <span class="tag">[STONE]</span>
        <span id="aoe-stone">200</span>
      </div>
      <div class="res-pill res-pop" title="Population vs House Capacity">
        <span class="tag">[POP]</span>
        <span><span id="aoe-pop">4</span>/<span id="aoe-maxpop">10</span></span>
      </div>
    </div>

    <!-- Quick Action Buttons -->
    <div class="top-right-sect">
      <button class="top-btn idle-btn" onclick="window.cycleIdleVillager()" title="Select Next Idle Villager (Hotkey: Z or .)">
        <span>[!] IDLE:</span> <span id="idle-count">0</span>
      </button>
      <button id="btn-town-bell" class="top-btn bell-btn" onclick="window.toggleTownBell()" title="Garrison Villagers into Town Center (Hotkey: B)">
        <span>[TOWN BELL]</span>
      </button>
      <button class="top-btn craft-btn" onclick="window.toggleCraftingModal()" title="Artisan Atelier & Blacksmith Forge">[CRAFTING]</button>
      <button id="btn-weather" class="top-btn weather-btn" onclick="window.cycleWeather()" title="Toggle Weather & Time of Day">[WEATHER: SUNNY]</button>
      <button class="top-btn" onclick="window.saveAoEGame()" title="Quick-Save Empire Status (F5)">[SAVE]</button>
      <button class="top-btn" onclick="window.loadAoEGame()" title="Quick-Load Saved Empire (F9)">[LOAD]</button>
      <button class="top-btn" onclick="window.toggleObjectivesModal()">[TASKS]</button>
      <button class="top-btn" onclick="window.toggleMenuModal()">[MENU]</button>
    </div>
  </div>

  <!-- BOTTOM RTS COMMAND CONSOLE (AoE II Authentic Architecture) -->
  <div id="aoe-bottom-bar">
    <!-- LEFT: Selection Portrait & Details -->
    <div class="console-left">
      <div class="entity-header">
        <div class="portrait-frame">
          <canvas id="portrait-canvas" width="68" height="68"></canvas>
        </div>
        <div class="entity-titles">
          <div id="entity-name" class="entity-name">Town Center</div>
          <div id="entity-type" class="entity-type">Civic Headquarters</div>
          <div class="hp-bar-outer">
            <div id="hp-bar-inner" class="hp-bar-inner" style="width: 100%;"></div>
          </div>
        </div>
      </div>

      <div id="entity-stats" class="entity-stats">
        <div>HP: <span id="stat-hp" class="stat-val">2400 / 2400</span></div>
        <div>Attack: <span id="stat-atk" class="stat-val">5</span></div>
        <div>Armor: <span id="stat-arm" class="stat-val">2 / 2</span></div>
        <div>Range: <span id="stat-rng" class="stat-val">6</span></div>
      </div>
    </div>

    <!-- CENTER: Action & Command Grid -->
    <div class="console-center">
      <div id="grid-tabs-bar" class="action-grid-tabs" style="display: none;">
        <button id="tab-build-eco" class="grid-tab-btn active" onclick="window.setBuildCategory('eco')">[ECONOMIC BUILDINGS (Q)]</button>
        <button id="tab-build-mil" class="grid-tab-btn" onclick="window.setBuildCategory('mil')">[MILITARY BUILDINGS (W)]</button>
        <button id="tab-commands" class="grid-tab-btn" onclick="window.setBuildCategory('cmd')">[COMMANDS & STANCES]</button>
      </div>

      <div id="action-grid" class="action-grid">
        <!-- 10 Action Buttons dynamically populated -->
      </div>

      <!-- Training & Research Queue Progress Bar -->
      <div id="train-queue-bar" class="train-queue-bar" style="display: none;">
        <span style="font-size: 9px; color: #93c5fd; font-weight: 800;">[TRAINING]:</span>
        <div style="flex: 1; background: #261609; height: 10px; border-radius: 2px; overflow: hidden;">
          <div id="queue-fill" class="queue-fill" style="width: 0%;"></div>
        </div>
        <div id="queue-slots" class="queue-slots"></div>
      </div>
    </div>

    <!-- RIGHT: Live RTS Radar Minimap -->
    <div class="console-right">
      <div class="minimap-wrapper" id="minimap-wrapper">
        <canvas id="minimap-canvas" width="196" height="154"></canvas>
      </div>
    </div>
  </div>

  <!-- CRAFTING ATELIER & FORGE MODAL -->
  <div id="crafting-modal" class="aoe-modal">
    <div class="aoe-modal-box">
      <div class="aoe-modal-header">
        <span class="aoe-modal-title">[ARTISAN CRAFTING ATELIER & FORGE]</span>
        <button class="aoe-close-btn" onclick="window.toggleCraftingModal()">[X]</button>
      </div>
      <p style="font-size: 11px; color: #d1c0a5; margin-bottom: 8px;">
        Harness raw timber, stone, and precious metals to forge specialized tools, sacred masterworks, and military armaments.
      </p>
      <div class="craft-recipes-grid" id="craft-recipes-container">
        <!-- Dynamically rendered crafting cards -->
      </div>
    </div>
  </div>

  <!-- OBJECTIVES & CAMPAIGN MODAL -->
  <div id="objectives-modal" class="aoe-modal">
    <div class="aoe-modal-box">
      <div class="aoe-modal-header">
        <span class="aoe-modal-title">[AGE OF EMPIRES // CAMPAIGN & OBJECTIVES]</span>
        <button class="aoe-close-btn" onclick="window.toggleObjectivesModal()">[X]</button>
      </div>
      <div style="font-size: 13px; line-height: 1.6; color: #e8ddc7; max-height: 60vh; overflow-y: auto;">
        <h4 style="color: #ffd700; margin-bottom: 4px;">ROYAL TASKS & BOUNTIES:</h4>
        <div id="modal-missions-list" style="margin-bottom: 12px;"></div>

        <h4 style="color: #ffd700; margin-bottom: 4px;">VICTORY CONDITIONS:</h4>
        <p><strong>1. Conquest Victory:</strong> Build an army of Swordsmen, Archers, and Knights to destroy the Rival Red Civilization's Town Center across the river.</p>
        <p><strong>2. Wonder Victory:</strong> Reach the Imperial Age, build a Wonder of the World, and defend it for 200 seconds against enemy onslaughts!</p>

        <h4 style="color: #ffd700; margin-top: 14px; margin-bottom: 4px;">THE FOUR AGES PROGRESSION:</h4>
        <p>&bull; <strong>Dark Age:</strong> Gather Food and Wood. Hunt Wild Boar in the jungle. Build Houses for population.</p>
        <p>&bull; <strong>Feudal Age (500 Food):</strong> Unlocks Barracks, Archery Range, Stable, Blacksmith, Watchtower, and Stone Walls.</p>
        <p>&bull; <strong>Castle Age (800 Food, 200 Gold):</strong> Unlocks Castles, Monasteries, Knights, Crossbowmen, and Monks ("WOLOLO")!</p>
        <p>&bull; <strong>Imperial Age (1000 Food, 800 Gold):</strong> Unlocks Paladins, Champions, Trebuchets, and the Wonder of the World.</p>

        <h4 style="color: #ffd700; margin-top: 14px; margin-bottom: 4px;">RTS CONTROLS & HOTKEYS:</h4>
        <p>&bull; <strong>Box Selection:</strong> Left-click and drag a green box to select multiple units.</p>
        <p>&bull; <strong>Smart Right-Click:</strong> Right-click terrain to move, right-click resources to gather, right-click wild animals to hunt, right-click enemies to attack, right-click damaged buildings to repair.</p>
        <p>&bull; <strong>Z or .</strong>: Cycle through idle villagers. <strong>B</strong>: Ring Town Bell.</p>
        <p>&bull; <strong>WASD / Arrow Keys</strong>: Pan camera. <strong>Mouse Wheel</strong>: Zoom.</p>
        <p>&bull; <strong>F5 / F9</strong>: Quick-Save / Quick-Load.</p>
      </div>
    </div>
  </div>

  <!-- SETTINGS & PAUSE MENU MODAL -->
  <div id="menu-modal" class="aoe-modal">
    <div class="aoe-modal-box">
      <div class="aoe-modal-header">
        <span class="aoe-modal-title">[AGE OF EMPIRES // MAIN MENU & SETTINGS]</span>
        <button class="aoe-close-btn" onclick="window.toggleMenuModal()">[RESUME]</button>
      </div>
      <div style="font-size: 13px; line-height: 1.6; color: #e8ddc7;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center;">
          <span>Sound Effects & Voice Barks:</span>
          <input type="range" id="sound-vol" min="0" max="1" step="0.1" value="0.8" onchange="window.setMasterVolume(this.value)">
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center;">
          <span>Camera Scroll Speed:</span>
          <select id="camera-speed" style="background: #3d2816; color: #ffd700; border: 1px solid #7c5828; padding: 4px 8px; border-radius: 4px;">
            <option value="1">Standard (1.0x)</option>
            <option value="1.5">Fast (1.5x)</option>
            <option value="2">Very Fast (2.0x)</option>
          </select>
        </div>
        <div style="background: #180e07; border: 1px solid #5a3e20; border-radius: 6px; padding: 12px; margin-top: 14px; font-size: 11px;">
          <div style="color: #ffd700; font-weight: 800; margin-bottom: 4px;">AGE OF EMPIRES RTS HISTORICAL SIMULATOR</div>
          <div>Built for the Meta Global Developer Hackathon. Solo Developer: <a href="https://github.com/pinoyUnknown" target="_blank" style="color: #ffd700;">PinoyUnknown</a></div>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 16px;">
          <button class="aoe-close-btn" onclick="window.saveAoEGame()">[SAVE GAME]</button>
          <button class="aoe-close-btn" onclick="window.loadAoEGame()">[LOAD GAME]</button>
          <button class="aoe-close-btn" onclick="window.toggleMenuModal()">[BACK TO GAME]</button>
        </div>
      </div>
    </div>
  </div>
    """
