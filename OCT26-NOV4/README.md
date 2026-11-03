# META 3D GEN STUDIO
### Autonomous Generative AI 3D Studio, Skeletal Auto-Rigger & PBR Engine
**Built for the Meta Global AI Developer Hackathon ($1,000,000 Prize Pool | Oct 26 – Nov 4, 2026)**

[![Meta Hackathon](https://img.shields.io/badge/Meta_AI-Global_Hackathon_2026-0081fb?style=for-the-badge&logo=meta)](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
[![Models](https://img.shields.io/badge/Models-SAM_3.1_%7C_Llama_3.2_90B_%7C_Auto--Rigger_v2_%7C_Neural_PBR-00f0ff?style=for-the-badge)](https://ai.meta.com/)
[![Security: Zero-Leak](https://img.shields.io/badge/Security-Zero--Leak_Credentials-10b981?style=for-the-badge)](SECURITY.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-8b5cf6?style=for-the-badge)](LICENSE)

---

## Executive Summary

**META 3D GEN STUDIO** is a clean, dedicated, generative 3D software studio connecting Meta's newest multimodal AI models—**Meta SAM 3.1 (Spatial Perception)**, **Meta Llama 3.2 90B (3D Geometry Synthesizer)**, and **Meta Auto-Rigger v2 (Skeletal Kinematics)**—into an integrated, production-grade 3D asset creation pipeline.

Designed with the ergonomics of **Blender 3D** and the accessibility of **Meshy.ai**, the studio enables creators, game developers, 3D artists, and Metaverse builders to turn natural language ideas and 2D images into **fully rigged, textured, watertight 3D models ready for export into Meta Quest, WebXR, Unreal Engine 5, Unity, and Blender.**

```
+---------------------------------------------------------------------------------------+
|                                  META 3D GEN STUDIO                                   |
|                                                                                       |
|   [Text Prompt / 2D Image]       [Meta Llama 3.2 90B]       [Spatial Marching Cubes]  |
|    - Natural Language Idea  ──>   Latent SDF Voxel Grid ──>  Watertight Quad Mesh     |
|    - Photo / Concept Art          Semantic Primitives        100% Manifold Geometry   |
|                                                                       │               |
|                                                                       ▼               |
|   [Meta Quest / Blender]         [Meta Auto-Rigger v2]      [Meta SAM 3.1 & PBR]     |
|    - Rigged .GLB Export     <──   17-Bone Humanoid      <──  UV Unwrapping &          |
|    - Wavefront .OBJ               Skeletal Hierarchy         Texture Baking           |
|    - Watertight .STL              Procedural Motion cycles   PBR Shaders              |
+---------------------------------------------------------------------------------------+
```

---

## The 4 Core AI 3D Generator Tools

### 1. AI Text-to-3D Generator (Llama 3.2 90B 3D Synthesizer)
- **Natural Language Input**: Type any 3D asset idea (e.g. *"Cyberpunk Mech Warrior with Armored Chassis & Laser Cannons"*).
- **AI Prompt Enhancer**: 1-click prompt optimization that automatically injects professional 3D qualifiers (*"8K PBR textures, clean quad topology, watertight manifold, game-ready UVs"*).
- **Concept Presets**: Instant archetypes for Humanoid Androids, Heavy Mechas, Stealth Aerial Drones, Alien Monoliths, and Cybernetic Hands.
- **Topology & Polycount Control**: Target low-poly (5k), balanced (25k), or high-density sculpt (80k) with sagittal X-axis symmetry.
- **5-Stage Generation Pipeline**: Visual real-time progress through Prompt Decomposition, Latent SDF Grid, Marching Cubes, PBR Baking, and Viewport Framing.

### 2. AI Image-to-3D Generator (Meta SAM 3.1 Depth & Silhouette Synthesizer)
- **2D Image Upload**: Drag-and-drop or upload any 2D concept art, character illustration, sketch, or photo.
- **Interactive SAM 3.1 Canvas**: Place Point Prompts or drag Bounding Boxes to segment the foreground subject from the background with zero-shot accuracy.
- **Volumetric Depth Extrusion**: Converts continuous luminance and depth gradients into solid 3D geometry with backshell beveling.
- **Parametric Sliders**: Adjust extrusion depth (0.5x to 5.0x), subdivision grid resolution (32x32 to 128x128), and bilateral normal smoothing.

### 3. AI Skeletal Auto-Rigging & Motion Studio (Meta Auto-Rigger v2)
- **17-Bone Humanoid Armature**: Generates a complete bipedal skeleton hierarchy (Pelvis, Spine, Chest, Neck, Head, Shoulders, Arms, Forearms, Hands, Hips, Thighs, Shins, Feet).
- **Armature Bone Visualizer**: Overlays a dynamic `THREE.SkeletonHelper` on the mesh with customizable bone links and joint spheres.
- **Procedural Motion Library**:
  - **Fluid Walk Cycle**: Natural rhythmic gait with arm swinging and pelvis bobbing.
  - **Idle Breathing**: Subtle thoracic and spinal expansion cadence.
  - **Kinematic Action**: Dynamic sweeping arm motion.
  - **Combat Stance**: Athletic martial readiness stance.
  - **Standard T-Pose**: Neutral binding rest pose.
- **Motion Player**: Play/Pause, speed multiplier (0.25x to 2.0x), and live scrubbing.
- **Inverse Kinematics / Bone Posing**: Fine-tune Head tilt, Spine bend, Left Arm, and Right Arm joint rotations in real time.

### 4. AI PBR Texture & Shader Studio
- **PBR Material Presets**: Studio Clay Matcap, PBR Photorealistic, Chrome Titanium, Cyber Neon Hologram, Refractive Glass, and Normal Vectors.
- **Real-Time Sliders**: Continuous control over Roughness, Metalness, Clearcoat, Ambient Occlusion, and Texture UV Tiling (1x to 6x).
- **1-Click Texture Projection**: Drapes extracted 2D textures or SAM masks directly onto 3D objects with automatic UV wrapping.

---

## Blender CAD 3D Viewport & Toolbar

- **High-Resolution WebGL Viewport**: Default 560px canvas, expandable to enlarged cinema mode (720px+).
- **Blender Studio Slate Workbench Theme**: Calibrated `#22252b` / `#2b2e36` background with 3-point studio lighting, ground floor grid, and XYZ orientation tripod.
- **Camera View Presets**: Instant 1-click angle switching for Front [1], Side [3], Top [7], and Isometric Perspective [5].
- **Viewport Tools**: Fit/Focus Model, 360° Turntable Auto-Rotation, Grid & Axes toggle, and 4K Viewport PNG Snapshot.
- **Custom 3D Import**: Drag-and-drop or browse custom `.STL`, `.OBJ`, `.GLTF`, and `.GLB` files with auto-scaling and bounding box framing.

---

## AI Pipeline Inspector & Multi-Format Exporters

- **Live Reasoning Stream**: Real-time trace of Meta Llama 3.2 90B token generation, SAM 3.1 spatial coordinates, and geometry extraction.
- **Mesh Manifold Diagnostics**: Real-time vertex counter, face counter, bounding dimensions (X, Y, Z in meters), and 100% Watertight manifold verification.
- **Quick Archetype Selector**: 1-click loading for Humanoid Biped, Cyber Mecha, Stealth Drone, Sci-Fi Monolith, and Cyber Hand.
- **Metaverse & Game Engine Exporters**:
  - **Export Rigged `.GLB` / `.GLTF`**: Embedded 17-bone armature, inverse bind matrices, and animations for Meta Quest, WebXR, Unreal Engine, and Unity.
  - **Export Quad `.OBJ`**: Clean polygon mesh for Blender 3D, Maya, and 3ds Max.
  - **Export Watertight `.STL`**: Solid manifold geometry ready for 3D slicing (Cura, PrusaSlicer, Bambu Studio).
  - **4K Viewport Snapshot**: High-resolution PNG render.

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **3D Engine & Viewport** | Three.js (r170), WebGL 2.0, GLTFExporter, OBJExporter, STLLoader, OBJLoader, GLTFLoader |
| **Animation & Rigging** | THREE.SkinnedMesh, THREE.SkeletonHelper, THREE.AnimationMixer, THREE.AnimationClip, THREE.Bone |
| **AI Perception & Vision** | Meta SAM 3.1 (Segment Anything), ViT Image Encoder, Zero-Shot Mask Extraction |
| **AI 3D Synthesis** | Meta Llama 3.2 Vision (90B / 11B), Llama 3.3 Reasoning, Muse Code Agent |
| **Frontend Platform** | Vite 5.4+, Vanilla JavaScript (ESM 2024), Native HTML5 Canvas, Master Vanilla CSS Design System |
| **Backend Microservice** | Python 3.10+, FastAPI, Uvicorn, NumPy, SciPy |
| **CLI & Test Suites** | Node.js ESM CLI (`test-models.js`, `security-check.js`) |

---

## Quick Start & Installation

### Prerequisites
- Node.js (v18+ or v20+)
- Python (v3.10+)

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/pinoyUnknown/META-GLOBAL-AI-DEVELOPER-HACKATHON.git
cd META-GLOBAL-AI-DEVELOPER-HACKATHON/OCT26-NOV4
npm install
```

### 2. Start the Local Studio
```bash
npm run dev -- --port 3000
```
Open your browser to `http://localhost:3000` to launch the **META 3D GEN STUDIO**.

### 3. Run Automated Model QA & Security Audits
```bash
# Run model invariant test suite (4/4 passed)
npm run test:models

# Run zero-exposure credential security scan
npm run security:check
```

---

## Security Architecture & Zero-Exposure Policy

This repository implements strict data privacy protocols to protect developer credentials:
- **Strict `.gitignore` Rules**: Automatically blocks `*.pem`, `*.key`, `*.cert`, `.env`, `.env.*`, passwords, tokens, and serial keys.
- **Pre-Commit Audit**: `npm run security:check` scans all workspace files to ensure zero secrets are committed.
- **Ephemeral Session Memory**: API credentials configured in the UI are held strictly in local memory and never exposed.
- See [SECURITY.md](file:///c:/Project-PinoyUnknown/META-GLOBAL-AI-DEVELOPER-HACKATHON/OCT26-NOV4/SECURITY.md) for full protocol specifications.

---

## Developer Network & Attribution

- **Lead Developer**: [unidentifiedcyberghost (GitHub)](https://github.com/unidentifiedcyberghost)
- **Organization**: [pinoyUnknown (GitHub)](https://github.com/pinoyUnknown)
- **Engineering Team**: [teamwhitehatdev (GitHub)](https://github.com/teamwhitehatdev)
- **Project Showcase**: [Instagram Post](https://www.instagram.com/p/Db4z7xmiJMQ)

---

## License

This project is licensed under the MIT License - see the [LICENSE](file:///c:/Project-PinoyUnknown/META-GLOBAL-AI-DEVELOPER-HACKATHON/OCT26-NOV4/LICENSE) file for details.
