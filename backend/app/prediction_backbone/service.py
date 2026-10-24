"""
Master Prediction Backbone Service.

Coordinates:
1. Multi-source ingestion & unified spatiotemporal store
2. Upstream Weather Event Model (Synoptic track + Local gridded track)
3. Branching Per-Parameter Models (Wind, Rain, Hail, Lightning, Heat, Drought, Flood)
4. Spatial downscaling to Block → Gram Panchayat boundaries with confidence propagation
5. Deterministic Warnings, Multi-Hazard Risk Scoring & Agronomic Advisory generation
6. TTL Caching matching forecast validity
7. Graceful degradation on missing/delayed feeds.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
import numpy as np

from backend.app.prediction_backbone.schema import (
    PredictionBackboneOutput,
    RegionSchema,
    EventSchema,
    FieldsSchema,
    ParticlesSchema,
    DataLineage
)
from backend.app.prediction_backbone.ingestion.ingestion_pipeline import ingestion_pipeline
from backend.app.prediction_backbone.models.weather_event_model import weather_event_model
from backend.app.prediction_backbone.models.parameter_models import parameter_models
from backend.app.prediction_backbone.downscaling.spatial_downscaler import spatial_downscaler
from backend.app.prediction_backbone.rules.warning_risk_advisory import warning_risk_advisory

logger = logging.getLogger("prediction_backbone.service")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BLOCKS_GEOJSON = os.path.join(BASE_DIR, "data", "admin_boundaries", "blocks_sample.geojson")
ADMIN_HIERARCHY = os.path.join(BASE_DIR, "frontend", "data", "india_admin_hierarchy.json")


class PredictionBackboneService:
    """
    Central API coordinator for the prediction backbone pipeline.
    """

    def __init__(self, cache_ttl_seconds: int = 900):
        self.version = "aryasaarthi-backbone-v2.1.0"
        self.cache_ttl = cache_ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._blocks_db: Dict[str, Dict[str, Any]] = {}
        self._load_admin_metadata()

    def _load_admin_metadata(self):
        """Loads sample blocks and admin hierarchy for instant block/panchayat resolution."""
        # 1. Load from blocks_sample.geojson
        if os.path.exists(BLOCKS_GEOJSON):
            try:
                with open(BLOCKS_GEOJSON, "r") as f:
                    data = json.load(f)
                for feat in data.get("features", []):
                    props = feat.get("properties", {})
                    bid = props.get("block_id")
                    if bid:
                        self._blocks_db[bid] = {
                            "block_id": bid,
                            "block_name": props.get("block_name"),
                            "district": props.get("district"),
                            "state": props.get("state"),
                            "lat": props.get("lat"),
                            "lon": props.get("lon"),
                            "elevation_m": props.get("elevation_m", 250.0),
                            "major_crops": props.get("major_crops", ["paddy"])
                        }
            except Exception as e:
                logger.warning(f"Error loading blocks geojson: {e}")

        # 2. Add Bolpur (West Bengal focus location from screenshots)
        self._blocks_db["WB_BIR_BOLPUR"] = {
            "block_id": "WB_BIR_BOLPUR",
            "block_name": "Bolpur (বোলপুর)",
            "district": "Birbhum",
            "state": "West Bengal",
            "lat": 23.6693,
            "lon": 87.7196,
            "elevation_m": 58.0,
            "major_crops": ["rice", "jute", "potato", "mustard"]
        }

        # 3. Load full admin hierarchy (including Durgapur, Asansol, Purba/Paschim Bardhaman, etc.)
        if os.path.exists(ADMIN_HIERARCHY):
            try:
                with open(ADMIN_HIERARCHY, "r", encoding="utf-8") as f:
                    hierarchy = json.load(f)
                for state_name, dists in hierarchy.items():
                    for dist_name, dist_info in dists.items():
                        for blk_name, blk_info in dist_info.get("blocks", {}).items():
                            blk_id = f"{state_name[:2].upper()}_{dist_name[:3].upper()}_{blk_name.replace(' ', '_').upper()}"
                            self._blocks_db[blk_id] = {
                                "block_id": blk_id,
                                "block_name": blk_name,
                                "district": dist_name,
                                "state": state_name,
                                "lat": float(blk_info.get("lat", dist_info.get("lat", 20.0))),
                                "lon": float(blk_info.get("lon", dist_info.get("lon", 78.0))),
                                "elevation_m": 120.0,
                                "major_crops": ["rice", "wheat", "pulses", "mustard"]
                            }
            except Exception as e:
                logger.warning(f"Error loading admin hierarchy in backbone service: {e}")

    def predict(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        block_id: Optional[str] = None,
        panchayat_id: Optional[str] = None,
        crop: str = "rice",
        stage: str = "vegetative",
        bypass_cache: bool = False
    ) -> PredictionBackboneOutput:
        """
        Executes end-to-end prediction backbone pipeline for given location/block/panchayat.
        """
        now = datetime.now(timezone.utc)
        valid_for = now + timedelta(hours=3)

        # 1. Resolve geographic & administrative coordinates
        resolved_meta = self._resolve_location(lat, lon, block_id, panchayat_id)
        resolved_lat = resolved_meta["lat"]
        resolved_lon = resolved_meta["lon"]
        bid = resolved_meta["block_id"]
        pid = resolved_meta["panchayat_id"]

        # Cache key based on region and forecast validity window (15-min bucket)
        valid_bucket = now.strftime("%Y%m%d%H") + f"_{(now.minute // 15)}"
        cache_key = f"{bid}_{pid}_{resolved_lat:.2f}_{resolved_lon:.2f}_{crop}_{stage}_{valid_bucket}"

        if not bypass_cache and cache_key in self._cache:
            cached_entry = self._cache[cache_key]
            if time.time() - cached_entry["cached_at"] < self.cache_ttl:
                return cached_entry["output"]

        # 2. Ingest multi-resolution data from unified spatiotemporal store
        ingest_packet = ingestion_pipeline.ingest_synoptic_and_local(
            lat=resolved_lat,
            lon=resolved_lon,
            block_id=bid,
            panchayat_id=pid,
            timestamp=now
        )
        atmospheric = ingest_packet["atmospheric"]
        historical_hazards = ingest_packet["historical_hazards"]
        ingestion_conf = ingest_packet["ingestion_confidence"]

        # 3. Weather Event Model (The Core Forecaster)
        # Track 1: Global / Synoptic Track (Cyclone & storm tracking)
        synoptic_event = weather_event_model.predict_synoptic_event(
            lat=resolved_lat,
            lon=resolved_lon,
            atmospheric_data=atmospheric,
            forecast_time=now
        )

        # Track 2: Local / Gridded Track (Continuous fields)
        grid_fields = weather_event_model.predict_gridded_fields(
            lat=resolved_lat,
            lon=resolved_lon,
            atmospheric_data=atmospheric,
            historical_hazards=historical_hazards,
            elevation_m=resolved_meta.get("elevation_m", 250.0),
            forecast_time=now
        )

        # 4. Per-Parameter Models (Wind, Rain, Hail, Lightning, Heat)
        wind_particles = parameter_models.compute_wind_vector_field(
            lat=resolved_lat,
            lon=resolved_lon,
            atmospheric_data=atmospheric,
            event=synoptic_event
        )
        rain_particles = parameter_models.compute_rain_particles(grid_fields)
        hail_prob = parameter_models.compute_hail_probability(atmospheric, grid_fields)
        lightning_prob = parameter_models.compute_lightning_probability(atmospheric, grid_fields)

        particles = ParticlesSchema(
            wind=wind_particles,
            rain=rain_particles,
            hail_prob=hail_prob,
            lightning_prob=lightning_prob
        )

        # 5. Spatial Downscaling: Grid → Block → Gram Panchayat
        panchayat_meta = {
            "elevation_m": resolved_meta.get("elevation_m", 250.0),
            "terrain_roughness_m": 35.0,
            "land_use": "agricultural",
            "slope_aspect_deg": 220.0
        }
        downscaled_fields, downscaled_wind, final_confidence, downscale_audit = spatial_downscaler.downscale_to_panchayat(
            grid_fields=grid_fields,
            grid_wind=wind_particles,
            parent_confidence=ingestion_conf,
            panchayat_meta=panchayat_meta,
            grid_elevation_m=200.0
        )
        particles.wind = downscaled_wind

        # 6. Warning, Risk & Advisory Layer
        warnings = warning_risk_advisory.evaluate_warnings(
            event=synoptic_event,
            fields=downscaled_fields,
            particles=particles
        )

        risk_assessment = warning_risk_advisory.compute_risk_assessment(
            event=synoptic_event,
            fields=downscaled_fields,
            particles=particles,
            historical_hazards=historical_hazards,
            crop_stage=stage
        )

        advisory = warning_risk_advisory.generate_advisory(
            crop=crop,
            stage=stage,
            risk=risk_assessment,
            fields=downscaled_fields,
            particles=particles,
            event=synoptic_event
        )

        # 7. Construct and validate official PredictionBackboneOutput schema
        region = RegionSchema(
            block_id=bid,
            panchayat_id=pid,
            lat=round(resolved_lat, 4),
            lon=round(resolved_lon, 4),
            block_name=resolved_meta.get("block_name"),
            panchayat_name=resolved_meta.get("panchayat_name"),
            district=resolved_meta.get("district"),
            state=resolved_meta.get("state"),
            elevation_m=resolved_meta.get("elevation_m")
        )

        lineage = DataLineage(
            feeds_ingested=ingest_packet["feeds_used"],
            fallbacks_applied=ingest_packet["fallbacks_applied"],
            confidence_degraded_by=ingest_packet["confidence_penalty"]
        )

        output = PredictionBackboneOutput(
            timestamp=now.isoformat(),
            valid_for=valid_for.isoformat(),
            region=region,
            event=synoptic_event,
            fields=downscaled_fields,
            particles=particles,
            model_version=self.version,
            confidence=final_confidence,
            warnings=warnings,
            risk_assessment=risk_assessment,
            advisory=advisory,
            data_lineage=lineage
        )

        # Store in TTL Cache
        self._cache[cache_key] = {
            "cached_at": time.time(),
            "output": output
        }

        return output

    def _resolve_location(
        self,
        lat: Optional[float],
        lon: Optional[float],
        block_id: Optional[str],
        panchayat_id: Optional[str]
    ) -> Dict[str, Any]:
        """Maps incoming search identifiers or coordinates to complete metadata."""
        # Case A: block_id is provided
        if block_id:
            # Check direct match
            if block_id in self._blocks_db:
                b = self._blocks_db[block_id]
                pid = panchayat_id or b.get("panchayat_id") or f"PANCH_{block_id}_01"
                return {
                    "lat": float(b.get("lat", 23.6693)),
                    "lon": float(b.get("lon", 87.7196)),
                    "block_id": b.get("block_id", block_id),
                    "panchayat_id": pid,
                    "block_name": b.get("block_name", block_id),
                    "panchayat_name": b.get("panchayat_name") or f"{b.get('block_name', block_id)} Gram Panchayat",
                    "district": b.get("district", "Birbhum"),
                    "state": b.get("state", "West Bengal"),
                    "elevation_m": float(b.get("elevation_m", 120.0))
                }
            # Search case-insensitive or partial (including district and state)
            b_lower = block_id.lower()
            for bid, b in self._blocks_db.items():
                if (b_lower in bid.lower() or 
                    (b.get("block_name") and b_lower in b["block_name"].lower()) or
                    (b.get("district") and b_lower in b["district"].lower()) or
                    (b.get("state") and b_lower in b["state"].lower())):
                    pid = panchayat_id or b.get("panchayat_id") or f"PANCH_{bid}_01"
                    return {
                        "lat": float(b.get("lat", 23.6693)),
                        "lon": float(b.get("lon", 87.7196)),
                        "block_id": b.get("block_id", bid),
                        "panchayat_id": pid,
                        "block_name": b.get("block_name", bid),
                        "panchayat_name": b.get("panchayat_name") or f"{b.get('block_name', bid)} Gram Panchayat",
                        "district": b.get("district", "Birbhum"),
                        "state": b.get("state", "West Bengal"),
                        "elevation_m": float(b.get("elevation_m", 120.0))
                    }

        # Case B: lat & lon provided
        if lat is not None and lon is not None:
            # Find nearest known block or generate representative ID
            closest_block = None
            min_dist = float("inf")
            for bid, b in self._blocks_db.items():
                b_lat = b.get("lat")
                b_lon = b.get("lon")
                if b_lat is not None and b_lon is not None:
                    dist = (lat - b_lat) ** 2 + (lon - b_lon) ** 2
                    if dist < min_dist:
                        min_dist = dist
                        closest_block = b

            if closest_block and min_dist < 0.25:  # within ~50km
                pid = panchayat_id or closest_block.get("panchayat_id") or f"PANCH_{closest_block['block_id']}_01"
                return {
                    "lat": lat,
                    "lon": lon,
                    "block_id": closest_block["block_id"],
                    "panchayat_id": pid,
                    "block_name": closest_block.get("block_name", closest_block["block_id"]),
                    "panchayat_name": closest_block.get("panchayat_name") or f"Panchayat near {closest_block.get('block_name', closest_block['block_id'])}",
                    "district": closest_block.get("district", "Local District"),
                    "state": closest_block.get("state", "India"),
                    "elevation_m": float(closest_block.get("elevation_m", 250.0))
                }

            # Custom location coordinate
            bid = block_id or f"LOC_{int(lat*100)}_{int(lon*100)}"
            pid = panchayat_id or f"PANCH_{int(lat*100)}_{int(lon*100)}"
            return {
                "lat": lat,
                "lon": lon,
                "block_id": bid,
                "panchayat_id": pid,
                "block_name": f"Area ({lat:.2f}N, {lon:.2f}E)",
                "panchayat_name": f"Panchayat ({lat:.2f}N, {lon:.2f}E)",
                "district": "Local District",
                "state": "India",
                "elevation_m": 220.0
            }

        # Default fallback to Bolpur (West Bengal focus from screenshots)
        base = dict(self._blocks_db.get("WB_BIR_BOLPUR", {}))
        return {
            "lat": float(base.get("lat", 23.6693)),
            "lon": float(base.get("lon", 87.7196)),
            "block_id": base.get("block_id", "WB_BIR_BOLPUR"),
            "panchayat_id": panchayat_id or base.get("panchayat_id", "PANCH_BOLPUR_01"),
            "block_name": base.get("block_name", "Bolpur (বোলপুর)"),
            "panchayat_name": base.get("panchayat_name", "Bolpur Gram Panchayat"),
            "district": base.get("district", "Birbhum"),
            "state": base.get("state", "West Bengal"),
            "elevation_m": float(base.get("elevation_m", 58.0))
        }

    def get_particle_grid(
        self,
        lat_min: float = 6.0,
        lat_max: float = 36.0,
        lon_min: float = 68.0,
        lon_max: float = 98.0,
        step_deg: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Generates a 2D particle vector grid across India and surrounding seas
        for MapLibre/Leaflet WebGL/Canvas streamline rendering.
        """
        grid = []
        for lat in np.arange(lat_min, lat_max + 0.1, step_deg):
            for lon in np.arange(lon_min, lon_max + 0.1, step_deg):
                atm = ingestion_pipeline.store.query_spatiotemporal_cube(lat, lon)
                event = weather_event_model.predict_synoptic_event(lat, lon, atm)
                wind = parameter_models.compute_wind_vector_field(lat, lon, atm, event)
                grid.append({
                    "lat": round(float(lat), 2),
                    "lon": round(float(lon), 2),
                    "u": wind.u_ms,
                    "v": wind.v_ms,
                    "speed_kmh": wind.speed_kmh,
                    "direction_deg": wind.direction_deg
                })
        return grid


# Singleton instance
prediction_backbone_service = PredictionBackboneService()
