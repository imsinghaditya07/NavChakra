"""
Multi-Source Data Ingestion Pipeline for AryaSaarthi Prediction Backbone.

Ingests:
1. IMD Gridded Rainfall/Temperature (0.25° ~25km synoptic down to station interpolation)
2. INSAT-3D/3DR Satellite TIR (Rapid scan 15-min cloud top brightness temp & cooling rates)
3. ERA5 / GFS Reanalysis & NWP Forecast (MSLP, geopotential height, SST, CAPE, vertical wind shear)
4. Ground AWS/ARG station observations
5. Historical Panchayat-level crop-loss & disaster incident records

Resilience:
- Implements spatial Barnes / Inverse Distance Weighting (IDW) interpolation fallback
- Flags degraded confidence when feeds are delayed or missing
- Never fabricates points: explicitly marks data lineage and fallback mechanism used.
"""

import os
import math
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
import numpy as np

from backend.app.prediction_backbone.ingestion.unified_store import unified_store, FeedStatus

logger = logging.getLogger("prediction_backbone.ingestion")


class IngestionPipeline:
    """
    Coordinates multi-resolution data ingestion into the unified spatiotemporal store.
    """

    def __init__(self):
        self.store = unified_store

    def ingest_synoptic_and_local(
        self,
        lat: float,
        lon: float,
        block_id: Optional[str] = None,
        panchayat_id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Executes unified ingestion for a specified coordinate and administrative region.
        Returns atmospheric state, feed health status, confidence penalty, and data lineage.
        """
        now = timestamp or datetime.now(timezone.utc)
        
        # 1. Query unified data cube for synoptic + meso variables
        atmospheric_cube = self.store.query_spatiotemporal_cube(lat=lat, lon=lon, timestamp=now)

        # 2. Check feed health & compute confidence degradation
        feed_health, confidence_penalty, fallbacks = self.store.get_feed_health_report()

        # 3. Query historical hazard records for ground truth context
        bid = block_id or "GENERIC_BLOCK"
        pid = panchayat_id or "GENERIC_PANCHAYAT"
        hazard_profile = self.store.get_panchayat_hazard_profile(bid, pid)

        # 4. Construct comprehensive ingestion packet
        base_confidence = 0.96 - confidence_penalty
        base_confidence = float(np.clip(base_confidence, 0.40, 0.99))

        feeds_used = [
            f"IMD Gridded 0.25° Rain/Temp ({feed_health['imd_gridded']['status']})",
            f"INSAT-3D/3DR TIR Multispectral ({feed_health['insat_satellite']['status']})",
            f"ERA5/GFS Synoptic Pressure & Shear ({feed_health['era5_gfs']['status']})",
            f"AWS/ARG Ground Network ({feed_health['aws_station_network']['status']})",
            f"Panchayat Historical Incident Records ({feed_health['panchayat_disaster_history']['status']})"
        ]

        return {
            "timestamp": now.isoformat(),
            "lat": lat,
            "lon": lon,
            "block_id": bid,
            "panchayat_id": pid,
            "atmospheric": atmospheric_cube,
            "historical_hazards": hazard_profile,
            "feeds_used": feeds_used,
            "fallbacks_applied": fallbacks,
            "confidence_penalty": confidence_penalty,
            "ingestion_confidence": round(base_confidence, 3)
        }

    def simulate_missing_feed(self, feed_name: str, fallback_type: str = FeedStatus.FALLBACK_REANALYSIS):
        """Allows testing graceful degradation under simulated network partition or radar outage."""
        self.store.set_feed_status(feed_name, fallback_type, latency_minutes=180, reliability=0.75)

    def restore_all_feeds(self):
        """Restores all feeds to optimal online status."""
        for f in ["imd_gridded", "insat_satellite", "era5_gfs", "aws_station_network", "panchayat_disaster_history"]:
            self.store.set_feed_status(f, FeedStatus.ONLINE, latency_minutes=10, reliability=0.98)


# Singleton instance
ingestion_pipeline = IngestionPipeline()
