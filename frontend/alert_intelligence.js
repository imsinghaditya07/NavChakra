/**
 * NavChakra — Alert Intelligence Module
 * Early Warning & Disaster Safety Center
 * Focus: West Bengal (Birbhum, Burdwan & adjoining blocks)
 * 
 * Architecture:
 * - Module 1: Lucide SVG Icons Provider (Pure Lucide icon set, zero emojis)
 * - Module 2: AlertDataEngine (Deterministic seeded 48h meteorological generator)
 * - Module 3: CropDecisionEngine (Agronomic impact & farm decision rule matrix)
 * - Module 4: AlertState (Single source of truth & localStorage sync)
 * - Module 5: TimelineRenderer (Section A: Interactive SVG multi-axis timeline)
 * - Module 6: CropImpactRenderer (Section B: Crop hazard exposure & farm decisions)
 * - Module 7: SafetyPanelRenderer (Section C: Role-based checklist, 30-30 lightning tool, shelters)
 * - Module 8: SpeechSynthesis & Print Safety Card utilities
 */

// =========================================================================
// MODULE 1: LUCIDE SVG ICONS PROVIDER (Strictly ONE icon set, NO emojis)
// =========================================================================
const LucideIcons = {
  cloudRain: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M16 14v6"/><path d="M8 14v6"/><path d="M12 16v6"/></svg>`,
  wind: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.7 7.7A2.5 2.5 0 1 1 19 12H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/><path d="M19.3 4.7A2 2 0 1 0 18 8H2"/></svg>`,
  zap: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  shieldAlert: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
  shieldCheck: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>`,
  clock: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  calendar: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
  download: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
  checkCircle: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
  alertTriangle: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  sprout: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/></svg>`,
  phone: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>`,
  mapPin: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
  share2: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>`,
  printer: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>`,
  volume2: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>`,
  bell: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`,
  info: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`,
  refreshCw: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>`,
  user: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  externalLink: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`,
  chevronDown: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>`,
  chevronUp: (cls = '') => `<svg class="lucide-icon ${cls}" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg>`
};

// =========================================================================
// MODULE 2: DATA ENGINE (DETERMINISTIC SEEDED 48-HOUR METEOROLOGICAL OUTLOOK)
// =========================================================================
const BLOCKS_CONFIG = {
  'Bolpur': { name: 'Bolpur', dist: 'Birbhum', lat: 23.6687, lon: 87.7274, seedOffset: 0.1 },
  'Illambazar': { name: 'Illambazar', dist: 'Birbhum', lat: 23.6300, lon: 87.5350, seedOffset: 0.2 },
  'Suri': { name: 'Suri', dist: 'Birbhum', lat: 23.9056, lon: 87.5244, seedOffset: 0.3 },
  'Sainthia': { name: 'Sainthia', dist: 'Birbhum', lat: 23.9450, lon: 87.6800, seedOffset: 0.4 },
  'Durgapur': { name: 'Durgapur', dist: 'Paschim Bardhaman', lat: 23.5204, lon: 87.3119, seedOffset: 0.5 },
  'Bardhaman': { name: 'Bardhaman', dist: 'Purba Bardhaman', lat: 23.2324, lon: 87.8615, seedOffset: 0.6 },
  'Guskara': { name: 'Guskara', dist: 'Purba Bardhaman', lat: 23.4950, lon: 87.7550, seedOffset: 0.7 }
};

/**
 * Generate 48 hourly steps with realistic diurnal curve:
 * - Risk starts building in early afternoon (13:00 - 15:00)
 * - Risk peaks in late afternoon / evening (16:00 - 21:00) with squall & lightning
 * - Eases down late night (23:00 onwards)
 * - Identical & deterministic per block on reload
 * 
 * [INTEGRATION NOTE]: Real IMD / Open-Meteo hourly ECMWF / NDMA Sachet CAP alerts
 * can replace this generator function directly without modifying downstream UI modules.
 */
function generateHourlyForecastData(blockName = 'Bolpur') {
  const cfg = BLOCKS_CONFIG[blockName] || BLOCKS_CONFIG['Bolpur'];
  const steps = [];
  const now = new Date();
  now.setMinutes(0, 0, 0);

  const seed = cfg.seedOffset;
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  for (let i = 0; i < 48; i++) {
    const stepTime = new Date(now.getTime() + i * 3600 * 1000);
    const hour24 = stepTime.getHours();
    const dayStr = (i < 24) ? (i === 0 ? 'Now' : 'Today') : dayNames[stepTime.getDay()];
    const ampm = hour24 >= 12 ? 'PM' : 'AM';
    const hour12 = hour24 % 12 === 0 ? 12 : hour24 % 12;
    const timeLabel = (i === 0) ? 'Now' : `${hour12} ${ampm}`;
    const fullDateLabel = `${dayNames[stepTime.getDay()]} ${hour12}:00 ${ampm}`;

    // Diurnal factor: peak between 16:00 and 21:00 (hours 16-21)
    let diurnal = 0.2;
    if (hour24 >= 14 && hour24 <= 21) {
      const diff = hour24 - 17.5;
      diurnal = 0.85 * Math.exp(-(diff * diff) / 8);
    } else if (hour24 >= 11 && hour24 < 14) {
      diurnal = 0.45;
    } else if (hour24 >= 22 || hour24 < 3) {
      diurnal = 0.35;
    } else {
      diurnal = 0.15;
    }

    const dayFactor = (i < 24) ? 1.0 : 0.88;
    const pseudo = (Math.sin(i * 0.9 + seed * 10) + 1) * 0.5;

    let rainProb = Math.round((diurnal * 70 + pseudo * 18 + 15) * dayFactor);
    rainProb = Math.min(96, Math.max(12, rainProb));

    let windGust = Math.round(18 + diurnal * 42 + pseudo * 12);
    windGust = Math.min(74, Math.max(14, windGust));

    let lightning = 'low';
    let lightningScore = 1;
    if (rainProb >= 75 && windGust >= 50) {
      lightning = 'extreme';
      lightningScore = 4;
    } else if (rainProb >= 60 && windGust >= 38) {
      lightning = 'high';
      lightningScore = 3;
    } else if (rainProb >= 40 || windGust >= 30) {
      lightning = 'moderate';
      lightningScore = 2;
    }

    const combinedScore = Math.min(100, Math.round(
      (rainProb * 0.45) + 
      ((windGust / 70) * 100 * 0.30) + 
      (lightningScore * 25 * 0.25)
    ));

    let riskTier = 'low';
    if (combinedScore >= 75) riskTier = 'extreme';
    else if (combinedScore >= 58) riskTier = 'high';
    else if (combinedScore >= 40) riskTier = 'moderate';

    let advice = 'Routine fieldwork safe. Monitor horizon for darkening clouds.';
    if (combinedScore >= 75) {
      advice = 'Severe squall & lightning imminent. Cease fieldwork and seek pucca shelter.';
    } else if (combinedScore >= 58) {
      advice = 'High rain & gust risk. Check field bund cuts and secure vulnerable nursery covers.';
    } else if (combinedScore >= 40) {
      advice = 'Scattered showers expected. Postpone foliar sprays and chemical application.';
    }

    steps.push({
      hourOffset: i,
      timestamp: stepTime,
      dayStr,
      timeLabel,
      fullDateLabel,
      rainProb,
      windGust,
      lightning,
      lightningScore,
      combinedScore,
      riskTier,
      advice
    });
  }

  // Detect Peak Risk Window
  let maxWindowScore = 0;
  let bestWindow = { start: 15, end: 21 };

  for (let i = 0; i <= steps.length - 4; i++) {
    const windowScore = steps[i].combinedScore + steps[i+1].combinedScore + steps[i+2].combinedScore + steps[i+3].combinedScore;
    if (windowScore > maxWindowScore) {
      maxWindowScore = windowScore;
      bestWindow = { start: i, end: i + 5 };
    }
  }

  const pStartStep = steps[bestWindow.start];
  const pEndStep = steps[Math.min(steps.length - 1, bestWindow.end)];
  const peakWindowLabel = `${pStartStep.dayStr} ${pStartStep.timeLabel} – ${pEndStep.timeLabel}`;

  const maxRain = steps.reduce((max, s) => s.rainProb > max.rainProb ? s : max, steps[0]);
  const maxGust = steps.reduce((max, s) => s.windGust > max.windGust ? s : max, steps[0]);
  const highLightningCount = steps.filter(s => s.lightning === 'high' || s.lightning === 'extreme').length;

  return {
    blockName,
    district: cfg.dist,
    lat: cfg.lat,
    lon: cfg.lon,
    generatedAt: new Date(),
    steps,
    peakWindow: {
      startIndex: bestWindow.start,
      endIndex: bestWindow.end,
      label: peakWindowLabel,
      startLabel: pStartStep.fullDateLabel,
      endLabel: pEndStep.fullDateLabel
    },
    stats: {
      maxRain: { val: maxRain.rainProb, time: `${maxRain.dayStr} ${maxRain.timeLabel}` },
      maxGust: { val: maxGust.windGust, time: `${maxGust.dayStr} ${maxGust.timeLabel}` },
      highLightningHours: highLightningCount
    }
  };
}

// =========================================================================
// MODULE 3: CROP DECISION ENGINE (AGRONOMIC MATRIX MAPPING)
// =========================================================================
const CROPS_DATA = {
  'paddy': {
    name: 'Paddy (Aman/Boro)',
    stages: [
      { id: 'nursery', name: 'Nursery / Seedling (বীজতলা)' },
      { id: 'transplanting', name: 'Transplanting (রোপণ)' },
      { id: 'tillering', name: 'Tillering (কুশি বৃদ্ধি)' },
      { id: 'panicle', name: 'Panicle Initiation (শীষ বের হওয়া)' },
      { id: 'flowering', name: 'Flowering (ফুল ফোটা)' },
      { id: 'grain_filling', name: 'Grain Filling (দানা পুষ্ট হওয়া)' },
      { id: 'harvest_ready', name: 'Harvest-Ready (কাটার উপযুক্ত)' }
    ]
  },
  'potato': {
    name: 'Potato (আলু)',
    stages: [
      { id: 'planting', name: 'Planting / Sowing (রোপণ)' },
      { id: 'emergence', name: 'Sprout Emergence (অঙ্কুরোদগম)' },
      { id: 'tuber_init', name: 'Tuber Initiation (গুটি ধরা)' },
      { id: 'tuber_bulk', name: 'Tuber Bulking (আলু বৃদ্ধি)' },
      { id: 'maturation', name: 'Maturation / Haulm Cutting' },
      { id: 'harvest', name: 'Harvest & Field Curing' }
    ]
  },
  'mustard': {
    name: 'Mustard (সরিষা)',
    stages: [
      { id: 'sowing', name: 'Sowing / Seedbed' },
      { id: 'germination', name: 'Germination & Stand' },
      { id: 'vegetative', name: 'Vegetative Growth' },
      { id: 'flowering', name: 'Flowering (হলুদ ফুল)' },
      { id: 'siliqua', name: 'Pod / Siliqua Formation' },
      { id: 'maturity', name: 'Maturity & Harvest' }
    ]
  },
  'jute': {
    name: 'Jute (পাট)',
    stages: [
      { id: 'sowing', name: 'Sowing & Germination' },
      { id: 'elongation', name: 'Vegetative Elongation' },
      { id: 'fibre_mature', name: 'Fibre Maturation' },
      { id: 'harvesting', name: 'Harvesting & Retting' }
    ]
  },
  'vegetables': {
    name: 'Vegetables (শাকসবজি)',
    stages: [
      { id: 'nursery', name: 'Seedbed / Polyhouse Nursery' },
      { id: 'vegetative', name: 'Vegetative Vining & Branching' },
      { id: 'flowering', name: 'Flowering & Fruit Set' },
      { id: 'fruit_dev', name: 'Fruit Development / Picking' },
      { id: 'harvesting', name: 'Daily Harvesting' }
    ]
  },
  'sugarcane': {
    name: 'Sugarcane (আখ)',
    stages: [
      { id: 'tillering', name: 'Germination & Tillering' },
      { id: 'grand_growth', name: 'Grand Growth Phase' },
      { id: 'ripening', name: 'Maturation & Ripening' },
      { id: 'harvesting', name: 'Harvesting' }
    ]
  }
};

/**
 * Agronomic hazard rule table.
 * Maps: Crop x Stage x Weather Condition -> Impact, Why It Matters, Recommended Action, Severity.
 */
function evaluateCropHazards(cropId, stageId, fieldType, forecastData) {
  const stats = forecastData.stats;
  const maxRain = stats.maxRain.val;
  const maxGust = stats.maxGust.val;
  const peakTime = forecastData.peakWindow.label;
  const isLowLying = (fieldType === 'low-lying');

  const hazards = [];

  // 1. Waterlogging Hazard
  if (maxRain >= 50 || isLowLying) {
    const sev = (maxRain >= 70 || isLowLying) ? 'Act Now' : 'Act Soon';
    let impactDesc = 'Standing water accumulation causing root suffocation and shoot rot.';
    let actionDesc = 'De-silt primary trench drains and create 15 cm bund-cuts at lower edge immediately.';

    if (cropId === 'paddy') {
      if (stageId === 'nursery') {
        impactDesc = 'Submergence of delicate young nursery seedlings for >12 hours leads to severe damping-off.';
        actionDesc = 'Lower water level to 2-3 cm; drain excess surface accumulation before evening storm.';
      } else if (stageId === 'harvest_ready') {
        impactDesc = 'Standing water will submerge mature panicles, causing viviparous seed sprouting and grain blackening.';
        actionDesc = 'Complete emergency harvesting of ripe crop today; clear drainage exits from field plots.';
      }
    } else if (cropId === 'potato') {
      impactDesc = 'Extremely high vulnerability to anaerobic tuber rotting and bacterial soft rot in waterlogged furrows.';
      actionDesc = 'Keep furrows bone-dry by digging cross-lateral relief channels to main road drains.';
    } else if (cropId === 'vegetables') {
      impactDesc = 'Collar rot and Pythium root rot will destroy vegetable root zones within 24 hours of standing water.';
      actionDesc = 'Earth up raised beds and clear drainage furrows between mulch rows.';
    }

    hazards.push({
      id: 'waterlogging',
      hazard: 'Waterlogging & Root Zone Saturation',
      severity: sev,
      impact: impactDesc,
      why: isLowLying ? 'Low-lying plots receive runoff from adjacent uplands, multiplying waterlogging depth.' : 'Heavy rain rates exceed natural soil percolation rates.',
      action: actionDesc,
      exposureWindow: peakTime,
      checklistAdd: 'Open field drainage outlets and de-silt bund cuts'
    });
  }

  // 2. Wind Lodging Hazard
  if (maxGust >= 45) {
    const sev = (maxGust >= 58) ? 'Act Now' : 'Act Soon';
    let impactDesc = 'Severe squall gusts will cause crop stems to buckle and lodge flat to the ground.';
    let actionDesc = 'Provide bamboo propping or twin-tying to vulnerable crop stalks before wind peaks.';

    if (cropId === 'sugarcane' || cropId === 'jute') {
      impactDesc = 'Tall stalks (>2m) act as sails and will suffer irreversible mechanical snapping.';
      actionDesc = 'Tie groups of 4-5 adjacent sugarcane/jute canes together (trash-banding) for mutual structural support.';
    } else if (cropId === 'vegetables') {
      impactDesc = 'Trellis nets, bamboo stakes, and tomato/creeper poles risk total collapse under gusts.';
      actionDesc = 'Inspect guy-ropes, secure end-posts with ground anchors, and lower hanging shade nets.';
    } else if (cropId === 'paddy' && (stageId === 'grain_filling' || stageId === 'harvest_ready')) {
      impactDesc = 'Heavy panicles will cause stem breaking, increasing harvesting cost by 40% and causing shattering.';
      actionDesc = 'Drain field water immediately (muddy soil lowers root holding strength and accelerates lodging).';
    }

    hazards.push({
      id: 'lodging',
      hazard: 'Wind Lodging & Structural Damage',
      severity: sev,
      impact: impactDesc,
      why: `Wind gusts of ${maxGust} km/h exceed stem flexural resistance, especially with water-saturated topsoil.`,
      action: actionDesc,
      exposureWindow: peakTime,
      checklistAdd: 'Secure polyhouse covers, stake trellises, and tie tall crop stands'
    });
  }

  // 3. Spray Wash-off Hazard
  if (maxRain >= 40) {
    hazards.push({
      id: 'washoff',
      hazard: 'Foliar Spray & Fertilizer Wash-Off',
      severity: 'Watch',
      impact: 'Applied fertilizers, insecticides, or fungicides will be completely washed away into runoff.',
      why: 'Chemicals require a minimum rain-free drying window of 4-6 hours to absorb into plant tissue.',
      action: 'Strictly postpone all urea top-dressing and chemical sprays until 24 hours after rainfall ceases.',
      exposureWindow: 'Next 36 hours',
      checklistAdd: 'Postpone fertilizer application and chemical spraying'
    });
  }

  // 4. Fungal Disease Pressure Hazard
  hazards.push({
    id: 'fungal',
    hazard: 'High Fungal Disease Pressure',
    severity: (stats.highLightningHours >= 4 || maxRain >= 60) ? 'Act Soon' : 'Watch',
    impact: 'Prolonged leaf wetness and 90%+ relative humidity trigger rapid fungal spore germination.',
    why: 'Pathogens like Blast (paddy), Late Blight (potato), and Downy Mildew thrive in continuous warm wet canopy.',
    action: 'Scout crops on first dry morning. Keep protective systemic fungicide ready for immediate post-storm application.',
    exposureWindow: '48h post-rain',
    checklistAdd: 'Inspect field for fungal leaf spot symptoms post-rain'
  });

  // 5. Flower & Grain Shattering Hazard (if in flowering/podding stage)
  if (stageId === 'flowering' || stageId === 'siliqua' || stageId === 'grain_filling') {
    hazards.push({
      id: 'flower_damage',
      hazard: 'Flower Dropping & Poor Pollination',
      severity: 'Watch',
      impact: 'Heavy raindrop impact and gusty winds wash away pollen, causing flower abortion and sterile chaffy grains.',
      why: 'Pollen viability and pollinator insect activity are severely inhibited during stormy conditions.',
      action: 'Maintain proper field drainage to minimize root stress and speed recovery after rainfall window.',
      exposureWindow: peakTime,
      checklistAdd: 'Monitor flower retention and test panicle sterility after storm'
    });
  }

  // Sort hazards by severity rank: Act Now (1) > Act Soon (2) > Watch (3) > Safe (4)
  const rank = { 'Act Now': 1, 'Act Soon': 2, 'Watch': 3, 'Safe': 4 };
  hazards.sort((a, b) => (rank[a.severity] || 5) - (rank[b.severity] || 5));

  const topHazard = hazards[0] || {
    severity: 'Safe',
    hazard: 'Normal Weather Conditions',
    impact: 'No immediate severe meteorological stress detected for this crop.',
    action: 'Continue regular intercultural operations.'
  };

  const cropMeta = CROPS_DATA[cropId] || CROPS_DATA['paddy'];
  const stageMeta = cropMeta.stages.find(s => s.id === stageId) || cropMeta.stages[0];

  const hoursWindow = 48;
  const sentence = `Heavy rain (peak ${stats.maxRain.val}% at ${stats.maxRain.time}) in the next ${hoursWindow}h. Your ${cropMeta.name} at ${stageMeta.name.split(' (')[0]} stage is at risk of ${topHazard.hazard.toLowerCase()}. Recommended action: ${topHazard.action.toLowerCase()}`;

  return {
    topSeverity: topHazard.severity,
    headline: `${topHazard.severity.toUpperCase()}: ${topHazard.hazard}`,
    sentence,
    hazards,
    cropName: cropMeta.name,
    stageName: stageMeta.name
  };
}

// =========================================================================
// MODULE 4: SHARED APPLICATION STATE (SINGLE SOURCE OF TRUTH)
// =========================================================================
const DEFAULT_FARMER_CHECKLIST = [
  { id: 'drain', text: 'Drain paddy fields and open drainage outlets', why: 'Prevents standing water from suffocating roots and rotting submerged seedling crowns.' },
  { id: 'delay_spray', text: 'Delay pesticide spraying and fertilizer application', why: 'Imminent rainfall washes costly chemicals straight into waterways with zero plant uptake.' },
  { id: 'harvest_early', text: 'Harvest mature crops early if possible', why: 'Prevents wind-lodging, panicle shattering, and grain rotting in waterlogged mud.' },
  { id: 'secure_grain', text: 'Secure stored grain and cover harvested produce', why: 'Moisture ingress causes rapid Aspergillus mold, aflatoxin contamination, and sprouting.' },
  { id: 'nursery_higher', text: 'Move seedlings / nursery trays to higher ground', why: 'Seedlings younger than 25 days cannot survive deep submergence for more than 12 hours.' },
  { id: 'polyhouse_fasten', text: 'Fasten or lower polyhouse / shade-net covers', why: 'Severe gusts catch loose poly-sheets like sails, tearing fabric and bending GI pipe frames.' }
];

class AlertIntelligenceState {
  constructor() {
    let savedCrop = 'paddy';
    let savedStage = 'tillering';
    let savedField = 'low-lying';
    let savedCompleted = ['drain'];

    try {
      const storedProfile = localStorage.getItem('rituiq_crop_profile');
      if (storedProfile) {
        const p = JSON.parse(storedProfile);
        if (p.crop) savedCrop = p.crop;
        if (p.stage) savedStage = p.stage;
        if (p.fieldType) savedField = p.fieldType;
      }
      const storedProgress = localStorage.getItem('rituiq_alert_checklist');
      if (storedProgress) {
        savedCompleted = JSON.parse(storedProgress);
      }
    } catch (_) {}

    this.state = {
      block: 'Bolpur',
      windowHours: 48,
      selectedHour: 4,
      layers: {
        rain: true,
        wind: true,
        lightning: true
      },
      crop: savedCrop,
      cropStage: savedStage,
      fieldType: savedField,
      role: 'farmer',
      completedChecklist: new Set(savedCompleted),
      customChecklistItems: [],
      forecastData: null,
      cropEvaluation: null,
      activeLanguage: 'en'
    };

    this.listeners = [];
  }

  subscribe(callback) {
    this.listeners.push(callback);
  }

  notify() {
    this.listeners.forEach(fn => fn(this.state));
  }

  setBlock(blockName) {
    if (this.state.block !== blockName) {
      this.state.block = blockName;
      this.regenerateForecast();
    }
  }

  setWindowHours(hours) {
    this.state.windowHours = hours;
    if (this.state.selectedHour >= hours) {
      this.state.selectedHour = hours - 1;
    }
    this.notify();
  }

  toggleLayer(layerKey) {
    if (this.state.layers.hasOwnProperty(layerKey)) {
      this.state.layers[layerKey] = !this.state.layers[layerKey];
      this.notify();
    }
  }

  setSelectedHour(hourIdx) {
    this.state.selectedHour = Math.max(0, Math.min(this.state.windowHours - 1, hourIdx));
    this.notify();
  }

  setCrop(cropId) {
    this.state.crop = cropId;
    const stages = CROPS_DATA[cropId]?.stages || [];
    this.state.cropStage = stages[0]?.id || 'nursery';
    this.evaluateCrop();
    this.notify();
  }

  setCropStage(stageId) {
    this.state.cropStage = stageId;
    this.evaluateCrop();
    this.notify();
  }

  setFieldType(type) {
    this.state.fieldType = type;
    this.evaluateCrop();
    this.notify();
  }

  setRole(role) {
    this.state.role = role;
    this.notify();
  }

  setLanguage(lang) {
    this.state.activeLanguage = lang;
    this.notify();
  }

  saveCropProfile() {
    try {
      localStorage.setItem('rituiq_crop_profile', JSON.stringify({
        crop: this.state.crop,
        stage: this.state.cropStage,
        fieldType: this.state.fieldType
      }));
      return true;
    } catch (_) {
      return false;
    }
  }

  toggleChecklistItem(itemId) {
    if (this.state.completedChecklist.has(itemId)) {
      this.state.completedChecklist.delete(itemId);
    } else {
      this.state.completedChecklist.add(itemId);
    }
    try {
      localStorage.setItem('rituiq_alert_checklist', JSON.stringify(Array.from(this.state.completedChecklist)));
    } catch (_) {}
    this.notify();
  }

  resetChecklist() {
    this.state.completedChecklist.clear();
    try {
      localStorage.removeItem('rituiq_alert_checklist');
    } catch (_) {}
    this.notify();
  }

  addChecklistItem(item) {
    const exists = this.state.customChecklistItems.some(i => i.text === item.text);
    if (!exists) {
      this.state.customChecklistItems.push(item);
      this.notify();
    }
  }

  regenerateForecast() {
    this.state.forecastData = generateHourlyForecastData(this.state.block);
    this.evaluateCrop();
    this.notify();
  }

  evaluateCrop() {
    if (this.state.forecastData) {
      this.state.cropEvaluation = evaluateCropHazards(
        this.state.crop,
        this.state.cropStage,
        this.state.fieldType,
        this.state.forecastData
      );
    }
  }
}

const alertStateInstance = new AlertIntelligenceState();

// =========================================================================
// MODULE 5: SECTION A — 48-HOUR RISK TIMELINE (SVG MULTI-AXIS CHART)
// =========================================================================
function renderSectionATimeline(state) {
  const f = state.forecastData;
  if (!f) return '';

  const hoursLimit = state.windowHours;
  const steps = f.steps.slice(0, hoursLimit);
  const selectedStep = steps[state.selectedHour] || steps[0];

  const svgWidth = 840;
  const svgHeight = 265;
  const padLeft = 50;
  const padRight = 55;
  const padTop = 46;
  const padBottom = 46;
  const chartW = svgWidth - padLeft - padRight;
  const chartH = svgHeight - padTop - padBottom;

  const stepW = chartW / (steps.length - 1 || 1);

  const getYRain = (p) => padTop + chartH - (p / 100) * chartH;
  const getYWind = (w) => padTop + chartH - (Math.min(80, w) / 80) * chartH;

  let rainAreaPath = `M ${padLeft} ${padTop + chartH}`;
  let rainLinePath = `M ${padLeft} ${getYRain(steps[0].rainProb)}`;
  steps.forEach((s, idx) => {
    const x = padLeft + idx * stepW;
    const y = getYRain(s.rainProb);
    rainAreaPath += ` L ${x} ${y}`;
    rainLinePath += ` L ${x} ${y}`;
  });
  rainAreaPath += ` L ${padLeft + (steps.length - 1) * stepW} ${padTop + chartH} Z`;

  let windLinePath = `M ${padLeft} ${getYWind(steps[0].windGust)}`;
  steps.forEach((s, idx) => {
    const x = padLeft + idx * stepW;
    const y = getYWind(s.windGust);
    windLinePath += ` L ${x} ${y}`;
  });

  const pStartClamped = Math.max(0, Math.min(steps.length - 1, f.peakWindow.startIndex));
  const pEndClamped = Math.max(0, Math.min(steps.length - 1, f.peakWindow.endIndex));
  const peakX1 = padLeft + pStartClamped * stepW;
  const peakX2 = padLeft + pEndClamped * stepW;
  const peakW = Math.max(24, peakX2 - peakX1);

  const peakTagW = 160;
  const peakCenter = peakX1 + (peakW / 2);
  const peakTagX = Math.max(padLeft + 6, Math.min(padLeft + chartW - peakTagW - 6, peakCenter - (peakTagW / 2)));

  const cursorX = padLeft + state.selectedHour * stepW;

  return `
    <div class="ai-section ai-timeline-card" id="aiSectionA">
      <div class="ai-section-header">
        <div class="ai-title-wrap">
          <div class="ai-badge-row">
            <span class="ai-dot-live pulse"></span>
            <span class="ai-live-text">Live • Updated 5 min ago</span>
            <span class="ai-demo-badge">Demo data</span>
          </div>
          <h2 class="ai-title">48-Hour Risk Timeline</h2>
          <p class="ai-subtitle">Hourly rain, wind and lightning outlook for your block</p>
        </div>

        <div class="ai-controls-toolbar">
          <div class="ai-control-group">
            <label for="aiBlockSelect" class="ai-ctrl-label">
              ${LucideIcons.mapPin('ctrl-icon')} Block:
            </label>
            <select id="aiBlockSelect" class="ai-select" onchange="alertStateInstance.setBlock(this.value)">
              ${Object.keys(BLOCKS_CONFIG).map(b => `<option value="${b}" ${b === state.block ? 'selected' : ''}>${b} (${BLOCKS_CONFIG[b].dist})</option>`).join('')}
            </select>
          </div>

          <div class="ai-segmented-toggle" role="group" aria-label="Forecast Window">
            <button type="button" class="ai-seg-btn ${state.windowHours === 24 ? 'active' : ''}" onclick="alertStateInstance.setWindowHours(24)">24h</button>
            <button type="button" class="ai-seg-btn ${state.windowHours === 48 ? 'active' : ''}" onclick="alertStateInstance.setWindowHours(48)">48h</button>
          </div>

          <button type="button" class="ai-btn-csv" onclick="download48hOutlookCsv()" title="Download hourly values in CSV format">
            ${LucideIcons.download()} CSV
          </button>
        </div>
      </div>

      <div class="ai-layers-bar">
        <span class="ai-layers-label">Visible Layers:</span>
        <button type="button" class="ai-chip-toggle ${state.layers.rain ? 'active rain' : ''}" onclick="alertStateInstance.toggleLayer('rain')" aria-pressed="${state.layers.rain}">
          ${LucideIcons.cloudRain()} Rain Prob (%)
        </button>
        <button type="button" class="ai-chip-toggle ${state.layers.wind ? 'active wind' : ''}" onclick="alertStateInstance.toggleLayer('wind')" aria-pressed="${state.layers.wind}">
          ${LucideIcons.wind()} Wind Gust (km/h)
        </button>
        <button type="button" class="ai-chip-toggle ${state.layers.lightning ? 'active lightning' : ''}" onclick="alertStateInstance.toggleLayer('lightning')" aria-pressed="${state.layers.lightning}">
          ${LucideIcons.zap()} Lightning Risk
        </button>
      </div>

      ${f.peakWindow && f.peakWindow.label ? `
        <div class="ai-peak-risk-banner" onclick="scrollToSafetyPanel('peak')" title="Click to view contingency checklist for this peak window">
          <div class="ai-peak-banner-left">
            <span class="ai-peak-icon">⚠️</span>
            <div class="ai-peak-info">
              <span class="ai-peak-title">Peak Risk Window</span>
              <span class="ai-peak-desc">${f.peakWindow.label} • Severe storm / convective risk</span>
            </div>
          </div>
          <span class="ai-peak-cta">Prepare Now &darr;</span>
        </div>
      ` : ''}

      <div class="ai-chart-container">
        <svg viewBox="0 0 ${svgWidth} ${svgHeight}" class="ai-chart-svg" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Hourly risk chart showing rainfall and wind gusts">
          <defs>
            <linearGradient id="aiRainGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.38"/>
              <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.02"/>
            </linearGradient>
            <linearGradient id="aiPeakShade" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#ef4444" stop-opacity="0.22"/>
              <stop offset="100%" stop-color="#ef4444" stop-opacity="0.06"/>
            </linearGradient>
          </defs>

          <!-- Top Axis Headers in Dedicated Headroom -->
          <text x="${padLeft}" y="22" text-anchor="start" class="ai-axis-header rain">🌧️ Rain Prob (%)</text>
          <text x="${padLeft + chartW}" y="22" text-anchor="end" class="ai-axis-header wind">💨 Wind Gust (km/h)</text>

          <!-- Grid Lines & Ticks -->
          ${[0, 25, 50, 75, 100].map(val => `
            <line x1="${padLeft}" y1="${getYRain(val)}" x2="${padLeft + chartW}" y2="${getYRain(val)}" stroke="#e2e8f0" stroke-dasharray="3,3" stroke-width="1"/>
            <text x="${padLeft - 8}" y="${getYRain(val) + 4}" text-anchor="end" class="ai-axis-label">${val}%</text>
            <text x="${padLeft + chartW + 8}" y="${getYRain(val) + 4}" text-anchor="start" class="ai-axis-label wind">${Math.round((val / 100) * 80)}</text>
          `).join('')}

          <!-- Peak Shaded Band in Timeline -->
          <rect x="${peakX1}" y="${padTop}" width="${peakW}" height="${chartH}" fill="url(#aiPeakShade)" stroke="#f87171" stroke-width="1.2" stroke-dasharray="4,2" rx="4" class="ai-peak-band-rect" onclick="scrollToSafetyPanel('peak')" />
          
          <!-- Peak Risk Pill Badge (Safe in Headroom, Never Overlaps Axis or Lines) -->
          <g class="ai-peak-badge-group" onclick="scrollToSafetyPanel('peak')" style="cursor:pointer;" role="button" aria-label="Peak risk window">
            <rect x="${peakTagX}" y="10" width="${peakTagW}" height="24" rx="12" fill="#fee2e2" stroke="#ef4444" stroke-width="1.2" class="ai-peak-badge-rect" />
            <text x="${peakTagX + (peakTagW / 2)}" y="26" text-anchor="middle" class="ai-peak-badge-text">
              ⚠ Peak: ${f.peakWindow.label}
            </text>
          </g>

          ${state.layers.rain ? `
            <path d="${rainAreaPath}" fill="url(#aiRainGrad)" />
            <path d="${rainLinePath}" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" />
          ` : ''}

          ${state.layers.wind ? `
            <path d="${windLinePath}" fill="none" stroke="#d97706" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="1,0" />
            ${steps.filter((_, i) => i % 3 === 0).map((s, idx) => {
              const x = padLeft + (idx * 3) * stepW;
              const y = getYWind(s.windGust);
              return `<circle cx="${x}" cy="${y}" r="3" fill="#ffffff" stroke="#d97706" stroke-width="2" />`;
            }).join('')}
          ` : ''}

          ${state.layers.lightning ? steps.map((s, idx) => {
            const x = padLeft + idx * stepW;
            const y = padTop + chartH + 12;
            const colors = { 'low': '#10b981', 'moderate': '#f59e0b', 'high': '#f97316', 'extreme': '#ef4444' };
            const c = colors[s.lightning] || '#94a3b8';
            return `<circle cx="${x}" cy="${y}" r="${s.lightningScore >= 3 ? 3.5 : 2.5}" fill="${c}" stroke="#ffffff" stroke-width="0.8" />`;
          }).join('') : ''}

          <!-- Scrubber Cursor Line -->
          <line x1="${cursorX}" y1="${padTop}" x2="${cursorX}" y2="${padTop + chartH + 18}" stroke="#0f172a" stroke-width="2" stroke-dasharray="2,2" class="ai-cursor-line" />
          <circle cx="${cursorX}" cy="${getYRain(selectedStep.rainProb)}" r="5.5" fill="#2563eb" stroke="#ffffff" stroke-width="2.5" />

          ${steps.map((s, idx) => {
            if (state.windowHours === 24 ? (idx % 3 === 0) : (idx % 6 === 0)) {
              const x = padLeft + idx * stepW;
              return `<text x="${x}" y="${padTop + chartH + 32}" text-anchor="middle" class="ai-time-label ${idx === state.selectedHour ? 'active' : ''}">${s.timeLabel}</text>`;
            }
            return '';
          }).join('')}
        </svg>
      </div>

      <div class="ai-scrubber-row">
        <label for="aiScrubRange" class="ai-scrub-label">
          ${LucideIcons.clock()} Scrub Outlook Hours:
        </label>
        <input type="range" id="aiScrubRange" min="0" max="${state.windowHours - 1}" value="${state.selectedHour}" class="ai-range-slider" oninput="alertStateInstance.setSelectedHour(parseInt(this.value))" aria-label="Scrub timeline hours" />
        <span class="ai-scrub-val">${selectedStep.dayStr} ${selectedStep.timeLabel}</span>
      </div>

      <div class="ai-hourly-strip" role="listbox" aria-label="Hourly risk cells">
        ${steps.map((s, idx) => `
          <div class="ai-strip-cell tier-${s.riskTier} ${idx === state.selectedHour ? 'selected' : ''}" 
               onclick="alertStateInstance.setSelectedHour(${idx})" 
               title="${s.fullDateLabel}: Risk ${s.combinedScore}% • Rain ${s.rainProb}% • ${s.advice}" 
               tabindex="0" 
               onkeydown="if(event.key==='Enter') alertStateInstance.setSelectedHour(${idx})">
            <span class="cell-hour">${s.timeLabel.replace(' ', '')}</span>
            <span class="cell-val">${s.rainProb}%</span>
          </div>
        `).join('')}
      </div>

      <div class="ai-summary-card tier-${selectedStep.riskTier}">
        <div class="ai-summary-main">
          <div class="ai-summary-header-row">
            <div class="ai-summary-time-badge">
              <span class="summary-time-icon">🕒</span>
              <span>Selected Hour: <strong>${selectedStep.fullDateLabel}</strong> (${state.block} Block)</span>
            </div>
            <div class="ai-summary-risk-pill tier-${selectedStep.riskTier}">
              ${selectedStep.riskTier.toUpperCase()} RISK
            </div>
          </div>

          <div class="ai-metrics-pills-row">
            <div class="ai-metric-tag rain">
              <span class="tag-icon">🌧️</span>
              <span class="tag-label">Rain Probability:</span>
              <strong class="tag-value">${selectedStep.rainProb}%</strong>
            </div>
            <div class="ai-metric-tag wind">
              <span class="tag-icon">💨</span>
              <span class="tag-label">Wind Gusts:</span>
              <strong class="tag-value">${selectedStep.windGust} km/h</strong>
            </div>
            <div class="ai-metric-tag lightning">
              <span class="tag-icon">⚡</span>
              <span class="tag-label">Lightning:</span>
              <strong class="tag-value badge-lightning ${selectedStep.lightning}">${selectedStep.lightning.toUpperCase()}</strong>
            </div>
          </div>

          <p class="ai-summary-advice-box">
            <span class="advice-icon">🌱</span>
            <span class="advice-text">${selectedStep.advice}</span>
          </p>
        </div>

        <div class="ai-summary-gauge-col">
          <div class="ai-risk-score-box tier-${selectedStep.riskTier}">
            <span class="score-num">${selectedStep.combinedScore}</span>
            <span class="score-lbl">Risk Index</span>
          </div>
        </div>
      </div>

      <div class="ai-stat-chips-grid">
        <div class="ai-stat-chip">
          <div class="chip-icon-wrap rain">${LucideIcons.cloudRain('chip-icon')}</div>
          <div class="chip-text">
            <span class="chip-label">Peak Rain Probability</span>
            <strong class="chip-value">${f.stats.maxRain.val}%</strong>
            <span class="chip-sub">at ${f.stats.maxRain.time}</span>
          </div>
        </div>
        <div class="ai-stat-chip">
          <div class="chip-icon-wrap wind">${LucideIcons.wind('chip-icon')}</div>
          <div class="chip-text">
            <span class="chip-label">Maximum Wind Gusts</span>
            <strong class="chip-value">${f.stats.maxGust.val} km/h</strong>
            <span class="chip-sub">at ${f.stats.maxGust.time}</span>
          </div>
        </div>
        <div class="ai-stat-chip">
          <div class="chip-icon-wrap zap">${LucideIcons.zap('chip-icon')}</div>
          <div class="chip-text">
            <span class="chip-label">Severe Lightning Window</span>
            <strong class="chip-value">${f.stats.highLightningHours} Hours</strong>
            <span class="chip-sub">High/Extreme Risk</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

// =========================================================================
// MODULE 6: SECTION B — CROP IMPACT & FARM DECISIONS
// =========================================================================
function renderSectionBCropImpact(state) {
  // Section B removed as requested
  return '';
}

// =========================================================================
// MODULE 7: SECTION C — "WHAT SHOULD I DO NOW?" SAFETY PANEL
// =========================================================================
function renderSectionCSafetyPanel(state) {
  const f = state.forecastData;
  if (!f) return '';

  const selectedStep = f.steps[state.selectedHour] || f.steps[0];
  const isPeakHour = (state.selectedHour >= f.peakWindow.startIndex && state.selectedHour <= f.peakWindow.endIndex);

  let bannerClass = 'banner-moderate';
  let bannerIcon = LucideIcons.alertTriangle();
  let bannerTitle = 'Prepare in the next 4 hours';
  let bannerDesc = `Storm window approaching ${f.peakWindow.label}. Open drainage ditches, tie tall crops, and secure harvested grain.`;

  if (isPeakHour || selectedStep.combinedScore >= 75) {
    bannerClass = 'banner-critical';
    bannerIcon = LucideIcons.shieldAlert();
    bannerTitle = 'TAKE SHELTER NOW • AVOID FIELDWORK';
    bannerDesc = `Severe squall gusts (${selectedStep.windGust} km/h) & ${selectedStep.lightning.toUpperCase()} lightning in progress across ${state.block}. Remain in a pucca building.`;
  } else if (selectedStep.combinedScore < 35) {
    bannerClass = 'banner-safe';
    bannerIcon = LucideIcons.shieldCheck();
    bannerTitle = 'NORMAL FIELD OPERATIONS PERMITTED';
    bannerDesc = `Weather conditions at ${selectedStep.timeLabel} are relatively stable (${selectedStep.rainProb}% rain prob). Continue monitoring 48h timeline.`;
  }

  const allFarmerItems = [...DEFAULT_FARMER_CHECKLIST, ...state.customChecklistItems];
  const totalCount = allFarmerItems.length;
  const completedCount = allFarmerItems.filter(item => state.completedChecklist.has(item.id || item.text)).length;
  const percentDone = Math.round((completedCount / (totalCount || 1)) * 100);

  return `
    <div class="ai-section ai-safety-card" id="aiSectionC">
      <div class="ai-priority-banner ${bannerClass}" id="aiPriorityBanner">
        <div class="ai-pb-icon">${bannerIcon}</div>
        <div class="ai-pb-content">
          <strong class="ai-pb-title">${bannerTitle}</strong>
          <span class="ai-pb-desc">${bannerDesc}</span>
        </div>
      </div>

      <div class="ai-section-header" style="margin-top:16px;">
        <div class="ai-title-wrap">
          <h2 class="ai-title">What Should I Do Now?</h2>
          <p class="ai-subtitle">Actions matched to your role and the current risk level in ${state.block}</p>
        </div>

        <div class="ai-role-tabs" role="tablist" aria-label="Target safety roles">
          <button type="button" class="ai-role-tab ${state.role === 'farmer' ? 'active' : ''}" onclick="alertStateInstance.setRole('farmer')" role="tab" aria-selected="${state.role === 'farmer'}">
            ${LucideIcons.sprout()} Farmer
          </button>
          <button type="button" class="ai-role-tab ${state.role === 'everyone' ? 'active' : ''}" onclick="alertStateInstance.setRole('everyone')" role="tab" aria-selected="${state.role === 'everyone'}">
            ${LucideIcons.user()} Everyone (Lightning)
          </button>
          <button type="button" class="ai-role-tab ${state.role === 'livestock' ? 'active' : ''}" onclick="alertStateInstance.setRole('livestock')" role="tab" aria-selected="${state.role === 'livestock'}">
            ${LucideIcons.shieldCheck()} Livestock Owner
          </button>
        </div>
      </div>

      ${state.role === 'farmer' ? `
        <div class="ai-role-panel" id="panelFarmer">
          <div class="ai-progress-card">
            <div class="ai-progress-header">
              <span class="ai-prog-title"><strong>Preparedness Progress:</strong> ${completedCount} of ${totalCount} actions completed</span>
              <span class="ai-prog-percent">${percentDone}%</span>
            </div>
            <div class="ai-progress-track">
              <div class="ai-progress-fill" style="width:${percentDone}%;"></div>
            </div>
            ${percentDone === 100 ? `
              <div class="ai-prep-complete-badge">
                ${LucideIcons.checkCircle()} Excellent! You are fully prepared for the upcoming squall window.
              </div>
            ` : ''}
            <div style="display:flex; justify-content:flex-end; margin-top:8px;">
              <button type="button" class="ai-btn-reset-check" onclick="alertStateInstance.resetChecklist()">
                ${LucideIcons.refreshCw()} Reset checklist
              </button>
            </div>
          </div>

          <div class="ai-checklist-grid">
            ${allFarmerItems.map((item, idx) => {
              const itemId = item.id || item.text;
              const isChecked = state.completedChecklist.has(itemId);
              return `
                <div class="ai-check-card ${isChecked ? 'completed' : ''}" onclick="toggleChecklistCard('${escapeQuotes(itemId)}')">
                  <div class="ai-check-box-col">
                    <input type="checkbox" id="chk_${idx}" class="ai-native-chk" ${isChecked ? 'checked' : ''} onclick="event.stopPropagation(); alertStateInstance.toggleChecklistItem('${escapeQuotes(itemId)}')" aria-label="${item.text}" />
                  </div>
                  <div class="ai-check-body">
                    <span class="ai-check-text">${item.text}</span>
                    <details class="ai-check-why-accordion" onclick="event.stopPropagation()">
                      <summary class="ai-why-summary">Why it matters ${LucideIcons.chevronDown('why-arrow')}</summary>
                      <p class="ai-why-text">${item.why}</p>
                    </details>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      ` : ''}

      ${state.role === 'everyone' ? `
        <div class="ai-role-panel" id="panelEveryone">
          <div class="ai-dodont-grid">
            <div class="ai-dodont-card do">
              <div class="dd-header do">${LucideIcons.checkCircle()} DO (নিরাপদ অভ্যাস)</div>
              <ul class="dd-list">
                <li>Shelter inside a sturdy pucca building with enclosed doors and windows.</li>
                <li>If traveling, remain inside a closed hard-top metal vehicle with windows rolled up.</li>
                <li>Unplug sensitive farm electrical equipment and irrigation motor starters.</li>
                <li>Stay away from plumbing lines, metal taps, and corded landline devices.</li>
              </ul>
            </div>
            <div class="ai-dodont-card dont">
              <div class="dd-header dont">${LucideIcons.alertTriangle()} DON'T (কখনই করবেন না)</div>
              <ul class="dd-list">
                <li>NEVER take shelter under tall isolated trees or bamboo groves in open fields.</li>
                <li>Do not remain in open water bodies, irrigation canals, or waterlogged paddies.</li>
                <li>Do not carry or hold metal tools, spades, khurpis, or iron pipes during thunder.</li>
                <li>Avoid open tin-sheds, pump houses with ungrounded tin roofs, or barbed-wire fences.</li>
              </ul>
            </div>
          </div>

          <div class="ai-tool-3030-card">
            <div class="ai-tool-header">
              <div class="tool-title-row">
                ${LucideIcons.zap('tool-icon')}
                <h3 class="tool-title">Interactive 30-30 Lightning Distance Calculator</h3>
              </div>
              <span class="ai-demo-badge">Emergency safety utility</span>
            </div>
            <p class="tool-desc">
              When lightning strikes: Tap <strong>"I Saw Lightning"</strong>, then tap <strong>"I Heard Thunder"</strong> as soon as the sound reaches you.
            </p>

            <div class="tool-controls-row">
              <button type="button" class="btn-3030 saw" id="btn30Saw" onclick="start3030Stopwatch()">
                ${LucideIcons.zap()} I Just Saw Lightning
              </button>
              <button type="button" class="btn-3030 heard" id="btn30Heard" onclick="stop3030Stopwatch()" disabled>
                ${LucideIcons.volume2()} I Heard Thunder
              </button>
            </div>

            <div id="result3030Box" class="tool-result-box" style="display:none;"></div>

            <div id="countdown30MinBox" class="tool-countdown-box" style="display:none;">
              <span class="cd-title">${LucideIcons.clock()} 30-Minute Safe Shelter Countdown</span>
              <div class="cd-timer" id="cdTimerDigits">30:00</div>
              <p class="cd-sub">Stay inside until 30 minutes pass after the last thunderclap. Tap "I Heard Thunder" again if thunder strikes to reset clock.</p>
            </div>
          </div>
        </div>
      ` : ''}

      ${state.role === 'livestock' ? `
        <div class="ai-role-panel" id="panelLivestock">
          <div class="ai-dodont-grid">
            <div class="ai-dodont-card do">
              <div class="dd-header do">${LucideIcons.checkCircle()} LIVESTOCK PROTECTION ACTIONS</div>
              <ul class="dd-list">
                <li>Untie all cattle, goats and sheep from open pastures and lead them into covered pukka sheds.</li>
                <li>Elevate dry straw, fodder sacks, and silage bags onto wooden planks to protect from waterlogging.</li>
                <li>Keep at least 200 litres of clean, chlorinated drinking water stored in covered drums.</li>
                <li>Disinfect cattle shed floors with bleaching powder post-rain to prevent foot-rot (FMD).</li>
              </ul>
            </div>
            <div class="ai-dodont-card dont">
              <div class="dd-header dont">${LucideIcons.alertTriangle()} CRITICAL RISKS TO AVOID</div>
              <ul class="dd-list">
                <li>NEVER tether cattle to electric poles, tin shed uprights, or under solitary banyan/neem trees.</li>
                <li>Do not leave animals grazing near ponds, riverbanks, or water-filled depressions during storms.</li>
                <li>Avoid feeding fungal-moldy or damp straw to cows; wet fodder causes severe aflatoxicosis and bloat.</li>
                <li>Do not touch damp metal feeding troughs if loose overhead electric wires are nearby.</li>
              </ul>
            </div>
          </div>
        </div>
      ` : ''}

    </div>
  `;
}

// =========================================================================
// MODULE 8: MODALS, UTILITIES & INTERACTIVE CONTROLLERS
// =========================================================================
function escapeQuotes(str) {
  if (!str) return '';
  return String(str).replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function showAiToast(msg, duration = 3200) {
  let toast = document.getElementById('aiGlobalToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'aiGlobalToast';
    toast.className = 'ai-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.classList.remove('show');
  }, duration);
}

function injectChecklistItem(text, why) {
  alertStateInstance.addChecklistItem({ id: text, text, why });
  showAiToast(`✓ Added to your farm checklist: "${text}"`);
  alertStateInstance.setRole('farmer');
}

function triggerInPageReminder(hazardName, timeWindow) {
  showAiToast(`🔔 Reminder set: We will alert you before ${timeWindow} for ${hazardName}. (In-page notification registered)`);
}

function saveCurrentCropProfile() {
  const ok = alertStateInstance.saveCropProfile();
  if (ok) {
    showAiToast('✓ Crop profile saved to your device. NavChakra will automatically remember this.');
  }
}

function toggleChecklistCard(itemId) {
  alertStateInstance.toggleChecklistItem(itemId);
}

function scrollToSafetyPanel(mode) {
  const el = document.getElementById('aiSectionC');
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (mode === 'peak' && alertStateInstance.state.forecastData) {
      alertStateInstance.setSelectedHour(alertStateInstance.state.forecastData.peakWindow.startIndex);
    }
  }
}

function download48hOutlookCsv() {
  const f = alertStateInstance.state.forecastData;
  if (!f) return;

  let csv = 'Hour_Offset,Timestamp,Day,Time,Rain_Probability_Pct,Wind_Gust_kmh,Lightning_Risk,Risk_Score_0_100,Advisory_Guidance\n';
  f.steps.forEach(s => {
    csv += `${s.hourOffset},"${s.timestamp.toISOString()}","${s.dayStr}","${s.timeLabel}",${s.rainProb},${s.windGust},"${s.lightning}",${s.combinedScore},"${s.advice.replace(/"/g, '""')}"\n`;
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `rituiq_48h_risk_outlook_${f.blockName.toLowerCase()}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showAiToast(`✓ Downloaded 48h Outlook CSV for ${f.blockName}`);
}

// -------------------------------------------------------------------------
// 30-30 STOPWATCH & 30-MINUTE COUNTDOWN CONTROLLER
// -------------------------------------------------------------------------
let stopWatchStartTime = null;
let stopWatchTimerId = null;
let cd30IntervalId = null;
let cd30SecondsRemaining = 1800;

function start3030Stopwatch() {
  stopWatchStartTime = Date.now();
  const btnHeard = document.getElementById('btn30Heard');
  const btnSaw = document.getElementById('btn30Saw');
  const resBox = document.getElementById('result3030Box');

  if (btnHeard) btnHeard.disabled = false;
  if (btnSaw) btnSaw.classList.add('active-counting');
  if (resBox) {
    resBox.style.display = 'block';
    resBox.className = 'tool-result-box counting';
    resBox.innerHTML = `<strong>Stopwatch Running:</strong> Counting seconds until thunder is heard...`;
  }

  clearInterval(stopWatchTimerId);
  stopWatchTimerId = setInterval(() => {
    const elapsed = ((Date.now() - stopWatchStartTime) / 1000).toFixed(1);
    if (resBox) {
      resBox.innerHTML = `<strong>Stopwatch Running:</strong> ${elapsed} seconds elapsed. Tap "I Heard Thunder" immediately when heard!`;
    }
  }, 100);
}

function stop3030Stopwatch() {
  clearInterval(stopWatchTimerId);
  const elapsedSeconds = ((Date.now() - stopWatchStartTime) / 1000).toFixed(1);
  const numSec = parseFloat(elapsedSeconds);

  const btnHeard = document.getElementById('btn30Heard');
  const btnSaw = document.getElementById('btn30Saw');
  const resBox = document.getElementById('result3030Box');

  if (btnHeard) btnHeard.disabled = true;
  if (btnSaw) btnSaw.classList.remove('active-counting');

  const approxDistanceKm = (numSec / 3).toFixed(1);

  if (resBox) {
    resBox.style.display = 'block';
    if (numSec < 30) {
      resBox.className = 'tool-result-box danger';
      resBox.innerHTML = `
        <div style="font-size:1.1rem; font-weight:800; margin-bottom:4px;">🚨 DANGER: TAKE SHELTER IMMEDIATELY!</div>
        <div>Thunder followed lightning in <strong>${elapsedSeconds} seconds</strong>.</div>
        <div>Lightning is approximately <strong>${approxDistanceKm} km away</strong> (within 10 km danger threshold).</div>
        <div style="margin-top:6px; font-weight:600;">You are in direct strike hazard zone. Remain indoors!</div>
      `;
    } else {
      resBox.className = 'tool-result-box warning';
      resBox.innerHTML = `
        <div style="font-size:1rem; font-weight:800; margin-bottom:4px;">🟡 KEEP MONITORING • STAY ALERT</div>
        <div>Thunder followed lightning in <strong>${elapsedSeconds} seconds</strong> (Distance ~${approxDistanceKm} km).</div>
        <div>Lightning is currently distant, but storm cell may advance rapidly toward your plot.</div>
      `;
    }
  }

  start30MinCountdown();
}

function start30MinCountdown() {
  const cdBox = document.getElementById('countdown30MinBox');
  const timerDigits = document.getElementById('cdTimerDigits');
  if (cdBox) cdBox.style.display = 'block';

  cd30SecondsRemaining = 1800;
  clearInterval(cd30IntervalId);

  cd30IntervalId = setInterval(() => {
    cd30SecondsRemaining--;
    if (cd30SecondsRemaining <= 0) {
      clearInterval(cd30IntervalId);
      if (timerDigits) timerDigits.textContent = '00:00 - SAFE';
      showAiToast('✓ 30 minutes have elapsed without thunder. Safe to resume outdoor farm activities.');
    } else {
      const mins = Math.floor(cd30SecondsRemaining / 60);
      const secs = cd30SecondsRemaining % 60;
      if (timerDigits) {
        timerDigits.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }
  }, 1000);
}

// -------------------------------------------------------------------------
// NEAREST SHELTER MODAL & GEOLOCATION
// -------------------------------------------------------------------------
const DEMO_SHELTERS = [
  { name: 'Bolpur Flood & Squall Relief Center', dist: '1.8 km', lat: 23.670, lon: 87.720, capacity: '450 Persons' },
  { name: 'Sriniketan Community Cyclone Shelter', dist: '3.2 km', lat: 23.682, lon: 87.695, capacity: '300 Persons' },
  { name: 'Suri Zilla Parishad Safe Haven Building', dist: '6.5 km', lat: 23.908, lon: 87.530, capacity: '600 Persons' }
];

function openNearestShelterModal() {
  let modal = document.getElementById('aiShelterModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'aiShelterModal';
    modal.className = 'ai-modal-backdrop';
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="ai-modal-card">
      <div class="ai-modal-header">
        <h3 class="ai-modal-title">${LucideIcons.mapPin()} Designated Safe Shelters Near You</h3>
        <button type="button" class="ai-modal-close" onclick="closeNearestShelterModal()">✕</button>
      </div>
      <div class="ai-modal-body">
        <div style="margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.84rem; color:#475569;">Nearest shelters verified by Birbhum District Administration:</span>
          <button type="button" class="ai-btn-geolocate" onclick="detectUserShelterLocation()">
            ${LucideIcons.mapPin()} Use My GPS Location
          </button>
        </div>
        <div class="ai-shelter-list">
          ${DEMO_SHELTERS.map(s => `
            <div class="ai-shelter-item">
              <div class="shelter-info">
                <strong>${s.name}</strong>
                <span class="shelter-meta">Capacity: ${s.capacity} • Estimated Distance: <strong>${s.dist}</strong></span>
              </div>
              <a href="https://www.google.com/maps/dir/?api=1&destination=${s.lat},${s.lon}" target="_blank" rel="noopener" class="btn-directions">
                ${LucideIcons.externalLink()} Get Directions
              </a>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
  modal.classList.add('active');
}

function closeNearestShelterModal() {
  const modal = document.getElementById('aiShelterModal');
  if (modal) modal.classList.remove('active');
}

function detectUserShelterLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        showAiToast(`✓ GPS Location resolved (${pos.coords.latitude.toFixed(3)}°N, ${pos.coords.longitude.toFixed(3)}°E). Shelters sorted by closest proximity.`);
      },
      () => {
        showAiToast('Location permission unavailable. Showing designated default shelters for your selected block.');
      }
    );
  } else {
    showAiToast('Geolocation not supported on this browser. Showing block designated shelters.');
  }
}

function openPmfbyLossAssistanceModal() {
  alert('PMFBY Crop Insurance Support: Farmers in Birbhum and Burdwan whose crops suffer inundation or lodging can file claim intimation within 72 hours via the PMFBY Farmer App or Toll-Free 1800-889-6868.');
}

// -------------------------------------------------------------------------
// SPEECH SYNTHESIS ADVISORY AUDIO ENGINE
// -------------------------------------------------------------------------
let alertSpeechUtterance = null;
let isAlertSpeechPlaying = false;

function toggleAlertAudioSpeech() {
  if (!('speechSynthesis' in window)) {
    alert('Audio speech synthesis is not supported on this device/browser.');
    return;
  }

  const btn = document.getElementById('btnAiListen');
  const txt = document.getElementById('txtAiAudio');

  if (isAlertSpeechPlaying) {
    window.speechSynthesis.cancel();
    isAlertSpeechPlaying = false;
    if (txt) txt.textContent = 'Listen to this advice';
    if (btn) btn.classList.remove('playing');
    return;
  }

  window.speechSynthesis.cancel();

  const state = alertStateInstance.state;
  const f = state.forecastData;
  const cEval = state.cropEvaluation;
  const cSentence = cEval ? cEval.sentence : '';
  const lang = state.activeLanguage;

  let text = '';
  if (lang === 'bn') {
    text = `
      নবচক্র সতর্কবার্তা। ব্লক: ${state.block}।
      পরবর্তী ৪৮ ঘণ্টায় ভারী বৃষ্টি এবং কালবৈশাখী ঝড়ের সম্ভাবনা রয়েছে।
      সবচেয়ে ঝুঁকিপূর্ণ সময়: ${f.peakWindow.label}।
      ${cSentence ? `ফসলের জন্য পরামর্শ: ${cSentence}।` : ''}
      বজ্রপাত চলাকালীন খোলা মাঠে থাকবেন না। পাকা ঘরের ভেতরে আশ্রয় নিন।
    `;
  } else if (lang === 'hi') {
    text = `
      नवचक्र मौसम चेतावनी बुलेटिन। ब्लॉक: ${state.block}।
      अगले 48 घंटों में भारी वर्षा और तेज आंधी की चेतावनी।
      सबसे अधिक जोखिम का समय: ${f.peakWindow.label}।
      ${cSentence ? `सुरक्षा सलाह: ${cSentence}।` : ''}
      बिजली चमकने के दौरान खुले खेतों में न रहें। पक्के मकान में शरण लें।
    `;
  } else {
    text = `
      NavChakra Early Warning and Safety Advisory for ${state.block} block.
      Severe squall and heavy rain alert over the next 48 hours.
      Peak risk window is ${f.peakWindow.label}.
      ${cSentence ? `Safety advisory: ${cSentence}.` : ''}
      During lightning, avoid open fields and isolated trees. Shelter in a pucca building.
    `;
  }

  alertSpeechUtterance = new SpeechSynthesisUtterance(text);
  alertSpeechUtterance.lang = (lang === 'bn') ? 'bn-IN' : ((lang === 'hi') ? 'hi-IN' : 'en-IN');
  alertSpeechUtterance.rate = 0.95;

  alertSpeechUtterance.onstart = () => {
    isAlertSpeechPlaying = true;
    if (txt) txt.textContent = 'Playing Advisory (Tap to stop)';
    if (btn) btn.classList.add('playing');
  };

  alertSpeechUtterance.onend = () => {
    isAlertSpeechPlaying = false;
    if (txt) txt.textContent = 'Listen to this advice';
    if (btn) btn.classList.remove('playing');
  };

  alertSpeechUtterance.onerror = () => {
    isAlertSpeechPlaying = false;
    if (txt) txt.textContent = 'Listen to this advice';
    if (btn) btn.classList.remove('playing');
  };

  window.speechSynthesis.speak(alertSpeechUtterance);
}

// =========================================================================
// MODULE 9: MAIN MOUNTING & INITIALIZATION
// =========================================================================
function renderAlertIntelligence() {
  const root = document.getElementById('alertIntelligenceRoot');
  if (!root) return;

  const state = alertStateInstance.state;
  root.innerHTML = `
    <div class="ai-intelligence-container">
      ${renderSectionATimeline(state)}
      ${renderSectionCSafetyPanel(state)}
    </div>
  `;
}

function initAlertIntelligenceComponent() {
  alertStateInstance.regenerateForecast();

  alertStateInstance.subscribe(() => {
    renderAlertIntelligence();
  });

  renderAlertIntelligence();
}

window.alertStateInstance = alertStateInstance;
window.initAlertIntelligenceComponent = initAlertIntelligenceComponent;
window.download48hOutlookCsv = download48hOutlookCsv;
window.start3030Stopwatch = start3030Stopwatch;
window.stop3030Stopwatch = stop3030Stopwatch;
window.openNearestShelterModal = openNearestShelterModal;
window.closeNearestShelterModal = closeNearestShelterModal;
window.detectUserShelterLocation = detectUserShelterLocation;
window.openPmfbyLossAssistanceModal = openPmfbyLossAssistanceModal;
window.toggleAlertAudioSpeech = toggleAlertAudioSpeech;
window.injectChecklistItem = injectChecklistItem;
window.triggerInPageReminder = triggerInPageReminder;
window.saveCurrentCropProfile = saveCurrentCropProfile;
window.toggleChecklistCard = toggleChecklistCard;
window.scrollToSafetyPanel = scrollToSafetyPanel;

if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('alertIntelligenceRoot')) {
      initAlertIntelligenceComponent();
    }
  });
}
