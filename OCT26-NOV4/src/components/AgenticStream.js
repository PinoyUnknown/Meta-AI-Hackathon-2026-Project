// Multi-Agent Chain-of-Thought Stream Component
import { metaModelService } from '../services/metaModelApi.js';

export class AgenticStream {
  constructor(containerElement, onCodeGenerated) {
    this.container = containerElement;
    this.onCodeGenerated = onCodeGenerated;
    this.steps = [];
    this.isRunning = false;
  }

  async runReasoning(domainId, target) {
    if (this.isRunning) return;
    this.isRunning = true;
    this.steps = [];
    this.render();

    try {
      for await (const step of metaModelService.streamMultiAgentReasoning(domainId, target)) {
        this.steps.push(step);
        this.render();

        if (step.code && this.onCodeGenerated) {
          this.onCodeGenerated(step.code);
        }
      }
    } finally {
      this.isRunning = false;
      this.render();
    }
  }

  render() {
    if (this.steps.length === 0) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 2.5rem 1rem; color: #64748b;">
          <div style="font-size: 0.95rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;">Agentic Reasoning Pipeline</div>
          <p style="font-size: 0.82rem; font-weight: 500;">Select a region or click on the vision canvas above to initiate the Meta AI Multi-Agent reasoning chain.</p>
          <p style="font-size: 0.72rem; margin-top: 0.4rem; color: #475569; font-family: var(--font-mono);">SAM 3.1 &bull; Llama 3.2 Vision &bull; Llama 3.3 &bull; Muse Code</p>
        </div>
      `;
      return;
    }

    let html = `<div class="agent-stream-container">`;

    this.steps.forEach((step, idx) => {
      const isLatest = idx === this.steps.length - 1 && this.isRunning;
      const metaEntries = step.telemetry ? Object.entries(step.telemetry) : [];

      html += `
        <div class="agent-step-card ${isLatest ? 'active-agent' : ''}">
          <div class="agent-header">
            <div class="agent-name">
              <span>${step.agent}</span>
              <span class="agent-model-tag">${step.model}</span>
            </div>
            <span style="font-size: 0.68rem; color: ${isLatest ? 'var(--neon-cyan)' : '#10b981'}; font-family: var(--font-mono); font-weight: 600;">
              ${isLatest ? 'ACTIVE' : 'VERIFIED'}
            </span>
          </div>

          <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 0.45rem; font-weight: 500;">
            Role: ${step.role}
          </div>

          <div class="agent-thought">
            ${step.thought.replace(/\n/g, '<br/>')}
          </div>

          ${metaEntries.length > 0 ? `
            <div class="agent-meta-grid">
              ${metaEntries.map(([k, v]) => `
                <div class="agent-meta-item">
                  <span class="agent-meta-key">${k}</span>
                  <span class="agent-meta-val">${v}</span>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${step.code ? `
            <div style="margin-top: 0.5rem; display: flex; justify-content: flex-end;">
              <span style="font-size: 0.7rem; color: var(--neon-cyan); font-family: var(--font-mono);">
                Simulation Script Synthesized &amp; Loaded
              </span>
            </div>
          ` : ''}
        </div>
      `;
    });

    if (this.isRunning) {
      html += `
        <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; font-size: 0.75rem; color: var(--neon-cyan); font-family: var(--font-mono);">
          <div class="status-dot"></div>
          Next Agent Synthesizing Physical Hypothesis...
        </div>
      `;
    }

    html += `</div>`;
    this.container.innerHTML = html;

    // Scroll to bottom
    const streamBox = this.container.querySelector('.agent-stream-container');
    if (streamBox) {
      streamBox.scrollTop = streamBox.scrollHeight;
    }
  }
}
