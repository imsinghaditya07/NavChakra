/**
 * Kisan Sewa & Kharif Crop Advisory Intelligence Engine
 * ARYASAARTHI Meteorological & Agronomic Decision Support System
 * 
 * Reusable Architecture:
 * - <CropSelector />
 * - <WeatherSummary />
 * - <AdvisoryStatus />
 * - <AdvisoryGrid /> & <AdvisoryCard />
 * - <AdvisoryModal />
 * - <AudioAdvisory />
 * - <GroundObservationModal />
 */

// =========================================================================
// 1. KHARIF CROPS & STAGES REPOSITORY
// =========================================================================
const KHARIF_CROPS = [
  { id: 'paddy', name: '🌾 Paddy / Rice (धान)', nameEn: 'Paddy / Rice', nameHi: 'धान', icon: '🌾', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'maize', name: '🌽 Maize (मक्का)', nameEn: 'Maize', nameHi: 'मक्का', icon: '🌽', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'bajra', name: '🌾 Bajra / Pearl Millet (बाजरा)', nameEn: 'Bajra', nameHi: 'बाजरा', icon: '🌾', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'jowar', name: '🌾 Jowar / Sorghum (ज्वार)', nameEn: 'Jowar', nameHi: 'ज्वार', icon: '🌾', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'ragi', name: '🌱 Ragi / Finger Millet (रागी)', nameEn: 'Ragi', nameHi: 'रागी', icon: '🌱', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'arhar', name: '🌱 Arhar / Pigeon Pea (अरहर / तुअर)', nameEn: 'Arhar / Pigeon Pea', nameHi: 'अरहर', icon: '🌱', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'moong', name: '🌱 Moong / Green Gram (मूंग)', nameEn: 'Moong', nameHi: 'मूंग', icon: '🌱', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'urad', name: '🌱 Urad / Black Gram (उड़द)', nameEn: 'Urad', nameHi: 'उड़द', icon: '🌱', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'soybean', name: '🫘 Soybean (सोयाबीन)', nameEn: 'Soybean', nameHi: 'सोयाबीन', icon: '🫘', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'groundnut', name: '🥜 Groundnut (मूंगफली)', nameEn: 'Groundnut', nameHi: 'मूंगफली', icon: '🥜', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'sesame', name: '🌿 Sesame / Til (तिल)', nameEn: 'Sesame', nameHi: 'तिल', icon: '🌿', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'cotton', name: '🌿 Cotton (कपास)', nameEn: 'Cotton', nameHi: 'कपास', icon: '🌿', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'jute', name: '🌿 Jute / Pat (जूट / पटसन)', nameEn: 'Jute', nameHi: 'जूट', icon: '🌿', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'sugarcane', name: '🎋 Sugarcane (गन्ना)', nameEn: 'Sugarcane', nameHi: 'गन्ना', icon: '🎋', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'vegetables', name: '🥬 Vegetables (सब्जियां)', nameEn: 'Vegetables', nameHi: 'सब्जियां', icon: '🥬', season: 'Kharif', supportedRegions: ['All'] },
  { id: 'mustard', name: '🌼 Mustard (सरसों - Seasonal)', nameEn: 'Mustard', nameHi: 'सरसों', icon: '🌼', season: 'Late Kharif / Toria', supportedRegions: ['North', 'East', 'Central'] }
];

const CROP_STAGES = [
  { id: 'field_prep', name: '🚜 Field Preparation (खेत की तैयारी)' },
  { id: 'seed_treatment', name: '🧪 Seed Treatment (बीज शोधन)' },
  { id: 'sowing_nursery', name: '🌱 Sowing / Nursery (बुवाई / नर्सरी)' },
  { id: 'transplanting', name: '🌿 Transplanting (रोपाई)' },
  { id: 'germination', name: '🌱 Germination (अंकुरण)' },
  { id: 'vegetative', name: '🌿 Vegetative Growth (वानस्पतिक वृद्धि)' },
  { id: 'flowering', name: '🌸 Flowering (फूल आना)' },
  { id: 'grain_pod', name: '🌾 Grain / Pod Formation (दाना / फली भराव)' },
  { id: 'maturity', name: '🍂 Crop Maturity (परिपक्वता)' },
  { id: 'harvest', name: '🌾 Harvest (कटाई)' },
  { id: 'post_harvest', name: '📦 Post-Harvest & Storage (भंडारण)' }
];

// Default demo meteorological state as requested
const DEFAULT_ADVISORY_STATE = {
  location: 'Muzaffarpur',
  block: 'Mushahari (Muzaffarpur Sadar)',
  crop: 'paddy',
  cropStage: 'vegetative',
  season: 'Kharif 2026',
  rainfall24h: 42,
  rainfallForecast24h: 58,
  rainfallForecast72h: 95,
  weatherForecast: 'Heavy Rain Possible',
  temperature: 31,
  humidity: 82,
  windSpeed: 18,
  soilMoisture: 'High'
};

let kisanCurrentState = { ...DEFAULT_ADVISORY_STATE };
let currentGeneratedAdvisories = null;
let kisanAudioUtterance = null;
let isKisanAudioPlaying = false;

// =========================================================================
// 2. CENTRALIZED ADVISORY DECISION ENGINE (WEATHER → RISK → ACTION → TIMING)
// =========================================================================
/**
 * Pure agronomic advisory engine.
 * Generates 8 core recommendations based on Location, Crop, Growth Stage, and Weather Parameters.
 */
function generateCropAdvisory(params) {
  const p = { ...DEFAULT_ADVISORY_STATE, ...params };
  const cropObj = KHARIF_CROPS.find(c => c.id === p.crop) || KHARIF_CROPS[0];
  const stageObj = CROP_STAGES.find(s => s.id === p.cropStage) || CROP_STAGES[5];
  const isHeavyRain = (p.rainfallForecast24h >= 35 || p.rainfall24h >= 35 || (p.weatherForecast && p.weatherForecast.toLowerCase().includes('heavy')));
  const isModerateRain = (!isHeavyRain && (p.rainfallForecast24h >= 10 || p.rainfall24h >= 10));
  const isDrySpell = (!isHeavyRain && !isModerateRain && p.rainfallForecast72h < 5);
  const isHighWind = (p.windSpeed >= 25);
  const isHighHumidity = (p.humidity >= 75);
  const isHighTemp = (p.temperature >= 35);

  // 1. Determine Overall Advisory Status Banner
  let overall = {
    tier: 'ACTION REQUIRED',
    statusClass: 'status-action',
    badge: '⚠️ FIELD ACTION REQUIRED',
    headline: `Heavy rainfall (${p.rainfallForecast24h} mm) expected within the next 24 hours in ${p.location}. Postpone fertilizer application, suspend chemical spraying, and open field drainage channels immediately.`,
    hindiHeadline: `अगले 24 घंटों में ${p.location} में भारी बारिश (${p.rainfallForecast24h} मिमी) की संभावना है। यूरिया/खाद का छिड़काव तुरंत रोकें और खेतों से जल निकासी नाली खोलें।`
  };

  if (isHeavyRain) {
    overall = {
      tier: 'HIGH RISK',
      statusClass: 'status-danger',
      badge: '🔴 HIGH RISK: HEAVY RAIN INCOMING',
      headline: `Severe wet spell warning (${p.rainfallForecast24h} mm / 24h). Postpone all sowing and top-dressing; secure drainage and safeguard mature produce immediately.`,
      hindiHeadline: `भारी बारिश की चेतावनी (${p.rainfallForecast24h} मिमी / 24 घंटे)। बुवाई और यूरिया छिड़काव रोकें; जल निकासी की व्यवस्था करें।`
    };
  } else if (isDrySpell && isHighTemp) {
    overall = {
      tier: 'CAUTION',
      statusClass: 'status-caution',
      badge: '🟡 CAUTION: MOISTURE STRESS',
      headline: `Prolonged dry window with high temperature (${p.temperature}°C). Conserve soil moisture using organic mulching; apply life-saving micro-irrigation where possible.`,
      hindiHeadline: `कम वर्षा और तेज धूप (${p.temperature}°C)। मिट्टी में नमी संरक्षण के लिए मल्चिंग करें और आवश्यकतानुसार हल्की सिंचाई दें।`
    };
  } else if (isModerateRain) {
    overall = {
      tier: 'FAVOURABLE',
      statusClass: 'status-favourable',
      badge: '🟢 FAVOURABLE MONSOON CONDITIONS',
      headline: `Moderate rainfall anticipated (${p.rainfallForecast24h} mm). Favourable for crop vegetative growth; plan inter-cultivation and split fertilizer during brief dry intervals.`,
      hindiHeadline: `सामान्य मानसूनी वर्षा अनुकूल है (${p.rainfallForecast24h} मिमी)। फसल वानस्पतिक बढ़वार के लिए उत्तम स्थिति।`
    };
  } else if (isHighWind) {
    overall = {
      tier: 'ACTION REQUIRED',
      statusClass: 'status-action',
      badge: '🟠 ACTION REQUIRED: GALE GUSTS',
      headline: `Strong winds (${p.windSpeed} km/h) forecasted. Provide physical support/staking for tall standing crops and suspend all foliar spraying to prevent spray drift.`,
      hindiHeadline: `तेज हवाएं (${p.windSpeed} किमी/घंटा)। खड़ी फसलों को सहारा दें और किसी भी प्रकार का कीटनाशक छिड़काव स्थगित रखें।`
    };
  }

  // Weather Risk Pill
  let weatherRiskBadge = '⚠ WEATHER RISK: HEAVY RAIN';
  if (isHeavyRain) weatherRiskBadge = '⚠ WEATHER RISK: HEAVY RAIN';
  else if (isDrySpell) weatherRiskBadge = '🟡 WEATHER RISK: DRY SPELL / DEFICIT';
  else if (isHighWind) weatherRiskBadge = '🟠 WEATHER RISK: HIGH WIND GUSTS';
  else if (isModerateRain) weatherRiskBadge = '🟢 WEATHER RISK: LOW / BENEFICIAL';
  else weatherRiskBadge = '🟢 WEATHER RISK: NORMAL KHARIF CONDITIONS';

  // -----------------------------------------------------------------------
  // Build 8 Core Advisory Cards
  // -----------------------------------------------------------------------

  // CARD 1: FIELD PREPARATION
  let card1 = {
    cardIndex: 1,
    icon: '🚜',
    category: 'Field Preparation',
    title: 'Field Preparation',
    statusBadge: isHeavyRain ? '⚠ Prepare Drainage' : (isDrySpell ? '✓ Deep Ploughing' : '✓ Fine Tilth Ready'),
    badgeClass: isHeavyRain ? 'badge-danger' : (isDrySpell ? 'badge-caution' : 'badge-success'),
    recommendation: isHeavyRain 
      ? 'Open and de-silt main drainage channels and bund cuts before rainfall.' 
      : (isDrySpell ? 'Carry out dust mulching to break soil capillary pores and arrest evaporation.' : 'Keep seedbed level and clear weeds during current clear conditions.'),
    reason: isHeavyRain 
      ? `Expected ${p.rainfallForecast24h} mm rain will saturate root-zone rapidly.` 
      : (isDrySpell ? 'High temperature accelerates topsoil moisture loss.' : 'Soil tilth is in ideal workable condition.'),
    timing: isHeavyRain ? 'Before rainfall window' : 'Within next 48 hours',
    details: {
      why: isHeavyRain 
        ? 'Heavy rainfall on closed fields results in immediate water stagnation, asphyxiating roots and causing collar rot in rainfed crops.' 
        : 'Proper field prep conserves moisture and creates an aerobic seed zone.',
      weatherBasis: `Rainfall 24h: ${p.rainfall24h} mm | Forecast: ${p.rainfallForecast24h} mm | Soil Moisture: ${p.soilMoisture}`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Clear all field inlet and outlet conduits to allow rapid water discharge.',
        'Strengthen field perimeter bunds to prevent muddy runoff from adjoining ditches.',
        'Keep farm machinery parked in elevated, sheltered shed areas.'
      ],
      whatToAvoid: [
        'Do not plough wet or submerged fields as this causes severe subsoil compaction.',
        'Avoid making narrow drainage channels that easily clog with vegetative debris.'
      ]
    }
  };

  // CARD 2: SOWING & TRANSPLANTING
  let card2Status = '⏸ Postpone Sowing';
  let card2Badge = 'badge-danger';
  let card2Rec = 'Postpone direct sowing and nursery transplanting until the wet spell ceases.';
  let card2Reason = `Heavy downpour (${p.rainfallForecast24h} mm) will dislodge seeds and drown seedlings.`;
  let card2Timing = 'After rainfall subsides (2–3 days)';

  if (p.cropStage === 'transplanting' || p.cropStage === 'sowing_nursery') {
    if (isHeavyRain) {
      card2Status = '⏸ Postpone Transplanting';
      card2Rec = 'Hold seedlings in the nursery bed; ensure nursery bed has active side drainage trenches.';
      card2Reason = 'Transplanting into submerged standing water leads to seedling rotting and poor root anchorage.';
    } else if (isModerateRain) {
      card2Status = '✓ Transplant Now';
      card2Badge = 'badge-success';
      card2Rec = 'Proceed with transplanting 20–25 day old seedlings; maintain 2–3 cm standing water in paddy.';
      card2Reason = 'Moisture levels and cloud cover reduce transplanting shock.';
      card2Timing = 'Immediate morning / evening hours';
    } else {
      card2Status = '🌱 Prepare Nursery';
      card2Badge = 'badge-info';
      card2Rec = 'Sow raised nursery beds and apply light sprinkling irrigation.';
      card2Reason = 'Controlled moisture needed for uniform seed sprouting.';
      card2Timing = 'Cool morning hours';
    }
  } else if (p.cropStage === 'vegetative' || p.cropStage === 'flowering') {
    card2Status = '✓ Stand Established';
    card2Badge = 'badge-success';
    card2Rec = 'Crop stand is fully established. Check plant population density across the plot.';
    card2Reason = 'Normal vegetative transition stage.';
    card2Timing = 'Season ongoing';
  } else if (isDrySpell) {
    card2Status = '⏸ Wait for Rain';
    card2Badge = 'badge-caution';
    card2Rec = 'Wait for soaking monsoon showers before sowing rainfed pulses/oilseeds.';
    card2Reason = 'Sowing in dry topsoil leads to patchy germination and poor stand establishment.';
    card2Timing = 'Upon arrival of wetting spell';
  }

  let card2 = {
    cardIndex: 2,
    icon: '🌱',
    category: 'Sowing & Transplanting',
    title: 'Sowing & Transplanting',
    statusBadge: card2Status,
    badgeClass: card2Badge,
    recommendation: card2Rec,
    reason: card2Reason,
    timing: card2Timing,
    details: {
      why: 'Germination and early root establishment dictate 40% of final yield. Heavy rain washes seeds away, while dry spells lead to seedling desiccation.',
      weatherBasis: `Temperature: ${p.temperature}°C | Humidity: ${p.humidity}% | Forecast: ${p.weatherForecast}`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Verify seed germination percentage (>85%) before planting.',
        'Treat seeds with Trichoderma viride @ 4g/kg seed for fungal root protection.',
        'Maintain optimum spacing (20 cm × 15 cm for paddy, 60 cm × 20 cm for maize).'
      ],
      whatToAvoid: [
        'Never broadcast untreated seeds on crust-hardened or waterlogged ground.',
        'Avoid transplanting over-aged seedlings (>30 days old) as tillering will be severely stunted.'
      ]
    }
  };

  // CARD 3: FERTILIZER
  let card3Status = '⏸ Postpone Application';
  let card3Badge = 'badge-danger';
  let card3Rec = 'Strictly postpone top-dressing with Urea, DAP, or MOP ahead of anticipated rainfall.';
  let card3Reason = 'Rainfall runoff causes heavy surface leaching and economic loss of expensive nutrients.';
  let card3Timing = 'Apply after dry window (48h post-rain)';

  if (isDrySpell) {
    card3Status = '⏸ Soil Moisture Deficit';
    card3Badge = 'badge-caution';
    card3Rec = 'Do not broadcast dry urea without sufficient root-zone soil moisture or irrigation.';
    card3Reason = 'Urea volatilizes as ammonia gas in dry hot soil, damaging foliage and wasting nitrogen.';
    card3Timing = 'With next irrigation / rainfall';
  } else if (isModerateRain) {
    card3Status = '✓ Split Application Ready';
    card3Badge = 'badge-success';
    card3Rec = 'Apply recommended second nitrogen dose in split doses once standing water drains to film level.';
    card3Reason = 'Moist soil facilitates quick nutrient uptake through root hairs.';
    card3Timing = 'Clear dry morning spell';
  }

  let card3 = {
    cardIndex: 3,
    icon: '🧪',
    category: 'Fertilizer Management',
    title: 'Fertilizer',
    statusBadge: card3Status,
    badgeClass: card3Badge,
    recommendation: card3Rec,
    reason: card3Reason,
    timing: card3Timing,
    details: {
      why: 'Fertilizer applied before torrential rain washes straight into drainage furrows, contaminating groundwater and leaving plants starved of nitrogen.',
      weatherBasis: `Forecast: ${p.weatherForecast} (${p.rainfallForecast24h} mm) | Humidity: ${p.humidity}%`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Drain standing excess water to a thin 2 cm film before broadcasting nitrogen.',
        'Mix neem-coated urea with moist soil 1 hour prior to application for slow release.',
        'Follow soil-health card balanced doses (NPK 100:50:50 for hybrid paddy/maize).'
      ],
      whatToAvoid: [
        'Never broadcast granular fertilizer when strong winds (>20 km/h) or downpours are imminent.',
        'Avoid applying excessive nitrogen under cloudy humid skies as it attracts stem borers.'
      ]
    }
  };

  // CARD 4: WATER MANAGEMENT
  let card4Status = isHeavyRain ? '⚠ Drain Excess Water' : (isDrySpell ? '💧 Light Irrigation Needed' : '✓ Conserve Moisture');
  let card4Badge = isHeavyRain ? 'badge-danger' : (isDrySpell ? 'badge-caution' : 'badge-success');
  let card4Rec = isHeavyRain 
    ? `Ensure field drainage. Clear field bund cuts to drain excess ${p.rainfallForecast24h} mm rainfall.` 
    : (isDrySpell ? 'Apply life-saving irrigation at critical growth stages (tillering/flowering).' : 'Conserve natural rain in fields with 5 cm bund height; no supplemental irrigation required.');
  let card4Reason = isHeavyRain 
    ? 'Soil moisture is already HIGH; additional rain risks complete root hypoxia.' 
    : (isDrySpell ? 'Soil moisture depleted; moisture stress impairs active nutrient absorption.' : 'Precipitation is well aligned with crop consumptive water use.');
  let card4Timing = isHeavyRain ? 'Immediate priority' : (isDrySpell ? 'During cooler evening hours' : 'Maintain routine check');

  let card4 = {
    cardIndex: 4,
    icon: '💧',
    category: 'Water Management',
    title: 'Water Management',
    statusBadge: card4Status,
    badgeClass: card4Badge,
    recommendation: card4Rec,
    reason: card4Reason,
    timing: card4Timing,
    details: {
      why: 'Proper water regulation prevents root asphyxiation in water-sensitive crops (maize, pulses, cotton) while maintaining critical water depth in paddy.',
      weatherBasis: `Rainfall 24h: ${p.rainfall24h} mm | Soil Moisture: ${p.soilMoisture} | Forecast: ${p.rainfallForecast24h} mm`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        cropObj.id === 'paddy' ? 'Maintain 3–5 cm water depth in vegetative paddy fields; drain excess over 7 cm.' : 'Maintain raised beds and ridge-and-furrow system to avoid root-zone waterlogging.',
        'Harvest excess runoff into on-farm rainwater ponds (Khet Talab) for later dry spell use.',
        'Check field bunds for rodent burrows and repair cracks to prevent water loss.'
      ],
      whatToAvoid: [
        'Do not let irrigation water stagnate in maize, arhar, or vegetable plots for more than 12 hours.',
        'Avoid flood irrigation during peak noon heat to prevent soil baking.'
      ]
    }
  };

  // CARD 5: PEST & DISEASE
  let card5Status = isHighHumidity ? '🟡 Monitor Closely' : '✓ Low Disease Pressure';
  let card5Badge = isHighHumidity ? 'badge-caution' : 'badge-success';
  let card5Rec = isHighHumidity 
    ? `Scout crop daily for ${cropObj.id === 'paddy' ? 'Blast & Sheath Blight lesions' : (cropObj.id === 'maize' ? 'Fall Armyworm whorl damage' : 'Fungal leaf spots and sucking pests')}.` 
    : 'Routine field scouting twice a week. No immediate chemical intervention required.';
  let card5Reason = isHighHumidity 
    ? `High humidity (${p.humidity}%) and warm weather (${p.temperature}°C) accelerate fungal spore germination.` 
    : 'Dry canopy and moderate winds keep pest populations below Economic Threshold Level (ETL).';
  let card5Timing = 'Morning inspection';

  let card5 = {
    cardIndex: 5,
    icon: '🐛',
    category: 'Pest & Disease Management',
    title: 'Pest & Disease',
    statusBadge: card5Status,
    badgeClass: card5Badge,
    recommendation: card5Rec,
    reason: card5Reason,
    timing: card5Timing,
    details: {
      why: 'Continuous monitoring enables biological and mechanical control before pests cross Economic Threshold Levels, saving chemical costs and preserving beneficial predators.',
      weatherBasis: `Humidity: ${p.humidity}% | Temp: ${p.temperature}°C | Forecast: ${p.weatherForecast}`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Install yellow sticky traps (10/acre) for whiteflies/aphids and pheromone traps (5/acre) for borers.',
        'Erect T-shaped bird perches (15/acre) to encourage natural predatory birds in the field.',
        'Only if ETL is crossed after rain subsides: Spray bio-pesticides like Neem Oil (Azadirachtin 1500 ppm @ 3 ml/L).'
      ],
      whatToAvoid: [
        'Never spray systemic chemical pesticides on wet foliage or when rain is expected within 4 hours.',
        'Do not use synthetic pyrethroids indiscriminately as they trigger resurgence of sucking pests.'
      ]
    }
  };

  // CARD 6: CROP CARE
  let card6Status = isHeavyRain ? '⏸ Wait for Dry Window' : '✓ Intercultural Operation';
  let card6Badge = isHeavyRain ? 'badge-caution' : 'badge-success';
  let card6Rec = isHeavyRain 
    ? 'Suspend manual hoeing and weeding until topsoil dries to workable moisture level.' 
    : 'Perform weeding and inter-cultivation to keep crop root-zone aerated and weed-free.';
  let card6Reason = isHeavyRain 
    ? 'Treading in muddy fields damages root hairs and spreads bacterial pathogens.' 
    : 'Crop is in critical vegetative window where weed competition severely reduces tillers.';
  let card6Timing = isHeavyRain ? '2–3 days post-rain' : 'Current dry window';

  let card6 = {
    cardIndex: 6,
    icon: '🌿',
    category: 'Crop Care & Interculture',
    title: 'Crop Care',
    statusBadge: card6Status,
    badgeClass: card6Badge,
    recommendation: card6Rec,
    reason: card6Reason,
    timing: card6Timing,
    details: {
      why: 'Weed-crop competition between 15–45 days after sowing robs up to 45% of soil nutrients and moisture. Timely interculture maintains soil aeration.',
      weatherBasis: `Soil Moisture: ${p.soilMoisture} | Wind: ${p.windSpeed} km/h`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Use cono-weeder or wheel-hoe in standing rows during optimum soil moisture (vapsa condition).',
        'In sugarcane or maize, earth up soil around stem bases to prevent lodging from gusty monsoonal winds.',
        'Spread crop residue mulch between wide-spaced rows to suppress weed seed emergence.'
      ],
      whatToAvoid: [
        'Do not weed in saturated waterlogged soil as roots are easily pulled out or traumatized.',
        'Avoid deep inter-row tillage that cuts lateral feeder roots during active tillering.'
      ]
    }
  };

  // CARD 7: HARVESTING
  let card7Status = (p.cropStage === 'maturity' || p.cropStage === 'harvest') ? (isHeavyRain ? '⚡ Harvest Before Rain' : '✓ Harvest Now') : '🌾 Monitor Crop Maturity';
  let card7Badge = (p.cropStage === 'maturity' || p.cropStage === 'harvest') ? (isHeavyRain ? 'badge-danger' : 'badge-success') : 'badge-info';
  let card7Rec = (p.cropStage === 'maturity' || p.cropStage === 'harvest')
    ? (isHeavyRain ? 'Harvest physiologically mature crop immediately before downpour begins.' : 'Harvest mature crop on bright sunny mornings; thresh and shade-dry promptly.')
    : 'Crop is in growing phase; maintain normal agronomic schedule until physiological maturity.';
  let card7Reason = isHeavyRain 
    ? 'Standing mature crop will lodge, resulting in grain shattering, discoloration, and viviparous sprouting.' 
    : 'Current crop stage does not require harvest operations.';
  let card7Timing = isHeavyRain ? 'Before storm onset' : 'At physiological maturity';

  let card7 = {
    cardIndex: 7,
    icon: '🌾',
    category: 'Harvest Planning',
    title: 'Harvesting',
    statusBadge: card7Status,
    badgeClass: card7Badge,
    recommendation: card7Rec,
    reason: card7Reason,
    timing: card7Timing,
    details: {
      why: 'Harvesting at 80–85% physiological maturity (grains golden yellow, moisture 20%) prevents shatter loss and avoids devastating field weather damage.',
      weatherBasis: `Rainfall Forecast: ${p.rainfallForecast24h} mm | Weather: ${p.weatherForecast}`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'If crop is 85% mature and heavy storms are forecast, harvest immediately with combine or sickle.',
        'Stack harvested bundles on high ground covered with tarpaulins to prevent water immersion.',
        'Ensure grain moisture is measured before threshing to prevent grain cracking.'
      ],
      whatToAvoid: [
        'Do not leave harvested sheaves lying scattered across open low-lying field furrows.',
        'Never harvest wet crop early in the morning with heavy dew on panicles.'
      ]
    }
  };

  // CARD 8: POST-HARVEST & STORAGE
  let card8Status = isHeavyRain ? '⚠ Protect Produce' : '✓ Dry & Safe Storage';
  let card8Badge = isHeavyRain ? 'badge-danger' : 'badge-success';
  let card8Rec = isHeavyRain 
    ? 'Shift all harvested bags and drying grains to covered pukka godowns; cover with watertight tarpaulins.' 
    : 'Sun dry threshed grains to below 12% moisture level before bagging in clean hermetic bags.';
  let card8Reason = isHeavyRain 
    ? 'Moisture ingress triggers Aspergillus mold, aflatoxin contamination, and rapid rotting.' 
    : 'Safe grain moisture protects against storage beetles, grain weevils, and damp fungal spoilage.';
  let card8Timing = isHeavyRain ? 'Immediate priority' : 'Bright sunny hours';

  let card8 = {
    cardIndex: 8,
    icon: '📦',
    category: 'Post-Harvest & Storage',
    title: 'Post-Harvest',
    statusBadge: card8Status,
    badgeClass: card8Badge,
    recommendation: card8Rec,
    reason: card8Reason,
    timing: card8Timing,
    details: {
      why: 'Up to 10% of agricultural production is lost post-harvest due to damp storage, fungal contamination, and improper grain drying.',
      weatherBasis: `Humidity: ${p.humidity}% | Forecast: ${p.weatherForecast}`,
      cropStage: `${cropObj.nameEn} • ${stageObj.name}`,
      whatToDo: [
        'Store grains in airtight Pusa bins, HDPE hermetic bags, or galvanized steel drums.',
        'Elevate grain sacks 30 cm above the floor on wooden pallets (dunnage) away from walls.',
        'Apply natural insect repellents like dried neem leaves (2% w/w) in grain storage bins.'
      ],
      whatToAvoid: [
        'Never stack grain bags directly onto damp concrete floors without polyethylene lining.',
        'Do not store freshly harvested wet grain without drying; it will heat up and spoil overnight.'
      ]
    }
  };

  return {
    params: p,
    crop: cropObj,
    cropStage: stageObj,
    overall,
    weatherRiskBadge,
    cards: [card1, card2, card3, card4, card5, card6, card7, card8]
  };
}

// =========================================================================
// 3. UI RENDERING & COMPONENT LIFECYCLE
// =========================================================================

/**
 * Initialize Kisan Crop Advisory Component
 */
function initCropAdvisoryComponent() {
  const container = document.getElementById('viewKisan');
  if (!container) return;

  // Render Skeleton Template
  container.innerHTML = `
    <!-- 1. HEADER -->
    <div class="kisan-header-bar">
      <div class="kisan-header-title-box">
        <h1 class="kisan-header-title">🌾 Kisan Sewa & Crop Advisory</h1>
        <p class="kisan-header-sub">
          Weather-based crop recommendations synchronized with rainfall, temperature and crop growth stage.
        </p>
      </div>
      <div class="kisan-header-actions">
        <button type="button" class="btn-kisan-audio" id="btnKisanAudio" onclick="toggleKisanAudioAdvisory()">
          <span id="kisanAudioIcon">🔊</span>
          <span id="kisanAudioText">Listen in Audio (आवाज़ में सुनें)</span>
        </button>
        <button type="button" class="btn-kisan-report" onclick="openKisanGroundObservationModal()">
          <span>📢</span> Report Ground Observation
        </button>
      </div>
    </div>

    <!-- 2. FARMER / CROP SELECTION BAR -->
    <div class="kisan-selection-panel">
      <div class="kisan-sel-group">
        <label for="kisanLocSelect" class="kisan-sel-label">Location (District)</label>
        <select id="kisanLocSelect" class="kisan-select" onchange="onKisanLocationChanged(this.value)">
          <option value="Muzaffarpur" selected>Muzaffarpur (मुज़फ़्फ़रपुर)</option>
          <option value="Patna">Patna (पटना)</option>
          <option value="Gaya">Gaya (गया)</option>
          <option value="Birbhum">Birbhum (बीरभूम)</option>
          <option value="Yavatmal">Yavatmal (यवतमाल)</option>
          <option value="Pune">Pune (पुणे)</option>
          <option value="Lucknow">Lucknow (लखनऊ)</option>
          <option value="Varanasi">Varanasi (वाराणसी)</option>
          <option value="Bhopal">Bhopal (भोपाल)</option>
          <option value="Coimbatore">Coimbatore (कोयंबटूर)</option>
        </select>
      </div>

      <div class="kisan-sel-group">
        <label for="kisanBlockSelect" class="kisan-sel-label">District / Block</label>
        <select id="kisanBlockSelect" class="kisan-select" onchange="onKisanBlockChanged(this.value)">
          <option value="Mushahari (Muzaffarpur Sadar)" selected>Mushahari (Muzaffarpur Sadar)</option>
          <option value="Kanti">Kanti</option>
          <option value="Motipur">Motipur</option>
          <option value="Marwan">Marwan</option>
          <option value="Saraiya">Saraiya</option>
        </select>
      </div>

      <div class="kisan-sel-group">
        <label for="kisanCropSelect" class="kisan-sel-label">Crop</label>
        <select id="kisanCropSelect" class="kisan-select" onchange="onKisanCropChanged(this.value)">
          ${KHARIF_CROPS.map(c => `<option value="${c.id}" ${c.id === 'paddy' ? 'selected' : ''}>${c.name}</option>`).join('')}
        </select>
      </div>

      <div class="kisan-sel-group">
        <label for="kisanStageSelect" class="kisan-sel-label">Crop Stage</label>
        <select id="kisanStageSelect" class="kisan-select" onchange="onKisanStageChanged(this.value)">
          ${CROP_STAGES.map(s => `<option value="${s.id}" ${s.id === 'vegetative' ? 'selected' : ''}>${s.name}</option>`).join('')}
        </select>
      </div>

      <div class="kisan-sel-group kisan-season-box">
        <label class="kisan-sel-label">Season</label>
        <div class="kisan-season-pill">Kharif 2026</div>
      </div>

      <div class="kisan-sel-action">
        <button type="button" class="btn-kisan-apply" onclick="applyKisanAdvisories()">
          Apply Advisory
        </button>
      </div>
    </div>

    <!-- 3. LIVE WEATHER SUMMARY STRIP -->
    <div class="kisan-weather-strip">
      <div class="kisan-weather-card">
        <div class="kisan-w-icon">🌧</div>
        <div class="kisan-w-info">
          <span class="kisan-w-label">Rainfall</span>
          <strong class="kisan-w-val" id="kisanValRainfall">${kisanCurrentState.rainfall24h} mm / 24h</strong>
        </div>
      </div>

      <div class="kisan-weather-card">
        <div class="kisan-w-icon">🌦</div>
        <div class="kisan-w-info">
          <span class="kisan-w-label">Forecast</span>
          <strong class="kisan-w-val" id="kisanValForecast">${kisanCurrentState.weatherForecast}</strong>
        </div>
      </div>

      <div class="kisan-weather-card">
        <div class="kisan-w-icon">🌡</div>
        <div class="kisan-w-info">
          <span class="kisan-w-label">Temperature</span>
          <strong class="kisan-w-val" id="kisanValTemp">${kisanCurrentState.temperature}°C</strong>
        </div>
      </div>

      <div class="kisan-weather-card">
        <div class="kisan-w-icon">💧</div>
        <div class="kisan-w-info">
          <span class="kisan-w-label">Humidity</span>
          <strong class="kisan-w-val" id="kisanValHumidity">${kisanCurrentState.humidity}%</strong>
        </div>
      </div>

      <div class="kisan-weather-card">
        <div class="kisan-w-icon">💨</div>
        <div class="kisan-w-info">
          <span class="kisan-w-label">Wind</span>
          <strong class="kisan-w-val" id="kisanValWind">${kisanCurrentState.windSpeed} km/h</strong>
        </div>
      </div>

      <div class="kisan-weather-badge-box">
        <div class="kisan-risk-badge" id="kisanWeatherRiskBadge">
          ${kisanCurrentState.rainfall24h >= 35 ? '⚠ WEATHER RISK: HEAVY RAIN' : '🟢 WEATHER RISK: NORMAL'}
        </div>
      </div>
    </div>



    <!-- 5. 8 CORE ADVISORY CARDS GRID (4 x 2 Desktop, 2 x 4 Tablet, 1-col Mobile) -->
    <div class="kisan-cards-grid" id="kisanCardsGrid">
      <!-- 8 Cards injected dynamically by updateCropAdvisoryUI() -->
    </div>

    <!-- 6. DETAIL MODAL / DRAWER -->
    <div class="kisan-modal-overlay" id="kisanDetailModalOverlay" onclick="if(event.target===this) closeKisanAdvisoryDetailModal()">
      <div class="kisan-detail-modal">
        <div class="kisan-modal-header">
          <div style="display:flex; align-items:center; gap:8px;">
            <span id="kisanModalIcon" style="font-size:1.5rem;">🚜</span>
            <h3 class="kisan-modal-title" id="kisanModalTitle">Field Preparation Advisory</h3>
          </div>
          <button type="button" class="kisan-modal-close" onclick="closeKisanAdvisoryDetailModal()">✕</button>
        </div>
        <div class="kisan-modal-body" id="kisanModalBody">
          <!-- Dynamic detail content -->
        </div>
      </div>
    </div>

    <!-- 7. REPORT GROUND OBSERVATION MODAL -->
    <div class="kisan-modal-overlay" id="kisanObsModalOverlay" onclick="if(event.target===this) closeKisanGroundObservationModal()">
      <div class="kisan-detail-modal" style="max-width:520px;">
        <div class="kisan-modal-header">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.4rem;">📢</span>
            <h3 class="kisan-modal-title">Report Ground Observation</h3>
          </div>
          <button type="button" class="kisan-modal-close" onclick="closeKisanGroundObservationModal()">✕</button>
        </div>
        <form class="kisan-obs-form" onsubmit="submitKisanGroundObservation(event)">
          <div class="kisan-form-group">
            <label class="kisan-form-label">Observation Type</label>
            <select id="kisanObsType" class="kisan-select" required>
              <option value="Rainfall" selected>🌧 Rainfall / जल वर्षा</option>
              <option value="Waterlogging">🌊 Waterlogging / जलभराव</option>
              <option value="Pest">🐛 Pest Attack / कीट प्रकोप</option>
              <option value="Disease">🍂 Disease / फसल रोग</option>
              <option value="Hailstorm">❄️ Hailstorm / ओलावृष्टि</option>
              <option value="Strong Wind">💨 Strong Wind / तेज आंधी</option>
              <option value="Crop Damage">🌾 Crop Damage / फसल क्षति</option>
              <option value="Dry Spell">☀️ Dry Spell / सूखा तनाव</option>
            </select>
          </div>

          <div class="kisan-form-group">
            <label class="kisan-form-label">Location</label>
            <input type="text" id="kisanObsLocation" class="kisan-input" readonly value="Muzaffarpur, Bihar" />
          </div>

          <div class="kisan-form-group">
            <label class="kisan-form-label">Field Observation Description</label>
            <textarea id="kisanObsDesc" class="kisan-textarea" rows="3" placeholder="Describe field conditions, standing water depth, pest symptoms, or damage observed..." required></textarea>
          </div>

          <div class="kisan-form-group">
            <label class="kisan-form-label">Upload Photo (Optional)</label>
            <input type="file" id="kisanObsFile" class="kisan-file-input" accept="image/*" onchange="previewKisanObsPhoto(this)" />
            <div id="kisanObsPhotoPreview" style="display:none; margin-top:8px;">
              <img id="kisanObsImgTag" src="" alt="Observation Preview" style="max-height:120px; border-radius:6px; border:1px solid #cbd5e1;" />
            </div>
          </div>

          <div id="kisanObsSuccessMsg" class="kisan-obs-success" style="display:none;">
            ✓ Observation submitted successfully. Thank you for empowering local farmer advisories!
          </div>

          <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:16px;">
            <button type="button" class="btn-kisan-secondary" onclick="closeKisanGroundObservationModal()">Cancel</button>
            <button type="submit" class="btn-kisan-primary" id="btnKisanObsSubmit">Submit Observation</button>
          </div>
        </form>
      </div>
    </div>
  `;

  // Synchronize location options with global appState if available
  syncKisanLocationsWithGlobalState();

  // Initial Advisory Calculation
  applyKisanAdvisories();
}

/**
 * Sync location dropdown with active system location
 */
function syncKisanLocationsWithGlobalState() {
  if (typeof appState !== 'undefined' && appState.locationHierarchy) {
    const loc = appState.locationHierarchy;
    if (loc.selectedDistrict) {
      kisanCurrentState.location = loc.selectedDistrict;
      const sel = document.getElementById('kisanLocSelect');
      if (sel) {
        let hasOpt = Array.from(sel.options).some(o => o.value === loc.selectedDistrict);
        if (!hasOpt) {
          const opt = document.createElement('option');
          opt.value = loc.selectedDistrict;
          opt.textContent = `${loc.selectedDistrict}${loc.selectedState ? ' (' + loc.selectedState + ')' : ''}`;
          sel.prepend(opt);
        }
        sel.value = loc.selectedDistrict;
      }
    }
    if (loc.selectedBlock) {
      kisanCurrentState.block = loc.selectedBlock;
    }
  }
}

/**
 * Handle Location Change
 */
function onKisanLocationChanged(locName) {
  kisanCurrentState.location = locName;
  
  // Populate realistic blocks for selected location
  const blkSel = document.getElementById('kisanBlockSelect');
  if (blkSel) {
    blkSel.innerHTML = '';
    const blockList = {
      'Muzaffarpur': ['Mushahari (Muzaffarpur Sadar)', 'Kanti', 'Motipur', 'Marwan', 'Saraiya', 'Sakra', 'Minapur', 'Bochahan'],
      'Patna': ['Danapur', 'Barh', 'Masaurhi', 'Phulwari Sharif', 'Fatwah', 'Bihta'],
      'Gaya': ['Bodh Gaya', 'Tekari', 'Sherghati', 'Manpur', 'Wazirganj'],
      'Birbhum': ['Bolpur Sriniketan', 'Suri I', 'Suri II', 'Nanoor', 'Ilambazar', 'Rampurhat I'],
      'Yavatmal': ['Pusad', 'Umarkhed', 'Digras', 'Darwha', 'Yavatmal Rural', 'Wani'],
      'Pune': ['Baramati', 'Haveli', 'Shirur', 'Junnar', 'Daund', 'Indapur'],
      'Lucknow': ['Bakshi Ka Talab', 'Sarojini Nagar', 'Mohanlalganj', 'Malihabad', 'Chinhat'],
      'Varanasi': ['Pindra', 'Kashi Vidyapeeth', 'Araziline', 'Cholapur', 'Harahua'],
      'Bhopal': ['Huzur', 'Berasia', 'Phanda'],
      'Coimbatore': ['Pollachi', 'Sulur', 'Anaimalai', 'Mettupalayam', 'Annur']
    };

    const blocks = blockList[locName] || [`${locName} Sadar`, `North ${locName}`, `South ${locName}`, `${locName} Rural`];
    blocks.forEach((b, idx) => {
      const opt = document.createElement('option');
      opt.value = b;
      opt.textContent = b;
      if (idx === 0) opt.selected = true;
      blkSel.appendChild(opt);
    });
    kisanCurrentState.block = blocks[0];
  }

  // Update weather state based on mock geographic regime
  if (locName === 'Birbhum' || locName === 'Muzaffarpur') {
    kisanCurrentState.rainfall24h = 42;
    kisanCurrentState.rainfallForecast24h = 58;
    kisanCurrentState.weatherForecast = 'Heavy Rain Possible';
    kisanCurrentState.temperature = 31;
    kisanCurrentState.humidity = 82;
    kisanCurrentState.windSpeed = 18;
    kisanCurrentState.soilMoisture = 'High';
  } else if (locName === 'Yavatmal' || locName === 'Gaya') {
    kisanCurrentState.rainfall24h = 4;
    kisanCurrentState.rainfallForecast24h = 8;
    kisanCurrentState.weatherForecast = 'Scattered Cloud / Deficit';
    kisanCurrentState.temperature = 34;
    kisanCurrentState.humidity = 58;
    kisanCurrentState.windSpeed = 12;
    kisanCurrentState.soilMoisture = 'Moderate';
  } else if (locName === 'Pune' || locName === 'Coimbatore') {
    kisanCurrentState.rainfall24h = 16;
    kisanCurrentState.rainfallForecast24h = 22;
    kisanCurrentState.weatherForecast = 'Light to Moderate Showers';
    kisanCurrentState.temperature = 28;
    kisanCurrentState.humidity = 76;
    kisanCurrentState.windSpeed = 15;
    kisanCurrentState.soilMoisture = 'Adequate';
  }

  updateKisanWeatherStrip();
  applyKisanAdvisories();
}

function onKisanBlockChanged(blkName) {
  kisanCurrentState.block = blkName;
  applyKisanAdvisories();
}

function onKisanCropChanged(cropId) {
  kisanCurrentState.crop = cropId;
  applyKisanAdvisories();
}

function onKisanStageChanged(stageId) {
  kisanCurrentState.cropStage = stageId;
  applyKisanAdvisories();
}

/**
 * Synchronize Weather Strip UI Elements
 */
function updateKisanWeatherStrip() {
  const rf = document.getElementById('kisanValRainfall');
  const fc = document.getElementById('kisanValForecast');
  const tp = document.getElementById('kisanValTemp');
  const hm = document.getElementById('kisanValHumidity');
  const wn = document.getElementById('kisanValWind');
  const bg = document.getElementById('kisanWeatherRiskBadge');

  if (rf) rf.textContent = `${kisanCurrentState.rainfall24h} mm / 24h`;
  if (fc) fc.textContent = kisanCurrentState.weatherForecast;
  if (tp) tp.textContent = `${kisanCurrentState.temperature}°C`;
  if (hm) hm.textContent = `${kisanCurrentState.humidity}%`;
  if (wn) wn.textContent = `${kisanCurrentState.windSpeed} km/h`;

  if (bg) {
    if (kisanCurrentState.rainfall24h >= 35 || kisanCurrentState.rainfallForecast24h >= 35) {
      bg.className = 'kisan-risk-badge badge-danger';
      bg.textContent = '⚠ WEATHER RISK: HEAVY RAIN';
    } else if (kisanCurrentState.rainfallForecast24h <= 5 && kisanCurrentState.temperature >= 34) {
      bg.className = 'kisan-risk-badge badge-caution';
      bg.textContent = '🟡 WEATHER RISK: MOISTURE STRESS';
    } else {
      bg.className = 'kisan-risk-badge badge-success';
      bg.textContent = '🟢 WEATHER RISK: FAVOURABLE KHARIF';
    }
  }
}

/**
 * Core Controller: Calculates and Renders the 8 Cards
 */
function applyKisanAdvisories() {
  currentGeneratedAdvisories = generateCropAdvisory(kisanCurrentState);
  updateKisanWeatherStrip();

  // 1. Update Main Advisory Banner
  const banner = document.getElementById('kisanAdvisoryBanner');
  const bBadge = document.getElementById('kisanBannerBadge');
  const bText = document.getElementById('kisanBannerText');

  if (banner && currentGeneratedAdvisories.overall) {
    const o = currentGeneratedAdvisories.overall;
    banner.className = `kisan-advisory-banner ${o.statusClass}`;
    if (bBadge) bBadge.textContent = o.badge;
    if (bText) bText.textContent = o.headline;
  }

  // 2. Render 8 Core Advisory Cards
  const grid = document.getElementById('kisanCardsGrid');
  if (!grid || !currentGeneratedAdvisories.cards) return;

  grid.innerHTML = currentGeneratedAdvisories.cards.map((c, idx) => `
    <div class="kisan-advisory-card" onclick="openKisanAdvisoryDetailModal(${idx})">
      <div class="kac-top-row">
        <div class="kac-title-box">
          <span class="kac-icon">${c.icon}</span>
          <strong class="kac-title">${c.title}</strong>
        </div>
        <span class="kac-status-badge ${c.badgeClass}">${c.statusBadge}</span>
      </div>

      <div class="kac-body">
        <p class="kac-recommendation">${c.recommendation}</p>
        <div class="kac-meta-row">
          <span class="kac-meta-tag"><strong>WHY:</strong> ${c.reason}</span>
          <span class="kac-meta-tag"><strong>WHEN:</strong> ${c.timing}</span>
        </div>
      </div>

      <div class="kac-footer">
        <button type="button" class="btn-kac-view" onclick="event.stopPropagation(); openKisanAdvisoryDetailModal(${idx})">
          View Details →
        </button>
      </div>
    </div>
  `).join('');
}

// =========================================================================
// 4. DETAIL DRAWER / MODAL
// =========================================================================
function openKisanAdvisoryDetailModal(cardIndex) {
  if (!currentGeneratedAdvisories || !currentGeneratedAdvisories.cards) return;
  const card = currentGeneratedAdvisories.cards[cardIndex];
  if (!card) return;

  const overlay = document.getElementById('kisanDetailModalOverlay');
  const icon = document.getElementById('kisanModalIcon');
  const title = document.getElementById('kisanModalTitle');
  const body = document.getElementById('kisanModalBody');

  if (icon) icon.textContent = card.icon;
  if (title) title.textContent = `${card.category} — ${card.statusBadge}`;

  if (body) {
    body.innerHTML = `
      <!-- Status Box -->
      <div class="kmd-status-box ${card.badgeClass}">
        <div style="font-size:0.85rem; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">Current Advisory Recommendation</div>
        <div style="font-size:1.1rem; font-weight:800; margin-top:4px;">${card.recommendation}</div>
      </div>

      <!-- Why & Weather Basis -->
      <div class="kmd-section">
        <h4 class="kmd-section-title">🔍 Why this recommendation?</h4>
        <p class="kmd-text">${card.details.why}</p>
      </div>

      <div class="kmd-meta-grid">
        <div class="kmd-meta-item">
          <span class="kmd-meta-label">Weather Basis</span>
          <strong class="kmd-meta-val">${card.details.weatherBasis}</strong>
        </div>
        <div class="kmd-meta-item">
          <span class="kmd-meta-label">Crop & Growth Stage</span>
          <strong class="kmd-meta-val">${card.details.cropStage}</strong>
        </div>
        <div class="kmd-meta-item">
          <span class="kmd-meta-label">Recommended Timing</span>
          <strong class="kmd-meta-val" style="color:#0f766e;">⏰ ${card.timing}</strong>
        </div>
      </div>

      <!-- What to Do -->
      <div class="kmd-section">
        <h4 class="kmd-section-title" style="color:#15803d;">✅ What To Do (अनुशंसित कार्य)</h4>
        <ul class="kmd-list do-list">
          ${card.details.whatToDo.map(item => `<li>${item}</li>`).join('')}
        </ul>
      </div>

      <!-- What to Avoid -->
      <div class="kmd-section">
        <h4 class="kmd-section-title" style="color:#dc2626;">❌ What To Avoid (सावधानियां एवं निषेध)</h4>
        <ul class="kmd-list avoid-list">
          ${card.details.whatToAvoid.map(item => `<li>${item}</li>`).join('')}
        </ul>
      </div>

      <div style="display:flex; justify-content:flex-end; margin-top:20px;">
        <button type="button" class="btn-kisan-primary" onclick="closeKisanAdvisoryDetailModal()">Close (बंद करें)</button>
      </div>
    `;
  }

  if (overlay) overlay.classList.add('active');
}

function closeKisanAdvisoryDetailModal() {
  const overlay = document.getElementById('kisanDetailModalOverlay');
  if (overlay) overlay.classList.remove('active');
}

// =========================================================================
// 5. AUDIO SPEECH SYNTHESIS ADVISORY (आवाज़ में सुनें)
// =========================================================================
function toggleKisanAudioAdvisory() {
  const icon = document.getElementById('kisanAudioIcon');
  const text = document.getElementById('kisanAudioText');
  const btn = document.getElementById('btnKisanAudio');

  if (!('speechSynthesis' in window)) {
    alert('Web Speech API is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
    return;
  }

  if (isKisanAudioPlaying) {
    window.speechSynthesis.cancel();
    isKisanAudioPlaying = false;
    if (icon) icon.textContent = '🔊';
    if (text) text.textContent = 'Listen in Audio (आवाज़ में सुनें)';
    if (btn) btn.classList.remove('playing');
    return;
  }

  window.speechSynthesis.cancel();

  if (!currentGeneratedAdvisories) {
    applyKisanAdvisories();
  }

  const p = kisanCurrentState;
  const o = currentGeneratedAdvisories.overall;
  const cards = currentGeneratedAdvisories.cards;

  // Build natural Hindi speech text
  const speechText = `
    किसान सेवा एवं फसल परामर्श बुलेटिन।
    स्थान: ${p.location}, ब्लॉक: ${p.block}।
    फसल: ${currentGeneratedAdvisories.crop.nameHi}, अवस्था: ${currentGeneratedAdvisories.cropStage.name}।
    मौसम पूर्वानुमान: 24 घंटे में ${p.rainfallForecast24h} मिलीमीटर वर्षा, तापमान ${p.temperature} डिग्री, आर्द्रता ${p.humidity} प्रतिशत।
    मुख्य सलाह: ${o.hindiHeadline || o.headline}।
    खाद प्रबंधन: ${cards[2].recommendation}।
    जल प्रबंधन: ${cards[3].recommendation}।
    कीट एवं रोग: ${cards[4].recommendation}।
    धन्यवाद। स्वस्थ फसल, समृद्ध किसान।
  `;

  kisanAudioUtterance = new SpeechSynthesisUtterance(speechText);
  kisanAudioUtterance.lang = 'hi-IN';
  kisanAudioUtterance.rate = 0.95;
  kisanAudioUtterance.pitch = 1.0;

  kisanAudioUtterance.onstart = function() {
    isKisanAudioPlaying = true;
    if (icon) icon.textContent = '⏸️';
    if (text) text.textContent = 'Playing Advisory (आवाज़ रोकें)';
    if (btn) btn.classList.add('playing');
  };

  kisanAudioUtterance.onend = function() {
    isKisanAudioPlaying = false;
    if (icon) icon.textContent = '🔊';
    if (text) text.textContent = 'Listen in Audio (आवाज़ में सुनें)';
    if (btn) btn.classList.remove('playing');
  };

  kisanAudioUtterance.onerror = function() {
    isKisanAudioPlaying = false;
    if (icon) icon.textContent = '🔊';
    if (text) text.textContent = 'Listen in Audio (आवाज़ में सुनें)';
    if (btn) btn.classList.remove('playing');
  };

  window.speechSynthesis.speak(kisanAudioUtterance);
}

// =========================================================================
// 6. GROUND OBSERVATION REPORTING MODAL & SUBMISSION
// =========================================================================
function openKisanGroundObservationModal() {
  const overlay = document.getElementById('kisanObsModalOverlay');
  const locInput = document.getElementById('kisanObsLocation');
  const successMsg = document.getElementById('kisanObsSuccessMsg');
  const preview = document.getElementById('kisanObsPhotoPreview');
  const desc = document.getElementById('kisanObsDesc');

  if (locInput) {
    locInput.value = `${kisanCurrentState.block || 'Sadar'}, ${kisanCurrentState.location}`;
  }
  if (successMsg) successMsg.style.display = 'none';
  if (preview) preview.style.display = 'none';
  if (desc) desc.value = '';

  if (overlay) overlay.classList.add('active');
}

function closeKisanGroundObservationModal() {
  const overlay = document.getElementById('kisanObsModalOverlay');
  if (overlay) overlay.classList.remove('active');
}

function previewKisanObsPhoto(input) {
  const preview = document.getElementById('kisanObsPhotoPreview');
  const img = document.getElementById('kisanObsImgTag');
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      if (img) img.src = e.target.result;
      if (preview) preview.style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function submitKisanGroundObservation(e) {
  e.preventDefault();
  const type = document.getElementById('kisanObsType')?.value || 'Rainfall';
  const loc = document.getElementById('kisanObsLocation')?.value || kisanCurrentState.location;
  const desc = document.getElementById('kisanObsDesc')?.value || '';
  const successMsg = document.getElementById('kisanObsSuccessMsg');
  const submitBtn = document.getElementById('btnKisanObsSubmit');

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
  }

  // Simulate instant client-side registration
  setTimeout(() => {
    if (successMsg) successMsg.style.display = 'block';
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submitted ✓';
    }

    // Auto-close modal after 2 seconds
    setTimeout(() => {
      closeKisanGroundObservationModal();
      if (submitBtn) submitBtn.textContent = 'Submit Observation';
    }, 2000);
  }, 400);
}

// Auto-boot upon window load or view switch
if (typeof window !== 'undefined') {
  window.KHARIF_CROPS = KHARIF_CROPS;
  window.CROP_STAGES = CROP_STAGES;
  window.DEFAULT_ADVISORY_STATE = DEFAULT_ADVISORY_STATE;
  window.kisanCurrentState = kisanCurrentState;
  window.generateCropAdvisory = generateCropAdvisory;
  window.initCropAdvisoryComponent = initCropAdvisoryComponent;
  window.applyKisanAdvisories = applyKisanAdvisories;
  window.onKisanLocationChanged = onKisanLocationChanged;
  window.onKisanBlockChanged = onKisanBlockChanged;
  window.onKisanCropChanged = onKisanCropChanged;
  window.onKisanStageChanged = onKisanStageChanged;
  window.openKisanAdvisoryDetailModal = openKisanAdvisoryDetailModal;
  window.closeKisanAdvisoryDetailModal = closeKisanAdvisoryDetailModal;
  window.toggleKisanAudioAdvisory = toggleKisanAudioAdvisory;
  window.openKisanGroundObservationModal = openKisanGroundObservationModal;
  window.closeKisanGroundObservationModal = closeKisanGroundObservationModal;
  window.previewKisanObsPhoto = previewKisanObsPhoto;
  window.submitKisanGroundObservation = submitKisanGroundObservation;

  document.addEventListener('DOMContentLoaded', () => {
    // If viewKisan exists in DOM, initialize
    if (document.getElementById('viewKisan')) {
      initCropAdvisoryComponent();
    }
  });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    KHARIF_CROPS,
    CROP_STAGES,
    DEFAULT_ADVISORY_STATE,
    generateCropAdvisory,
    initCropAdvisoryComponent,
    applyKisanAdvisories
  };
}

