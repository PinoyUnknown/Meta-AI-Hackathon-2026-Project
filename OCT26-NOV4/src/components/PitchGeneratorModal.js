// Hackathon Pitch Deck & Application Form Answer Generator Modal
export class PitchGeneratorModal {
  constructor() {
    this.modalElement = null;
  }

  show() {
    if (this.modalElement) this.close();

    this.modalElement = document.createElement('div');
    this.modalElement.className = 'modal-backdrop';
    this.modalElement.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <div class="brand-logo" style="width: 28px; height: 28px; border-radius: 6px;">
              <svg viewBox="0 0 24 24" fill="#fff" width="16" height="16">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <h3 class="modal-title">Meta Global AI Hackathon Application Kit</h3>
          </div>
          <button class="close-btn" id="modal-close">&times;</button>
        </div>

        <div class="modal-body">
          <div style="background: rgba(0, 129, 251, 0.12); border: 1px solid rgba(0, 129, 251, 0.3); border-radius: 10px; padding: 0.85rem; font-size: 0.78rem; color: #bae6fd;">
            <strong>Ready-to-Submit Hackathon Answers:</strong> Generated for the Cerebral Valley / Meta AI Developer Hackathon ($1,000,000 Prize Pool). Tailored to match both <em>"Push the Frontier"</em> &amp; <em>"Build for Your World"</em> selection criteria.
          </div>

          <!-- Question 1: Project Idea & Theme Fit -->
          <div class="q-box">
            <div class="q-title" style="display: flex; justify-content: space-between; align-items: center;">
              <span>Criterion 1: Your Project Idea &amp; Theme Fit (Weight: 50%)</span>
              <button class="btn btn-secondary copy-btn" data-target="q1-text" style="font-size: 0.68rem; padding: 0.2rem 0.5rem;">Copy Answer</button>
            </div>
            <div id="q1-text" class="q-text">
<strong>Project Title:</strong> MetaFrontier NeuroTwin: Autonomous Multimodal Digital-Twin &amp; Physical AI Discovery Studio<br/><br/>
<strong>Theme Fit:</strong> Push the Frontier (Primary) &amp; Build for Your World (Secondary).<br/><br/>
<strong>Core Problem &amp; Innovation:</strong><br/>
In frontier domains like robotics, bio-engineering, clean energy, and semiconductor fabrication, translating unstructured physical sensor data (high-res camera feeds, SEM imagery, and infrared thermography) into actionable simulation models is extraordinarily slow and error-prone. Human operators manually calculate spatial coordinates, estimate stress distributions, and hand-write safety-critical simulations.<br/><br/>
MetaFrontier NeuroTwin bridges this divide by uniting Meta's newest models into an autonomous closed-loop physical reasoning system:
1. <strong>Spatial Perception:</strong> Meta SAM 3.1 executes zero-shot sub-millimeter segmentation of micro-fractures, mechanical gears, cell nuclei, and thermal shunts from interactive point/box prompts.
2. <strong>Physical Reasoning:</strong> Meta Llama 3.2 Vision (90B) and Llama 3.3 (70B) analyze visual masks, compute governing physical stress/kinematic equations (Von Mises stress, Navier-Stokes, quantum tunneling), and formulate remediation protocols.
3. <strong>Autonomous Simulation:</strong> Meta Muse Code Agent generates executable Python / PyBullet / ROS2 simulation scripts in real time to validate physical stability.
4. <strong>Interactive 3D Digital Twin:</strong> Live WebGL/Three.js digital twin reflects diagnosed stress heatmaps and kinematics dynamically in an intuitive studio interface.
            </div>
          </div>

          <!-- Question 2: Technical Skill & Architecture -->
          <div class="q-box">
            <div class="q-title" style="display: flex; justify-content: space-between; align-items: center;">
              <span>Criterion 2: Technical Skill, Model Integration &amp; Techniques (Weight: 50%)</span>
              <button class="btn btn-secondary copy-btn" data-target="q2-text" style="font-size: 0.68rem; padding: 0.2rem 0.5rem;">Copy Answer</button>
            </div>
            <div id="q2-text" class="q-text">
<strong>Technical Architecture &amp; Meta Model Integration:</strong><br/>
- <strong>Model Stack:</strong> Meta SAM 3.1 &amp; SAM 2 (zero-shot mask contour vectorization), Meta Llama 3.2 90B Multimodal Vision (spatial reasoning), Meta Llama 3.3 70B Instruct (chain-of-thought planning), Meta Muse Code Agent (simulation synthesis), and Llama Guard 3 (safety and physical invariant verification).<br/>
- <strong>Agentic Workflow:</strong> Implemented a 4-agent collaborative pipeline (Perception Agent → Domain Physics Reasoner → Muse Code Synthesizer → Red-Team QA Verifier). Agents communicate via structured telemetry and validate invariant boundaries before execution.<br/>
- <strong>Frontend &amp; Visualization:</strong> Modern high-performance Vanilla CSS / JavaScript interface with Three.js 3D digital-twin rendering, interactive HTML5 canvas segmentation with real-time coordinate HUD, and dynamic telemetry graphs.<br/>
- <strong>Backend &amp; CLI:</strong> Python FastAPI engine supporting live Meta Model API endpoints with fallback offline deterministic neural simulation, accompanied by a Node.js CLI tool (<code>meta-frontier-cli</code>) for automated testing, batch dataset processing, and ML model QA benchmarking.
            </div>
          </div>

          <!-- Persona Impact Breakdown -->
          <div class="q-box">
            <div class="q-title">Target Audience &amp; Ecosystem Impact</div>
            <div class="q-text" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">
              <div>
                <strong style="color: var(--neon-cyan);">For Developers:</strong> Clean API, modular agent adapters, and instant scaffolding for physical AI applications.
              </div>
              <div>
                <strong style="color: var(--neon-cyan);">For Testers &amp; QA:</strong> Automated red-teaming matrix, adversarial robustness scoring, and invariant verification.
              </div>
              <div>
                <strong style="color: #10b981;">For Scientists &amp; Roboticists:</strong> Automated kinematic torque solvers, bio-cell ratio tracking, and solar thermography derating.
              </div>
              <div>
                <strong style="color: #c084fc;">For ML Researchers:</strong> Zero-shot SAM prompt tuning, IoU benchmark scoring, and token throughput latency metrics.
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button id="btn-download-pitch" class="btn btn-secondary">
            Download Submission Markdown (.md)
          </button>
          <button id="btn-modal-done" class="btn btn-primary">
            Done
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(this.modalElement);

    // Attach event listeners
    this.modalElement.querySelector('#modal-close').addEventListener('click', () => this.close());
    this.modalElement.querySelector('#btn-modal-done').addEventListener('click', () => this.close());

    // Copy buttons
    this.modalElement.querySelectorAll('.copy-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const textElement = this.modalElement.querySelector(`#${targetId}`);
        if (textElement) {
          navigator.clipboard.writeText(textElement.innerText);
          const original = btn.textContent;
          btn.textContent = 'Copied!';
          setTimeout(() => { btn.textContent = original; }, 2000);
        }
      });
    });

    // Download pitch markdown
    this.modalElement.querySelector('#btn-download-pitch').addEventListener('click', () => {
      const q1 = this.modalElement.querySelector('#q1-text').innerText;
      const q2 = this.modalElement.querySelector('#q2-text').innerText;
      const md = `# Meta Global AI Developer Hackathon Submission\n\n## Criterion 1: Project Idea & Theme Fit\n\n${q1}\n\n## Criterion 2: Technical Skill & Architecture\n\n${q2}\n`;
      const blob = new Blob([md], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'META_HACKATHON_APPLICATION.md';
      a.click();
    });
  }

  close() {
    if (this.modalElement && this.modalElement.parentNode) {
      this.modalElement.parentNode.removeChild(this.modalElement);
      this.modalElement = null;
    }
  }
}
