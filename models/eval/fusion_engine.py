"""
Fusion Layer & Safety Override Engine for Hyperlocal Risk Assessment.
Combines:
1. Model A: Seasonal Onset & Break Probability (7-30 Days)
2. Model B: Convective Nowcasting Probability (0-30 Mins)
3. Live Radar / Satellite / Sensor Telemetry
4. Verified Crowd-Source Ground Observations & Disagreement Override

Explicit Formula:
  RiskScore = w_A * P_break + w_B * P_storm + w_live * I_radar
  Tiers:
    0.00 <= RiskScore < 0.35 : GREEN (Safe / Normal Operations)
    0.35 <= RiskScore < 0.60 : YELLOW (Watch / Moisture Alert)
    0.60 <= RiskScore < 0.80 : ORANGE (High Alert / Action Required)
    0.80 <= RiskScore <= 1.00: RED (Severe Warning / Emergency)

Failure-Mode Override Fallback:
  If Ground Observations >= 3 reports of severe rain/squall OR rain_gauge >= 15 mm/hr
  AND Model Risk was predicted as GREEN (< 0.35),
  FORCE OVERRIDE to RED (Emergency Alert) with audit trail tag: "OVERRIDE_CROWD_DISAGREEMENT".
"""

import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class HyperlocalFusionEngine:
    def __init__(self, weight_a: float = 0.40, weight_b: float = 0.45, weight_live: float = 0.15):
        self.w_a = weight_a
        self.w_b = weight_b
        self.w_live = weight_live

    def compute_risk(
        self,
        prob_break: float,
        prob_storm: float,
        live_radar_intensity: float = 0.0,
        crowd_reports_count: int = 0,
        crowd_report_type: str = "clear",
        live_rain_rate_mmh: float = 0.0
    ) -> dict:
        """
        Executes explicit fusion and failure-mode crowd override checks.
        """
        # Clamp inputs
        p_a = max(0.0, min(1.0, float(prob_break)))
        p_b = max(0.0, min(1.0, float(prob_storm)))
        p_live = max(0.0, min(1.0, float(live_radar_intensity)))

        # Explicit Weighted Score
        base_score = (self.w_a * p_a) + (self.w_b * p_b) + (self.w_live * p_live)
        base_score = round(base_score, 3)

        # Baseline Risk Tier
        if base_score < 0.35:
            risk_tier = "GREEN"
            tier_label_en = "Normal / Safe Conditions"
            tier_label_hi = "सामान्य / सुरक्षित स्थिति"
        elif base_score < 0.60:
            risk_tier = "YELLOW"
            tier_label_en = "Watch / Caution (Dry Spell or Pre-Storm Inflow)"
            tier_label_hi = "सतर्कता / निगरानी (शुष्क दौर या पूर्व-तूफान स्थिति)"
        elif base_score < 0.80:
            risk_tier = "ORANGE"
            tier_label_en = "High Alert (Imminent Break / Strong Convective Threat)"
            tier_label_hi = "उच्च चेतावनी (मानसून ब्रेक या भारी आंधी की संभावना)"
        else:
            risk_tier = "RED"
            tier_label_en = "Severe Warning / Critical Agronomic Action Required"
            tier_label_hi = "गंभीर आपातकालीन चेतावनी (तुरंत बचाव उपाय करें)"

        # Check Failure-Mode Fallback Override
        is_override = False
        override_reason = None

        is_critical_crowd = (crowd_reports_count >= 3) and (crowd_report_type in ["heavy_rain", "severe_storm", "hail"])
        is_gauge_spurt = live_rain_rate_mmh >= 15.0

        if (is_critical_crowd or is_gauge_spurt) and risk_tier in ["GREEN", "YELLOW"]:
            is_override = True
            risk_tier = "RED"
            base_score = 0.95
            tier_label_en = "EMERGENCY OVERRIDE (Ground Contradiction Detected)"
            tier_label_hi = "आपातकालीन ओवरराइड (धरातल से भारी वर्षा/तूफान की पुष्टि)"
            override_reason = (
                f"Crowd reports ({crowd_reports_count} verified '{crowd_report_type}') or "
                f"gauge rain ({live_rain_rate_mmh} mm/hr) strongly contradicted safe model forecast."
            )
            logging.warning(f"SAFETY OVERRIDE TRIGGERED: {override_reason}")

        return {
            "fusion_risk_score": base_score,
            "risk_tier": risk_tier,
            "tier_label_en": tier_label_en,
            "tier_label_hi": tier_label_hi,
            "is_override_triggered": is_override,
            "override_reason": override_reason,
            "weights_used": {
                "w_model_a_seasonal": self.w_a,
                "w_model_b_nowcast": self.w_b,
                "w_live_radar": self.w_live
            },
            "timestamp": time.time()
        }


fusion_engine = HyperlocalFusionEngine()
