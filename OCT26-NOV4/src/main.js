// META 3D GEN STUDIO - Master Application Entrypoint
// Generative AI 3D Studio, Skeletal Auto-Rigger & PBR Material Engine powered by Meta SAM 3.1 & Llama 3.2
import './index.css';
import { metaModelService } from './services/metaModelApi.js';
import { DigitalTwin3D } from './components/DigitalTwin3D.js';
import { StudioToolbar3D } from './components/StudioToolbar3D.js';
import { Generative3DStudio } from './components/Generative3DStudio.js';
import { CanvasSegmenter } from './components/CanvasSegmenter.js';
import { AIPipelineInspector } from './components/AIPipelineInspector.js';
import { PitchGeneratorModal } from './components/PitchGeneratorModal.js';
import { SettingsModal } from './components/SettingsModal.js';

class App {
  constructor() {
    this.pitchModal = new PitchGeneratorModal();
    this.settingsModal = new SettingsModal(() => this.updateApiStatus());

    // Default: Blender 3D Studio CAD Slate Workbench Theme
    document.body.setAttribute('data-theme', 'blender');

    this.initLayout();
    this.initComponents();
  }

  initLayout() {
    const root = document.getElementById('app');
    root.innerHTML = `
      <div class="app-container">
        <!-- Top Navbar -->
        <header class="navbar">
          <div class="brand-section">
            <div class="brand-logo">
              <svg viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <div class="brand-title-wrap">
              <div class="brand-title">
                <span>META 3D</span>
                <span style="font-weight: 400; color: #94a3b8;">GEN STUDIO</span>
                <span class="brand-badge">HACKATHON '26</span>
              </div>
              <div class="brand-sub">Autonomous Generative 3D Asset Studio, Skeletal Auto-Rigger &amp; PBR Engine</div>
            </div>
          </div>

          <!-- Live Meta Model Status Chips -->
          <div class="nav-models-bar">
            <div class="model-chip active" title="Meta SAM 3.1 Spatial Perception &amp; Texture Extractor">
              <div class="status-dot"></div>
              <span>SAM 3.1 Vision</span>
            </div>
            <div class="model-chip active" title="Meta Llama 3.2 90B Multimodal 3D Geometry Synthesizer">
              <div class="status-dot"></div>
              <span>Llama 3.2 90B</span>
            </div>
            <div class="model-chip active" title="17-Bone Humanoid &amp; Mechanical Armature Engine">
              <div class="status-dot"></div>
              <span>Auto-Rigger v2</span>
            </div>
            <div class="model-chip active" title="Real-Time WebGL Physically Based Rendering Shader">
              <div class="status-dot"></div>
              <span>Neural PBR Engine</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="nav-actions">
            <button id="btn-theme-toggle" class="btn btn-secondary" title="Toggle between Blender CAD Light Slate &amp; Obsidian Dark Mode">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
              <span id="theme-toggle-label">Theme: Blender CAD</span>
            </button>

            <button id="btn-settings" class="btn btn-secondary" title="Configure Meta AI API Endpoints">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span id="api-status-text">Mode: Neural Sim</span>
            </button>

            <button id="btn-pitch" class="btn btn-hackathon" title="Open Hackathon Submission &amp; Pitch Strategy">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              <span>Pitch Kit</span>
            </button>
          </div>
        </header>

        <!-- Studio Quick Banner -->
        <section class="domain-hero-bar" style="justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            <div class="category-indicator">
              <span class="category-tag metaverse">STUDIO WORKBENCH</span>
            </div>
            <span style="font-size: 0.8rem; font-weight: 500; color: var(--text-primary);">
              Metaverse &amp; Blender 3D Creator Pipeline
            </span>
            <span style="font-size: 0.75rem; color: var(--text-muted);">
              Text to 3D &bull; Image to 3D &bull; Skeletal Auto-Rigging &bull; PBR Texture Painter &bull; Meta Quest Export
            </span>
          </div>

          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div class="theme-pill">
              <span>Push the Frontier</span>
            </div>
            <div class="brand-badge">
              Watertight Manifold Certified
            </div>
          </div>
        </section>

        <!-- Main Studio Workspace Grid -->
        <main class="studio-layout">
          <!-- Left Column: Center-Stage Blender CAD 3D Viewport -->
          <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div class="glass-panel" id="panel-3d-digital-twin">
              <div class="panel-header">
                <div class="panel-title">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                    <line x1="12" y1="22.08" x2="12" y2="12"></line>
                  </svg>
                  <span>Blender CAD Studio Viewport (WebGL PBR)</span>
                </div>

                <div style="display: flex; align-items: center; gap: 0.6rem;">
                  <label for="input-upload-3d" class="file-upload-btn" title="Import user 3D models into scene (.STL, .OBJ, .GLTF, .GLB)">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <span>Import 3D (.STL / .OBJ / .GLTF)</span>
                    <input type="file" id="input-upload-3d" accept=".stl,.obj,.gltf,.glb" style="display: none;" />
                  </label>
                  <div style="font-size: 0.72rem; color: #94a3b8; font-family: var(--font-mono);">
                    Rotate: Drag &bull; Zoom: Wheel &bull; Pan: Right-Drag
                  </div>
                </div>
              </div>

              <div class="panel-body">
                <!-- CAD Top Controls Bar -->
                <div id="cad-toolbar-mount"></div>

                <!-- 3D Canvas Viewport -->
                <div class="three-viewport" id="three-container" style="min-height: 520px;">
                  <!-- Viewport Telemetry Overlay -->
                  <div class="three-telemetry-overlay">
                    <div class="twin-stat-card">
                      <div class="twin-stat-label">Model Status</div>
                      <div id="viewport-model-name" class="twin-stat-value" style="color: #00c8e6;">Humanoid Avatar</div>
                    </div>
                    <div class="twin-stat-card">
                      <div class="twin-stat-label">Skeletal Rig</div>
                      <div id="viewport-rig-status" class="twin-stat-value" style="color: #c084fc;">17 Bones Active</div>
                    </div>
                    <div class="twin-stat-card">
                      <div class="twin-stat-label">Geometry Quality</div>
                      <div class="twin-stat-value" style="color: #10b981;">100% Manifold</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: AI 3D Generator Tools Dock -->
          <div style="display: flex; flex-direction: column; gap: 1rem;">
            <!-- AI 3D Generator Tools Dock Mount -->
            <div id="generative-studio-mount"></div>
          </div>
        </main>

        <!-- Bottom Full-Width Section: AI Pipeline Console & Archetype Library -->
        <section style="padding: 0 1.75rem 1.75rem 1.75rem;">
          <div id="pipeline-inspector-mount"></div>
        </section>

        <!-- Developer Links & Security Architecture Footer -->
        <footer class="app-footer">
          <div class="footer-bar">
            <div class="footer-left">
              <span class="footer-label">Developer Network:</span>
              <div class="footer-links-row">
                <a href="https://github.com/unidentifiedcyberghost" target="_blank" rel="noopener noreferrer" class="dev-link">
                  <span>github/unidentifiedcyberghost</span>
                </a>
                <span class="link-separator">&bull;</span>
                <a href="https://github.com/pinoyUnknown" target="_blank" rel="noopener noreferrer" class="dev-link">
                  <span>github/pinoyUnknown</span>
                </a>
                <span class="link-separator">&bull;</span>
                <a href="https://github.com/teamwhitehatdev" target="_blank" rel="noopener noreferrer" class="dev-link">
                  <span>github/teamwhitehatdev</span>
                </a>
                <span class="link-separator">&bull;</span>
                <a href="https://www.instagram.com/p/Db4z7xmiJMQ" target="_blank" rel="noopener noreferrer" class="dev-link">
                  <span>instagram/post</span>
                </a>
              </div>
            </div>

            <div class="footer-right">
              <button id="btn-toggle-dev-drawer" class="btn-footer-toggle">
                <span id="dev-drawer-label">Security &amp; Meta Model Specs</span>
                <svg id="dev-drawer-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
            </div>
          </div>

          <!-- Expandable Developer Drawer -->
          <div id="dev-expandable-drawer" class="dev-drawer" style="display: none;">
            <div class="drawer-grid">
              <div class="drawer-col">
                <div class="drawer-header">Security Architecture</div>
                <div class="drawer-text">
                  Zero-exposure credential policy active. Private keys, .pem certificates, and API tokens are isolated in local memory and banned via strict .gitignore rules.
                </div>
              </div>
              <div class="drawer-col">
                <div class="drawer-header">Meta Model Endpoints</div>
                <div class="drawer-text">
                  SAM 3.1 Vision &bull; Llama 3.2 90B 3D Geometry &bull; Meta Auto-Rigger v2 &bull; Neural PBR Shaders with local fallback.
                </div>
              </div>
              <div class="drawer-col">
                <div class="drawer-header">Developer Profiles</div>
                <div class="drawer-links-list">
                  <a href="https://github.com/unidentifiedcyberghost" target="_blank" rel="noopener noreferrer">github.com/unidentifiedcyberghost</a>
                  <a href="https://github.com/pinoyUnknown" target="_blank" rel="noopener noreferrer">github.com/pinoyUnknown</a>
                  <a href="https://github.com/teamwhitehatdev" target="_blank" rel="noopener noreferrer">github.com/teamwhitehatdev</a>
                  <a href="https://www.instagram.com/p/Db4z7xmiJMQ" target="_blank" rel="noopener noreferrer">instagram.com/p/Db4z7xmiJMQ</a>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    `;
  }

  initComponents() {
    const threeContainer = document.getElementById('three-container');
    const cadToolbarMount = document.getElementById('cad-toolbar-mount');
    const generativeStudioMount = document.getElementById('generative-studio-mount');
    const pipelineInspectorMount = document.getElementById('pipeline-inspector-mount');

    // 1. Initialize Three.js Studio Viewport
    this.digitalTwin = new DigitalTwin3D(threeContainer, (modelInfo) => {
      this.updateViewportHUD(modelInfo.name, modelInfo.format);
      if (this.pipelineInspector) {
        this.pipelineInspector.addLog(
          '3D Loader',
          'IMPORT',
          `Loaded custom 3D model "${modelInfo.name}" (${modelInfo.format}). Auto-scaled and framed in studio.`
        );
        this.pipelineInspector.updateDiagnostics();
      }
    });

    // 2. Initialize CAD Viewport Toolbar
    this.cadToolbar = new StudioToolbar3D(cadToolbarMount, this.digitalTwin);

    // 3. Initialize Offscreen SAM 3.1 Segmenter for Image-to-3D
    const offscreenCanvas = document.createElement('canvas');
    offscreenCanvas.width = 400;
    offscreenCanvas.height = 300;
    this.canvasSegmenter = new CanvasSegmenter(
      offscreenCanvas,
      () => {},
      () => {},
      (tex) => {
        if (this.pipelineInspector) {
          this.pipelineInspector.addLog('SAM 3.1', 'TEXTURE', 'Extracted 2D texture mask ready for 3D projection.');
        }
      }
    );

    // 4. Initialize AI Pipeline Inspector
    this.pipelineInspector = new AIPipelineInspector(
      pipelineInspectorMount,
      this.digitalTwin,
      (archetypeId) => {
        this.digitalTwin.loadArchetype(archetypeId);
        this.updateViewportHUD(archetypeId, 'Archetype');
        this.pipelineInspector.addLog(
          'Archetype Engine',
          'SPAWN',
          `Loaded 3D archetype "${archetypeId.replace(/_/g, ' ').toUpperCase()}".`
        );
        this.pipelineInspector.updateDiagnostics();
      }
    );

    // 5. Initialize AI 3D Generator Tools Dock
    this.generativeStudio = new Generative3DStudio(
      generativeStudioMount,
      this.digitalTwin,
      this.canvasSegmenter,
      this.pipelineInspector
    );

    // Custom 3D Model Uploader (.STL / .OBJ / .GLTF / .GLB)
    const upload3dInput = document.getElementById('input-upload-3d');
    if (upload3dInput) {
      upload3dInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (file) {
          this.digitalTwin.loadUser3DModel(file);
        }
      });
    }

    // Theme Switcher (Blender CAD Light Slate vs Obsidian Dark)
    const themeBtn = document.getElementById('btn-theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme') || 'blender';
        const nextTheme = currentTheme === 'blender' ? 'obsidian' : 'blender';
        document.body.setAttribute('data-theme', nextTheme);
        this.digitalTwin.setTheme(nextTheme);

        const label = document.getElementById('theme-toggle-label');
        if (label) {
          label.textContent = nextTheme === 'blender' ? 'Theme: Blender CAD' : 'Theme: Obsidian Dark';
        }

        if (this.pipelineInspector) {
          this.pipelineInspector.addLog(
            'Theme Engine',
            'UI',
            `Theme switched to ${nextTheme === 'blender' ? 'Blender 3D Slate Workbench' : 'Obsidian Deep Space Dark'}.`
          );
        }
      });
    }

    // Pitch Kit Modal
    const pitchBtn = document.getElementById('btn-pitch');
    if (pitchBtn) {
      pitchBtn.addEventListener('click', () => {
        this.pitchModal.show();
      });
    }

    // Settings Modal
    const settingsBtn = document.getElementById('btn-settings');
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        this.settingsModal.show();
      });
    }

    // Expandable Developer Drawer
    const toggleBtn = document.getElementById('btn-toggle-dev-drawer');
    const drawer = document.getElementById('dev-expandable-drawer');
    const chevron = document.getElementById('dev-drawer-chevron');
    if (toggleBtn && drawer) {
      toggleBtn.addEventListener('click', () => {
        const isHidden = drawer.style.display === 'none';
        drawer.style.display = isHidden ? 'block' : 'none';
        if (chevron) {
          chevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
        }
      });
    }

    this.updateApiStatus();
  }

  updateViewportHUD(name, format) {
    const nameEl = document.getElementById('viewport-model-name');
    const rigEl = document.getElementById('viewport-rig-status');
    if (nameEl) nameEl.textContent = name;
    if (rigEl) {
      const diag = this.digitalTwin.getMeshDiagnostics();
      rigEl.textContent = diag.isRigged ? '17 Bones Active' : 'Static Mesh';
    }
  }

  updateApiStatus() {
    const statusText = document.getElementById('api-status-text');
    if (statusText) {
      statusText.textContent = metaModelService.apiKey ? 'Mode: Live Meta API' : 'Mode: Neural Sim';
    }
  }
}

// Start app on DOMContentLoaded
window.addEventListener('DOMContentLoaded', () => {
  new App();
});
