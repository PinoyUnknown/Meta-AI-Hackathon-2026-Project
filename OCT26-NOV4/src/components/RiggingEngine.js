// Auto-Rigging & Skeletal Animation Studio Engine
import * as THREE from 'three';

export class RiggingEngine {
  constructor(scene) {
    this.scene = scene;
    this.bones = {};
    this.boneList = [];
    this.skeleton = null;
    this.skinnedMesh = null;
    this.skeletonHelper = null;
    this.mixer = null;
    this.clips = {};
    this.activeAction = null;
    this.isPlaying = true;
    this.speed = 1.0;
    this.isRigged = false;
    this.showArmature = true;
  }

  // Build a fully articulated 17-bone Humanoid Rig
  buildRiggedHumanoid(texture = null) {
    // 1. Construct Hierarchical Bone Tree
    const root = new THREE.Bone();
    root.name = 'Root';
    root.position.set(0, 0, 0);

    const pelvis = new THREE.Bone();
    pelvis.name = 'Pelvis';
    pelvis.position.set(0, 1.3, 0);
    root.add(pelvis);

    const spine = new THREE.Bone();
    spine.name = 'Spine';
    spine.position.set(0, 0.45, 0);
    pelvis.add(spine);

    const chest = new THREE.Bone();
    chest.name = 'Chest';
    chest.position.set(0, 0.45, 0);
    spine.add(chest);

    const neck = new THREE.Bone();
    neck.name = 'Neck';
    neck.position.set(0, 0.35, 0);
    chest.add(neck);

    const head = new THREE.Bone();
    head.name = 'Head';
    head.position.set(0, 0.3, 0);
    neck.add(head);

    // Left Arm Hierarchy
    const leftShoulder = new THREE.Bone();
    leftShoulder.name = 'LeftShoulder';
    leftShoulder.position.set(0.45, 0.35, 0);
    chest.add(leftShoulder);

    const leftArm = new THREE.Bone();
    leftArm.name = 'LeftArm';
    leftArm.position.set(0.4, -0.05, 0);
    leftShoulder.add(leftArm);

    const leftForearm = new THREE.Bone();
    leftForearm.name = 'LeftForearm';
    leftForearm.position.set(0.45, 0, 0);
    leftArm.add(leftForearm);

    const leftHand = new THREE.Bone();
    leftHand.name = 'LeftHand';
    leftHand.position.set(0.35, 0, 0);
    leftForearm.add(leftHand);

    // Right Arm Hierarchy
    const rightShoulder = new THREE.Bone();
    rightShoulder.name = 'RightShoulder';
    rightShoulder.position.set(-0.45, 0.35, 0);
    chest.add(rightShoulder);

    const rightArm = new THREE.Bone();
    rightArm.name = 'RightArm';
    rightArm.position.set(-0.4, -0.05, 0);
    rightShoulder.add(rightArm);

    const rightForearm = new THREE.Bone();
    rightForearm.name = 'RightForearm';
    rightForearm.position.set(-0.45, 0, 0);
    rightArm.add(rightForearm);

    const rightHand = new THREE.Bone();
    rightHand.name = 'RightHand';
    rightHand.position.set(-0.35, 0, 0);
    rightForearm.add(rightHand);

    // Left Leg Hierarchy
    const leftHip = new THREE.Bone();
    leftHip.name = 'LeftHip';
    leftHip.position.set(0.25, -0.1, 0);
    pelvis.add(leftHip);

    const leftKnee = new THREE.Bone();
    leftKnee.name = 'LeftKnee';
    leftKnee.position.set(0, -0.65, 0);
    leftHip.add(leftKnee);

    const leftFoot = new THREE.Bone();
    leftFoot.name = 'LeftFoot';
    leftFoot.position.set(0, -0.65, 0.1);
    leftKnee.add(leftFoot);

    // Right Leg Hierarchy
    const rightHip = new THREE.Bone();
    rightHip.name = 'RightHip';
    rightHip.position.set(-0.25, -0.1, 0);
    pelvis.add(rightHip);

    const rightKnee = new THREE.Bone();
    rightKnee.name = 'RightKnee';
    rightKnee.position.set(0, -0.65, 0);
    rightHip.add(rightKnee);

    const rightFoot = new THREE.Bone();
    rightFoot.name = 'RightFoot';
    rightFoot.position.set(0, -0.65, 0.1);
    rightKnee.add(rightFoot);

    this.boneList = [
      root, pelvis, spine, chest, neck, head,
      leftShoulder, leftArm, leftForearm, leftHand,
      rightShoulder, rightArm, rightForearm, rightHand,
      leftHip, leftKnee, leftFoot,
      rightHip, rightKnee, rightFoot
    ];

    this.boneList.forEach((b, idx) => {
      this.bones[b.name] = b;
      b.userData.index = idx;
    });

    this.skeleton = new THREE.Skeleton(this.boneList);

    // 2. Build Bipedal Skinned Mesh Geometry
    const geometry = new THREE.CylinderGeometry(0.35, 0.35, 2.9, 16, 24);
    const position = geometry.attributes.position;
    const skinIndices = [];
    const skinWeights = [];

    // Assign vertex bone skinning weights based on Y-height and X-symmetry
    for (let i = 0; i < position.count; i++) {
      const y = position.getY(i) + 1.45; // Offset to 0-3m
      const x = position.getX(i);

      if (y > 2.5) {
        // Head / Neck
        skinIndices.push(this.bones['Head'].userData.index, this.bones['Neck'].userData.index, 0, 0);
        skinWeights.push(0.8, 0.2, 0, 0);
      } else if (y > 2.0) {
        // Chest / Shoulders
        if (x > 0.15) {
          skinIndices.push(this.bones['LeftShoulder'].userData.index, this.bones['Chest'].userData.index, 0, 0);
          skinWeights.push(0.65, 0.35, 0, 0);
        } else if (x < -0.15) {
          skinIndices.push(this.bones['RightShoulder'].userData.index, this.bones['Chest'].userData.index, 0, 0);
          skinWeights.push(0.65, 0.35, 0, 0);
        } else {
          skinIndices.push(this.bones['Chest'].userData.index, this.bones['Spine'].userData.index, 0, 0);
          skinWeights.push(0.7, 0.3, 0, 0);
        }
      } else if (y > 1.3) {
        // Spine / Pelvis
        skinIndices.push(this.bones['Spine'].userData.index, this.bones['Pelvis'].userData.index, 0, 0);
        skinWeights.push(0.6, 0.4, 0, 0);
      } else if (y > 0.65) {
        // Thighs / Hips
        if (x >= 0) {
          skinIndices.push(this.bones['LeftHip'].userData.index, this.bones['LeftKnee'].userData.index, 0, 0);
          skinWeights.push(0.7, 0.3, 0, 0);
        } else {
          skinIndices.push(this.bones['RightHip'].userData.index, this.bones['RightKnee'].userData.index, 0, 0);
          skinWeights.push(0.7, 0.3, 0, 0);
        }
      } else {
        // Knees / Feet
        if (x >= 0) {
          skinIndices.push(this.bones['LeftKnee'].userData.index, this.bones['LeftFoot'].userData.index, 0, 0);
          skinWeights.push(0.6, 0.4, 0, 0);
        } else {
          skinIndices.push(this.bones['RightKnee'].userData.index, this.bones['RightFoot'].userData.index, 0, 0);
          skinWeights.push(0.6, 0.4, 0, 0);
        }
      }
    }

    geometry.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(skinIndices, 4));
    geometry.setAttribute('skinWeight', new THREE.Float32BufferAttribute(skinWeights, 4));
    geometry.computeVertexNormals();

    // 3. Create PBR Material
    const material = new THREE.MeshStandardMaterial({
      color: texture ? 0xffffff : 0xd6dbe4,
      metalness: 0.3,
      roughness: 0.4,
      map: texture || null
    });

    this.skinnedMesh = new THREE.SkinnedMesh(geometry, material);
    this.skinnedMesh.add(root);
    this.skinnedMesh.bind(this.skeleton);
    this.skinnedMesh.castShadow = true;
    this.skinnedMesh.receiveShadow = true;

    // 4. Skeleton Helper (Armature visualizer matching Blender 3D bone view)
    this.skeletonHelper = new THREE.SkeletonHelper(this.skinnedMesh);
    this.skeletonHelper.material.linewidth = 2;
    this.skeletonHelper.visible = this.showArmature;

    // 5. Build Animation Mixer & Cycles
    this.mixer = new THREE.AnimationMixer(this.skinnedMesh);
    this.createAnimationClips();

    this.isRigged = true;
    return {
      mesh: this.skinnedMesh,
      helper: this.skeletonHelper
    };
  }

  // Create built-in procedural animation cycles
  createAnimationClips() {
    const times = [0, 0.5, 1.0, 1.5, 2.0];

    // Helper to generate quaternion track for bone rotation
    const makeQuatTrack = (boneName, eulerAngles) => {
      const values = [];
      const q = new THREE.Quaternion();
      for (const [x, y, z] of eulerAngles) {
        q.setFromEuler(new THREE.Euler(x, y, z));
        values.push(q.x, q.y, q.z, q.w);
      }
      return new THREE.QuaternionKeyframeTrack(`${boneName}.quaternion`, times, values);
    };

    // 1. Idle Breathing Cycle
    const idleTracks = [
      makeQuatTrack('Chest', [
        [0, 0, 0],
        [0.05, 0, 0],
        [0, 0, 0],
        [-0.04, 0, 0],
        [0, 0, 0]
      ]),
      makeQuatTrack('LeftArm', [
        [0, 0, 0.15],
        [0.05, 0, 0.2],
        [0, 0, 0.15],
        [-0.03, 0, 0.12],
        [0, 0, 0.15]
      ]),
      makeQuatTrack('RightArm', [
        [0, 0, -0.15],
        [0.05, 0, -0.2],
        [0, 0, -0.15],
        [-0.03, 0, -0.12],
        [0, 0, -0.15]
      ]),
      makeQuatTrack('Head', [
        [0, 0, 0],
        [0.03, 0.05, 0],
        [0, 0, 0],
        [-0.02, -0.05, 0],
        [0, 0, 0]
      ])
    ];
    this.clips['idle'] = new THREE.AnimationClip('idle', 2.0, idleTracks);

    // 2. Locomotion / Walk Cycle
    const walkTracks = [
      makeQuatTrack('LeftHip', [
        [-0.35, 0, 0],
        [0, 0, 0],
        [0.35, 0, 0],
        [0, 0, 0],
        [-0.35, 0, 0]
      ]),
      makeQuatTrack('RightHip', [
        [0.35, 0, 0],
        [0, 0, 0],
        [-0.35, 0, 0],
        [0, 0, 0],
        [0.35, 0, 0]
      ]),
      makeQuatTrack('LeftArm', [
        [0.3, 0, 0.1],
        [0, 0, 0.1],
        [-0.3, 0, 0.1],
        [0, 0, 0.1],
        [0.3, 0, 0.1]
      ]),
      makeQuatTrack('RightArm', [
        [-0.3, 0, -0.1],
        [0, 0, -0.1],
        [0.3, 0, -0.1],
        [0, 0, -0.1],
        [-0.3, 0, -0.1]
      ]),
      makeQuatTrack('Spine', [
        [0, 0.08, 0],
        [0, 0, 0],
        [0, -0.08, 0],
        [0, 0, 0],
        [0, 0.08, 0]
      ])
    ];
    this.clips['walk'] = new THREE.AnimationClip('walk', 2.0, walkTracks);

    // 3. Kinematic Range-of-Motion Sweep
    const kinematicTracks = [
      makeQuatTrack('LeftArm', [
        [0, 0, 0],
        [Math.PI / 2, 0, 0.3],
        [Math.PI * 0.9, 0, 0],
        [Math.PI / 2, 0, -0.2],
        [0, 0, 0]
      ]),
      makeQuatTrack('RightArm', [
        [0, 0, 0],
        [-Math.PI / 2, 0, -0.3],
        [-Math.PI * 0.9, 0, 0],
        [-Math.PI / 2, 0, 0.2],
        [0, 0, 0]
      ]),
      makeQuatTrack('Head', [
        [0, -0.6, 0],
        [0, 0, 0],
        [0, 0.6, 0],
        [0, 0, 0],
        [0, -0.6, 0]
      ])
    ];
    this.clips['kinematic'] = new THREE.AnimationClip('kinematic', 2.0, kinematicTracks);

    // Start with Idle
    this.playClip('idle');
  }

  playClip(clipName) {
    if (!this.mixer || !this.clips[clipName]) return;

    if (this.activeAction) {
      this.activeAction.fadeOut(0.3);
    }

    const action = this.mixer.clipAction(this.clips[clipName]);
    action.reset();
    action.fadeIn(0.3);
    action.play();
    this.activeAction = action;
  }

  stopAllAnimations() {
    if (this.mixer) {
      this.mixer.stopAllAction();
      this.activeAction = null;
    }
  }

  setSpeed(speedVal) {
    this.speed = speedVal;
    if (this.mixer) {
      this.mixer.timeScale = speedVal;
    }
  }

  setArmatureVisible(visible) {
    this.showArmature = visible;
    if (this.skeletonHelper) {
      this.skeletonHelper.visible = visible;
    }
  }

  // Manual bone pose rotation
  setBoneRotation(boneName, xRad, yRad, zRad) {
    const bone = this.bones[boneName];
    if (bone) {
      if (xRad !== undefined) bone.rotation.x = xRad;
      if (yRad !== undefined) bone.rotation.y = yRad;
      if (zRad !== undefined) bone.rotation.z = zRad;
    }
  }

  update(delta) {
    if (this.mixer && this.isPlaying) {
      this.mixer.update(delta);
    }
    if (this.skeletonHelper && this.skeletonHelper.visible) {
      this.skeletonHelper.update();
    }
  }
}
