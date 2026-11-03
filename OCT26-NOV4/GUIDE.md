# 📖 MetaFrontier NeuroTwin — Complete Step-by-Step Operator & Developer Guide

A comprehensive, cross-platform guide for running, configuring, testing, and developing **MetaFrontier NeuroTwin** on **Windows**, **Linux**, and **macOS**.

---

## 📋 Table of Contents
1. [System Prerequisites](#1-system-prerequisites)
2. [Quick Start (One-Liner)](#2-quick-start-one-liner)
3. [Windows Setup & Execution Guide](#3-windows-setup--execution-guide)
4. [Linux & macOS Setup & Execution Guide](#4-linux--macos-setup--execution-guide)
5. [Security & Credential Management](#5-security--credential-management)
6. [Interactive Studio Features & Workflow](#6-interactive-studio-features--workflow)
7. [CLI Tools & Automated Testing](#7-cli-tools--automated-testing)
8. [Configuring Live Meta Model API Keys](#8-configuring-live-meta-model-api-keys)
9. [Developer Network & Profiles](#9-developer-network--profiles)

---

## 1. System Prerequisites

Before starting, ensure your system meets the minimum requirements:

- **Node.js**: v18.0.0 or higher (Tested with Node v22)
- **npm**: v9.0.0 or higher (Tested with npm v11)
- **Python**: v3.10 or higher (Optional, needed for FastAPI backend)
- **Web Browser**: Any modern browser (Google Chrome, Microsoft Edge, Brave, Firefox) with WebGL enabled.

To check your installed runtimes, run:
```bash
node -v
npm -v
python --version
```

---

## 2. Quick Start (One-Liner)

```bash
# Clone/navigate to directory and start the local studio
npm install && npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 3. Windows Setup & Execution Guide

### Option A: PowerShell (Recommended)

1. **Open PowerShell as User** and navigate to the project directory:
   ```powershell
   cd c:\Project-PinoyUnknown\META-GLOBAL-AI-DEVELOPER-HACKATHON\OCT26-NOV4
   ```

2. **Install Node Dependencies**:
   ```powershell
   npm install
   ```

3. **Run Security & Credential Check**:
   ```powershell
   npm run security:check
   ```
   *Verifies zero private keys, `.pem` certificates, or passwords are exposed.*

4. **Launch the Visual Web Studio**:
   ```powershell
   npm run dev
   ```
   *Starts the Vite dev server at `http://localhost:3000`.*

5. **(Optional) Launch Python FastAPI AI Engine** in a separate terminal:
   ```powershell
   python server/server.py
   ```
   *Runs backend API on `http://localhost:8000`.*

6. **Open in your Default Browser**:
   ```powershell
   Start-Process http://localhost:3000
   ```

---

### Option B: Windows Command Prompt (CMD)

```cmd
cd c:\Project-PinoyUnknown\META-GLOBAL-AI-DEVELOPER-HACKATHON\OCT26-NOV4
npm install
npm run dev
start http://localhost:3000
```

---

## 4. Linux & macOS Setup & Execution Guide

Works seamlessly on Ubuntu, Debian, Fedora, Arch, CentOS, and macOS:

1. **Clone or Navigate to the Directory**:
   ```bash
   cd /path/to/META-GLOBAL-AI-DEVELOPER-HACKATHON/OCT26-NOV4
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **(Optional) Set up Python Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r server/requirements.txt
   ```

4. **Run the Pre-Commit Security Audit**:
   ```bash
   npm run security:check
   ```

5. **Start the Frontend Studio**:
   ```bash
   npm run dev -- --host
   ```
   Access `http://localhost:3000` from your browser.

6. **Start the Python Backend Engine** (in another terminal):
   ```bash
   python3 server/server.py
   ```

---

## 5. Security & Credential Management

The project is pre-configured with a zero-leak credential architecture:

1. **Copy the Safe Environment Template**:
   ```bash
   cp .env.example .env
   ```
2. **Edit `.env` locally**: Add your local credentials (e.g. `META_MODEL_API_KEY`).
3. **Automatic `.gitignore` Protection**:
   The repository `.gitignore` automatically blocks `.env`, `.pem`, `*.key`, `admin/`, and password dumps from ever being committed or leaked.
4. **Run the Security Auditor**:
   ```bash
   npm run security:check
   ```

---

## 6. Interactive Studio Features & Workflow

When you open `http://localhost:3000`, the studio provides:

1. **Interactive Vision Canvas (SAM 3.1)**:
   - Click anywhere on the high-resolution engineering feed to set a **Point Prompt**.
   - Select **Bounding Box** mode to drag a prompt rectangle over an area.
   - The Segment Anything Model (SAM 3.1) instantly isolates the mask with neon contour boundaries and spatial IoU scores.
2. **Real-Time 3D Digital Twin (Three.js)**:
   - Orbit controls: Left-click and drag to rotate the 3D model; mouse wheel to zoom.
   - Dynamically highlights physical stress points (turning glowing amber/crimson) when an anomaly is diagnosed.
3. **Multi-Agent Reasoning Loop**:
   - Four collaborative Meta agents stream live thoughts:
     - **Perception Agent**: Isolates boundaries and bounding coordinates.
     - **Physical Reasoner Agent**: Computes Von Mises stress and constitutive equations.
     - **Muse Code Agent**: Synthesizes simulation code.
     - **Red-Team QA Agent**: Validates safety constraints and physical invariants.
4. **Sandboxed Code Runner**:
   - Inspect the synthesized Python script and click **"Run Simulation"** to execute within the virtual sandbox.
5. **Model Evaluation & Red-Team Matrix**:
   - Click **"Run Comprehensive Model Benchmarks"** to measure latency, throughput (tok/s, FPS), and memory footprint.
6. **Hackathon Pitch Kit**:
   - Click **"Hackathon Pitch Kit"** in the top navigation bar to view pre-filled, copy-to-clipboard answers for the Cerebral Valley Meta Hackathon application form.

---

## 7. CLI Tools & Automated Testing

For headless servers, automated CI/CD pipelines, or terminal-based developers:

```bash
# 1. Terminal Multi-Agent Demonstration
npm run start
# or: node cli/meta-frontier-cli.js --demo

# 2. Automated Model QA & Invariant Test Suite
npm run test:models

# 3. Model Benchmark Matrix (CLI Table)
node cli/meta-frontier-cli.js benchmark

# 4. View Hackathon Pitch Answers in CLI
node cli/meta-frontier-cli.js pitch

# 5. Security Scanner
npm run security:check
```

---

## 8. Configuring Live Meta Model API Keys

The system is designed to work **100% out-of-the-box in zero-config offline mode** using deterministic neural simulation. 

To connect live Meta Model API endpoints:
1. Click the **"Settings"** button on the top right navigation bar.
2. Enter your **Meta Model API Key / Bearer Token** (`sk-meta-...`).
3. Set your backend engine URL (defaults to `http://localhost:8000`).
4. Click **"Save Configuration"**.
   - Your key is stored in your private browser memory session and will never be logged to disk or committed to git.

---

## 9. Developer Network & Profiles

The developer network links are accessible in the bottom footer of the application and open directly in your browser:

- **Unidentified Cyber Ghost**: [https://github.com/unidentifiedcyberghost](https://github.com/unidentifiedcyberghost)
- **PinoyUnknown**: [https://github.com/pinoyUnknown](https://github.com/pinoyUnknown)
- **Team White Hat Dev**: [https://github.com/teamwhitehatdev](https://github.com/teamwhitehatdev)
- **Instagram Profile**: [https://www.instagram.com/p/Db4z7xmiJMQ](https://www.instagram.com/p/Db4z7xmiJMQ)
