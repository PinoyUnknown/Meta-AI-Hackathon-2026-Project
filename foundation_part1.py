part1 = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FOUNDATION: ORGANIC SETTLEMENT SIMULATOR</title>
  <style>
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
      background: #87ceeb;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      color: #2c2416;
    }
    #canvas-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    /* Top Medieval Resource & Realm Ledger */
    #hud {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 10;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px 20px;
    }

    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      pointer-events: auto;
    }

    .town-plate {
      background: #2b1f14;
      border: 2px solid #c9933b;
      border-radius: 8px;
      padding: 8px 18px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
      display: flex;
      flex-direction: column;
    }
    .town-title {
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 1.2px;
      color: #f7e6b5;
      text-transform: uppercase;
      font-family: Georgia, serif;
    }
    .town-sub {
      font-size: 10px;
      color: #d1b88c;
      letter-spacing: 0.8px;
      font-weight: 600;
    }

    .resource-ledger {
      display: flex;
      gap: 14px;
      background: rgba(254, 249, 235, 0.96);
      border: 2px solid #8c6838;
      border-radius: 10px;
      padding: 8px 18px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .res-item {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 13px;
      font-weight: 700;
      color: #3d2c1d;
    }
    .res-tag {
      font-size: 10px;
      font-weight: 800;
      color: #8c6838;
      background: #f1e4ce;
      padding: 2px 5px;
      border-radius: 4px;
    }

    .pop-badge {
      display: flex;
      gap: 12px;
      background: #2b1f14;
      border: 2px solid #c9933b;
      border-radius: 8px;
      padding: 8px 16px;
      color: #f7e6b5;
      font-size: 12px;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    }

    /* Left Quest & Estate Dispatch Card */
    .quest-card {
      position: absolute;
      top: 75px;
      left: 20px;
      width: 290px;
      background: rgba(253, 248, 235, 0.96);
      border: 2px solid #8c6838;
      border-radius: 10px;
      padding: 14px 16px;
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
      pointer-events: auto;
      font-family: Georgia, serif;
    }
    .quest-tag {
      font-size: 10px;
      font-weight: 800;
      color: #8c6838;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .quest-title {
      font-size: 14px;
      font-weight: 800;
      color: #4a3420;
      margin-bottom: 6px;
    }
    .quest-desc {
      font-size: 11px;
      color: #5c4530;
      line-height: 1.45;
      font-family: 'Segoe UI', sans-serif;
      margin-bottom: 8px;
    }
    .quest-progress {
      font-size: 11px;
      font-weight: 700;
      color: #15803d;
      font-family: monospace;
    }

    /* Bottom Building Placement Dock (Foundation Gridless Builder) */
    .dock-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      width: 100%;
      pointer-events: auto;
    }
    .building-dock {
      display: flex;
      gap: 8px;
      background: rgba(43, 31, 20, 0.96);
      border: 2px solid #c9933b;
      border-radius: 12px;
      padding: 8px 12px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
      max-width: 95vw;
      overflow-x: auto;
    }
    .b-btn {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      background: #4a3420;
      border: 1px solid #8c6838;
      border-radius: 8px;
      padding: 8px 12px;
      min-width: 86px;
      cursor: pointer;
      color: #f7e6b5;
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .b-btn:hover {
      background: #6b4c30;
      border-color: #f3c262;
      transform: translateY(-2px);
    }
    .b-btn.active {
      background: #855d38;
      border-color: #ffd875;
      box-shadow: 0 0 12px #ffd875;
      transform: translateY(-3px);
    }
    .b-tag {
      font-size: 9px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #d1b88c;
    }
    .b-name {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .b-cost {
      font-size: 9px;
      color: #e5c287;
    }

    .controls-hint {
      background: rgba(254, 249, 235, 0.92);
      border: 1px solid #8c6838;
      border-radius: 6px;
      padding: 4px 14px;
      font-size: 11px;
      color: #4a3420;
      font-weight: 600;
      display: flex;
      gap: 12px;
    }
    .controls-hint kbd {
      background: #2b1f14;
      color: #f7e6b5;
      padding: 1px 5px;
      border-radius: 3px;
      font-family: monospace;
      font-size: 10px;
    }

    /* Villager & Building Inspector Cards */
    #inspector-card {
      position: absolute;
      bottom: 120px;
      right: 20px;
      width: 270px;
      background: rgba(253, 248, 235, 0.96);
      border: 2px solid #8c6838;
      border-radius: 10px;
      padding: 14px 16px;
      box-shadow: 0 6px 25px rgba(0, 0, 0, 0.35);
      display: none;
      pointer-events: auto;
      font-family: Georgia, serif;
    }
    .insp-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #c9933b;
      padding-bottom: 6px;
      margin-bottom: 8px;
    }
    .insp-title {
      font-size: 14px;
      font-weight: 800;
      color: #4a3420;
    }
    .insp-close {
      background: none;
      border: none;
      font-size: 14px;
      font-weight: bold;
      color: #8c6838;
      cursor: pointer;
    }
    .insp-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      margin-bottom: 4px;
      color: #5c4530;
      font-family: 'Segoe UI', sans-serif;
    }
    .insp-val {
      font-weight: 700;
      color: #2c2416;
    }

    /* Settings & Pause Modal (ESC Key) */
    #settings-modal {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(8px);
      z-index: 100;
      display: none;
      justify-content: center;
      align-items: center;
    }
    .modal-box {
      width: 90%;
      max-width: 620px;
      background: #fdfaf2;
      border: 3px solid #8c6838;
      border-radius: 12px;
      box-shadow: 0 10px 45px rgba(0, 0, 0, 0.6);
      padding: 24px 28px;
      color: #3b2818;
    }
    .modal-title {
      font-size: 18px;
      font-weight: 800;
      font-family: Georgia, serif;
      color: #5c3818;
      border-bottom: 2px solid #c9933b;
      padding-bottom: 8px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .settings-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      font-size: 13px;
      font-weight: 600;
    }
    .settings-row input[type="range"] {
      width: 180px;
      accent-color: #c9933b;
    }
    .settings-row select {
      background: #f4ede0;
      border: 1px solid #8c6838;
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 12px;
      color: #3b2818;
    }
    .btn-action {
      background: #855d38;
      border: 1px solid #c9933b;
      border-radius: 6px;
      color: #f7e6b5;
      padding: 8px 18px;
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-action:hover {
      background: #a07248;
      border-color: #ffd875;
    }
  </style>
</head>
"""
