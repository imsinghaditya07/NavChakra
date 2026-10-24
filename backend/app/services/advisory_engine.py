"""
Expert-System Agronomic Advisory Engine.
Deterministic Rule Layer on top of ML Predictions (Kept strictly separate for auditability).
Aligns with ICAR (Indian Council of Agricultural Research) & IMD Agromet guidelines.
"""

import json
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class AgronomicAdvisoryEngine:
    def __init__(self):
        pass

    def generate_advisory(
        self,
        crop: str,
        stage: str,
        prob_break: float,
        prob_storm: float,
        soil_moisture_proxy: float = 0.35,
        recent_rain_7d: float = 20.0
    ) -> Dict[str, Any]:
        """
        Deterministic rule evaluation.
        Returns: rule_id, risk_level, advisory text in EN, HI, MR, and action checklist.
        """
        crop = crop.lower()
        stage = stage.lower()

        # Rule evaluation logic
        # 1. Critical Break during Sowing / Seedling
        if ("sow" in stage or "nursery" in stage) and prob_break >= 0.65:
            rule_id = "RULE_SOW_BREAK_CRITICAL"
            urgency = "HIGH"
            adv_en = (
                f"Severe monsoon break expected ({prob_break*100:.0f}% probability). "
                "Delay sowing/transplanting by 7–10 days until monsoon revival cycle. "
                "Do not sow on dry seedbeds; prepare short-duration alternative contingency seeds (e.g. Bajra/Moong)."
            )
            adv_hi = (
                f"मानसून में लंबा ब्रेक आने की संभावना ({prob_break*100:.0f}%) है। "
                "बुवाई/रोपाई 7-10 दिनों के लिए टालें जब तक पुनर्जीवन न हो। "
                "सूखी मिट्टी में बीज न डालें; वैकल्पिक कम अवधि की फसलों (बाजरा/मूंग) की तैयारी रखें।"
            )
            adv_mr = (
                f"पावसात मोठा खंड पडण्याची शक्यता ({prob_break*100:.0f}%) आहे. "
                "पेरणी किंवा पुनर्लागवड 7-10 दिवस पुढे ढकला. "
                "ओलावा नसताना पेरणी करू नका; पर्यायी कमी कालावधीच्या बियाण्यांची व्यवस्था करा."
            )
            action_items = [
                "Postpone sowing operations for 7-10 days",
                "Ensure seeds are treated with Trichoderma or bio-fungicide",
                "Ready contingency seeds for drought-tolerant pulse varieties"
            ]

        # 2. Convective Storm Nowcast Alert (Thunderstorm / Lightning / High Squalls)
        elif prob_storm >= 0.70:
            rule_id = "RULE_STORM_NOWCAST_SEVERE"
            urgency = "IMMEDIATE"
            adv_en = (
                f"Severe thunderstorm, squalls and lightning hazard active within 30 minutes ({prob_storm*100:.0f}% risk). "
                "Immediately suspend field spraying, harvesting, and tractor operations. "
                "Seek sturdy indoor shelter; do not stand under isolated trees, metal electric poles, or tin sheds."
            )
            adv_hi = (
                f"अगले 30 मिनट में तीव्र आंधी, बिजली गिरने और तूफान का गंभीर खतरा ({prob_storm*100:.0f}%) है। "
                "खेत में कीटनाशक छिड़काव, कटाई और जुताई तुरंत रोकें। "
                "पक्के मकान में शरण लें; अकेले पेड़ों, बिजली के खंभों या खुले टिन शेड के नीचे कतई न रुकें।"
            )
            adv_mr = (
                f"पुढील 30 मिनिटांत वादळी पाऊस आणि वीज पडण्याचा मोठा धोका ({prob_storm*100:.0f}%) आहे. "
                "शेतात फवारणी, कापणी किंवा नांगरणीचे काम तात्काळ थांबवा. "
                "सुरक्षित पक्क्या इमारतीत आसरा घ्या; झाडांखाली किंवा विजेच्या खांबाजवळ थांबू नका."
            )
            action_items = [
                "Halt all outdoor farm activity immediately",
                "Tie down lightweight greenhouse nets and machinery covers",
                "Keep livestock away from electrical fences and open gullies"
            ]

        # 3. Break during Flowering / Reproductive Stage (Maximum Yield Penalty)
        elif ("flower" in stage or "boll" in stage or "silking" in stage) and prob_break >= 0.60:
            rule_id = "RULE_REPRODUCTIVE_MOISTURE_STRESS"
            urgency = "HIGH"
            adv_en = (
                f"Monsoon break spell ({prob_break*100:.0f}% prob) during critical reproductive stage. "
                "Immediately arrange life-saving micro-irrigation or sprinkler from farm pond. "
                "Apply 2% Potassium Nitrate (KNO3) or dust/straw mulch to reduce transpirational water loss."
            )
            adv_hi = (
                f"फसल की फूल/बालियां बनने की नाजुक अवस्था में बारिश में रुकावट ({prob_break*100:.0f}%) का अनुमान है। "
                "खेत के तालाब (फार्म पॉन्ड) या बोरवेल से तुरंत जीवनरक्षक हल्की सिंचाई (ड्रिप/स्प्रिंकलर) दें। "
                "नमी संरक्षण हेतु पुआल/मल्चिंग करें और 2% पोटेशियम नाइट्रेट का छिड़काव करें।"
            )
            adv_mr = (
                f"पीक फुलोरा/बोंड धरण्याच्या नाजूक टप्प्यावर पावसाचा खंड ({prob_break*100:.0f}%) जाणवणार आहे. "
                "शेततळ्यातून तुषार किंवा ठिबकद्वारे तातडीने संरक्षित पाणी द्या. "
                "बाष्पीभवन रोखण्यासाठी पालापाचोळ्याचे आच्छादन करा आणि 2% पोटॅशियम नायट्रेट फवारा."
            )
            action_items = [
                "Provide critical life-saving irrigation via drip/sprinkler",
                "Apply crop residue mulch between rows",
                "Avoid nitrogenous top-dressing fertilizers until break breaks"
            ]

        # 4. Active Monsoon / Heavy Rain during Tillering / Vegetative
        elif prob_break < 0.30 and prob_storm < 0.50 and (recent_rain_7d > 80.0 or soil_moisture_proxy > 0.70):
            rule_id = "RULE_EXCESS_MOISTURE_DRAINAGE"
            urgency = "MEDIUM"
            adv_en = (
                "Continuous active monsoon rainfall. Soil is near saturation. "
                "Clear field boundary drainage furrows to prevent root-zone waterlogging. "
                "Postpone urea top-dressing until heavy percolation subsides to prevent leaching."
            )
            adv_hi = (
                "लगातार सक्रिय मानसूनी बारिश के कारण खेत में अत्यधिक नमी है। "
                "खेत की मेड़ों और जल निकासी नालियों को खोलें ताकि जलभराव न हो। "
                "यूरिया का छिड़काव अभी रोकें ताकि पोषक तत्व बह न जाएं।"
            )
            adv_mr = (
                "सतत सुरू असलेल्या पावसामुळे शेतात पाणी साचण्याची शक्यता आहे. "
                "पाण्याचा निचरा होण्यासाठी शेतातील चर व गटारे मोकळी करा. "
                "युरिया खताची मात्रा पाऊस मंदावल्यावरच द्या."
            )
            action_items = [
                "Open trench outlets for excess surface runoff drainage",
                "Scout for fungal leaf spots after persistent wet spells",
                "Withhold heavy chemical applications"
            ]

        # 5. Normal Favorable Monsoon Window
        else:
            rule_id = "RULE_FAVORABLE_GROWTH_WINDOW"
            urgency = "LOW"
            adv_en = (
                "Favorable soil moisture and stable monsoon circulation. "
                "Proceed with scheduled intercultural operations, weeding, and balanced fertilizer application."
            )
            adv_hi = (
                "अनुकूल मानसूनी परिस्थितियां और पर्याप्त मृदा नमी। "
                "निर्धारित निराई-गुड़ाई, खरपतवार नियंत्रण और उर्वरक प्रबंधन जारी रखें।"
            )
            adv_mr = (
                "अनुकूल हवामान आणि समाधानकारक ओलावा. "
                "तणनियंत्रण, खते देणे आणि इतर आंतरमशागतीची कामे वेळेवर पूर्ण करा."
            )
            action_items = [
                "Complete weeding while soil moisture is optimal",
                "Monitor for early pest arrivals",
                "Maintain normal crop care schedule"
            ]

        return {
            "rule_id": rule_id,
            "crop": crop,
            "stage": stage,
            "urgency": urgency,
            "advisory_en": adv_en,
            "advisory_hi": adv_hi,
            "advisory_mr": adv_mr,
            "action_items": action_items
        }


advisory_engine = AgronomicAdvisoryEngine()
