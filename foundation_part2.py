part2 = r"""<body>
  <div id="canvas-container"></div>

  <div id="hud">
    <!-- Top Bar: Realm Name & Resource Ledger -->
    <div class="top-bar">
      <div class="town-plate">
        <div class="town-title">RIVERWOOD REALM</div>
        <div class="town-sub">FOUNDATION // ORGANIC SETTLEMENT SIMULATOR</div>
      </div>

      <div class="resource-ledger">
        <div class="res-item"><span class="res-tag">[GOLD]</span> <span id="res-gold">250</span></div>
        <div class="res-item"><span class="res-tag">[WOOD]</span> <span id="res-wood">40</span></div>
        <div class="res-item"><span class="res-tag">[STONE]</span> <span id="res-stone">20</span></div>
        <div class="res-item"><span class="res-tag">[BERRIES]</span> <span id="res-berries">30</span></div>
        <div class="res-item"><span class="res-tag">[BREAD]</span> <span id="res-bread">15</span></div>
      </div>

      <div class="pop-badge">
        <div>[SERFS: <span id="pop-count" style="color: #38bdf8;">6</span>]</div>
        <div>[HAPPINESS: <span id="pop-happy" style="color: #10b981;">100%</span>]</div>
        <button id="btn-settings-hud" class="btn-action" style="padding: 4px 10px; font-size: 11px;">[SETTINGS]</button>
      </div>
    </div>

    <!-- Left Quest & Estate Dispatch Card -->
    <div class="quest-card">
      <div class="quest-tag">[ESTATE DISPATCH // KINGDOM CHARTER]</div>
      <div id="quest-title" class="quest-title">1. Lay the Foundation</div>
      <div id="quest-desc" class="quest-desc">Construct a Lumber Camp and a Town Well to secure vital supplies for your serfs.</div>
      <div id="quest-progress" class="quest-progress">[PROGRESS: 0/2 BUILDINGS]</div>
    </div>

    <!-- Villager / Building Inspector Card -->
    <div id="inspector-card">
      <div class="insp-header">
        <div id="insp-title" class="insp-title">Godwin the Woodcutter</div>
        <button class="insp-close" onclick="closeInspector()">[X]</button>
      </div>
      <div class="insp-row"><span>Status:</span> <span id="insp-status" class="insp-val">Serf</span></div>
      <div class="insp-row"><span>Profession:</span> <span id="insp-job" class="insp-val">Woodcutter</span></div>
      <div class="insp-row"><span>Current Task:</span> <span id="insp-task" class="insp-val">Harvesting Oak</span></div>
      <div class="insp-row"><span>Hunger:</span> <span id="insp-hunger" class="insp-val" style="color: #10b981;">Satisfied</span></div>
      <div class="insp-row"><span>Thirst:</span> <span id="insp-thirst" class="insp-val" style="color: #10b981;">Quenched</span></div>
      <div class="insp-row"><span>Shelter:</span> <span id="insp-shelter" class="insp-val" style="color: #10b981;">Thatched Cottage</span></div>
    </div>

    <!-- Bottom Building Placement Dock -->
    <div class="dock-container">
      <div class="controls-hint">
        <span><kbd>WASD / Arrows</kbd> Pan View</span>
        <span><kbd>Right-Drag</kbd> Rotate Horizon</span>
        <span><kbd>Mouse Scroll</kbd> Zoom 8m - 260m</span>
        <span><kbd>R</kbd> Rotate Structure</span>
        <span><kbd>ESC</kbd> Settings & Pause</span>
      </div>

      <div class="building-dock">
        <div class="b-btn" onclick="selectBuildType('center')">
          <span class="b-tag">[CORE]</span>
          <span class="b-name">Town Hall</span>
          <span class="b-cost">FREE</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('lumber')">
          <span class="b-tag">[PROD]</span>
          <span class="b-name">Lumber Camp</span>
          <span class="b-cost">15 Wood</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('quarry')">
          <span class="b-tag">[PROD]</span>
          <span class="b-name">Stone Quarry</span>
          <span class="b-cost">20 Wood</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('well')">
          <span class="b-tag">[CIVIC]</span>
          <span class="b-name">Town Well</span>
          <span class="b-cost">10 Stone</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('cottage')">
          <span class="b-tag">[RES]</span>
          <span class="b-name">Cottage</span>
          <span class="b-cost">12 Wood, 5 Stone</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('market')">
          <span class="b-tag">[COMM]</span>
          <span class="b-name">Market Stall</span>
          <span class="b-cost">15 Wood, 5 Gold</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('windmill')">
          <span class="b-tag">[AGRI]</span>
          <span class="b-name">Windmill</span>
          <span class="b-cost">25 Wood, 10 Stone</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('church')">
          <span class="b-tag">[FAITH]</span>
          <span class="b-name">Rustic Church</span>
          <span class="b-cost">40 Stone, 20 Wood</span>
        </div>
        <div class="b-btn" onclick="selectBuildType('keep')">
          <span class="b-tag">[DEF]</span>
          <span class="b-name">Lord's Keep</span>
          <span class="b-cost">60 Stone, 40 Wood</span>
        </div>
        <div class="b-btn" onclick="toggleZoningTool()" style="border-color: #10b981;">
          <span class="b-tag" style="color: #34d399;">[ZONE]</span>
          <span class="b-name" id="zone-btn-name">Paint Zone</span>
          <span class="b-cost">Residential</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Settings & Pause Modal (ESC Key) -->
  <div id="settings-modal">
    <div class="modal-box">
      <div class="modal-title">
        <span>[REALM SETTINGS & PAUSE]</span>
        <span style="font-size: 11px; color: #8c6838; font-family: sans-serif;">PRESS ESC TO RESUME</span>
      </div>

      <div class="settings-row">
        <span>Sunlight Brightness:</span>
        <input type="range" id="slider-brightness" min="0.6" max="2.4" step="0.1" value="1.5">
        <span id="val-brightness">150%</span>
      </div>

      <div class="settings-row">
        <span>Master Audio Volume:</span>
        <input type="range" id="slider-volume" min="0" max="1" step="0.05" value="0.75">
        <span id="val-volume">75%</span>
      </div>

      <div class="settings-row">
        <span>GPU Quality & Shaders:</span>
        <select id="select-gpu">
          <option value="ultra">Ultra (High PBR & Shadows)</option>
          <option value="high" selected>High (Optimal 60 FPS)</option>
          <option value="medium">Performance (Low Shadows)</option>
        </select>
      </div>

      <div class="settings-row">
        <span>Resolution Scaling:</span>
        <select id="select-resolution">
          <option value="1.0" selected>Native 100% (1080p / 1440p / 4K)</option>
          <option value="0.75">Balanced 75%</option>
          <option value="0.5">High Performance 50%</option>
        </select>
      </div>

      <div class="settings-row">
        <span>Display Monitor:</span>
        <select id="select-monitor">
          <option value="1">Primary Desktop Display (Default)</option>
          <option value="2">Secondary Studio Display</option>
          <option value="vr">Meta Horizon XR Headset Display</option>
        </select>
      </div>

      <div style="background: #f4ede0; border: 1px solid #c9933b; border-radius: 8px; padding: 12px; margin-top: 14px; font-size: 11px; line-height: 1.6;">
        <div style="font-weight: 800; color: #4a3420; margin-bottom: 2px;">
          FOUNDATION: ORGANIC SETTLEMENT SIMULATOR (v9.0.0 PROTOTYPE)
        </div>
        <div style="color: #6b4c30; margin-bottom: 6px;">
          Inspired by Foundation (Polymorph Games). Grid-less organic medieval town building, dynamic desire footpaths, autonomous serfs, modular monuments, and estate supply chain economy.
        </div>
        <div>
          <strong>Lead Developer:</strong> <a href="https://github.com/pinoyUnknown" target="_blank" style="color: #855d38; font-weight: bold;">github.com/pinoyUnknown</a> |
          <a href="https://instagram.com/pinoyunknown" target="_blank" style="color: #855d38; font-weight: bold;">instagram.com/pinoyunknown</a>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px;">
        <button class="btn-action" onclick="togglePauseSettings()">[RESUME REALM]</button>
      </div>
    </div>
  </div>
"""
