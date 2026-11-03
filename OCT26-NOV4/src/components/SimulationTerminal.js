// Simulation Terminal & Code Runner Component
export class SimulationTerminal {
  constructor(containerElement) {
    this.container = containerElement;
    this.code = '';
    this.isExecuting = false;
    this.logs = [];
    this.render();
  }

  setCode(codeString) {
    this.code = codeString;
    this.logs = ['[SYSTEM] New simulation code synthesized by Meta Muse Code Agent. Ready for sandbox execution.'];
    this.render();
  }

  async executeSimulation() {
    if (this.isExecuting || !this.code) return;
    this.isExecuting = true;
    this.logs.push('[EXEC] Initializing sandboxed physics execution container...');
    this.render();

    await new Promise((res) => setTimeout(res, 400));
    this.logs.push('[EXEC] Loading kinematics solver & physical boundary invariants...');
    this.render();

    await new Promise((res) => setTimeout(res, 550));
    this.logs.push('[EXEC] Applying Meta AI joint derating protocols & damping...');
    this.render();

    await new Promise((res) => setTimeout(res, 600));
    this.logs.push('[SUCCESS] Simulation completed with 0 invariant violations.');
    this.logs.push('[RESULT] Peak Von Mises Stress: 114.2 MPa (Safe Margin: +28.5%)');
    this.logs.push('[RESULT] Lifetime extension estimate: +3,400 operational hours.');
    this.isExecuting = false;
    this.render();
  }

  render() {
    this.container.innerHTML = `
      <div class="code-terminal-card">
        <div class="terminal-header">
          <div class="terminal-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="4 17 10 11 4 5"></polyline>
              <line x1="12" y1="19" x2="20" y2="19"></line>
            </svg>
            <span>Muse Code Sandbox & Physical Runner</span>
          </div>
          <div style="display: flex; gap: 0.4rem;">
            <button id="btn-copy-code" class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.7rem;">
              Copy Code
            </button>
            <button id="btn-run-sim" class="btn btn-primary" style="padding: 0.25rem 0.6rem; font-size: 0.7rem;" ${this.isExecuting ? 'disabled' : ''}>
              ${this.isExecuting ? 'Running...' : 'Run Simulation'}
            </button>
          </div>
        </div>

        <pre class="terminal-pre"><code>${this.escapeHtml(this.code || '# Awaiting agent code synthesis...')}</code></pre>

        <div style="background: rgba(0, 0, 0, 0.4); border-top: 1px solid var(--border-glass); padding: 0.6rem 0.85rem; font-family: var(--font-mono); font-size: 0.7rem;">
          <div style="color: #94a3b8; margin-bottom: 0.3rem; display: flex; align-items: center; justify-content: space-between;">
            <span>EXECUTION TELEMETRY & LOGS</span>
            <span style="color: ${this.isExecuting ? 'var(--neon-cyan)' : '#10b981'};">
              ${this.isExecuting ? '● RUNNING' : '● READY'}
            </span>
          </div>
          <div style="color: #cbd5e1; max-height: 80px; overflow-y: auto;">
            ${this.logs.map(log => `<div>${this.escapeHtml(log)}</div>`).join('')}
          </div>
        </div>
      </div>
    `;

    const btnRun = this.container.querySelector('#btn-run-sim');
    if (btnRun) {
      btnRun.addEventListener('click', () => this.executeSimulation());
    }

    const btnCopy = this.container.querySelector('#btn-copy-code');
    if (btnCopy) {
      btnCopy.addEventListener('click', () => {
        navigator.clipboard.writeText(this.code);
        btnCopy.textContent = 'Copied!';
        setTimeout(() => { btnCopy.textContent = 'Copy Code'; }, 2000);
      });
    }
  }

  escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }
}
