// API & Runtime Configuration Modal
import { metaModelService } from '../services/metaModelApi.js';

export class SettingsModal {
  constructor(onSaved) {
    this.onSaved = onSaved;
    this.modalElement = null;
  }

  show() {
    if (this.modalElement) this.close();

    const currentKey = metaModelService.apiKey;
    const currentEndpoint = metaModelService.endpointUrl;

    this.modalElement = document.createElement('div');
    this.modalElement.className = 'modal-backdrop';
    this.modalElement.innerHTML = `
      <div class="modal-content" style="max-width: 560px;">
        <div class="modal-header">
          <h3 class="modal-title">Meta Model API &amp; Runtime Settings</h3>
          <button class="close-btn" id="settings-close">&times;</button>
        </div>

        <div class="modal-body">
          <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5;">
            Configure your Meta Model API credentials or use the built-in deterministic Neural Simulation mode for zero-configuration hackathon offline presentations.
          </p>

          <div>
            <label style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--neon-cyan); display: block; margin-bottom: 0.4rem;">
              META MODEL API KEY / BEARER TOKEN
            </label>
            <input type="password" id="input-api-key" class="input-field" placeholder="sk-meta-... or Llama token" value="${currentKey}" />
            <span style="font-size: 0.68rem; color: #64748b; margin-top: 0.25rem; display: block;">
              Leave blank to run in offline high-precision Neural Simulation mode.
            </span>
          </div>

          <div>
            <label style="font-size: 0.75rem; font-family: var(--font-mono); color: #cbd5e1; display: block; margin-bottom: 0.4rem;">
              BACKEND ENGINE URL (FASTAPI / LOCALHOST)
            </label>
            <input type="text" id="input-endpoint" class="input-field" placeholder="http://localhost:8000" value="${currentEndpoint}" />
          </div>

          <div style="background: rgba(14, 22, 40, 0.5); border: 1px solid var(--border-glass); border-radius: 8px; padding: 0.75rem;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.25rem;">Active Model Matrix:</div>
            <div style="font-size: 0.7rem; color: #94a3b8; font-family: var(--font-mono); line-height: 1.6;">
              • Vision &amp; Spatial: <code>meta-ai/SAM-3.1-Segment-Anything</code><br/>
              • Multimodal Inspection: <code>meta-llama/Llama-3.2-90B-Vision-Instruct</code><br/>
              • Physical Reasoning: <code>meta-llama/Llama-3.3-70B-Instruct</code><br/>
              • Agentic Code Generation: <code>meta-ai/Muse-Code-Synthesizer</code>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button id="btn-cancel-settings" class="btn btn-secondary">Cancel</button>
          <button id="btn-save-settings" class="btn btn-primary">Save Configuration</button>
        </div>
      </div>
    `;

    document.body.appendChild(this.modalElement);

    this.modalElement.querySelector('#settings-close').addEventListener('click', () => this.close());
    this.modalElement.querySelector('#btn-cancel-settings').addEventListener('click', () => this.close());

    this.modalElement.querySelector('#btn-save-settings').addEventListener('click', () => {
      const newKey = this.modalElement.querySelector('#input-api-key').value.trim();
      const newEndpoint = this.modalElement.querySelector('#input-endpoint').value.trim();
      metaModelService.setApiKey(newKey);
      metaModelService.setEndpointUrl(newEndpoint);
      if (this.onSaved) this.onSaved();
      this.close();
    });
  }

  close() {
    if (this.modalElement && this.modalElement.parentNode) {
      this.modalElement.parentNode.removeChild(this.modalElement);
      this.modalElement = null;
    }
  }
}
