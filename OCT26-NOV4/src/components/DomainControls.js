// Domain Controls & Educational Segmentation Helper Component
export class DomainControls {
  constructor(containerElement, onParamChanged) {
    this.container = containerElement;
    this.onParamChanged = onParamChanged;
    this.currentDomainId = 'robotics';
    this.currentStepText = 'Ready: Click on the image to place a Point Prompt (X, Y) or drag a Bounding Box.';

    // Default domain state
    this.state = {
      robotics: { j1: 0, j2: 0, derating: 12 },
      biomedical: { confluence: 74, phase: 'Prometaphase', channel: 'GFP' },
      energy: { irradiance: 850, temp: 84.6, bypassActive: false },
      microelectronics: { node: '7nm', thickness: 4.2, vdd: 0.75 }
    };

    this.render();
  }

  setDomain(domainId) {
    this.currentDomainId = domainId;
    this.render();
  }

  updateStepStatus(text) {
    this.currentStepText = text;
    const tracker = this.container.querySelector('#sam-step-text');
    if (tracker) {
      tracker.textContent = text;
    }
  }

  render() {
    const domainId = this.currentDomainId;

    let controlsHtml = '';

    if (domainId === 'robotics') {
      const { j1, j2, derating } = this.state.robotics;
      controlsHtml = `
        <div class="cad-slider-grid">
          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Joint 1 Turret Rotation</span>
              <span id="val-j1" class="cad-value-badge">${j1}°</span>
            </div>
            <input type="range" id="slider-j1" class="cad-slider" min="-90" max="90" value="${j1}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Joint 2 Shoulder Angle</span>
              <span id="val-j2" class="cad-value-badge">${j2}°</span>
            </div>
            <input type="range" id="slider-j2" class="cad-slider" min="-45" max="45" value="${j2}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Harmonic Drive Derating</span>
              <span id="val-derating" class="cad-value-badge">${derating}%</span>
            </div>
            <input type="range" id="slider-derating" class="cad-slider" min="5" max="40" value="${derating}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Kinematic Feedback</span>
              <span class="cad-value-badge" style="color: #10b981;">STABLE</span>
            </div>
            <div style="font-size: 0.65rem; color: #94a3b8; font-family: var(--font-mono); margin-top: 2px;">
              Von Mises: 114.2 MPa | Margin: +28.5%
            </div>
          </div>
        </div>
      `;
    } else if (domainId === 'biomedical') {
      const { confluence, phase, channel } = this.state.biomedical;
      controlsHtml = `
        <div class="cad-slider-grid">
          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Colony Confluence</span>
              <span id="val-confluence" class="cad-value-badge">${confluence}%</span>
            </div>
            <input type="range" id="slider-confluence" class="cad-slider" min="20" max="95" value="${confluence}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Fluorescence Channel</span>
              <span id="val-channel" class="cad-value-badge">${channel}</span>
            </div>
            <select id="select-channel" class="input-field" style="padding: 0.2rem 0.4rem; font-size: 0.7rem;">
              <option value="GFP" ${channel === 'GFP' ? 'selected' : ''}>GFP-Tubulin (Cytoskeleton)</option>
              <option value="DAPI" ${channel === 'DAPI' ? 'selected' : ''}>DAPI (Nuclear DNA)</option>
              <option value="Cy5" ${channel === 'Cy5' ? 'selected' : ''}>Cy5 (Mitotic Actin)</option>
            </select>
          </div>
        </div>
      `;
    } else if (domainId === 'energy') {
      const { irradiance, temp } = this.state.energy;
      controlsHtml = `
        <div class="cad-slider-grid">
          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Solar Irradiance</span>
              <span id="val-irradiance" class="cad-value-badge">${irradiance} W/m²</span>
            </div>
            <input type="range" id="slider-irradiance" class="cad-slider" min="200" max="1100" value="${irradiance}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Hotspot Core Temp</span>
              <span id="val-temp" class="cad-value-badge" style="color: #f59e0b;">${temp} °C</span>
            </div>
            <input type="range" id="slider-temp" class="cad-slider" min="35" max="95" value="${temp}" />
          </div>
        </div>
      `;
    } else if (domainId === 'microelectronics') {
      const { thickness, vdd } = this.state.microelectronics;
      controlsHtml = `
        <div class="cad-slider-grid">
          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Gate Dielectric Thickness</span>
              <span id="val-thickness" class="cad-value-badge">${thickness} nm</span>
            </div>
            <input type="range" id="slider-thickness" class="cad-slider" min="1.5" max="8.0" step="0.1" value="${thickness}" />
          </div>

          <div class="cad-slider-row">
            <div class="cad-slider-meta">
              <span class="cad-slider-label">Operating Voltage (Vdd)</span>
              <span id="val-vdd" class="cad-value-badge">${vdd} V</span>
            </div>
            <input type="range" id="slider-vdd" class="cad-slider" min="0.5" max="1.2" step="0.05" value="${vdd}" />
          </div>
        </div>
      `;
    }

    this.container.innerHTML = `
      <!-- Educational Explanation Card: What is happening under the hood? -->
      <div class="sam-guide-card">
        <div class="sam-guide-header">
          <span class="sam-guide-title">Spatial Segmentation &amp; Physical Twin Guide</span>
          <span class="hud-badge" style="font-size: 0.65rem; border-color: rgba(255,255,255,0.15);">META SAM 3.1 PIPELINE</span>
        </div>

        <div class="sam-step-tracker">
          <div class="status-dot"></div>
          <span id="sam-step-text">${this.currentStepText}</span>
        </div>

        <div class="sam-explanation-grid">
          <div class="sam-pill-help">
            <div class="sam-pill-title">Point Prompt</div>
            <div class="sam-pill-desc">
              Places a positive coordinate (X,Y) directly on a feature. SAM encodes this point into positional embeddings, evaluating cross-attention to isolate the discrete physical component.
            </div>
          </div>

          <div class="sam-pill-help">
            <div class="sam-pill-title">Bounding Box</div>
            <div class="sam-pill-desc">
              Draws a spatial constraint rectangle [X1, Y1, X2, Y2]. Constrains SAM's mask decoder strictly inside the box to segment bounded features without surrounding clutter.
            </div>
          </div>

          <div class="sam-pill-help">
            <div class="sam-pill-title">Why Segmentation?</div>
            <div class="sam-pill-desc">
              LLMs cannot compute stress from raw pixels alone. SAM isolates the exact physical boundaries, allowing Llama 3.2 to calculate true surface area, fatigue, and 3D digital-twin coordinates.
            </div>
          </div>
        </div>
      </div>

      <!-- Domain Interactive Parameters Inspector -->
      <div class="cad-panel">
        <div class="cad-panel-header">
          <div class="cad-panel-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="4" y1="21" x2="4" y2="14"></line>
              <line x1="4" y1="10" x2="4" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12" y2="3"></line>
              <line x1="20" y1="21" x2="20" y2="16"></line>
              <line x1="20" y1="12" x2="20" y2="3"></line>
            </svg>
            <span>Domain Parameter Controls (Interactive Telemetry)</span>
          </div>
          <span style="font-size: 0.65rem; color: #94a3b8; font-family: var(--font-mono);">
            Adjusting parameters updates 3D model &amp; equations live
          </span>
        </div>
        ${controlsHtml}
      </div>
    `;

    this.attachSliderListeners();
  }

  attachSliderListeners() {
    const domainId = this.currentDomainId;

    if (domainId === 'robotics') {
      const sJ1 = this.container.querySelector('#slider-j1');
      const sJ2 = this.container.querySelector('#slider-j2');
      const sDerating = this.container.querySelector('#slider-derating');

      const updateRobotics = () => {
        const j1 = parseInt(sJ1.value, 10);
        const j2 = parseInt(sJ2.value, 10);
        const derating = parseInt(sDerating.value, 10);
        this.state.robotics = { j1, j2, derating };

        this.container.querySelector('#val-j1').textContent = `${j1}°`;
        this.container.querySelector('#val-j2').textContent = `${j2}°`;
        this.container.querySelector('#val-derating').textContent = `${derating}%`;

        if (this.onParamChanged) {
          this.onParamChanged('robotics', {
            j1Rad: (j1 * Math.PI) / 180,
            j2Rad: (j2 * Math.PI) / 180,
            derating
          });
        }
      };

      if (sJ1) sJ1.addEventListener('input', updateRobotics);
      if (sJ2) sJ2.addEventListener('input', updateRobotics);
      if (sDerating) sDerating.addEventListener('input', updateRobotics);

    } else if (domainId === 'biomedical') {
      const sConf = this.container.querySelector('#slider-confluence');
      if (sConf) {
        sConf.addEventListener('input', () => {
          const conf = parseInt(sConf.value, 10);
          this.state.biomedical.confluence = conf;
          this.container.querySelector('#val-confluence').textContent = `${conf}%`;
          if (this.onParamChanged) {
            this.onParamChanged('biomedical', { confluenceScale: conf / 100 });
          }
        });
      }
    } else if (domainId === 'energy') {
      const sTemp = this.container.querySelector('#slider-temp');
      const sIrr = this.container.querySelector('#slider-irradiance');
      if (sTemp) {
        sTemp.addEventListener('input', () => {
          const t = parseFloat(sTemp.value);
          this.state.energy.temp = t;
          this.container.querySelector('#val-temp').textContent = `${t} °C`;
          if (this.onParamChanged) {
            this.onParamChanged('energy', { hotspotTemp: t });
          }
        });
      }
      if (sIrr) {
        sIrr.addEventListener('input', () => {
          const irr = parseInt(sIrr.value, 10);
          this.state.energy.irradiance = irr;
          this.container.querySelector('#val-irradiance').textContent = `${irr} W/m²`;
        });
      }
    } else if (domainId === 'microelectronics') {
      const sThick = this.container.querySelector('#slider-thickness');
      const sVdd = this.container.querySelector('#slider-vdd');
      if (sThick) {
        sThick.addEventListener('input', () => {
          const nm = parseFloat(sThick.value);
          this.state.microelectronics.thickness = nm;
          this.container.querySelector('#val-thickness').textContent = `${nm} nm`;
          if (this.onParamChanged) {
            this.onParamChanged('microelectronics', { thicknessNm: nm });
          }
        });
      }
      if (sVdd) {
        sVdd.addEventListener('input', () => {
          const v = parseFloat(sVdd.value);
          this.state.microelectronics.vdd = v;
          this.container.querySelector('#val-vdd').textContent = `${v} V`;
        });
      }
    }
  }
}
