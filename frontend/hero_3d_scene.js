/**
 * RituIQ - Living 3D Agricultural Landscape Scene (Three.js WebGL Engine)
 * Realistic, Weather-Responsive 3D Village & Farm Experience
 * 
 * Environments Supported:
 *  - ☀️ Sunny (Golden Sunlight, Pollen Motes, Crisp Shadows)
 *  - 🌧️ Rain (Rain Streaks, Wet Reflective Soil, Distant Mist)
 *  - ⛈️ Storm (Heavy Rain, Lightning Flashes, Strong Wind Sway)
 *  - ☁️ Cloudy (Diffused Soft Light, Overcast Sky, Moving Cloud Puffs)
 *  - 🌫️ Fog (Atmospheric Volumetric Fog, Sharp Foreground, Faded Mountains)
 *  - 🌙 Night (Moonlight, Midnight Sky, Warm Village Lanterns)
 */

(function () {
  'use strict';

  // Weather Presets Configuration
  const WEATHER_PRESETS = {
    sunny: {
      name: '☀️ खिली धूप (Sunny Farmland)',
      temp: '29°C',
      humidity: '56%',
      rainProb: '8%',
      wind: '11 km/h WNW',
      skyTop: 0x60a5fa, // Bright Indian daylight sky
      skyBottom: 0xfef08a,
      sunColor: 0xfffbeb,
      sunIntensity: 1.55,
      hemiSky: 0xdbeafe,
      hemiGround: 0x65a30d,
      hemiIntensity: 1.05,
      fogColor: 0x93c5fd,
      fogDensity: 0.006,
      rainCount: 0,
      pollenActive: true,
      lightningActive: false,
      windSpeed: 1.2,
      windAngle: 0.08,
      soilRoughness: 0.82,
      soilMetalness: 0.05,
      soilColor: 0x543821,
      cropColor: 0x4ade80, // Vibrant lush agricultural green
      villageLightIntensity: 0.0
    },
    rain: {
      name: '🌧️ मानसूनी वर्षा (Monsoon Rain)',
      temp: '25°C',
      humidity: '88%',
      rainProb: '92%',
      wind: '18 km/h SW',
      skyTop: 0x334155,
      skyBottom: 0x64748b,
      sunColor: 0x94a3b8,
      sunIntensity: 0.45,
      hemiSky: 0x64748b,
      hemiGround: 0x1e3a1e,
      hemiIntensity: 0.55,
      fogColor: 0x64748b,
      fogDensity: 0.026,
      rainCount: 1400,
      pollenActive: false,
      lightningActive: false,
      windSpeed: 2.5,
      windAngle: 0.18,
      soilRoughness: 0.22, // Wet reflective soil puddles
      soilMetalness: 0.35,
      soilColor: 0x27190d,
      cropColor: 0x166534,
      villageLightIntensity: 0.4
    },
    storm: {
      name: '⛈️ चक्रवाती तूफान (Cyclone / Heavy Squall)',
      temp: '23°C',
      humidity: '96%',
      rainProb: '100%',
      wind: '38 km/h S',
      skyTop: 0x0f172a,
      skyBottom: 0x1e293b,
      sunColor: 0x475569,
      sunIntensity: 0.25,
      hemiSky: 0x334155,
      hemiGround: 0x142b14,
      hemiIntensity: 0.4,
      fogColor: 0x1e293b,
      fogDensity: 0.042,
      rainCount: 2200,
      pollenActive: false,
      lightningActive: true,
      windSpeed: 4.8,
      windAngle: 0.35,
      soilRoughness: 0.15,
      soilMetalness: 0.45,
      soilColor: 0x1a1109,
      cropColor: 0x14532d,
      villageLightIntensity: 0.6
    },
    cloudy: {
      name: '☁️ सघन बादलों का डेरा (Overcast Clouds)',
      temp: '26°C',
      humidity: '74%',
      rainProb: '42%',
      wind: '14 km/h W',
      skyTop: 0x64748b,
      skyBottom: 0x94a3b8,
      sunColor: 0xd1d5db,
      sunIntensity: 0.7,
      hemiSky: 0x94a3b8,
      hemiGround: 0x365314,
      hemiIntensity: 0.65,
      fogColor: 0x94a3b8,
      fogDensity: 0.016,
      rainCount: 0,
      pollenActive: false,
      lightningActive: false,
      windSpeed: 1.6,
      windAngle: 0.12,
      soilRoughness: 0.82,
      soilMetalness: 0.08,
      soilColor: 0x3d2612,
      cropColor: 0x4d7c0f,
      villageLightIntensity: 0.2
    },
    fog: {
      name: '🌫️ घना शीतकालीन कोहरा (Dense Rural Mist)',
      temp: '17°C',
      humidity: '94%',
      rainProb: '20%',
      wind: '5 km/h NE',
      skyTop: 0x94a3b8,
      skyBottom: 0xe2e8f0,
      sunColor: 0xffedd5,
      sunIntensity: 0.5,
      hemiSky: 0xcbd5e1,
      hemiGround: 0x2d4818,
      hemiIntensity: 0.6,
      fogColor: 0xd6dee8,
      fogDensity: 0.065, // Volumetric mist that hides distant mountains
      rainCount: 0,
      pollenActive: false,
      lightningActive: false,
      windSpeed: 0.7,
      windAngle: 0.05,
      soilRoughness: 0.55,
      soilMetalness: 0.15,
      soilColor: 0x362110,
      cropColor: 0x3f6212,
      villageLightIntensity: 0.8
    },
    night: {
      name: '🌙 शांत ग्रामीण रात्रि (Peaceful Rural Night)',
      temp: '21°C',
      humidity: '72%',
      rainProb: '12%',
      wind: '7 km/h NW',
      skyTop: 0x030712,
      skyBottom: 0x0f172a,
      sunColor: 0x7dd3fc, // Cool silvery moonlight
      sunIntensity: 0.45,
      hemiSky: 0x1e293b,
      hemiGround: 0x0a1a0d,
      hemiIntensity: 0.35,
      fogColor: 0x0b1322,
      fogDensity: 0.022,
      rainCount: 0,
      pollenActive: false,
      lightningActive: false,
      windSpeed: 1.0,
      windAngle: 0.07,
      soilRoughness: 0.7,
      soilMetalness: 0.1,
      soilColor: 0x1c130b,
      cropColor: 0x166534,
      villageLightIntensity: 1.2 // Warm glowing lanterns in huts
    }
  };

  // State Variables
  let scene, camera, renderer, clock;
  let terrainMesh, soilMaterial, cropMaterial;
  let cropsGroup, treesGroup, villageGroup, mountainsGroup;
  let farmerGroup, oxenGroup, cloudPuffsGroup;
  let sunLight, hemiLight, villageLights = [];
  let rainSystem, rainGeometry, rainPositions, rainVelocities;
  let pollenSystem, pollenGeometry, pollenPositions;
  let skyDomeMesh, skyDomeMaterial;

  const curHour = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Kolkata' })).getHours();
  const isNightInitial = (curHour < 6 || curHour >= 18);
  let currentPreset = isNightInitial ? WEATHER_PRESETS.night : WEATHER_PRESETS.sunny;
  let targetPreset = isNightInitial ? WEATHER_PRESETS.night : WEATHER_PRESETS.sunny;
  let transitionProgress = 1.0;
  const TRANSITION_SPEED = 0.035;

  let mouseX = 0, mouseY = 0;
  let targetCamX = 0, targetCamY = 6.2;
  let curCamX = 0, curCamY = 6.2;

  let lightningTimer = 0;
  let nextLightningTime = 3.0;

  // -------------------------------------------------------------------------
  // INITIALIZATION
  // -------------------------------------------------------------------------
  function initHero3DScene() {
    const container = document.getElementById('hero3dCanvasContainer');
    if (!container) return;

    if (typeof THREE === 'undefined') {
      console.warn('Three.js library is not loaded. Skipping 3D hero scene.');
      return;
    }

    // Clean previous if re-init
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }

    const width = container.clientWidth || 1100;
    const height = container.clientHeight || 480;

    clock = new THREE.Clock();

    // 1. Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(currentPreset.fogColor, currentPreset.fogDensity);

    // 2. Camera
    camera = new THREE.PerspectiveCamera(40, width / height, 0.5, 350);
    camera.position.set(0, 6.2, 19.5);
    camera.lookAt(0, 2.2, 0);

    // 3. Renderer
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance'
      });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.05;
      container.appendChild(renderer.domElement);
    } catch (e) {
      console.warn('WebGL not supported:', e);
      return;
    }

    // 4. Build Environment Elements
    createSkyBackdrop();
    createLighting();
    createFarmlandTerrain();
    createCropRows();
    createFarmerAndOxenTeam();
    createVillageHuts();
    createTreesAndFlora();
    createDistantMountains();
    createRainParticles();
    createPollenParticles();
    createCloudVolumes();

    // 5. Mouse Parallax Listeners
    const banner = document.getElementById('heroBanner3D') || container;
    banner.addEventListener('mousemove', onBannerMouseMove);
    banner.addEventListener('mouseleave', () => {
      mouseX = 0;
      mouseY = 0;
    });

    // 6. Window Resize
    window.addEventListener('resize', onWindowResize);

    // 7. Start Animation Loop
    animate();

    // 8. Apply live weather state (Night vs Sunny)
    setHeroWeatherState(isNightInitial ? 'night' : 'sunny');

    console.log('🌾 RituIQ 3D Living Farm Landscape Initialized.');
  }

  // -------------------------------------------------------------------------
  // 1. SKY BACKDROP DOME
  // -------------------------------------------------------------------------
  function createSkyBackdrop() {
    scene.background = new THREE.Color(currentPreset.skyTop);
    const skyGeo = new THREE.SphereGeometry(180, 24, 16);
    skyDomeMaterial = new THREE.MeshBasicMaterial({
      color: currentPreset.skyTop,
      side: THREE.BackSide,
      depthWrite: false
    });
    skyDomeMesh = new THREE.Mesh(skyGeo, skyDomeMaterial);
    scene.add(skyDomeMesh);
  }

  // -------------------------------------------------------------------------
  // 2. LIGHTING SETUP
  // -------------------------------------------------------------------------
  function createLighting() {
    // Hemisphere Light (Sky + Ground bounce)
    hemiLight = new THREE.HemisphereLight(
      currentPreset.hemiSky,
      currentPreset.hemiGround,
      currentPreset.hemiIntensity
    );
    hemiLight.position.set(0, 50, 0);
    scene.add(hemiLight);

    // Directional Sunlight / Moonlight
    sunLight = new THREE.DirectionalLight(currentPreset.sunColor, currentPreset.sunIntensity);
    sunLight.position.set(22, 28, 16);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 80;
    const d = 20;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);
  }

  // -------------------------------------------------------------------------
  // 3. FARMLAND TERRAIN & FURROW ROWS
  // -------------------------------------------------------------------------
  function createFarmlandTerrain() {
    const geo = new THREE.PlaneGeometry(75, 60, 70, 60);
    geo.rotateX(-Math.PI / 2);

    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i);
      const z = pos.getZ(i);

      // Natural agricultural slope and terraces
      let y = Math.sin(x * 0.08) * 1.3 + Math.cos(z * 0.07) * 1.5 - z * 0.16;

      // Cultivated field furrows (rows running along the field)
      const furrow = Math.sin(x * 1.25 + z * 0.22) * 0.24;
      y += furrow;

      // Higher terrace ridges on boundaries
      if (Math.abs(x) > 16) {
        y += Math.pow((Math.abs(x) - 16) * 0.28, 1.8);
      }

      pos.setY(i, y);
    }
    geo.computeVertexNormals();

    soilMaterial = new THREE.MeshStandardMaterial({
      color: currentPreset.soilColor,
      roughness: currentPreset.soilRoughness,
      metalness: currentPreset.soilMetalness,
      flatShading: false
    });

    terrainMesh = new THREE.Mesh(geo, soilMaterial);
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }

  // -------------------------------------------------------------------------
  // 4. DENSE CROP ROWS (PADDY / WHEAT FIELDS)
  // -------------------------------------------------------------------------
  function createCropRows() {
    cropsGroup = new THREE.Group();

    // Create a base single crop tuft geometry
    const stalkGeo = new THREE.CylinderGeometry(0.02, 0.05, 0.85, 4);
    stalkGeo.translate(0, 0.42, 0);

    cropMaterial = new THREE.MeshStandardMaterial({
      color: currentPreset.cropColor,
      roughness: 0.65,
      metalness: 0.1
    });

    // Populate crop rows along the field contours
    const rowCount = 24;
    const cropsPerRow = 22;

    for (let r = 0; r < rowCount; r++) {
      const zRow = -16 + r * 1.1;
      const xOffset = Math.sin(r * 0.5) * 0.6;

      for (let c = 0; c < cropsPerRow; c++) {
        const xPos = -14 + c * 1.35 + (r % 2) * 0.25 + xOffset;

        // Skip middle furrow area where farmer and oxen work
        if (xPos > -4.5 && xPos < 1.0 && zRow > -1 && zRow < 6) {
          continue;
        }

        const tuft = new THREE.Group();

        // 3-4 blades per tuft with slight tilt
        for (let b = 0; b < 3; b++) {
          const blade = new THREE.Mesh(stalkGeo, cropMaterial);
          const angle = (b * Math.PI * 2) / 3 + Math.random() * 0.4;
          const tilt = 0.15 + Math.random() * 0.2;
          blade.rotation.set(Math.sin(angle) * tilt, angle, Math.cos(angle) * tilt);
          const scaleY = 0.8 + Math.random() * 0.45;
          blade.scale.set(1, scaleY, 1);
          blade.castShadow = (r < 10);
          tuft.add(blade);
        }

        // Calculate ground height at this (x, z)
        const groundY = getTerrainHeight(xPos, zRow);
        tuft.position.set(xPos, groundY, zRow);
        tuft.userData = {
          baseX: xPos,
          baseZ: zRow,
          swayOffset: xPos * 0.7 + zRow * 0.5 + Math.random()
        };

        cropsGroup.add(tuft);
      }
    }

    scene.add(cropsGroup);
  }

  // -------------------------------------------------------------------------
  // 5. 3D FARMER & PAIR OF INDIAN OXEN (BULLOCKS) WITH PLOW
  // -------------------------------------------------------------------------
  function createFarmerAndOxenTeam() {
    const teamGroup = new THREE.Group();
    teamGroup.position.set(-2.4, 1.45, 3.4);
    teamGroup.scale.set(1.35, 1.35, 1.35);
    teamGroup.rotation.y = -0.22; // Angled working across the terrace

    // Materials
    const oxBodyMat = new THREE.MeshStandardMaterial({ color: 0xededed, roughness: 0.7 });
    const oxHornMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 });
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.85 });
    const turbanMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.6 }); // Traditional orange pagdi
    const skinMat = new THREE.MeshStandardMaterial({ color: 0xc2785c, roughness: 0.7 });
    const clothMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.8 });

    // Function to build a single Indian Bullock (Zebu cattle)
    function buildBullock(xOffset) {
      const bullock = new THREE.Group();
      bullock.position.set(xOffset, 0, 0);

      // Torso
      const bodyGeo = new THREE.BoxGeometry(0.85, 0.9, 1.8);
      const body = new THREE.Mesh(bodyGeo, oxBodyMat);
      body.position.y = 0.9;
      body.castShadow = true;
      bullock.add(body);

      // Zebu Hump (कूबड़) - distinctive Indian breed feature
      const humpGeo = new THREE.SphereGeometry(0.35, 8, 8);
      humpGeo.scale(0.8, 1.1, 0.9);
      const hump = new THREE.Mesh(humpGeo, oxBodyMat);
      hump.position.set(0, 1.5, 0.45);
      hump.castShadow = true;
      bullock.add(hump);

      // Head & Neck
      const headGroup = new THREE.Group();
      headGroup.position.set(0, 1.25, 1.0);

      const headGeo = new THREE.BoxGeometry(0.45, 0.5, 0.7);
      const head = new THREE.Mesh(headGeo, oxBodyMat);
      head.position.set(0, 0, 0.25);
      head.rotation.x = 0.2;
      headGroup.add(head);

      // Horns (Curved Upwards)
      [-0.22, 0.22].forEach((hX) => {
        const hornGeo = new THREE.ConeGeometry(0.06, 0.45, 5);
        hornGeo.translate(0, 0.22, 0);
        const horn = new THREE.Mesh(hornGeo, oxHornMat);
        horn.position.set(hX, 0.25, 0.2);
        horn.rotation.set(0.35, 0, hX > 0 ? -0.4 : 0.4);
        headGroup.add(horn);
      });

      bullock.add(headGroup);

      // 4 Legs
      const legGeo = new THREE.BoxGeometry(0.2, 0.85, 0.2);
      legGeo.translate(0, -0.42, 0);
      const legs = [];
      const legCoords = [
        [-0.3, 0.5, 0.6], [0.3, 0.5, 0.6],
        [-0.3, 0.5, -0.6], [0.3, 0.5, -0.6]
      ];
      legCoords.forEach((coord, idx) => {
        const leg = new THREE.Mesh(legGeo, oxBodyMat);
        leg.position.set(coord[0], coord[1], coord[2]);
        leg.castShadow = true;
        bullock.add(leg);
        legs.push(leg);
      });

      bullock.userData = { legs: legs, headGroup: headGroup };
      return bullock;
    }

    // Pair of Oxen (Left & Right)
    const leftOx = buildBullock(-0.65);
    const rightOx = buildBullock(0.65);
    oxenGroup = new THREE.Group();
    oxenGroup.add(leftOx);
    oxenGroup.add(rightOx);
    teamGroup.add(oxenGroup);

    // Wooden Yoke (जूआ) across both bullocks' necks
    const yokeGeo = new THREE.BoxGeometry(2.1, 0.12, 0.16);
    const yoke = new THREE.Mesh(yokeGeo, woodMat);
    yoke.position.set(0, 1.45, 0.45);
    yoke.castShadow = true;
    teamGroup.add(yoke);

    // Central Plow Beam (हरीस)
    const beamGeo = new THREE.CylinderGeometry(0.06, 0.06, 3.2, 5);
    beamGeo.rotateX(Math.PI / 2);
    const beam = new THREE.Mesh(beamGeo, woodMat);
    beam.position.set(0, 0.8, -1.1);
    beam.rotation.x = -0.22;
    beam.castShadow = true;
    teamGroup.add(beam);

    // Traditional Wooden Plow Body (हल की कुर)
    const plowGeo = new THREE.ConeGeometry(0.28, 0.9, 4);
    plowGeo.rotateX(Math.PI / 2.3);
    const plow = new THREE.Mesh(plowGeo, woodMat);
    plow.position.set(0, 0.35, -2.6);
    plow.castShadow = true;
    teamGroup.add(plow);

    // FARMER (किसान)
    farmerGroup = new THREE.Group();
    farmerGroup.position.set(0, 0, -3.1);

    // Legs
    const fLegGeo = new THREE.BoxGeometry(0.18, 0.85, 0.2);
    fLegGeo.translate(0, -0.42, 0);
    const lLeg = new THREE.Mesh(fLegGeo, clothMat);
    lLeg.position.set(-0.16, 0.85, 0);
    const rLeg = new THREE.Mesh(fLegGeo, clothMat);
    rLeg.position.set(0.16, 0.85, 0);
    farmerGroup.add(lLeg);
    farmerGroup.add(rLeg);

    // Torso (Kurta)
    const fTorsoGeo = new THREE.BoxGeometry(0.55, 0.75, 0.32);
    const fTorso = new THREE.Mesh(fTorsoGeo, clothMat);
    fTorso.position.y = 1.25;
    fTorso.castShadow = true;
    farmerGroup.add(fTorso);

    // Head
    const fHeadGeo = new THREE.SphereGeometry(0.18, 8, 8);
    const fHead = new THREE.Mesh(fHeadGeo, skinMat);
    fHead.position.set(0, 1.8, 0);
    farmerGroup.add(fHead);

    // Pagdi / Turban (पगड़ी)
    const turbanGeo = new THREE.TorusGeometry(0.2, 0.12, 6, 12);
    turbanGeo.rotateX(Math.PI / 2);
    const turban = new THREE.Mesh(turbanGeo, turbanMat);
    turban.position.set(0, 1.9, 0);
    turban.castShadow = true;
    farmerGroup.add(turban);

    // Arms holding plow handle
    const armGeo = new THREE.BoxGeometry(0.12, 0.65, 0.12);
    armGeo.translate(0, -0.3, 0);
    const lArm = new THREE.Mesh(armGeo, skinMat);
    lArm.position.set(-0.35, 1.55, 0.1);
    lArm.rotation.set(0.7, 0, -0.2);
    const rArm = new THREE.Mesh(armGeo, skinMat);
    rArm.position.set(0.35, 1.55, 0.1);
    rArm.rotation.set(0.7, 0, 0.2);
    farmerGroup.add(lArm);
    farmerGroup.add(rArm);

    // Small Lantern on plow for Night mode
    const lanternGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.22, 6);
    const lanternMat = new THREE.MeshBasicMaterial({ color: 0xffedd5 });
    const lantern = new THREE.Mesh(lanternGeo, lanternMat);
    lantern.position.set(0.3, 0.75, -2.4);
    teamGroup.add(lantern);

    const farmerLanternLight = new THREE.PointLight(0xf59e0b, 0, 6);
    farmerLanternLight.position.set(0.3, 0.8, -2.4);
    teamGroup.add(farmerLanternLight);
    villageLights.push(farmerLanternLight);

    teamGroup.add(farmerGroup);
    scene.add(teamGroup);
  }

  // -------------------------------------------------------------------------
  // 6. TRADITIONAL INDIAN VILLAGE HUTS (DISTANCE KNIGHTS)
  // -------------------------------------------------------------------------
  function createVillageHuts() {
    villageGroup = new THREE.Group();

    const wallMat = new THREE.MeshStandardMaterial({ color: 0xa16207, roughness: 0.9 });
    const thatchMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.95 });
    const windowMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });

    const hutPositions = [
      { x: 9.5, z: -10.5, s: 1.2, r: 0.3 },
      { x: 13.0, z: -13.0, s: 1.4, r: -0.2 },
      { x: 7.2, z: -14.5, s: 1.0, r: 0.5 },
      { x: -14.5, z: -16.0, s: 1.1, r: -0.4 },
      { x: 17.5, z: -15.5, s: 1.3, r: 0.1 }
    ];

    hutPositions.forEach((h) => {
      const hut = new THREE.Group();
      const y = getTerrainHeight(h.x, h.z);
      hut.position.set(h.x, y, h.z);
      hut.scale.set(h.s, h.s, h.s);
      hut.rotation.y = h.r;

      // Mud Walls
      const wallGeo = new THREE.BoxGeometry(2.0, 1.2, 1.8);
      const wall = new THREE.Mesh(wallGeo, wallMat);
      wall.position.y = 0.6;
      wall.castShadow = true;
      hut.add(wall);

      // Sloping Thatched Roof
      const roofGeo = new THREE.ConeGeometry(1.8, 1.1, 4);
      roofGeo.rotateY(Math.PI / 4);
      const roof = new THREE.Mesh(roofGeo, thatchMat);
      roof.position.y = 1.7;
      roof.castShadow = true;
      hut.add(roof);

      // Window with warm lantern inside
      const winGeo = new THREE.PlaneGeometry(0.35, 0.35);
      const win = new THREE.Mesh(winGeo, windowMat);
      win.position.set(0, 0.7, 0.91);
      hut.add(win);

      // PointLight for evening/night warm glow
      const vLight = new THREE.PointLight(0xf59e0b, currentPreset.villageLightIntensity, 8);
      vLight.position.set(0, 0.8, 1.2);
      hut.add(vLight);
      villageLights.push(vLight);

      villageGroup.add(hut);
    });

    scene.add(villageGroup);
  }

  // -------------------------------------------------------------------------
  // 7. COUNTRYSIDE TREES (NEEM, BANYAN & MANGO SHAPES)
  // -------------------------------------------------------------------------
  function createTreesAndFlora() {
    treesGroup = new THREE.Group();

    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.9 });
    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x166534,
      roughness: 0.75,
      flatShading: true
    });

    const treeCoords = [
      { x: -16.5, z: -7.0, s: 1.4 },
      { x: -18.0, z: -11.5, s: 1.6 },
      { x: -13.0, z: -13.0, s: 1.2 },
      { x: 5.5, z: -12.0, s: 1.1 },
      { x: 15.5, z: -8.0, s: 1.5 },
      { x: 19.5, z: -11.0, s: 1.7 },
      { x: 11.5, z: -18.0, s: 1.8 },
      { x: -8.5, z: -19.0, s: 1.5 }
    ];

    treeCoords.forEach((t) => {
      const tree = new THREE.Group();
      const y = getTerrainHeight(t.x, t.z);
      tree.position.set(t.x, y, t.z);
      tree.scale.set(t.s, t.s, t.s);

      // Trunk
      const trunkGeo = new THREE.CylinderGeometry(0.2, 0.35, 2.2, 6);
      const trunk = new THREE.Mesh(trunkGeo, trunkMat);
      trunk.position.y = 1.1;
      trunk.castShadow = true;
      tree.add(trunk);

      // Layered Canopy
      const c1Geo = new THREE.DodecahedronGeometry(1.4, 1);
      const c1 = new THREE.Mesh(c1Geo, leafMat);
      c1.position.y = 2.4;
      c1.castShadow = true;
      tree.add(c1);

      const c2Geo = new THREE.DodecahedronGeometry(1.0, 1);
      const c2 = new THREE.Mesh(c2Geo, leafMat);
      c2.position.set(0.4, 3.1, 0.2);
      c2.castShadow = true;
      tree.add(c2);

      tree.userData = { swayOffset: t.x * 0.5 };
      treesGroup.add(tree);
    });

    scene.add(treesGroup);
  }

  // -------------------------------------------------------------------------
  // 8. DISTANT MOUNTAIN RIDGES
  // -------------------------------------------------------------------------
  function createDistantMountains() {
    mountainsGroup = new THREE.Group();

    const mtnMat1 = new THREE.MeshStandardMaterial({
      color: 0x1e3a24,
      roughness: 0.95,
      flatShading: true
    });
    const mtnMat2 = new THREE.MeshStandardMaterial({
      color: 0x162c1b,
      roughness: 0.95,
      flatShading: true
    });

    // Ridge 1 (Mid-Distance)
    for (let i = 0; i < 9; i++) {
      const coneGeo = new THREE.ConeGeometry(9 + (i % 3) * 3, 14 + (i % 4) * 3, 6);
      const mtn = new THREE.Mesh(coneGeo, mtnMat1);
      mtn.position.set(-36 + i * 9.5, 3.5, -34 - (i % 2) * 5);
      mtn.scale.set(1.4, 1, 0.7);
      mountainsGroup.add(mtn);
    }

    // Ridge 2 (Far Horizon)
    for (let i = 0; i < 7; i++) {
      const coneGeo2 = new THREE.ConeGeometry(14 + (i % 2) * 4, 20 + (i % 3) * 4, 5);
      const mtn2 = new THREE.Mesh(coneGeo2, mtnMat2);
      mtn2.position.set(-32 + i * 12.0, 6.0, -52 - (i % 2) * 4);
      mtn2.scale.set(1.5, 1, 0.8);
      mountainsGroup.add(mtn2);
    }

    scene.add(mountainsGroup);
  }

  // -------------------------------------------------------------------------
  // 9. DYNAMIC RAIN PARTICLE SYSTEM (DOWNPOUR TOWARD CAMERA)
  // -------------------------------------------------------------------------
  function createRainParticles() {
    const maxRain = 2400;
    rainGeometry = new THREE.BufferGeometry();
    rainPositions = new Float32Array(maxRain * 3);
    rainVelocities = new Float32Array(maxRain);

    for (let i = 0; i < maxRain; i++) {
      rainPositions[i * 3] = (Math.random() - 0.5) * 60;
      rainPositions[i * 3 + 1] = Math.random() * 26;
      rainPositions[i * 3 + 2] = (Math.random() - 0.5) * 45 + 5;
      rainVelocities[i] = 0.5 + Math.random() * 0.45;
    }

    rainGeometry.setAttribute('position', new THREE.BufferAttribute(rainPositions, 3));

    const rainMat = new THREE.PointsMaterial({
      color: 0xcfd8dc,
      size: 0.16,
      transparent: true,
      opacity: 0.0, // starts hidden in sunny mode
      blending: THREE.AdditiveBlending
    });

    rainSystem = new THREE.Points(rainGeometry, rainMat);
    scene.add(rainSystem);
  }

  // -------------------------------------------------------------------------
  // 10. GOLDEN POLLEN / SUN DUST MOTES (SUNNY MODE)
  // -------------------------------------------------------------------------
  function createPollenParticles() {
    const count = 90;
    pollenGeometry = new THREE.BufferGeometry();
    pollenPositions = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      pollenPositions[i * 3] = (Math.random() - 0.5) * 35;
      pollenPositions[i * 3 + 1] = 0.5 + Math.random() * 8.0;
      pollenPositions[i * 3 + 2] = (Math.random() - 0.5) * 25 + 5;
    }

    pollenGeometry.setAttribute('position', new THREE.BufferAttribute(pollenPositions, 3));

    const pollenMat = new THREE.PointsMaterial({
      color: 0xfef08a,
      size: 0.22,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    });

    pollenSystem = new THREE.Points(pollenGeometry, pollenMat);
    scene.add(pollenSystem);
  }

  // -------------------------------------------------------------------------
  // 11. PROCEDURAL DRIFTING CLOUDS
  // -------------------------------------------------------------------------
  function createCloudVolumes() {
    cloudPuffsGroup = new THREE.Group();

    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.9,
      transparent: true,
      opacity: 0.65
    });

    for (let c = 0; c < 6; c++) {
      const cluster = new THREE.Group();
      const puffCount = 4 + Math.floor(Math.random() * 4);
      for (let p = 0; p < puffCount; p++) {
        const puffGeo = new THREE.SphereGeometry(1.8 + Math.random() * 1.5, 7, 7);
        const puff = new THREE.Mesh(puffGeo, cloudMat);
        puff.position.set(
          (Math.random() - 0.5) * 4.5,
          (Math.random() - 0.5) * 1.5,
          (Math.random() - 0.5) * 3.0
        );
        cluster.add(puff);
      }
      cluster.position.set(-30 + c * 14, 18 + (c % 3) * 2.5, -25 + (c % 2) * 8);
      cluster.userData = { speed: 0.012 + Math.random() * 0.008 };
      cloudPuffsGroup.add(cluster);
    }

    scene.add(cloudPuffsGroup);
  }

  // -------------------------------------------------------------------------
  // TERRAIN HEIGHT SAMPLER
  // -------------------------------------------------------------------------
  function getTerrainHeight(x, z) {
    let y = Math.sin(x * 0.08) * 1.3 + Math.cos(z * 0.07) * 1.5 - z * 0.16;
    y += Math.sin(x * 1.25 + z * 0.22) * 0.24;
    if (Math.abs(x) > 16) {
      y += Math.pow((Math.abs(x) - 16) * 0.28, 1.8);
    }
    return y;
  }

  // -------------------------------------------------------------------------
  // MOUSE PARALLAX HANDLER
  // -------------------------------------------------------------------------
  function onBannerMouseMove(e) {
    const banner = document.getElementById('heroBanner3D');
    if (!banner) return;
    const rect = banner.getBoundingClientRect();
    mouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouseY = ((e.clientY - rect.top) / rect.height) * 2 - 1;
  }

  function onWindowResize() {
    const container = document.getElementById('hero3dCanvasContainer');
    if (!container || !renderer || !camera) return;
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  // -------------------------------------------------------------------------
  // WEATHER STATE CONTROLLER (SMOOTH TRANSITIONS)
  // -------------------------------------------------------------------------
  function setHeroWeatherState(weatherKey) {
    const preset = WEATHER_PRESETS[weatherKey];
    if (!preset) return;

    targetPreset = preset;
    transitionProgress = 0.0;

    // Update switcher buttons UI
    const allBtns = ['btnWeatherSunny', 'btnWeatherRain', 'btnWeatherStorm', 'btnWeatherCloudy', 'btnWeatherFog', 'btnWeatherNight'];
    allBtns.forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.classList.remove('active');
    });

    const activeBtnMap = {
      sunny: 'btnWeatherSunny',
      rain: 'btnWeatherRain',
      storm: 'btnWeatherStorm',
      cloudy: 'btnWeatherCloudy',
      fog: 'btnWeatherFog',
      night: 'btnWeatherNight'
    };
    const activeBtn = document.getElementById(activeBtnMap[weatherKey]);
    if (activeBtn) activeBtn.classList.add('active');

    // Update Header Status Chip & Telemetry UI
    const condElem = document.getElementById('heroWeatherCondition');
    const tempElem = document.getElementById('heroTemp');
    const humElem = document.getElementById('heroHumidity');
    const rainElem = document.getElementById('heroRainProb');
    const windElem = document.getElementById('heroWind');
    const iconElem = document.getElementById('heroWeatherIcon');

    if (condElem) condElem.textContent = preset.name;
    if (tempElem) tempElem.textContent = preset.temp;
    if (humElem) humElem.textContent = preset.humidity;
    if (rainElem) rainElem.textContent = preset.rainProb;
    if (windElem) windElem.textContent = preset.wind;

    const iconMap = {
      sunny: '☀️',
      rain: '🌧️',
      storm: '⛈️',
      cloudy: '☁️',
      fog: '🌫️',
      night: '🌙'
    };
    if (iconElem) iconElem.textContent = iconMap[weatherKey] || '🌾';
  }

  // Helper color lerp
  function lerpColor(c1, c2, alpha) {
    const col1 = new THREE.Color(c1);
    const col2 = new THREE.Color(c2);
    return col1.lerp(col2, alpha);
  }

  // -------------------------------------------------------------------------
  // MAIN ANIMATION LOOP (60 FPS)
  // -------------------------------------------------------------------------
  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const time = clock.getElapsedTime();

    // 1. Smooth Weather State Lerp
    if (transitionProgress < 1.0) {
      transitionProgress = Math.min(1.0, transitionProgress + TRANSITION_SPEED);

      // Lerp Lighting
      sunLight.color = lerpColor(currentPreset.sunColor, targetPreset.sunColor, transitionProgress);
      sunLight.intensity = THREE.MathUtils.lerp(currentPreset.sunIntensity, targetPreset.sunIntensity, transitionProgress);

      hemiLight.color = lerpColor(currentPreset.hemiSky, targetPreset.hemiSky, transitionProgress);
      hemiLight.groundColor = lerpColor(currentPreset.hemiGround, targetPreset.hemiGround, transitionProgress);
      hemiLight.intensity = THREE.MathUtils.lerp(currentPreset.hemiIntensity, targetPreset.hemiIntensity, transitionProgress);

      // Lerp Fog
      const fogCol = lerpColor(currentPreset.fogColor, targetPreset.fogColor, transitionProgress);
      scene.fog.color = fogCol;
      scene.fog.density = THREE.MathUtils.lerp(currentPreset.fogDensity, targetPreset.fogDensity, transitionProgress);

      // Lerp Sky Dome & Scene Background
      const skyCol = lerpColor(currentPreset.skyTop, targetPreset.skyTop, transitionProgress);
      skyDomeMaterial.color = skyCol;
      scene.background = skyCol;

      // Lerp Soil (Wet reflections vs matte)
      soilMaterial.roughness = THREE.MathUtils.lerp(currentPreset.soilRoughness, targetPreset.soilRoughness, transitionProgress);
      soilMaterial.metalness = THREE.MathUtils.lerp(currentPreset.soilMetalness, targetPreset.soilMetalness, transitionProgress);
      soilMaterial.color = lerpColor(currentPreset.soilColor, targetPreset.soilColor, transitionProgress);

      // Lerp Crops Color
      cropMaterial.color = lerpColor(currentPreset.cropColor, targetPreset.cropColor, transitionProgress);

      // Lerp Village Lights
      const targetVLight = THREE.MathUtils.lerp(currentPreset.villageLightIntensity, targetPreset.villageLightIntensity, transitionProgress);
      villageLights.forEach(vl => { vl.intensity = targetVLight; });

      // Lerp Rain Opacity
      const targetRainOpacity = targetPreset.rainCount > 0 ? (targetPreset.rainCount > 1500 ? 0.9 : 0.75) : 0.0;
      rainSystem.material.opacity = THREE.MathUtils.lerp(rainSystem.material.opacity, targetRainOpacity, transitionProgress);

      // Lerp Pollen Opacity
      pollenSystem.material.opacity = targetPreset.pollenActive ? 0.8 : 0.0;

      if (transitionProgress >= 1.0) {
        currentPreset = targetPreset;
      }
    }

    // 2. Parallax Camera Damping & Subtle Cinematic Drift
    targetCamX = mouseX * 2.2;
    targetCamY = 6.2 - mouseY * 0.9;
    curCamX += (targetCamX - curCamX) * 0.04;
    curCamY += (targetCamY - curCamY) * 0.04;

    const idleBreathing = Math.sin(time * 0.45) * 0.08;
    camera.position.x = curCamX;
    camera.position.y = curCamY + idleBreathing;
    camera.lookAt(curCamX * 0.4, 2.2, 0);

    // 3. Crops Swaying in the Wind
    const activeWindSpeed = THREE.MathUtils.lerp(currentPreset.windSpeed, targetPreset.windSpeed, transitionProgress);
    const activeWindAngle = THREE.MathUtils.lerp(currentPreset.windAngle, targetPreset.windAngle, transitionProgress);

    if (cropsGroup) {
      cropsGroup.children.forEach(tuft => {
        const offset = tuft.userData.swayOffset;
        tuft.rotation.z = Math.sin(time * activeWindSpeed + offset) * activeWindAngle;
        tuft.rotation.x = Math.cos(time * activeWindSpeed * 0.8 + offset) * (activeWindAngle * 0.35);
      });
    }

    // 4. Oxen & Farmer Subtle Walking Plowing Animation
    if (oxenGroup) {
      oxenGroup.children.forEach((ox, idx) => {
        const legPhase = time * 3.2 + (idx * Math.PI);
        if (ox.userData && ox.userData.legs) {
          ox.userData.legs[0].rotation.x = Math.sin(legPhase) * 0.22;
          ox.userData.legs[1].rotation.x = -Math.sin(legPhase) * 0.22;
          ox.userData.legs[2].rotation.x = -Math.sin(legPhase) * 0.18;
          ox.userData.legs[3].rotation.x = Math.sin(legPhase) * 0.18;
        }
        if (ox.userData && ox.userData.headGroup) {
          ox.userData.headGroup.rotation.x = Math.sin(time * 2.2 + idx) * 0.06;
        }
      });
    }
    if (farmerGroup) {
      farmerGroup.position.y = Math.sin(time * 3.2) * 0.03;
    }

    // 5. Trees Swaying
    if (treesGroup) {
      treesGroup.children.forEach(tr => {
        tr.rotation.z = Math.sin(time * activeWindSpeed * 0.6 + tr.userData.swayOffset) * (activeWindAngle * 0.25);
      });
    }

    // 6. Rain Animation (Slanted downpour towards camera)
    if (rainSystem && rainSystem.material.opacity > 0.02) {
      const positions = rainGeometry.attributes.position.array;
      const count = positions.length / 3;
      const rainSpeed = activeWindSpeed * 0.18 + 0.55;
      const windSlant = -activeWindAngle * 0.6;

      for (let i = 0; i < count; i++) {
        positions[i * 3 + 1] -= rainVelocities[i] * rainSpeed;
        positions[i * 3] += windSlant;

        // Reset if hit ground or out of view
        if (positions[i * 3 + 1] < 0.2) {
          positions[i * 3 + 1] = 25.0;
          positions[i * 3] = (Math.random() - 0.5) * 60;
        }
      }
      rainGeometry.attributes.position.needsUpdate = true;
    }

    // 7. Pollen Motes Animation (Floating upward in Sunny breeze)
    if (pollenSystem && pollenSystem.material.opacity > 0.05) {
      const pPos = pollenGeometry.attributes.position.array;
      const count = pPos.length / 3;
      for (let i = 0; i < count; i++) {
        pPos[i * 3 + 1] += 0.015;
        pPos[i * 3] += Math.sin(time + i) * 0.01;
        if (pPos[i * 3 + 1] > 10.0) {
          pPos[i * 3 + 1] = 0.5;
        }
      }
      pollenGeometry.attributes.position.needsUpdate = true;
    }

    // 8. Clouds Drifting
    if (cloudPuffsGroup) {
      cloudPuffsGroup.children.forEach(cl => {
        cl.position.x += cl.userData.speed * (activeWindSpeed * 0.7);
        if (cl.position.x > 38) {
          cl.position.x = -38;
        }
      });
    }

    // 9. Lightning in Storm Mode
    if (targetPreset.lightningActive) {
      lightningTimer += delta;
      if (lightningTimer > nextLightningTime) {
        // Trigger subtle atmospheric lightning flash
        sunLight.intensity = 4.2;
        sunLight.color.setHex(0xf8fafc);
        setTimeout(() => {
          sunLight.intensity = targetPreset.sunIntensity;
          sunLight.color.setHex(targetPreset.sunColor);
        }, 90);
        lightningTimer = 0;
        nextLightningTime = 3.5 + Math.random() * 5.0;
      }
    }

    renderer.render(scene, camera);
  }

  // Expose to window for UI controls
  window.initHero3DScene = initHero3DScene;
  window.setHeroWeatherState = setHeroWeatherState;

  // Auto initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHero3DScene);
  } else {
    setTimeout(initHero3DScene, 200);
  }

})();
