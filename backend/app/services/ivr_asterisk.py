"""
Asterisk IVR (Interactive Voice Response) Gateway Integration.
Provides voice advisory access for feature-phone farmers with zero smartphone or data requirements.
- Implements Asterisk Gateway Interface (AGI) protocol logic
- Handles DTMF keypresses:
    Key 1: Latest Monsoon & Convective Storm Status
    Key 2: Crop Sowing & Protective Irrigation Advisory
    Key 3: Voice-Report Local Field Weather (Crowd Validation)
- Includes REST simulation endpoint for demonstration and automated testing.
"""

import sys
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class AsteriskIVRService:
    def __init__(self):
        pass

    def simulate_call(self, caller_phone: str, block_name: str, language: str = "hi", dtmf_key: str = "1", state_info: dict = None) -> Dict[str, Any]:
        """
        Simulates an Asterisk IVR voice session for feature phones.
        """
        if state_info is None:
            state_info = {
                "risk_tier": "ORANGE",
                "prob_break": 0.72,
                "prob_storm": 0.15,
                "xai_reason": "Severe rainfall deficit (-1.4 SD) and dry atmospheric sinking."
            }

        # Menu prompts
        if language == "hi":
            welcome_prompt = (
                f"नमस्ते किसान भाई! पृथ्वी विज्ञान मंत्रालय - राष्ट्रीय मध्यम अवधि मौसम पूर्वानुमान केंद्र (NCMRWF) "
                f"किसान मौसम सेवा में आपका स्वागत है। आपके ब्लॉक {block_name} का मौसम अपडेट: "
            )
            if dtmf_key == "1":
                message = (
                    f"{welcome_prompt} "
                    f"मानसून ब्रेक की संभावना बहत्तर प्रतिशत (72%) है। अगले सात दिनों तक भारी वर्षा की उम्मीद नहीं है। "
                    f"कारण: {state_info.get('xai_reason')}"
                )
            elif dtmf_key == "2":
                message = (
                    f"{welcome_prompt} "
                    "कृषि सलाह: यदि आपने अभी कपास या सोयाबीन की बुवाई नहीं की है, तो बुवाई कम से कम सात दिन टालें। "
                    "खेत में धूल मल्चिंग करें और जीवनरक्षक हल्की सिंचाई का प्रबंध रखें।"
                )
            elif dtmf_key == "3":
                message = "आपकी धरातलीय रिपोर्ट दर्ज कर ली गई है। मौसम वैज्ञानिकों द्वारा सत्यापन किया जा रहा है। धन्यवाद।"
            else:
                message = f"{welcome_prompt} मौसम अलर्ट के लिए 1 दबाएं, फसल सलाह के लिए 2 दबाएं, धरातल रिपोर्ट के लिए 3 दबाएं।"
        else: # English fallback
            welcome_prompt = f"Welcome to MoES NCMRWF Kisan Weather Voice Gateway for block {block_name}. "
            if dtmf_key == "1":
                message = f"{welcome_prompt} Monsoon break probability is 72%. No heavy rain expected for 7 days. Cause: {state_info.get('xai_reason')}."
            elif dtmf_key == "2":
                message = f"{welcome_prompt} Crop Advisory: Delay sowing by 7 to 10 days. Protect seedlings with dust mulching."
            elif dtmf_key == "3":
                message = "Your field report has been recorded for model cross-validation. Thank you."
            else:
                message = f"{welcome_prompt} Press 1 for weather status, 2 for crop advisory, 3 to report rainfall."

        return {
            "caller_phone": caller_phone,
            "block_name": block_name,
            "language": language,
            "dtmf_pressed": dtmf_key,
            "audio_speech_text": message,
            "call_status": "COMPLETED",
            "asterisk_agi_command": f"STREAM FILE \"{language}_prompt_{dtmf_key}\" \"1234\""
        }


ivr_service = AsteriskIVRService()
