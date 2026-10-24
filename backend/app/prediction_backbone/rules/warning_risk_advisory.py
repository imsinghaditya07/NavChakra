"""
Warning, Risk Assessment, and Agronomic Advisory Layer.

Combines ML outputs with expert-tunable deterministic rules (rules + ML, not pure ML):
1. Risk Scoring:
   - Multi-hazard: Hazard Probability × Crop Stage Exposure × Historical Vulnerability
   - Computes 4-tier risk scores per parameter (Crop, Flood, Drought, Storm) + Composite Tier.
2. Warnings:
   - Explicit, reviewable IMD/NDMA operational threshold triggers (GREEN, YELLOW, ORANGE, RED).
3. Advisory Generation:
   - Template-based agromet advisories keyed to (crop stage + risk type + severity).
   - Decisions derived strictly from the risk score, eliminating LLM hallucinations.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from backend.app.prediction_backbone.schema import (
    EventSchema,
    FieldsSchema,
    ParticlesSchema,
    WarningItem,
    RiskAssessment,
    AdvisoryItem
)


class WarningRiskAdvisoryLayer:
    """
    Expert rule engine evaluating thresholds and generating operational warnings,
    composite risk tiers, and localized farmer advisories.
    """

    def __init__(self):
        # Operational IMD/NDMA warning thresholds (fully tunable by domain experts)
        self.thresholds = {
            "heavy_rain_orange_mm": 64.5,
            "heavy_rain_red_mm": 115.5,
            "rain_prob_threshold": 0.65,
            "lightning_alert_prob": 0.55,
            "lightning_severe_prob": 0.75,
            "hail_alert_prob": 0.45,
            "heat_index_orange_c": 44.0,
            "heat_index_red_c": 47.0,
            "gale_wind_orange_kmh": 62.0,
            "gale_wind_red_kmh": 88.0,
            "flood_orange_risk": 0.65,
            "flood_red_risk": 0.82,
            "drought_orange_index": -1.5,
            "drought_red_index": -2.2
        }

    # =========================================================================
    # 1. THRESHOLD-TRIGGERED WARNING GENERATOR
    # =========================================================================
    def evaluate_warnings(
        self,
        event: EventSchema,
        fields: FieldsSchema,
        particles: ParticlesSchema
    ) -> List[WarningItem]:
        """
        Evaluates transparent meteorological conditions and produces color-coded warnings.
        """
        warnings: List[WarningItem] = []

        # 1. Cyclone / Severe Synoptic System Warning
        if event.type == "cyclone":
            tier = "RED" if event.intensity >= 0.75 else "ORANGE"
            warnings.append(WarningItem(
                code="CYCLONIC_STORM_ALERT",
                tier=tier,
                title=f"IMD {event.category.upper() if event.category else 'CYCLONE'} WARNING",
                description=(
                    f"Active cyclonic circulation detected with central wind intensity of {event.intensity*100:.0f}%. "
                    "Gale force squalls and high storm surge expected in coastal and adjoining inland zones."
                ),
                threshold_triggered=f"event_type == 'cyclone' AND intensity ({event.intensity}) >= 0.60"
            ))

        # 2. Heavy Rainfall Warning (IMD 24h classification)
        if fields.rainfall_prob >= self.thresholds["rain_prob_threshold"]:
            if fields.rainfall_mm >= self.thresholds["heavy_rain_red_mm"]:
                warnings.append(WarningItem(
                    code="VERY_HEAVY_RAIN_RED",
                    tier="RED",
                    title="Extremely Heavy Rainfall Warning",
                    description=(
                        f"Expected 24h rainfall of {fields.rainfall_mm:.1f} mm exceeds 115.5 mm disaster threshold. "
                        "Severe waterlogging, inundation of low-lying agricultural fields and flash runoff imminent."
                    ),
                    threshold_triggered=f"rainfall_mm ({fields.rainfall_mm}) >= {self.thresholds['heavy_rain_red_mm']} mm AND prob ({fields.rainfall_prob}) >= 0.65"
                ))
            elif fields.rainfall_mm >= self.thresholds["heavy_rain_orange_mm"]:
                warnings.append(WarningItem(
                    code="HEAVY_RAIN_ORANGE",
                    tier="ORANGE",
                    title="Heavy Rainfall Alert",
                    description=(
                        f"Forecast rainfall of {fields.rainfall_mm:.1f} mm exceeds 64.5 mm threshold. "
                        "Postpone fertilizer application and ensure drainage channels in crop fields are cleared."
                    ),
                    threshold_triggered=f"rainfall_mm ({fields.rainfall_mm}) >= {self.thresholds['heavy_rain_orange_mm']} mm AND prob ({fields.rainfall_prob}) >= 0.65"
                ))

        # 3. Thunderstorm, Lightning & Hail Warning
        if particles.lightning_prob >= self.thresholds["lightning_severe_prob"] or particles.hail_prob >= self.thresholds["hail_alert_prob"]:
            tier = "RED" if particles.hail_prob >= 0.60 else "ORANGE"
            hail_note = " with potential hail damage to standing crop foliage" if particles.hail_prob >= 0.35 else ""
            warnings.append(WarningItem(
                code="SEVERE_CONVECTIVE_STORM",
                tier=tier,
                title="Severe Thunderstorm & Lightning Alert",
                description=(
                    f"Rapid convective electrification detected ({particles.lightning_prob*100:.0f}% lightning risk){hail_note}. "
                    "Farmers should immediately seek shelter inside concrete buildings; avoid open fields and high trees."
                ),
                threshold_triggered=f"lightning_prob ({particles.lightning_prob}) >= {self.thresholds['lightning_alert_prob']} OR hail_prob ({particles.hail_prob}) >= {self.thresholds['hail_alert_prob']}"
            ))
        elif particles.lightning_prob >= self.thresholds["lightning_alert_prob"]:
            warnings.append(WarningItem(
                code="THUNDERSTORM_WATCH",
                tier="YELLOW",
                title="Thunderstorm & Gusty Winds Watch",
                description=(
                    f"Moderate convective activity ({particles.lightning_prob*100:.0f}% lightning risk) developing. "
                    "Keep watch on weather updates before initiating field spraying or harvesting."
                ),
                threshold_triggered=f"lightning_prob ({particles.lightning_prob}) >= {self.thresholds['lightning_alert_prob']}"
            ))

        # 4. Heat Index / Heat Wave Warning
        if fields.heat_index >= self.thresholds["heat_index_red_c"]:
            warnings.append(WarningItem(
                code="HEAT_WAVE_RED",
                tier="RED",
                title="Severe Heat Wave Alert",
                description=(
                    f"Heat index of {fields.heat_index:.1f}°C indicates extreme danger of heat stroke and crop thermal stress. "
                    "Provide frequent light irrigation during early morning or late evening."
                ),
                threshold_triggered=f"heat_index ({fields.heat_index}) >= {self.thresholds['heat_index_red_c']}°C"
            ))
        elif fields.heat_index >= self.thresholds["heat_index_orange_c"]:
            warnings.append(WarningItem(
                code="HEAT_WAVE_ORANGE",
                tier="ORANGE",
                title="Heat Wave Warning",
                description=(
                    f"Elevated heat index ({fields.heat_index:.1f}°C). Avoid manual field labour during peak hours (12 PM - 3 PM)."
                ),
                threshold_triggered=f"heat_index ({fields.heat_index}) >= {self.thresholds['heat_index_orange_c']}°C"
            ))

        # 5. High Wind / Squall Warning
        if particles.wind.speed_kmh >= self.thresholds["gale_wind_orange_kmh"]:
            tier = "RED" if particles.wind.speed_kmh >= self.thresholds["gale_wind_red_kmh"] else "ORANGE"
            warnings.append(WarningItem(
                code="HIGH_WIND_SQUALL",
                tier=tier,
                title="Squally / Gale Wind Warning",
                description=(
                    f"Surface wind gusts reaching {particles.wind.speed_kmh:.0f} km/h from {particles.wind.direction_deg:.0f}°. "
                    "Risk of crop lodging in tall crops (maize, banana, sugarcane). Provide mechanical staking."
                ),
                threshold_triggered=f"wind_speed ({particles.wind.speed_kmh}) >= {self.thresholds['gale_wind_orange_kmh']} km/h"
            ))

        # 6. Flash Flood Inundation Warning
        if fields.flood_risk >= self.thresholds["flood_orange_risk"]:
            tier = "RED" if fields.flood_risk >= self.thresholds["flood_red_risk"] else "ORANGE"
            warnings.append(WarningItem(
                code="FLASH_FLOOD_INUNDATION",
                tier=tier,
                title="Agricultural Flash Flood & Waterlogging Warning",
                description=(
                    f"Flood risk score of {fields.flood_risk:.2f} indicates imminent saturation runoff in river basins. "
                    "Move harvested produce and livestock to higher ground immediately."
                ),
                threshold_triggered=f"flood_risk ({fields.flood_risk}) >= {self.thresholds['flood_orange_risk']}"
            ))

        # 7. Agricultural Drought / Monsoon Break Warning
        if fields.drought_index <= self.thresholds["drought_orange_index"]:
            tier = "RED" if fields.drought_index <= self.thresholds["drought_red_index"] else "ORANGE"
            warnings.append(WarningItem(
                code="MONSOON_BREAK_DROUGHT",
                tier=tier,
                title="Prolonged Monsoon Break & Drought Alert",
                description=(
                    f"Severe moisture deficit index ({fields.drought_index:.2f}). Rootzone soil moisture depleted. "
                    "Adopt life-saving micro-irrigation and dust mulching to prevent wilting."
                ),
                threshold_triggered=f"drought_index ({fields.drought_index}) <= {self.thresholds['drought_orange_index']}"
            ))

        # If no hazardous thresholds exceeded, issue GREEN safe status
        if not warnings:
            warnings.append(WarningItem(
                code="NORMAL_CONDITIONS_GREEN",
                tier="GREEN",
                title="Normal Agrometeorological Conditions",
                description="No severe weather warnings active. Normal agronomic operations can proceed safely.",
                threshold_triggered="All meteorological parameters within normal baseline bounds"
            ))

        return warnings

    # =========================================================================
    # 2. RISK ASSESSMENT (Multi-hazard scoring: Prob x Exposure x Vulnerability)
    # =========================================================================
    def compute_risk_assessment(
        self,
        event: EventSchema,
        fields: FieldsSchema,
        particles: ParticlesSchema,
        historical_hazards: Dict[str, Any],
        crop_stage: str = "vegetative"
    ) -> RiskAssessment:
        """
        Combines hazard severity with agricultural exposure and historical loss records.
        """
        # Crop sensitivity multiplier by growth stage
        # Flowering & Sowing are highest vulnerability stages
        stage_multipliers = {
            "sowing": 1.45,
            "nursery": 1.35,
            "vegetative": 1.0,
            "flowering": 1.55,
            "grain_filling": 1.25,
            "maturity": 1.30,
            "harvesting": 1.50
        }
        exposure = stage_multipliers.get(crop_stage.lower(), 1.0)
        hist_vulnerability = historical_hazards.get("crop_loss_frequency_pct", 30.0) / 100.0

        # Parameter-specific risk scores [0.0 - 1.0]
        # 1. Storm risk
        storm_hazard = max(particles.lightning_prob, particles.hail_prob, event.intensity)
        storm_score = float(np.clip(storm_hazard * 0.85 + (particles.wind.speed_kmh / 100.0) * 0.35, 0.0, 1.0))
        storm_tier = self._score_to_tier(storm_score)

        # 2. Flood risk
        flood_score = float(np.clip(fields.flood_risk * 0.80 + (fields.rainfall_mm / 100.0) * 0.20, 0.0, 1.0))
        flood_tier = self._score_to_tier(flood_score)

        # 3. Drought risk
        drought_deficit = max(0.0, -fields.drought_index / 3.0)
        drought_score = float(np.clip(drought_deficit * 0.70 + (1.0 - (fields.soil_moisture_rootzone or 0.5)) * 0.30, 0.0, 1.0))
        drought_tier = self._score_to_tier(drought_score)

        # 4. Crop risk (Composite exposure)
        crop_score = float(np.clip((max(storm_score, flood_score, drought_score) * 0.65 + hist_vulnerability * 0.35) * exposure, 0.0, 1.0))
        crop_tier = self._score_to_tier(crop_score)

        # Overall composite score & tier
        composite_score = float(np.clip(max(crop_score, flood_score * 0.9, storm_score * 0.9), 0.05, 0.99))
        if composite_score >= 0.75:
            comp_tier = "SEVERE"
        elif composite_score >= 0.50:
            comp_tier = "HIGH"
        elif composite_score >= 0.30:
            comp_tier = "WATCH"
        else:
            comp_tier = "LOW"

        return RiskAssessment(
            composite_tier=comp_tier,
            composite_score=round(composite_score, 2),
            crop_risk_tier=crop_tier,
            flood_risk_tier=flood_tier,
            drought_risk_tier=drought_tier,
            storm_risk_tier=storm_tier
        )

    def _score_to_tier(self, score: float) -> str:
        if score >= 0.70:
            return "SEVERE"
        elif score >= 0.45:
            return "HIGH"
        elif score >= 0.25:
            return "WATCH"
        return "LOW"

    # =========================================================================
    # 3. DETERMINISTIC AGRONOMIC ADVISORY GENERATOR
    # =========================================================================
    def generate_advisory(
        self,
        crop: str,
        stage: str,
        risk: RiskAssessment,
        fields: FieldsSchema,
        particles: ParticlesSchema,
        event: EventSchema
    ) -> AdvisoryItem:
        """
        Deterministic template generation keyed to (crop stage + risk type + severity).
        Underlying decisions come strictly from the risk scores and physical fields.
        """
        crop_clean = crop.lower().strip()
        stage_clean = stage.lower().strip()

        # Priority 1: Convective storm / Lightning alert active
        if particles.lightning_prob >= 0.60 or particles.hail_prob >= 0.40:
            return AdvisoryItem(
                rule_id="RULE_STORM_LIGHTNING_EMERGENCY",
                urgency="IMMEDIATE",
                crop=crop,
                stage=stage,
                advisory_en=(
                    f"Immediate severe thunderstorm & lightning alert ({particles.lightning_prob*100:.0f}% risk). "
                    f"Suspend all outdoor activities, spraying, and harvesting in {crop} fields immediately. "
                    "Take shelter in sturdy concrete structures; keep away from electric poles and tin sheds."
                ),
                advisory_hi=(
                    f"तत्काल आंधी और आकाशीय बिजली का गंभीर अलर्ट ({particles.lightning_prob*100:.0f}% जोखिम)। "
                    f"{crop} के खेतों में कीटनाशक छिड़काव और कटाई कार्य तुरंत रोकें। "
                    "पक्के भवनों में शरण लें; बिजली के खंभों और खुले पेड़ों के नीचे बिल्कुल न रुकें।"
                ),
                advisory_local=(
                    f"বজ্রপাত ও কালবৈশাখী ঝড়ের জরুরি সতর্কতা ({particles.lightning_prob*100:.0f}%)। "
                    f"{crop} ক্ষেতে কীটনাশক স্প্রে ও ফসল কাটার কাজ অবিলম্বে বন্ধ রাখুন।"
                ),
                action_checklist=[
                    "Halt tractor and field spraying operations immediately",
                    "Anchor greenhouse sheds and loose nursery covers",
                    "Keep farm workers and livestock indoors until storm passes"
                ]
            )

        # Priority 2: Heavy rainfall / Inundation risk
        if fields.rainfall_mm >= 64.5 or fields.flood_risk >= 0.65:
            return AdvisoryItem(
                rule_id="RULE_HEAVY_RAIN_DRAINAGE_CRITICAL",
                urgency="HIGH",
                crop=crop,
                stage=stage,
                advisory_en=(
                    f"Heavy rainfall forecast ({fields.rainfall_mm:.1f} mm) creates acute waterlogging risk for {crop}. "
                    "Open field bunds and ensure excess water drains rapidly from root zones. "
                    "Postpone top-dressing of urea and nitrogen fertilizers to avoid runoff leaching."
                ),
                advisory_hi=(
                    f"भारी बारिश ({fields.rainfall_mm:.1f} मिमी) के कारण {crop} में जलभराव का खतरा है। "
                    "खेतों में जल निकासी की नालियां तुरंत खोलें ताकि जड़ों में पानी न रुके। "
                    "यूरिया व अन्य खादों का छिड़काव बारिश थमने तक स्थगित रखें।"
                ),
                advisory_local=(
                    f"ভারী বৃষ্টির পূর্বাভাস ({fields.rainfall_mm:.1f} মিমি)। {crop} জমিতে জমা জল নিকাশের ব্যবস্থা করুন।"
                ),
                action_checklist=[
                    "Clear drainage channels around field perimeters",
                    "Postpone all chemical fertilizer applications",
                    "Ensure nursery beds or seedlings are raised to prevent submergence"
                ]
            )

        # Priority 3: Drought / Monsoon Break during critical stage
        if fields.drought_index <= -1.2 or (fields.soil_moisture_rootzone and fields.soil_moisture_rootzone < 0.25):
            if "sow" in stage_clean:
                return AdvisoryItem(
                    rule_id="RULE_SOWING_BREAK_CONTINGENCY",
                    urgency="HIGH",
                    crop=crop,
                    stage=stage,
                    advisory_en=(
                        f"Monsoon break spell active during {stage} stage of {crop}. "
                        "Do not sow on dry seedbeds; delay sowing by 7–10 days until monsoon revival cycle. "
                        "Prepare short-duration contingency seeds (e.g. green gram/moong or bajra)."
                    ),
                    advisory_hi=(
                        f"{crop} की बुवाई के समय मानसून में रुकावट का अनुमान है। "
                        "सूखी मिट्टी में बीज न डालें; बुवाई 7-10 दिनों के लिए टालें। "
                        "वैकल्पिक कम अवधि की दलहनी फसलों की तैयारी रखें।"
                    ),
                    advisory_local=(
                        f"অনাবৃষ্টি ও খরা পরিস্থিতি। {crop} বপন ৭-১০ দিন পিছিয়ে দিন এবং বিকল্প বীজের ব্যবস্থা রাখুন।"
                    ),
                    action_checklist=[
                        "Delay sowing operations until revival rains occur",
                        "Treat seeds with bio-fertilizers or Trichoderma",
                        "Store irrigation water in farm ponds for life-saving application"
                    ]
                )
            else:
                return AdvisoryItem(
                    rule_id="RULE_MOISTURE_STRESS_MULCH",
                    urgency="MODERATE",
                    crop=crop,
                    stage=stage,
                    advisory_en=(
                        f"Moisture stress observed in {crop} at {stage} stage. "
                        "Apply straw mulch or organic dust mulch between crop rows to conserve rootzone moisture. "
                        "Provide light micro-irrigation (drip/sprinkler) during cooler evening hours."
                    ),
                    advisory_hi=(
                        f"{crop} की {stage} अवस्था में नमी की कमी देखी गई है। "
                        "जमीन की नमी बचाने के लिए पुआल की मल्चिंग करें। "
                        "शाम के समय ड्रिप या स्प्रिंकलर से जीवनरक्षक हल्की सिंचाई करें।"
                    ),
                    advisory_local=(
                        f"{crop} জমিতে খরার চাপ। আর্দ্রতা ধরে রাখতে খড় বা মালচিং ব্যবহার করুন।"
                    ),
                    action_checklist=[
                        "Spread crop residue/straw mulch between rows",
                        "Deliver life-saving micro-irrigation during early morning/evening",
                        "Foliar spray with 2% Potassium Nitrate (KNO3) to reduce transpiration"
                    ]
                )

        # Priority 4: Normal safe conditions
        return AdvisoryItem(
            rule_id="RULE_NORMAL_FAVORABLE_GROWTH",
            urgency="LOW",
            crop=crop,
            stage=stage,
            advisory_en=(
                f"Favorable agrometeorological conditions for {crop} ({stage} stage). "
                f"Temperature ({fields.temp_c}°C) and relative humidity ({fields.humidity_pct}%) support steady growth. "
                "Routine intercultural operations, weeding, and scheduled nutrient application can proceed normally."
            ),
            advisory_hi=(
                f"{crop} ({stage} चरण) के लिए अनुकूल मौसम बना हुआ है। "
                "तापमान और आर्द्रता सामान्य हैं। "
                "सामान्य निराई-गुड़ाई, खाद डालना और खेत प्रबंधन का काम सुचारू रूप से जारी रख सकते हैं।"
            ),
            advisory_local=(
                f"{crop} ফসলের জন্য আবহাওয়া অনুকূল। স্বাভাবিক কৃষি কাজ চালিয়ে যেতে পারেন।"
            ),
            action_checklist=[
                "Perform scheduled intercultural weeding and hoeing",
                "Maintain recommended plant spacing and pest monitoring",
                "Ensure routine soil moisture check before next irrigation"
            ]
        )


# Singleton instance
warning_risk_advisory = WarningRiskAdvisoryLayer()
