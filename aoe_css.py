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
      gap: 12px;
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
      gap: 4px;
      animation: pulseAdvance 2s infinite alternate;
    }
    @keyframes pulseAdvance {
      from { box-shadow: 0 0 4px #f59e0b; }
      to { box-shadow: 0 0 12px #f59e0b; }
    }

    .resource-row {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .res-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #19120b;
      border: 1px solid #5a3e20;
      border-radius: 4px;
      padding: 3px 8px;
      font-weight: 700;
      font-size: 13px;
      color: #f3eedf;
      min-width: 82px;
    }
    .res-pill .tag {
      font-size: 10px;
      font-weight: 900;
      letter-spacing: 0.5px;
    }
    .res-wood .tag { color: #86efac; }
    .res-food .tag { color: #fca5a5; }
    .res-gold .tag { color: #fde047; }
    .res-stone .tag { color: #cbd5e1; }
    .res-pop .tag { color: #93c5fd; }

    .top-right-sect {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .top-btn {
      background: linear-gradient(180deg, #3d2816 0%, #25180c 100%);
      border: 1px solid #997039;
      border-radius: 4px;
      padding: 5px 10px;
      font-size: 11px;
      font-weight: 700;
      color: #f7eed7;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .top-btn:hover {
      background: linear-gradient(180deg, #53381e 0%, #362312 100%);
      border-color: #ffd700;
      color: #fff;
    }
    .idle-btn {
      background: linear-gradient(180deg, #854d0e 0%, #543105 100%);
      border-color: #eab308;
      color: #fef08a;
    }
    .bell-btn {
      background: linear-gradient(180deg, #991b1b 0%, #580c0c 100%);
      border-color: #ef4444;
      color: #fee2e2;
    }

    /* BOTTOM RTS COMMAND CONSOLE (AoE II Authentic Architecture) */
    #aoe-bottom-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 180px;
      background: linear-gradient(180deg, #2b1d12 0%, #170f08 100%);
      border-top: 3px solid #8e6834;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.8);
      display: flex;
      z-index: 50;
      pointer-events: auto;
    }

    /* LEFT SECTION: Selection Info & Unit Portrait */
    .console-left {
      width: 290px;
      min-width: 290px;
      border-right: 2px solid #5a3e20;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: rgba(18, 12, 7, 0.6);
    }

    .entity-header {
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .portrait-frame {
      width: 64px;
      height: 64px;
      border: 2px solid #c9933b;
      border-radius: 4px;
      background: #110c07;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 0 8px rgba(0,0,0,0.8);
    }
    .portrait-canvas {
      width: 100%;
      height: 100%;
    }

    .entity-titles {
      flex: 1;
    }
    .entity-name {
      font-size: 15px;
      font-weight: 800;
      color: #ffd700;
      text-shadow: 1px 1px 2px #000;
      margin-bottom: 2px;
    }
    .entity-type {
      font-size: 11px;
      color: #bfa889;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .hp-bar-outer {
      width: 100%;
      height: 8px;
      background: #2b1111;
      border: 1px solid #5a3e20;
      border-radius: 3px;
      margin-top: 6px;
      overflow: hidden;
    }
    .hp-bar-inner {
      height: 100%;
      width: 100%;
      background: #22c55e;
      transition: width 0.2s ease;
    }

    .entity-stats {
      font-size: 11px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px 8px;
      color: #d1c0a5;
      background: #1f140b;
      padding: 6px 8px;
      border: 1px solid #3d2816;
      border-radius: 4px;
      margin-top: 6px;
    }
    .stat-val {
      font-weight: 700;
      color: #fef08a;
    }

    /* CENTER SECTION: 3x5 Action & Command Grid */
    .console-center {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 10px 14px;
      border-right: 2px solid #5a3e20;
      position: relative;
    }

    .action-grid-tabs {
      display: flex;
      gap: 6px;
      margin-bottom: 8px;
    }
    .grid-tab-btn {
      background: #28190d;
      border: 1px solid #634320;
      border-radius: 4px;
      padding: 3px 10px;
      font-size: 10px;
      font-weight: 800;
      color: #cbb292;
      cursor: pointer;
    }
    .grid-tab-btn.active {
      background: #5a3b1a;
      border-color: #ffd700;
      color: #ffd700;
    }

    .action-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 6px;
      height: 116px;
    }

    .action-btn {
      background: linear-gradient(180deg, #3d2716 0%, #201309 100%);
      border: 1.5px solid #7c5828;
      border-radius: 4px;
      color: #f3eedf;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 4px;
      font-size: 10px;
      font-weight: 700;
      text-align: center;
      transition: all 0.12s;
      position: relative;
    }
    .action-btn:hover:not(:disabled) {
      background: linear-gradient(180deg, #593920 0%, #352010 100%);
      border-color: #ffd700;
      transform: translateY(-1px);
      box-shadow: 0 3px 8px rgba(0,0,0,0.6);
    }
    .action-btn:active:not(:disabled) {
      transform: translateY(1px);
    }
    .action-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      filter: grayscale(80%);
    }
    .btn-hotkey {
      position: absolute;
      top: 2px;
      right: 3px;
      font-size: 8px;
      color: #d97706;
      font-weight: 900;
    }
    .btn-name {
      font-size: 10px;
      font-weight: 800;
      color: #ffd700;
      margin-top: 2px;
    }
    .btn-cost {
      font-size: 9px;
      color: #d1c0a5;
      margin-top: 1px;
    }

    /* Training Queue Bar */
    .train-queue-bar {
      position: absolute;
      bottom: 6px;
      left: 14px;
      right: 14px;
      height: 18px;
      background: #180e07;
      border: 1px solid #5a3e20;
      border-radius: 3px;
      display: flex;
      align-items: center;
      padding: 0 4px;
      gap: 6px;
    }
    .queue-fill {
      height: 10px;
      background: #2563eb;
      border-radius: 2px;
      transition: width 0.1s linear;
    }
    .queue-slots {
      display: flex;
      gap: 4px;
      font-size: 9px;
      color: #fef08a;
      font-weight: 700;
    }

    /* RIGHT SECTION: RTS Radar Minimap */
    .console-right {
      width: 220px;
      min-width: 220px;
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

    /* 3D FLOATING HOVER TOOLTIP */
    #hover-tooltip {
      position: absolute;
      pointer-events: none;
      background: rgba(22, 14, 8, 0.92);
      border: 1.5px solid #d4af37;
      border-radius: 6px;
      padding: 8px 12px;
      color: #fbf5e6;
      font-size: 11px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.8);
      z-index: 1000;
      display: none;
      transform: translate(-50%, -125%);
      backdrop-filter: blur(4px);
    }
    .tip-title {
      font-size: 13px;
      font-weight: 800;
      color: #ffd700;
      margin-bottom: 2px;
    }
    .tip-sub {
      color: #d1c0a5;
      font-size: 10px;
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
      padding: 3px 9px;
      cursor: pointer;
      border-radius: 4px;
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
