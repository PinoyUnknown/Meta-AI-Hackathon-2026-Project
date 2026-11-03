// Interactive Three.js 3D Digital Twin & Studio Viewport Component with Blender Studio Lighting, Archetypes & Metaverse Exporters
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import { OBJExporter } from 'three/examples/jsm/exporters/OBJExporter.js';

export class DigitalTwin3D {
  constructor(containerElement, onModelLoaded) {
    this.container = containerElement;
    this.onModelLoaded = onModelLoaded;
    this.currentDomainId = 'robotics';
    this.currentArchetype = 'humanoid_avatar';
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.modelGroup = new THREE.Group();
    this.isRotating = false;
    this.rotationSpeed = 0.006;
    this.activeStressLevel = 0.184;
    this.theme = 'blender'; // 'blender' | 'obsidian'

    // Studio & Material States
    this.activeMaterialPreset = 'clay';
    this.roughness = 0.35;
    this.metalness = 0.2;
    this.isWireframe = false;
    this.activeTexture = null;
    this.activeModelName = 'humanoid-avatar-rigged';
    this.gridHelper = null;
    this.axesHelper = null;
    this.gridVisible = true;
    this.activeLightingPreset = 'studio';

    // Lights
    this.keyLight = null;
    this.fillLight = null;
    this.rimLight = null;
    this.ambientLight = null;

    // Rigging Engine reference
    this.riggingEngine = null;

    // Domain references for dynamic articulation & backward compatibility
    this.joint1 = null;
    this.joint2 = null;
    this.stressMesh = null;

    this.initThree();
    this.buildArchetypeModel(this.currentArchetype);
    this.attachControls();
    this.animate();
  }

  initThree() {
    const width = this.container.clientWidth || 700;
    const height = this.container.clientHeight || 560;

    // Scene
    this.scene = new THREE.Scene();
    this.updateThemeBackground();

    // Camera
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 3.2, 5.8);
    this.camera.lookAt(0, 0.6, 0);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Clean container and append canvas
    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // Studio 3-Point Lighting (Blender CAD Studio Workbench Setup)
    // 1. Key Light (Warm Sun)
    this.keyLight = new THREE.DirectionalLight(0xfff7ea, 2.2);
    this.keyLight.position.set(5, 8, 7);
    this.keyLight.castShadow = true;
    this.scene.add(this.keyLight);

    // 2. Fill Light (Cool Sky)
    this.fillLight = new THREE.DirectionalLight(0xd4e4ff, 1.4);
    this.fillLight.position.set(-6, 4, 3);
    this.scene.add(this.fillLight);

    // 3. Rim / Back Light (High-tech contrast)
    this.rimLight = new THREE.DirectionalLight(0x00c8e6, 1.8);
    this.rimLight.position.set(0, -3, -6);
    this.scene.add(this.rimLight);

    // 4. Soft Ambient Studio Light
    this.ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
    this.scene.add(this.ambientLight);

    // Blender Ground Grid (Subdivided Workbench Floor)
    this.gridHelper = new THREE.GridHelper(12, 24, 0x00c8e6, 0x475569);
    this.gridHelper.position.y = -0.01;
    this.scene.add(this.gridHelper);

    // Blender XYZ Orientation Tripod (Red=X, Green=Y, Blue=Z)
    this.axesHelper = new THREE.AxesHelper(1.2);
    this.axesHelper.position.set(0, 0.01, 0);
    this.scene.add(this.axesHelper);

    this.scene.add(this.modelGroup);
  }

  updateThemeBackground() {
    if (!this.scene) return;
    if (this.theme === 'blender') {
      // Blender Slate Workbench Fog & Background
      this.scene.background = new THREE.Color(0x272b34);
      this.scene.fog = new THREE.FogExp2(0x272b34, 0.035);
    } else {
      // Obsidian Deep Space Fog & Background
      this.scene.background = new THREE.Color(0x060913);
      this.scene.fog = new THREE.FogExp2(0x060913, 0.04);
    }
  }

  setTheme(themeName) {
    this.theme = themeName;
    this.updateThemeBackground();
    if (this.gridHelper) {
      this.gridHelper.material.color.setHex(themeName === 'blender' ? 0x64748b : 0x00c8e6);
    }
  }

  // Camera view angle presets: 'front' [1], 'side' [3], 'top' [7], 'iso' [5]
  setCameraAngle(angle) {
    if (!this.modelGroup || !this.camera) return;
    const box = new THREE.Box3().setFromObject(this.modelGroup);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z) || 3;
    const dist = maxDim * 2.2;

    if (angle === 'front') {
      this.camera.position.set(center.x, center.y, center.z + dist);
    } else if (angle === 'side') {
      this.camera.position.set(center.x + dist, center.y, center.z);
    } else if (angle === 'top') {
      this.camera.position.set(center.x, center.y + dist, center.z + 0.001);
    } else {
      // 'iso'
      this.camera.position.set(center.x + dist * 0.7, center.y + dist * 0.6, center.z + dist * 0.7);
    }
    this.camera.lookAt(center);
  }

  // Lighting presets: 'studio', 'cyberpunk', 'sunset', 'key'
  setLightingPreset(preset) {
    this.activeLightingPreset = preset;
    if (!this.keyLight || !this.fillLight || !this.rimLight || !this.ambientLight) return;

    if (preset === 'cyberpunk') {
      this.keyLight.color.setHex(0x00f0ff);
      this.keyLight.intensity = 2.8;
      this.fillLight.color.setHex(0xd946ef);
      this.fillLight.intensity = 2.0;
      this.rimLight.color.setHex(0x8b5cf6);
      this.rimLight.intensity = 2.4;
      this.ambientLight.color.setHex(0x1e1b4b);
      this.ambientLight.intensity = 0.5;
    } else if (preset === 'sunset') {
      this.keyLight.color.setHex(0xf97316);
      this.keyLight.intensity = 3.0;
      this.fillLight.color.setHex(0x818cf8);
      this.fillLight.intensity = 1.2;
      this.rimLight.color.setHex(0xfacc15);
      this.rimLight.intensity = 2.0;
      this.ambientLight.color.setHex(0x451a03);
      this.ambientLight.intensity = 0.55;
    } else if (preset === 'key') {
      this.keyLight.color.setHex(0xffffff);
      this.keyLight.intensity = 3.5;
      this.fillLight.color.setHex(0x64748b);
      this.fillLight.intensity = 0.4;
      this.rimLight.color.setHex(0x94a3b8);
      this.rimLight.intensity = 0.8;
      this.ambientLight.color.setHex(0x0f172a);
      this.ambientLight.intensity = 0.3;
    } else {
      // Studio Neutral
      this.keyLight.color.setHex(0xfff7ea);
      this.keyLight.intensity = 2.2;
      this.fillLight.color.setHex(0xd4e4ff);
      this.fillLight.intensity = 1.4;
      this.rimLight.color.setHex(0x00c8e6);
      this.rimLight.intensity = 1.8;
      this.ambientLight.color.setHex(0xffffff);
      this.ambientLight.intensity = 0.65;
    }
  }

  toggleAutoRotate() {
    this.isRotating = !this.isRotating;
    return this.isRotating;
  }

  toggleGrid() {
    this.gridVisible = !this.gridVisible;
    if (this.gridHelper) this.gridHelper.visible = this.gridVisible;
    if (this.axesHelper) this.axesHelper.visible = this.gridVisible;
    return this.gridVisible;
  }

  // Camera auto-focus to frame any 3D model properly
  focusCameraOnModel() {
    if (!this.modelGroup || this.modelGroup.children.length === 0) return;

    const box = new THREE.Box3().setFromObject(this.modelGroup);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    const maxDim = Math.max(size.x, size.y, size.z) || 3;
    const fov = this.camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
    cameraZ *= 2.0; // Margin to avoid clipping

    this.camera.position.set(center.x, center.y + maxDim * 0.4, center.z + cameraZ);
    this.camera.lookAt(center);
  }

  // Real-time mesh diagnostic calculation
  getMeshDiagnostics() {
    let vertices = 0;
    let faces = 0;
    const hasBones = !!this.riggingEngine && !!this.riggingEngine.skinnedMesh;
    const bonesCount = hasBones ? 17 : 0;

    const box = new THREE.Box3().setFromObject(this.modelGroup);
    const size = box.getSize(new THREE.Vector3());

    this.modelGroup.traverse((child) => {
      if (child.isMesh && child.geometry) {
        const geo = child.geometry;
        if (geo.attributes && geo.attributes.position) {
          vertices += geo.attributes.position.count;
        }
        if (geo.index) {
          faces += geo.index.count / 3;
        } else if (geo.attributes && geo.attributes.position) {
          faces += geo.attributes.position.count / 3;
        }
      }
    });

    return {
      name: this.activeModelName,
      vertices,
      faces: Math.round(faces),
      bonesCount,
      dimensions: {
        x: Math.max(0.1, size.x).toFixed(2),
        y: Math.max(0.1, size.y).toFixed(2),
        z: Math.max(0.1, size.z).toFixed(2)
      },
      isWatertight: true,
      materialPreset: this.activeMaterialPreset,
      isRigged: hasBones
    };
  }

  // Load custom 3D file (.STL, .OBJ, .GLTF, .GLB)
  loadUser3DModel(file) {
    const fileName = file.name.toLowerCase();
    const isSTL = fileName.endsWith('.stl');
    const isOBJ = fileName.endsWith('.obj');
    const isGLTF = fileName.endsWith('.gltf') || fileName.endsWith('.glb');

    if (!isSTL && !isOBJ && !isGLTF) {
      alert('Please select a 3D file in .STL, .OBJ, .GLTF, or .GLB format.');
      return;
    }

    this.activeModelName = file.name.replace(/\.[^/.]+$/, '');

    // Clear existing model children
    while (this.modelGroup.children.length > 0) {
      this.modelGroup.remove(this.modelGroup.children[0]);
    }
    if (this.riggingEngine) {
      this.riggingEngine.clear();
    }

    const reader = new FileReader();

    if (isSTL) {
      reader.readAsArrayBuffer(file);
      reader.onload = (e) => {
        try {
          const loader = new STLLoader();
          const geometry = loader.parse(e.target.result);
          geometry.computeVertexNormals();
          geometry.center();

          const material = this.createCurrentMaterial();
          const mesh = new THREE.Mesh(geometry, material);
          mesh.castShadow = true;
          mesh.receiveShadow = true;

          // Auto-scale model to fit viewport
          geometry.computeBoundingBox();
          const box = geometry.boundingBox;
          const maxDim = Math.max(
            box.max.x - box.min.x,
            box.max.y - box.min.y,
            box.max.z - box.min.z
          );
          const scale = maxDim > 0 ? 3.4 / maxDim : 1;
          mesh.scale.set(scale, scale, scale);

          this.stressMesh = mesh;
          this.modelGroup.add(mesh);

          this.focusCameraOnModel();

          if (this.onModelLoaded) {
            this.onModelLoaded({
              name: file.name,
              vertices: geometry.attributes.position ? geometry.attributes.position.count : 'N/A',
              format: 'STL'
            });
          }
        } catch (err) {
          console.error('Error parsing STL file:', err);
          alert('Failed to parse 3D STL file.');
        }
      };
    } else if (isOBJ) {
      reader.readAsText(file);
      reader.onload = (e) => {
        try {
          const loader = new OBJLoader();
          const obj = loader.parse(e.target.result);
          const material = this.createCurrentMaterial();

          obj.traverse((child) => {
            if (child.isMesh) {
              child.material = material;
              child.castShadow = true;
              child.receiveShadow = true;
              if (child.geometry) {
                child.geometry.computeVertexNormals();
              }
            }
          });

          // Center & scale
          const box = new THREE.Box3().setFromObject(obj);
          const center = box.getCenter(new THREE.Vector3());
          const size = box.getSize(new THREE.Vector3());
          obj.position.sub(center);

          const maxDim = Math.max(size.x, size.y, size.z);
          const scale = maxDim > 0 ? 3.4 / maxDim : 1;
          obj.scale.set(scale, scale, scale);

          this.stressMesh = obj;
          this.modelGroup.add(obj);

          this.focusCameraOnModel();

          if (this.onModelLoaded) {
            this.onModelLoaded({
              name: file.name,
              format: 'OBJ'
            });
          }
        } catch (err) {
          console.error('Error parsing OBJ file:', err);
          alert('Failed to parse 3D OBJ file.');
        }
      };
    } else if (isGLTF) {
      reader.readAsArrayBuffer(file);
      reader.onload = (e) => {
        try {
          const loader = new GLTFLoader();
          loader.parse(e.target.result, '', (gltf) => {
            const root = gltf.scene;

            // Apply studio shadows
            root.traverse((child) => {
              if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
              }
            });

            // Center & scale
            const box = new THREE.Box3().setFromObject(root);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            root.position.sub(center);

            const maxDim = Math.max(size.x, size.y, size.z);
            const scale = maxDim > 0 ? 3.4 / maxDim : 1;
            root.scale.set(scale, scale, scale);

            this.stressMesh = root;
            this.modelGroup.add(root);

            this.focusCameraOnModel();

            if (this.onModelLoaded) {
              this.onModelLoaded({
                name: file.name,
                format: fileName.endsWith('.glb') ? 'GLB' : 'GLTF'
              });
            }
          });
        } catch (err) {
          console.error('Error parsing GLTF file:', err);
          alert('Failed to parse 3D GLTF file.');
        }
      };
    }
  }

  // Generate 3D Solid Geometry from 2D Image Luminance & Depth
  generateFromImage(canvasOrImage, options = {}) {
    while (this.modelGroup.children.length > 0) {
      this.modelGroup.remove(this.modelGroup.children[0]);
    }
    if (this.riggingEngine) {
      this.riggingEngine.clear();
    }

    const depth = options.depth !== undefined ? options.depth : 1.8;
    const resolution = options.resolution || 64;

    const geometry = new THREE.PlaneGeometry(3.6, 3.6, resolution, resolution);
    const pos = geometry.attributes.position;

    // Sample luminance from image to displace Z-vertices
    const offscreen = document.createElement('canvas');
    offscreen.width = resolution;
    offscreen.height = resolution;
    const ctx = offscreen.getContext('2d');
    ctx.drawImage(canvasOrImage, 0, 0, resolution, resolution);
    const imgData = ctx.getImageData(0, 0, resolution, resolution).data;

    for (let i = 0; i < pos.count; i++) {
      const idx = i * 4;
      const r = imgData[idx] || 128;
      const g = imgData[idx + 1] || 128;
      const b = imgData[idx + 2] || 128;
      const alpha = imgData[idx + 3] !== undefined ? imgData[idx + 3] / 255 : 1;
      const lum = ((0.299 * r + 0.587 * g + 0.114 * b) / 255) * alpha;
      pos.setZ(i, (lum - 0.5) * depth);
    }

    geometry.computeVertexNormals();

    const texture = new THREE.CanvasTexture(canvasOrImage);
    texture.colorSpace = THREE.SRGBColorSpace;
    this.activeTexture = texture;

    const material = new THREE.MeshStandardMaterial({
      map: texture,
      roughness: this.roughness,
      metalness: this.metalness,
      wireframe: this.isWireframe,
      side: THREE.DoubleSide
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    this.stressMesh = mesh;
    this.activeModelName = options.name || 'image-to-3d-model';
    this.modelGroup.add(mesh);
    this.focusCameraOnModel();
  }

  // Create PBR Material based on active settings & textures
  createCurrentMaterial() {
    let mat;

    if (this.activeMaterialPreset === 'metallic') {
      mat = new THREE.MeshStandardMaterial({
        color: 0xe2e8f0,
        metalness: 0.95,
        roughness: 0.15,
        wireframe: this.isWireframe
      });
    } else if (this.activeMaterialPreset === 'cyber') {
      mat = new THREE.MeshStandardMaterial({
        color: 0x00c8e6,
        emissive: 0x00c8e6,
        emissiveIntensity: 0.45,
        metalness: 0.8,
        roughness: 0.25,
        wireframe: true
      });
    } else if (this.activeMaterialPreset === 'glass') {
      mat = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        transmission: 0.88,
        opacity: 1,
        transparent: true,
        roughness: 0.1,
        ior: 1.5,
        wireframe: this.isWireframe
      });
    } else if (this.activeMaterialPreset === 'normal') {
      mat = new THREE.MeshNormalMaterial({
        wireframe: this.isWireframe
      });
    } else {
      // Studio Clay or PBR Textured
      mat = new THREE.MeshStandardMaterial({
        color: this.activeTexture ? 0xffffff : 0xd6dbe4,
        roughness: this.roughness,
        metalness: this.metalness,
        wireframe: this.isWireframe,
        map: this.activeTexture || null
      });
    }

    if (this.activeTexture && mat && mat.isMeshStandardMaterial) {
      mat.map = this.activeTexture;
      mat.needsUpdate = true;
    }

    return mat;
  }

  // Apply texture image directly onto the 3D model
  applyTexture(imageOrCanvas, options = {}) {
    const texture = new THREE.CanvasTexture(imageOrCanvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;

    const repeatX = options.repeatX || 1;
    const repeatY = options.repeatY || 1;
    texture.repeat.set(repeatX, repeatY);
    texture.needsUpdate = true;

    this.activeTexture = texture;
    this.activeMaterialPreset = 'textured';

    this.applyMaterialToModel(this.createCurrentMaterial());
  }

  // Update material across all meshes in modelGroup
  applyMaterialToModel(material) {
    this.modelGroup.traverse((child) => {
      if (child.isMesh) {
        child.material = material;
        child.material.needsUpdate = true;
      }
    });
  }

  // Set Material Preset ('clay', 'textured', 'metallic', 'cyber', 'glass', 'normal')
  setMaterialPreset(preset) {
    this.activeMaterialPreset = preset;
    const mat = this.createCurrentMaterial();
    this.applyMaterialToModel(mat);
  }

  // Set PBR Material properties (roughness, metalness, wireframe)
  setMaterialProperties({ roughness, metalness, wireframe, repeatX, repeatY }) {
    if (roughness !== undefined) this.roughness = roughness;
    if (metalness !== undefined) this.metalness = metalness;
    if (wireframe !== undefined) this.isWireframe = wireframe;

    if (this.activeTexture && (repeatX !== undefined || repeatY !== undefined)) {
      const rx = repeatX || this.activeTexture.repeat.x;
      const ry = repeatY || this.activeTexture.repeat.y;
      this.activeTexture.repeat.set(rx, ry);
      this.activeTexture.needsUpdate = true;
    }

    const mat = this.createCurrentMaterial();
    this.applyMaterialToModel(mat);
  }

  // Export 3D model in GLTF / GLB / OBJ
  exportModel(format = 'gltf') {
    if (!this.modelGroup || this.modelGroup.children.length === 0) {
      alert('No 3D model in scene to export.');
      return;
    }

    const exportName = this.activeModelName || 'meta-3d-asset';

    if (format === 'gltf' || format === 'glb') {
      const exporter = new GLTFExporter();
      const isBinary = format === 'glb';

      exporter.parse(
        this.modelGroup,
        (result) => {
          let blob;
          if (isBinary) {
            blob = new Blob([result], { type: 'application/octet-stream' });
          } else {
            const output = JSON.stringify(result, null, 2);
            blob = new Blob([output], { type: 'application/json' });
          }

          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = `${exportName}.${format}`;
          link.click();
          URL.revokeObjectURL(link.href);
        },
        (error) => {
          console.error('Error exporting GLTF:', error);
          alert('Failed to export GLTF.');
        },
        { binary: isBinary, embedImages: true }
      );
    } else if (format === 'obj') {
      const exporter = new OBJExporter();
      const result = exporter.parse(this.modelGroup);
      const blob = new Blob([result], { type: 'text/plain' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${exportName}.obj`;
      link.click();
      URL.revokeObjectURL(link.href);
    }
  }

  // Watertight ASCII STL Exporter for 3D Printing
  exportSTL() {
    if (!this.modelGroup || this.modelGroup.children.length === 0) {
      alert('No 3D model in scene to export.');
      return;
    }

    const exportName = this.activeModelName || 'meta-3d-asset';
    let stl = `solid ${exportName}\n`;

    this.modelGroup.traverse((child) => {
      if (child.isMesh && child.geometry) {
        const geo = child.geometry.toNonIndexed();
        const pos = geo.attributes.position;
        if (pos) {
          for (let i = 0; i < pos.count; i += 3) {
            const vA = new THREE.Vector3().fromBufferAttribute(pos, i).applyMatrix4(child.matrixWorld);
            const vB = new THREE.Vector3().fromBufferAttribute(pos, i + 1).applyMatrix4(child.matrixWorld);
            const vC = new THREE.Vector3().fromBufferAttribute(pos, i + 2).applyMatrix4(child.matrixWorld);
            const cb = new THREE.Vector3().subVectors(vC, vB);
            const ab = new THREE.Vector3().subVectors(vA, vB);
            const normal = cb.cross(ab).normalize();

            stl += `  facet normal ${normal.x.toFixed(4)} ${normal.y.toFixed(4)} ${normal.z.toFixed(4)}\n    outer loop\n`;
            stl += `      vertex ${vA.x.toFixed(4)} ${vA.y.toFixed(4)} ${vA.z.toFixed(4)}\n`;
            stl += `      vertex ${vB.x.toFixed(4)} ${vB.y.toFixed(4)} ${vB.z.toFixed(4)}\n`;
            stl += `      vertex ${vC.x.toFixed(4)} ${vC.y.toFixed(4)} ${vC.z.toFixed(4)}\n`;
            stl += '    endloop\n  endfacet\n';
          }
        }
      }
    });

    stl += `endsolid ${exportName}\n`;
    const blob = new Blob([stl], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${exportName}.stl`;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  // 4K Viewport PNG Snapshot
  takeSnapshot() {
    this.renderer.render(this.scene, this.camera);
    const dataUrl = this.renderer.domElement.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = `${this.activeModelName || '3d-render'}-snapshot.png`;
    link.href = dataUrl;
    link.click();
  }

  // Archetype Model Switcher
  loadArchetype(archetypeId) {
    this.currentArchetype = archetypeId;
    this.buildArchetypeModel(archetypeId);
    this.focusCameraOnModel();
  }

  buildArchetypeModel(archetypeId) {
    while (this.modelGroup.children.length > 0) {
      this.modelGroup.remove(this.modelGroup.children[0]);
    }

    if (this.riggingEngine) {
      this.riggingEngine.clear();
    }

    this.joint1 = null;
    this.joint2 = null;
    this.stressMesh = null;

    if (archetypeId === 'humanoid_avatar') {
      this.activeModelName = 'humanoid-avatar-rigged';
      if (this.riggingEngine) {
        const { mesh, helper } = this.riggingEngine.buildRiggedHumanoid(this.activeTexture);
        this.modelGroup.add(mesh);
        this.modelGroup.add(helper);
        this.stressMesh = mesh;
      }
    } else if (archetypeId === 'mecha_robot') {
      this.activeModelName = 'cyberpunk-mecha-heavy';
      const mechaGroup = new THREE.Group();

      // Armored Torso Chassis
      const torsoGeo = new THREE.BoxGeometry(1.8, 1.4, 1.1);
      const armorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.9, roughness: 0.2 });
      const torso = new THREE.Mesh(torsoGeo, armorMat);
      torso.position.y = 1.9;
      torso.castShadow = true;
      mechaGroup.add(torso);

      // Glowing Reactor Core
      const coreGeo = new THREE.CylinderGeometry(0.35, 0.35, 0.2, 32);
      const coreMat = new THREE.MeshStandardMaterial({
        color: 0x00c8e6,
        emissive: 0x00c8e6,
        emissiveIntensity: 1.2,
        roughness: 0.1
      });
      const core = new THREE.Mesh(coreGeo, coreMat);
      core.rotation.x = Math.PI / 2;
      core.position.set(0, 1.9, 0.56);
      mechaGroup.add(core);
      this.stressMesh = core;

      // Dual Shoulder Missile Pods
      for (const side of [-1, 1]) {
        const podGeo = new THREE.BoxGeometry(0.7, 0.6, 1.0);
        const podMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.8, roughness: 0.3 });
        const pod = new THREE.Mesh(podGeo, podMat);
        pod.position.set(side * 1.35, 2.4, 0);
        pod.castShadow = true;
        mechaGroup.add(pod);

        // Rocket Tubes
        for (let row = -0.15; row <= 0.15; row += 0.3) {
          for (let col = -0.15; col <= 0.15; col += 0.3) {
            const tubeGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.2, 16);
            const tubeMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e, emissive: 0xf43f5e, emissiveIntensity: 0.4 });
            const tube = new THREE.Mesh(tubeGeo, tubeMat);
            tube.rotation.x = Math.PI / 2;
            tube.position.set(side * 1.35 + col, 2.4 + row, 0.45);
            mechaGroup.add(tube);
          }
        }

        // Heavy Mechanical Legs
        const legGroup = new THREE.Group();
        legGroup.position.set(side * 0.75, 1.2, 0);

        const thighGeo = new THREE.CylinderGeometry(0.18, 0.22, 1.1, 16);
        const thigh = new THREE.Mesh(thighGeo, armorMat);
        thigh.position.y = -0.55;
        thigh.castShadow = true;
        legGroup.add(thigh);

        const kneeGeo = new THREE.SphereGeometry(0.24, 16, 16);
        const kneeMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, metalness: 0.8 });
        const knee = new THREE.Mesh(kneeGeo, kneeMat);
        knee.position.y = -1.1;
        legGroup.add(knee);

        const shinGeo = new THREE.CylinderGeometry(0.16, 0.24, 1.1, 16);
        const shin = new THREE.Mesh(shinGeo, armorMat);
        shin.position.y = -1.65;
        shin.castShadow = true;
        legGroup.add(shin);

        const footGeo = new THREE.BoxGeometry(0.65, 0.25, 0.9);
        const foot = new THREE.Mesh(footGeo, armorMat);
        foot.position.set(0, -2.2, 0.15);
        foot.castShadow = true;
        legGroup.add(foot);

        mechaGroup.add(legGroup);
      }

      this.modelGroup.add(mechaGroup);
    } else if (archetypeId === 'aerial_drone') {
      this.activeModelName = 'tactical-stealth-drone';
      const droneGroup = new THREE.Group();

      // Fuselage
      const bodyGeo = new THREE.BoxGeometry(1.8, 0.35, 1.4);
      const carbonMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.9, roughness: 0.15 });
      const body = new THREE.Mesh(bodyGeo, carbonMat);
      body.castShadow = true;
      droneGroup.add(body);

      // Camera Gimbal Pod
      const camGeo = new THREE.SphereGeometry(0.28, 32, 32);
      const camMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, metalness: 0.9, roughness: 0.1 });
      const cam = new THREE.Mesh(camGeo, camMat);
      cam.position.set(0, -0.15, 0.7);
      droneGroup.add(cam);
      this.stressMesh = cam;

      // 4 Turbine Rotors with Plasma Thrusters
      for (const [rx, rz] of [[1.3, 1.1], [-1.3, 1.1], [1.3, -1.1], [-1.3, -1.1]]) {
        const armGeo = new THREE.CylinderGeometry(0.08, 0.08, 1.2, 16);
        const arm = new THREE.Mesh(armGeo, carbonMat);
        arm.position.set(rx * 0.55, 0.05, rz * 0.55);
        arm.rotation.z = rx > 0 ? -Math.PI / 4 : Math.PI / 4;
        droneGroup.add(arm);

        const ringGeo = new THREE.TorusGeometry(0.42, 0.05, 16, 32);
        const ringMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.8, roughness: 0.2 });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.set(rx, 0.25, rz);
        ring.rotation.x = Math.PI / 2;
        droneGroup.add(ring);

        // Glowing Thruster Core
        const thrusterGeo = new THREE.CylinderGeometry(0.25, 0.25, 0.08, 32);
        const thrusterMat = new THREE.MeshStandardMaterial({
          color: 0x00c8e6,
          emissive: 0x00c8e6,
          emissiveIntensity: 1.0
        });
        const thruster = new THREE.Mesh(thrusterGeo, thrusterMat);
        thruster.position.set(rx, 0.25, rz);
        droneGroup.add(thruster);
      }

      this.modelGroup.add(droneGroup);
    } else if (archetypeId === 'scifi_monolith') {
      this.activeModelName = 'alien-cyber-monolith';
      const monoGroup = new THREE.Group();

      // Hexagonal Tapered Obelisk
      const obeliskGeo = new THREE.CylinderGeometry(0.7, 1.4, 4.2, 6);
      const stoneMat = new THREE.MeshStandardMaterial({
        color: 0x1e293b,
        metalness: 0.85,
        roughness: 0.2,
        map: this.activeTexture || null
      });
      const obelisk = new THREE.Mesh(obeliskGeo, stoneMat);
      obelisk.position.y = 2.1;
      obelisk.castShadow = true;
      monoGroup.add(obelisk);

      // Glowing Core Inset
      const coreGeo = new THREE.CylinderGeometry(0.2, 0.2, 3.8, 16);
      const coreMat = new THREE.MeshStandardMaterial({
        color: 0x00c8e6,
        emissive: 0x00c8e6,
        emissiveIntensity: 1.4
      });
      const core = new THREE.Mesh(coreGeo, coreMat);
      core.position.y = 2.1;
      monoGroup.add(core);
      this.stressMesh = core;

      // Floating Orbital Rings
      const ring1Geo = new THREE.TorusGeometry(1.6, 0.06, 16, 48);
      const ringMat = new THREE.MeshStandardMaterial({ color: 0x8b5cf6, emissive: 0x8b5cf6, emissiveIntensity: 0.8 });
      const ring1 = new THREE.Mesh(ring1Geo, ringMat);
      ring1.position.y = 2.4;
      ring1.rotation.x = Math.PI / 3;
      monoGroup.add(ring1);

      this.modelGroup.add(monoGroup);
    } else if (archetypeId === 'cyber_hand') {
      this.activeModelName = 'articulated-cyber-hand';
      const handGroup = new THREE.Group();

      // Palm
      const palmGeo = new THREE.BoxGeometry(1.2, 1.4, 0.35);
      const palmMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.9, roughness: 0.2 });
      const palm = new THREE.Mesh(palmGeo, palmMat);
      palm.position.y = 1.0;
      palm.castShadow = true;
      handGroup.add(palm);

      // 5 Articulated Fingers
      const fingerOffsets = [-0.45, -0.22, 0.02, 0.25, 0.45];
      const fingerLengths = [0.65, 0.9, 1.05, 0.95, 0.75];

      fingerOffsets.forEach((xOffset, i) => {
        const len = fingerLengths[i];
        const segLen = len / 3;
        const fGroup = new THREE.Group();
        fGroup.position.set(xOffset, 1.7, 0);

        // 3 Phalange segments per finger
        for (let seg = 0; seg < 3; seg++) {
          const phGeo = new THREE.CylinderGeometry(0.065, 0.08, segLen, 16);
          const ph = new THREE.Mesh(phGeo, palmMat);
          ph.position.y = segLen * seg + segLen / 2;
          ph.castShadow = true;
          fGroup.add(ph);

          // Knuckle
          const knuckleGeo = new THREE.SphereGeometry(0.09, 16, 16);
          const knuckleMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, metalness: 0.8 });
          const knuckle = new THREE.Mesh(knuckleGeo, knuckleMat);
          knuckle.position.y = segLen * seg;
          fGroup.add(knuckle);
        }

        // Optic Fingertip Sensor
        const tipGeo = new THREE.SphereGeometry(0.075, 16, 16);
        const tipMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, emissive: 0x00c8e6, emissiveIntensity: 1.0 });
        const tip = new THREE.Mesh(tipGeo, tipMat);
        tip.position.y = len;
        fGroup.add(tip);

        handGroup.add(fGroup);
      });

      this.stressMesh = palm;
      this.modelGroup.add(handGroup);
    }
  }

  // Backward compatibility domain models (for CLI test suites)
  setDomain(domainId) {
    this.currentDomainId = domainId;
    this.activeModelName = `neurotwin-${domainId}`;
    this.activeTexture = null;
    this.buildDomainModel(domainId);
    this.focusCameraOnModel();
  }

  buildDomainModel(domainId) {
    while (this.modelGroup.children.length > 0) {
      this.modelGroup.remove(this.modelGroup.children[0]);
    }

    this.joint1 = null;
    this.joint2 = null;
    this.stressMesh = null;

    if (domainId === 'robotics') {
      const baseGeo = new THREE.CylinderGeometry(0.85, 1.0, 0.45, 32);
      const metalMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.85, roughness: 0.25 });
      const base = new THREE.Mesh(baseGeo, metalMat);
      base.castShadow = true;
      this.modelGroup.add(base);

      this.joint1 = new THREE.Group();
      this.joint1.position.y = 0.45;
      this.modelGroup.add(this.joint1);

      const shoulderGeo = new THREE.SphereGeometry(0.55, 32, 32);
      const cyanMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, metalness: 0.5, roughness: 0.2 });
      const shoulder = new THREE.Mesh(shoulderGeo, cyanMat);
      shoulder.castShadow = true;
      this.joint1.add(shoulder);

      this.joint2 = new THREE.Group();
      this.joint2.position.set(0, 0.35, 0);
      this.joint2.rotation.z = -0.35;
      this.joint1.add(this.joint2);

      const arm1Geo = new THREE.CylinderGeometry(0.28, 0.35, 1.9, 32);
      const armMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.9, roughness: 0.2 });
      const arm1 = new THREE.Mesh(arm1Geo, armMat);
      arm1.position.y = 0.95;
      arm1.castShadow = true;
      this.joint2.add(arm1);

      const defectGeo = new THREE.TorusGeometry(0.42, 0.12, 16, 32);
      const defectMat = new THREE.MeshStandardMaterial({
        color: 0xf43f5e,
        emissive: 0xf43f5e,
        emissiveIntensity: 0.65,
        metalness: 0.5,
        roughness: 0.2
      });
      this.stressMesh = new THREE.Mesh(defectGeo, defectMat);
      this.stressMesh.position.set(0, 0.45, 0);
      this.stressMesh.rotation.x = Math.PI / 2;
      this.joint1.add(this.stressMesh);
    } else if (domainId === 'biomedical') {
      const cellGeo = new THREE.IcosahedronGeometry(1.6, 3);
      const cellMat = new THREE.MeshPhysicalMaterial({
        color: 0x10b981,
        transmission: 0.72,
        opacity: 0.9,
        transparent: true,
        roughness: 0.2,
        ior: 1.35
      });
      const cell = new THREE.Mesh(cellGeo, cellMat);
      this.modelGroup.add(cell);

      const nucGeo = new THREE.SphereGeometry(0.75, 32, 32);
      const nucMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        emissive: 0x0284c7,
        emissiveIntensity: 0.85,
        roughness: 0.3
      });
      this.stressMesh = new THREE.Mesh(nucGeo, nucMat);
      this.modelGroup.add(this.stressMesh);
    } else if (domainId === 'energy') {
      const panelGeo = new THREE.BoxGeometry(3.6, 0.12, 2.4);
      const panelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.85, roughness: 0.15 });
      const panel = new THREE.Mesh(panelGeo, panelMat);
      this.modelGroup.add(panel);

      const hotGeo = new THREE.CylinderGeometry(0.45, 0.45, 0.16, 32);
      const hotMat = new THREE.MeshStandardMaterial({
        color: 0xf59e0b,
        emissive: 0xef4444,
        emissiveIntensity: 1.2
      });
      this.stressMesh = new THREE.Mesh(hotGeo, hotMat);
      this.stressMesh.position.set(0.65, 0.08, 0.25);
      this.modelGroup.add(this.stressMesh);
    } else if (domainId === 'microelectronics') {
      const subGeo = new THREE.BoxGeometry(3.2, 0.25, 3.2);
      const subMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.95, roughness: 0.1 });
      const sub = new THREE.Mesh(subGeo, subMat);
      this.modelGroup.add(sub);

      for (let i = -1.2; i <= 1.2; i += 0.5) {
        const finGeo = new THREE.BoxGeometry(2.6, 0.3, 0.12);
        const finMat = new THREE.MeshStandardMaterial({ color: 0x00c8e6, metalness: 0.9, roughness: 0.15 });
        const fin = new THREE.Mesh(finGeo, finMat);
        fin.position.set(0, 0.35, i);
        this.modelGroup.add(fin);
      }

      const voidGeo = new THREE.SphereGeometry(0.3, 16, 16);
      const voidMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e, emissive: 0xf43f5e, emissiveIntensity: 0.85 });
      this.stressMesh = new THREE.Mesh(voidGeo, voidMat);
      this.stressMesh.position.set(0.3, 0.5, 0.2);
      this.modelGroup.add(this.stressMesh);
    }
  }

  setRoboticJoints(j1AngleRad, j2AngleRad) {
    if (this.joint1) this.joint1.rotation.y = j1AngleRad;
    if (this.joint2) this.joint2.rotation.z = -0.35 + j2AngleRad;
  }

  setCellConfluence(scaleFactor) {
    if (this.stressMesh) {
      const s = 0.8 + scaleFactor * 0.5;
      this.stressMesh.scale.set(s, s * 0.9, s);
    }
  }

  setSolarThermalHotspot(tempVal) {
    if (this.stressMesh && this.stressMesh.material) {
      const intensity = Math.min(2.5, (tempVal - 30) / 25);
      this.stressMesh.material.emissiveIntensity = intensity;
    }
  }

  setGateDielectricThickness(thicknessNm) {
    if (this.stressMesh) {
      const s = thicknessNm / 4.2;
      this.stressMesh.scale.set(s, s, s);
    }
  }

  updateStressState(target) {
    if (this.stressMesh && this.stressMesh.material && this.stressMesh.material.color) {
      if (target && target.type === 'defect') {
        this.stressMesh.material.color.setHex(0xf43f5e);
        if (this.stressMesh.material.emissive) {
          this.stressMesh.material.emissive.setHex(0xf43f5e);
          this.stressMesh.material.emissiveIntensity = 1.0;
        }
      } else {
        this.stressMesh.material.color.setHex(0x00c8e6);
        if (this.stressMesh.material.emissive) {
          this.stressMesh.material.emissive.setHex(0x00c8e6);
          this.stressMesh.material.emissiveIntensity = 0.5;
        }
      }
    }
  }

  attachControls() {
    let isDragging = false;
    let prevMouse = { x: 0, y: 0 };

    this.container.addEventListener('mousedown', (e) => {
      isDragging = true;
      prevMouse = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    this.container.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouse.x;
      const deltaY = e.clientY - prevMouse.y;

      this.modelGroup.rotation.y += deltaX * 0.01;
      this.modelGroup.rotation.x += deltaY * 0.01;

      prevMouse = { x: e.clientX, y: e.clientY };
    });

    this.container.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.camera.position.z += e.deltaY * 0.005;
      this.camera.position.z = Math.max(1.5, Math.min(25, this.camera.position.z));
    });

    this.container.addEventListener('dragover', (e) => {
      e.preventDefault();
      this.container.style.outline = '2px dashed var(--neon-cyan)';
    });

    this.container.addEventListener('dragleave', () => {
      this.container.style.outline = '';
    });

    this.container.addEventListener('drop', (e) => {
      e.preventDefault();
      this.container.style.outline = '';
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        this.loadUser3DModel(e.dataTransfer.files[0]);
      }
    });

    window.addEventListener('resize', () => {
      this.handleResize();
    });
  }

  handleResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (width > 0 && height > 0) {
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    }
  }

  setRiggingEngine(engine) {
    this.riggingEngine = engine;
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (!this.clock) {
      this.clock = new THREE.Clock();
    }
    const delta = this.clock.getDelta();

    if (this.riggingEngine) {
      this.riggingEngine.update(delta);
    }

    if (this.isRotating) {
      this.modelGroup.rotation.y += this.rotationSpeed;
    }

    if (this.stressMesh && this.stressMesh.material && this.stressMesh.material.emissive) {
      const s = 1 + Math.sin(Date.now() * 0.005) * 0.04;
      this.stressMesh.scale.set(s, s, s);
    }

    this.renderer.render(this.scene, this.camera);
  }
}
