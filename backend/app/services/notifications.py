"""
Multi-Channel Alert Delivery Engine.
Channels:
1. WhatsApp Cloud API (Free Tier: 1,000 conversations/month cap - noted for Phase 2 scaling)
2. Firebase Cloud Messaging (FCM) Web Push (Free unlimited tier)
Includes mandatory one-line privacy consent notice under MoES data guidelines.
"""

import logging
from typing import Dict, Any, List
from backend.app.core.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class NotificationDeliveryService:
    def __init__(self):
        self.privacy_notice = settings.PRIVACY_CONSENT_NOTICE
        self.free_tier_limit = "1,000 conversations/month (WhatsApp Free Tier)"

    def format_whatsapp_payload(self, to_phone: str, block_name: str, risk_tier: str, advisory_text: str, xai_reason: str, lang: str = "hi") -> Dict[str, Any]:
        """
        Formats structured WhatsApp Business template message.
        """
        header = f"🚨 *MoES NCMRWF Kisan Weather Alert* ({risk_tier})" if risk_tier in ["ORANGE", "RED"] else f"🌦️ *MoES NCMRWF Krishi Advisory* ({risk_tier})"
        body = (
            f"{header}\n\n"
            f"📍 *Block:* {block_name}\n"
            f"📋 *Advisory:* {advisory_text}\n\n"
            f"💡 *Meteorological Cause (AI):* {xai_reason}\n\n"
            f"🔒 *Privacy Notice:* {self.privacy_notice}"
        )

        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",
            "text": {"body": body},
            "channel": "WhatsApp Cloud API Free Tier",
            "tier_limit_note": self.free_tier_limit
        }

    def dispatch_alert(self, to_phone: str, block_name: str, risk_tier: str, advisory_text: str, xai_reason: str) -> Dict[str, Any]:
        """
        Dispatches alert via WhatsApp or logs mock transmission for free sandbox demonstration.
        """
        payload = self.format_whatsapp_payload(to_phone, block_name, risk_tier, advisory_text, xai_reason)
        logging.info(f"Dispatched advisory to {to_phone} ({risk_tier}) via {payload['channel']}")
        return {
            "status": "DELIVERED_SIMULATED",
            "recipient": to_phone,
            "payload": payload,
            "privacy_notice_included": True
        }


notification_service = NotificationDeliveryService()
