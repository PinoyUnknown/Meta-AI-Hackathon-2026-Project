// Blender CAD Studio Viewport Toolbar Component
export class StudioToolbar3D {
  constructor(mountElement, digitalTwin) {
    this.mount = mountElement;
    this.digitalTwin = digitalTwin;
    this.isMaximized = false;
    this.activeAngle = 'iso';
    this.activeShading = 'clay';
    this.activeLighting = 'studio';

    this.render();
  }

  render() {
    this.mount.innerHTML = `
      <div class="cad-viewport-toolbar">
        <!-- Row 1: Camera Navigation & Orbit Controls -->
        <div class="cad-toolbar-row">
          <div class="cad-tool-group">
            <span class="cad-group-label">Camera Angle:</span>
            <div class="cad-button-pills">
              <button class="cad-pill-btn ${this.activeAngle === 'front' ? 'active' : ''}" data-angle="front" title="Front View [NumPad 1]">
                <span>Front [1]</span>
              </button>
              <button class="cad-pill-btn ${this.activeAngle === 'side' ? 'active' : ''}" data-angle="side" title="Side View [NumPad 3]">
                <span>Side [3]</span>
              </button>
              <button class="cad-pill-btn ${this.activeAngle === 'top' ? 'active' : ''}" data-angle="top" title="Top View [NumPad 7]">
                <span>Top [7]</span>
              </button>
              <button class="cad-pill-btn ${this.activeAngle === 'iso' ? 'active' : ''}" data-angle="iso" title="Isometric Perspective [NumPad 5]">
                <span>Isometric [5]</span>
              </button>
            </div>
          </div>

          <div class="cad-tool-group">
            <button id="btn-cad-focus" class="studio-tool-btn" title="Center camera and fit 3D model in view [NumPad .]">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="7"></circle>
                <line x1="12" y1="2" x2="12" y2="5"></line>
                <line x1="12" y1="19" x2="12" y2="22"></line>
                <line x1="2" y1="12" x2="5" y2="12"></line>
                <line x1="19" y1="12" x2="22" y2="12"></line>
              </svg>
              <span>Fit / Focus</span>
            </button>

            <button id="btn-cad-rotate" class="studio-tool-btn ${this.digitalTwin.isRotating ? 'active' : ''}" title="Toggle turntable 360-degree auto-rotation">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"></polyline>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
              </svg>
              <span id="label-cad-rotate">Turntable: ${this.digitalTwin.isRotating ? 'On' : 'Off'}</span>
            </button>

            <button id="btn-cad-grid" class="studio-tool-btn active" title="Toggle floor workbench grid &amp; axes">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="3" y1="15" x2="21" y2="15"></line>
                <line x1="9" y1="3" x2="9" y2="21"></line>
                <line x1="15" y1="3" x2="15" y2="21"></line>
              </svg>
              <span id="label-cad-grid">Grid: On</span>
            </button>

            <button id="btn-cad-max" class="studio-tool-btn" title="Toggle cinema enlarged 3D viewport">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 3 21 3 21 9"></polyline>
                <polyline points="9 21 3 21 3 15"></polyline>
                <line x1="21" y1="3" x2="14" y2="10"></line>
                <line x1="3" y1="21" x2="10" y2="14"></line>
              </svg>
              <span id="label-cad-max">Enlarge View</span>
            </button>
          </div>
        </div>

        <!-- Row 2: Shading Modes & Studio Lighting -->
        <div class="cad-toolbar-row" style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 0.5rem;">
          <div class="cad-tool-group">
            <span class="cad-group-label">Shading:</span>
            <div class="cad-button-pills">
              <button class="cad-pill-btn ${this.activeShading === 'pbr' ? 'active' : ''}" data-shading="textured" title="Realistic PBR Shading">
                <span>PBR Realistic</span>
              </button>
              <button class="cad-pill-btn ${this.activeShading === 'clay' ? 'active' : ''}" data-shading="clay" title="Blender Matcap Clay Sculpt">
                <span>Clay Matcap</span>
              </button>
              <button class="cad-pill-btn ${this.activeShading === 'wireframe' ? 'active' : ''}" data-shading="wireframe" title="Inspect Quad Topology">
                <span>Wireframe</span>
              </button>
              <button class="cad-pill-btn ${this.activeShading === 'normal' ? 'active' : ''}" data-shading="normal" title="Inspect Face Normals">
                <span>Normal Maps</span>
              </button>
              <button class="cad-pill-btn ${this.activeShading === 'cyber' ? 'active' : ''}" data-shading="cyber" title="Holographic Cyber Glow">
                <span>Cyber Glow</span>
              </button>
            </div>
          </div>

          <div class="cad-tool-group">
            <span class="cad-group-label">Lighting:</span>
            <div class="cad-button-pills">
              <button class="cad-pill-btn ${this.activeLighting === 'studio' ? 'active' : ''}" data-light="studio">
                <span>Studio Neutral</span>
              </button>
              <button class="cad-pill-btn ${this.activeLighting === 'cyberpunk' ? 'active' : ''}" data-light="cyberpunk">
                <span>Cyberpunk</span>
              </button>
              <button class="cad-pill-btn ${this.activeLighting === 'sunset' ? 'active' : ''}" data-light="sunset">
                <span>Warm Sunset</span>
              </button>
              <button class="cad-pill-btn ${this.activeLighting === 'key' ? 'active' : ''}" data-light="key">
                <span>High Key</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  attachEventListeners() {
    // Camera angle pills
    const angleBtns = this.mount.querySelectorAll('[data-angle]');
    angleBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        angleBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const angle = btn.getAttribute('data-angle');
        this.activeAngle = angle;
        this.digitalTwin.setCameraAngle(angle);
      });
    });

    // Shading pills
    const shadingBtns = this.mount.querySelectorAll('[data-shading]');
    shadingBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        shadingBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const shading = btn.getAttribute('data-shading');
        this.activeShading = shading;
        if (shading === 'wireframe') {
          this.digitalTwin.setMaterialProperties({ wireframe: true });
        } else {
          this.digitalTwin.setMaterialProperties({ wireframe: false });
          this.digitalTwin.setMaterialPreset(shading);
        }
      });
    });

    // Lighting pills
    const lightBtns = this.mount.querySelectorAll('[data-light]');
    lightBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        lightBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const light = btn.getAttribute('data-light');
        this.activeLighting = light;
        this.digitalTwin.setLightingPreset(light);
      });
    });

    // Focus
    const btnFocus = this.mount.querySelector('#btn-cad-focus');
    if (btnFocus) {
      btnFocus.addEventListener('click', () => {
        this.digitalTwin.focusCameraOnModel();
      });
    }

    // Auto rotate
    const btnRotate = this.mount.querySelector('#btn-cad-rotate');
    const labelRotate = this.mount.querySelector('#label-cad-rotate');
    if (btnRotate) {
      btnRotate.addEventListener('click', () => {
        const rotating = this.digitalTwin.toggleAutoRotate();
        btnRotate.classList.toggle('active', rotating);
        if (labelRotate) labelRotate.textContent = `Turntable: ${rotating ? 'On' : 'Off'}`;
      });
    }

    // Grid toggle
    const btnGrid = this.mount.querySelector('#btn-cad-grid');
    const labelGrid = this.mount.querySelector('#label-cad-grid');
    if (btnGrid) {
      btnGrid.addEventListener('click', () => {
        const visible = this.digitalTwin.toggleGrid();
        btnGrid.classList.toggle('active', visible);
        if (labelGrid) labelGrid.textContent = `Grid: ${visible ? 'On' : 'Off'}`;
      });
    }

    // Maximize Viewport
    const btnMax = this.mount.querySelector('#btn-cad-max');
    const labelMax = this.mount.querySelector('#label-cad-max');
    if (btnMax) {
      btnMax.addEventListener('click', () => {
        this.isMaximized = !this.isMaximized;
        const container = document.getElementById('three-container');
        if (container) {
          container.classList.toggle('maximized-viewport', this.isMaximized);
          setTimeout(() => {
            this.digitalTwin.handleResize();
            this.digitalTwin.focusCameraOnModel();
          }, 150);
        }
        btnMax.classList.toggle('active', this.isMaximized);
        if (labelMax) labelMax.textContent = this.isMaximized ? 'Standard View' : 'Enlarge View';
      });
    }
  }
}
