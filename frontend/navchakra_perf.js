/**
 * NavChakra (ऋतुIQ) — High-Performance Animation & Telemetry Engine (v2026.1)
 * 
 * Provides:
 * 1. Single unified 60 FPS requestAnimationFrame loop with precise delta-time (dt).
 * 2. Adaptive Quality Controller (auto-scales particle density if FPS < 45).
 * 3. Spatial indexing for O(1) atmospheric wind field vector lookups.
 * 4. Automatic canvas devicePixelRatio capping (max 2.0) to prevent HiDPI fillrate throttling.
 * 5. Dev-Only Performance & FPS HUD (toggle with 'F' or '~' key).
 * 6. Global tab visibility & idle lifecycle management.
 */

(function(window) {
  'use strict';

  // Master Engine Configuration
  const CONFIG = {
    targetFps: 60,
    targetFrameMs: 1000 / 60, // 16.66ms
    maxDpr: 2.0,
    lowFpsThreshold: 45,
    highFpsThreshold: 55,
    sampleWindow: 30
  };

  // State
  const state = {
    isRunning: false,
    lastTime: performance.now(),
    deltaTime: 0,
    fps: 60,
    frameTimeMs: 16.6,
    frameCount: 0,
    fpsHistory: [],
    qualityTier: 'HIGH', // 'HIGH' (100%), 'BALANCED' (75%), 'ECO' (50%)
    qualityMultiplier: 1.0,
    hudVisible: false,
    subsystems: new Map() // name -> { updateFn, isVisibleFn, priority }
  };

  // ---------------------------------------------------------------------------
  // 1. MASTER ANIMATION LOOP (Delta-Time Driven)
  // ---------------------------------------------------------------------------
  function masterLoop(timestamp) {
    if (!state.isRunning) return;

    const now = timestamp || performance.now();
    const elapsed = now - state.lastTime;
    state.lastTime = now;

    // Delta time in seconds, clamped to avoid spiral of death on tab resume
    state.deltaTime = Math.min(elapsed / 1000, 0.1);
    state.frameTimeMs = elapsed;

    // Rolling FPS calculation
    if (elapsed > 0) {
      const currentFps = 1000 / elapsed;
      state.fpsHistory.push(currentFps);
      if (state.fpsHistory.length > CONFIG.sampleWindow) {
        state.fpsHistory.shift();
      }
      const sum = state.fpsHistory.reduce((a, b) => a + b, 0);
      state.fps = Math.round(sum / state.fpsHistory.length);
    }

    // Adaptive Quality Balancing
    if (state.fpsHistory.length >= CONFIG.sampleWindow) {
      if (state.fps < CONFIG.lowFpsThreshold) {
        if (state.qualityTier === 'HIGH') {
          setQualityTier('BALANCED');
        } else if (state.qualityTier === 'BALANCED') {
          setQualityTier('ECO');
        }
      } else if (state.fps >= CONFIG.highFpsThreshold) {
        if (state.qualityTier === 'ECO') {
          setQualityTier('BALANCED');
        } else if (state.qualityTier === 'BALANCED' && state.frameCount % 180 === 0) {
          setQualityTier('HIGH');
        }
      }
    }

    state.frameCount++;

    // Execute active subsystems
    state.subsystems.forEach((subsystem, name) => {
      try {
        if (!subsystem.isVisibleFn || subsystem.isVisibleFn()) {
          subsystem.updateFn(state.deltaTime, now, state.qualityMultiplier);
        }
      } catch (err) {
        console.warn(`[NavChakra PerfEngine] Subsystem error in ${name}:`, err);
      }
    });

    // Update Dev HUD if visible
    if (state.hudVisible && state.frameCount % 6 === 0) {
      updateHudUI();
    }

    requestAnimationFrame(masterLoop);
  }

  function setQualityTier(tier) {
    state.qualityTier = tier;
    if (tier === 'HIGH') state.qualityMultiplier = 1.0;
    else if (tier === 'BALANCED') state.qualityMultiplier = 0.75;
    else if (tier === 'ECO') state.qualityMultiplier = 0.50;

    // Trigger subsystem resize/adjustment if needed
    window.dispatchEvent(new CustomEvent('navchakra-quality-changed', {
      detail: { tier: state.qualityTier, multiplier: state.qualityMultiplier }
    }));
  }

  function start() {
    if (state.isRunning) return;
    state.isRunning = true;
    state.lastTime = performance.now();
    requestAnimationFrame(masterLoop);
  }

  function stop() {
    state.isRunning = false;
  }

  // ---------------------------------------------------------------------------
  // 2. SUBSYSTEM REGISTRATION
  // ---------------------------------------------------------------------------
  function registerSubsystem(name, updateFn, isVisibleFn) {
    state.subsystems.set(name, { updateFn, isVisibleFn });
  }

  function unregisterSubsystem(name) {
    state.subsystems.delete(name);
  }

  // ---------------------------------------------------------------------------
  // 3. CANVAS DEVICEPIXELRATIO OPTIMIZATION
  // ---------------------------------------------------------------------------
  function getOptimalDpr() {
    return Math.min(window.devicePixelRatio || 1, CONFIG.maxDpr);
  }

  function configureCanvasDpr(canvas, ctx, width, height) {
    if (!canvas || !ctx) return;
    const dpr = getOptimalDpr();
    if (canvas.width !== Math.round(width * dpr) || canvas.height !== Math.round(height * dpr)) {
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
  }

  // ---------------------------------------------------------------------------
  // 4. SPATIAL WIND GRID LOOKUP (O(1) Spatial Hash Table)
  // ---------------------------------------------------------------------------
  class SpatialWindGrid {
    constructor() {
      this.gridMap = new Map();
      this.minLat = 6.0;
      this.maxLat = 38.0;
      this.minLon = 66.0;
      this.maxLon = 98.0;
      this.resolution = 0.5; // 0.5 degree geographic resolution (~55km)
    }

    build(pointArray) {
      this.gridMap.clear();
      if (!Array.isArray(pointArray) || pointArray.length === 0) return;

      for (let i = 0; i < pointArray.length; i++) {
        const pt = pointArray[i];
        if (!pt || !Number.isFinite(pt.lat) || !Number.isFinite(pt.lon)) continue;
        const key = this.getKey(pt.lat, pt.lon);
        this.gridMap.set(key, { u: pt.u, v: pt.v, speed: pt.speed || Math.hypot(pt.u, pt.v) });
      }
    }

    getKey(lat, lon) {
      const qLat = Math.round(lat / this.resolution) * this.resolution;
      const qLon = Math.round(lon / this.resolution) * this.resolution;
      return `${qLat.toFixed(1)},${qLon.toFixed(1)}`;
    }

    lookup(lat, lon, fallbackFn) {
      const key = this.getKey(lat, lon);
      const val = this.gridMap.get(key);
      if (val) return val;

      if (typeof fallbackFn === 'function') {
        const res = fallbackFn(lat, lon);
        if (res) {
          this.gridMap.set(key, res);
          return res;
        }
      }

      // Default baseline Indian monsoon westerly flow
      if (lat < 20) return { u: 14.5, v: 7.2, speed: 16.2 };
      if (lat < 27 && lon > 80) return { u: -8.5, v: -3.5, speed: 9.2 };
      return { u: 5.2, v: 3.1, speed: 6.0 };
    }
  }

  const globalWindGrid = new SpatialWindGrid();

  // ---------------------------------------------------------------------------
  // 5. DEV-ONLY FPS & PERFORMANCE HUD (Toggle with 'F' or '~' key)
  // ---------------------------------------------------------------------------
  let hudContainer = null;

  function initHud() {
    if (document.getElementById('navchakra-perf-hud')) return;

    hudContainer = document.createElement('div');
    hudContainer.id = 'navchakra-perf-hud';
    hudContainer.setAttribute('role', 'region');
    hudContainer.setAttribute('aria-label', 'NavChakra Performance HUD');
    hudContainer.style.cssText = `
      position: fixed;
      bottom: 18px;
      right: 18px;
      z-index: 999999;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 12px;
      padding: 10px 14px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      color: #f8fafc;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      display: none;
      min-width: 170px;
      pointer-events: auto;
      user-select: none;
    `;

    hudContainer.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; border-bottom:1px solid rgba(255,255,255,0.12); padding-bottom:4px;">
        <span style="font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:5px;">
          <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10b981; box-shadow:0 0 6px #10b981;"></span>
          NavChakra Perf
        </span>
        <button id="btnPerfClose" style="color:#94a3b8; font-size:12px; padding:0 3px; cursor:pointer;" title="Hide HUD (Press 'F' to toggle)">✕</button>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
        <span style="color:#94a3b8;">FPS:</span>
        <span id="hudFpsVal" style="font-size:16px; font-weight:900; color:#10b981;">60</span>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
        <span style="color:#94a3b8;">Frame:</span>
        <span id="hudFrameVal" style="color:#e2e8f0; font-weight:700;">16.6 ms</span>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
        <span style="color:#94a3b8;">Quality:</span>
        <span id="hudQualityVal" style="color:#38bdf8; font-weight:700;">HIGH (100%)</span>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:9.5px; color:#64748b; margin-top:5px; border-top:1px dashed rgba(255,255,255,0.08); padding-top:3px;">
        <span>Toggle: 'F' key</span>
        <span id="hudDprVal">DPR: 1.0x</span>
      </div>
    `;

    document.body.appendChild(hudContainer);

    document.getElementById('btnPerfClose').addEventListener('click', toggleHud);

    // Global Key Listener for Quick HUD Toggle (Key 'f' / 'F' or '~')
    window.addEventListener('keydown', (e) => {
      // Don't toggle if user is typing in an input or textarea
      const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : '';
      if (tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable) {
        return;
      }
      if (e.key === 'f' || e.key === 'F' || e.key === '`' || e.key === '~') {
        toggleHud();
      }
    });
  }

  function toggleHud() {
    state.hudVisible = !state.hudVisible;
    if (hudContainer) {
      hudContainer.style.display = state.hudVisible ? 'block' : 'none';
      if (state.hudVisible) updateHudUI();
    }
  }

  function updateHudUI() {
    if (!hudContainer) return;
    const elFps = document.getElementById('hudFpsVal');
    const elFrame = document.getElementById('hudFrameVal');
    const elQual = document.getElementById('hudQualityVal');
    const elDpr = document.getElementById('hudDprVal');

    if (elFps) {
      elFps.textContent = `${state.fps}`;
      if (state.fps >= 55) elFps.style.color = '#10b981'; // Green
      else if (state.fps >= 42) elFps.style.color = '#f59e0b'; // Amber
      else elFps.style.color = '#ef4444'; // Red
    }

    if (elFrame) {
      elFrame.textContent = `${state.frameTimeMs.toFixed(1)} ms`;
    }

    if (elQual) {
      elQual.textContent = `${state.qualityTier} (${Math.round(state.qualityMultiplier * 100)}%)`;
    }

    if (elDpr) {
      elDpr.textContent = `DPR: ${getOptimalDpr().toFixed(1)}x`;
    }
  }

  // ---------------------------------------------------------------------------
  // 6. GLOBAL LIFECYCLE & VISIBILITY MANAGEMENT
  // ---------------------------------------------------------------------------
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      state.isRunning = false;
    } else {
      state.lastTime = performance.now();
      state.fpsHistory = [];
      if (!state.isRunning) {
        state.isRunning = true;
        requestAnimationFrame(masterLoop);
      }
    }
  });

  // Auto-init on DOM readiness
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initHud();
      start();
    });
  } else {
    initHud();
    start();
  }

  // Export Global API
  window.NavChakraPerf = {
    start,
    stop,
    registerSubsystem,
    unregisterSubsystem,
    getOptimalDpr,
    configureCanvasDpr,
    SpatialWindGrid: globalWindGrid,
    setQualityTier,
    getQualityMultiplier: () => state.qualityMultiplier,
    toggleHud,
    isHudVisible: () => state.hudVisible,
    getFps: () => state.fps,
    getDeltaTime: () => state.deltaTime
  };

})(window);
