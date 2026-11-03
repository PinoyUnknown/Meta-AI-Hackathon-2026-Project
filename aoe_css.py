def get_aoe_css():
    return """
    /* =========================================================================
       AGE OF EMPIRES // AUTHENTIC RTS INTERFACE & STYLING
       ========================================================================= */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #0d0a08;
      font-family: 'Cinzel', 'Trajan Pro', 'Georgia', serif;
      color: #f5eedb;
    }

    #canvas-container {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    /* Selection Box (RTS Click & Drag) */
    #selection-box {
      position: absolute;
      border: 1.5px solid #4ade80;
      background: rgba(74, 222, 128, 0.18);
      pointer-events: none;
      z-index: 99;
      display: none;
    }

    /* TOP RESOURCE & STATUS BANNER (Classic AoE Wood/Gold Header) */
    #aoe-top-bar {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 48px;
      background: linear-gradient(180deg, #2a1d13 0%, #1c130c 100%);
      border-bottom: 2px solid #8e6834;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 50;
      font-size: 13px;
      letter-spacing: 0.5px;
    }

    .top-left-sect {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .civ-shield {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #3a2717;
      border: 1px solid #c9933b;
      border-radius: 4px;
      padding: 4px 8px;
      font-weight: 800;
      color: #ffd700;
      text-shadow: 1px 1px 2px #000;
    }

    .age-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(180deg, #4a1212 0%, #2b0808 100%);
      border: 1px solid #e11d48;
      border-radius: 4px;
      padding: 4px 10px;
      font-weight: 800;
      color: #ffe4e6;
      box-shadow: inset 0 0 8px rgba(225, 29, 72, 0.4);
    }

    .age-advance-btn {
      background: linear-gradient(180deg, #b45309 0%, #78350f 100%);
      border: 1px solid #f59e0b;
      border-radius: 4px;
      color: #fff;
      font-weight: 800;
      font-size: 11px;
      padding: 4px 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .age-advance-btn:hover {
      background: linear-gradient(180deg, #d97706 0%, #92400e 100%);
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.6);
    }

    .level-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(180deg, #2b1f15 0%, #170f08 100%);
      border: 1px solid #b8860b;
      border-radius: 4px;
      padding: 4px 9px;
      color: #fef08a;
      font-weight: 800;
      font-size: 11px;
      box-shadow: inset 0 0 6px rgba(184, 134, 11, 0.3);
    }

    /* 4 Classic AoE Resources & Pop Cap */
    .resource-row {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .res-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #150e09;
      border: 1px solid #583c21;
      border-radius: 4px;
      padding: 4px 8px;
      font-weight: 700;
      min-width: 78px;
      justify-content: space-between;
    }
    .res-pill .tag {
      font-size: 11px;
      font-weight: 800;
    }
    .res-wood .tag { color: #84cc16; }
    .res-food .tag { color: #f97316; }
    .res-gold .tag { color: #eab308; }
    .res-stone .tag { color: #94a3b8; }
    .res-pop .tag { color: #38bdf8; }

    .top-right-sect {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .top-btn {
      background: linear-gradient(180deg, #3d2816 0%, #24160a 100%);
      border: 1px solid #7c5828;
      border-radius: 4px;
      color: #f5eedb;
      font-family: inherit;
      font-size: 11px;
      font-weight: 700;
      padding: 5px 9px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .top-btn:hover {
      background: linear-gradient(180deg, #53371f 0%, #352110 100%);
      border-color: #c9933b;
      color: #fff;
    }

    .idle-btn {
      background: linear-gradient(180deg, #854d0e 0%, #533008 100%);
      border-color: #ca8a04;
      color: #fef08a;
    }

    .bell-btn {
      background: linear-gradient(180deg, #991b1b 0%, #580c0c 100%);
      border-color: #ef4444;
      color: #fecaca;
    }

    .craft-btn {
      background: linear-gradient(180deg, #0f766e 0%, #115e59 100%);
      border-color: #14b8a6;
      color: #ccfbf1;
    }

    .weather-btn {
      background: linear-gradient(180deg, #1e3a8a 0%, #172554 100%);
      border-color: #3b82f6;
      color: #bfdbfe;
    }

    /* FLOATING ROYAL TASKS & BOUNTIES TRACKER (Top-Left) */
    #mission-hud {
      position: absolute;
      top: 56px;
      left: 16px;
      width: 280px;
      background: rgba(22, 14, 8, 0.94);
      border: 2px solid #c9933b;
      border-radius: 6px;
      padding: 10px 12px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.85);
      z-index: 45;
      backdrop-filter: blur(4px);
    }
    .mission-hud-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #7c5828;
      padding-bottom: 6px;
      margin-bottom: 8px;
    }
    .mission-hud-title {
      font-size: 11px;
      font-weight: 800;
      color: #ffd700;
      letter-spacing: 0.5px;
    }
    .mission-current-title {
      font-size: 12px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }
    .mission-current-desc {
      font-size: 10px;
      color: #d1c0a5;
      line-height: 1.4;
      margin-bottom: 6px;
    }
    .mission-reward-tag {
      font-size: 10px;
      font-weight: 800;
      color: #4ade80;
    }

    /* BOTTOM RTS COMMAND CONSOLE (AoE II Authentic Architecture) */
    #aoe-bottom-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 172px;
      background: linear-gradient(180deg, #24160a 0%, #150d06 100%);
      border-top: 3px solid #8e6834;
      box-shadow: 0 -6px 20px rgba(0, 0, 0, 0.8);
      display: grid;
      grid-template-columns: 290px 1fr 220px;
      z-index: 50;
    }

    /* LEFT: Selection Portrait & Details */
    .console-left {
      border-right: 2px solid #5a3e20;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #1a1008;
    }

    .entity-header {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .portrait-frame {
      width: 68px;
      height: 68px;
      border: 2px solid #c9933b;
      border-radius: 4px;
      background: #0d0804;
      box-shadow: inset 0 0 10px #000;
      overflow: hidden;
      flex-shrink: 0;
    }

    .entity-titles {
      flex: 1;
      min-width: 0;
    }

    .entity-name {
      font-size: 14px;
      font-weight: 800;
      color: #ffd700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }

    .entity-type {
      font-size: 10px;
      color: #a89478;
      margin-bottom: 6px;
    }

    .hp-bar-outer {
      width: 100%;
      height: 8px;
      background: #331f11;
      border: 1px solid #5a3e20;
      border-radius: 2px;
      overflow: hidden;
    }

    .hp-bar-inner {
      height: 100%;
      background: #22c55e;
      transition: width 0.15s ease-out;
    }

    .entity-stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3px 8px;
      font-size: 10px;
      color: #d1c0a5;
      background: #110b06;
      border: 1px solid #3d2816;
      border-radius: 3px;
      padding: 6px 8px;
    }
    .stat-val {
      font-weight: 800;
      color: #fff;
    }

    /* CENTER: Action & Command Grid */
    .console-center {
      padding: 8px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border-right: 2px solid #5a3e20;
      background: #160e07;
      min-width: 0;
    }

    .action-grid-tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 6px;
    }

    .grid-tab-btn {
      background: #2b1c10;
      border: 1px solid #5a3e20;
      color: #d1c0a5;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      cursor: pointer;
      border-radius: 3px;
    }
    .grid-tab-btn.active {
      background: #5a3e20;
      border-color: #ffd700;
      color: #ffd700;
    }

    .action-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      grid-template-rows: repeat(2, 44px);
      gap: 6px;
      flex: 1;
    }

    .action-btn {
      background: linear-gradient(180deg, #3d2816 0%, #201309 100%);
      border: 1.5px solid #6b4923;
      border-radius: 4px;
      color: #f5eedb;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      position: relative;
      padding: 2px;
      transition: all 0.1s;
    }
    .action-btn:hover:not(:disabled) {
      border-color: #ffd700;
      background: linear-gradient(180deg, #53371f 0%, #301d0f 100%);
      box-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
    }
    .action-btn:disabled {
      opacity: 0.35;
      cursor: not-allowed;
      filter: grayscale(0.8);
    }

    .btn-hotkey {
      position: absolute;
      top: 2px;
      left: 4px;
      font-size: 9px;
      font-weight: 900;
      color: #ffd700;
    }

    .btn-label {
      font-size: 10px;
      font-weight: 700;
      text-align: center;
      line-height: 1.1;
      margin-top: 4px;
    }

    .btn-cost {
      font-size: 9px;
      color: #a89478;
      margin-top: 1px;
    }

    .train-queue-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px solid #3d2816;
    }
    .queue-fill {
      height: 100%;
      background: #3b82f6;
      transition: width 0.1s linear;
    }
    .queue-slots {
      display: flex;
      gap: 4px;
    }
    .queue-slot {
      width: 22px;
      height: 22px;
      border: 1px solid #7c5828;
      border-radius: 2px;
      background: #1f1309;
      font-size: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffd700;
      font-weight: 800;
    }

    /* RIGHT: Live Radar Minimap */
    .console-right {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px;
      background: #110b06;
    }

    .minimap-wrapper {
      width: 196px;
      height: 154px;
      border: 2px solid #8e6834;
      border-radius: 4px;
      position: relative;
      cursor: crosshair;
      overflow: hidden;
      background: #1b2615;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }
    #minimap-canvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    /* 3D FLOATING HOVER TOOLTIP (Medieval Scroll Look) */
    #hover-tooltip {
      position: absolute;
      pointer-events: none;
      background: rgba(22, 14, 8, 0.94);
      border: 1.5px solid #d4af37;
      border-radius: 6px;
      padding: 8px 12px;
      color: #fbf5e6;
      font-size: 11px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.85);
      z-index: 1000;
      display: none;
      transform: translate(-50%, -125%);
      backdrop-filter: blur(4px);
      max-width: 260px;
    }
    .tip-title {
      font-size: 12px;
      font-weight: 800;
      color: #ffd700;
      margin-bottom: 2px;
    }
    .tip-sub {
      color: #d1c0a5;
      font-size: 10px;
      line-height: 1.3;
    }

    /* NOTIFICATION BANNER */
    #aoe-notice {
      position: absolute;
      top: 60px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(30, 18, 9, 0.95);
      border: 2px solid #eab308;
      border-radius: 6px;
      padding: 8px 24px;
      font-size: 13px;
      font-weight: 800;
      color: #fef08a;
      box-shadow: 0 4px 20px rgba(0,0,0,0.8);
      z-index: 100;
      display: none;
      pointer-events: none;
      letter-spacing: 0.5px;
    }

    /* MODALS & OVERLAYS */
    .aoe-modal {
      position: fixed;
      inset: 0;
      background: rgba(12, 8, 5, 0.78);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .aoe-modal-box {
      width: 640px;
      max-width: 90vw;
      background: #25170d;
      border: 3px solid #c9933b;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.9);
      padding: 20px 24px;
      color: #f3eedf;
    }
    .aoe-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #5a3e20;
      padding-bottom: 10px;
      margin-bottom: 14px;
    }
    .aoe-modal-title {
      font-size: 18px;
      font-weight: 800;
      color: #ffd700;
    }
    .aoe-close-btn {
      background: #3d2816;
      border: 1px solid #7c5828;
      color: #ffd700;
      font-weight: 800;
      padding: 4px 10px;
      cursor: pointer;
      border-radius: 4px;
      font-family: inherit;
    }
    .aoe-close-btn:hover {
      background: #5a3e20;
      border-color: #ffd700;
    }

    /* CRAFTING ATELIER RECIPES GRID */
    .craft-recipes-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }
    .craft-card {
      background: #180e07;
      border: 1.5px solid #5a3e20;
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .craft-card-title {
      font-size: 13px;
      font-weight: 800;
      color: #ffd700;
      margin-bottom: 4px;
    }
    .craft-card-desc {
      font-size: 11px;
      color: #d1c0a5;
      margin-bottom: 8px;
    }
    .craft-card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .craft-cost {
      font-size: 10px;
      color: #f59e0b;
      font-weight: 700;
    }

    /* WONDER COUNTDOWN OVERLAY */
    #wonder-banner {
      position: absolute;
      top: 56px;
      right: 18px;
      background: rgba(60, 20, 10, 0.9);
      border: 2px solid #ffd700;
      border-radius: 6px;
      padding: 8px 14px;
      display: none;
      flex-direction: column;
      align-items: center;
      z-index: 80;
      box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
    .wonder-title {
      font-size: 11px;
      color: #fde047;
      font-weight: 800;
    }
    .wonder-timer {
      font-size: 20px;
      color: #fff;
      font-weight: 900;
      margin-top: 2px;
    }
    """
