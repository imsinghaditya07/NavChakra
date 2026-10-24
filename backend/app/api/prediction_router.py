"""
Prediction Backbone Endpoints Router.

Exposes:
- GET /predict/block/{block_id}
- GET /predict/panchayat/{panchayat_id}
- POST /predict/pipeline (or /predict/query)
- GET /predict/events
- GET /predict/particles/grid
- GET /predict/benchmark/eval
"""

from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field

from backend.app.prediction_backbone.schema import PredictionBackboneOutput
from backend.app.prediction_backbone.service import prediction_backbone_service
from backend.app.prediction_backbone.evaluation.metrics import MeteorologicalEvaluator

router = APIRouter(tags=["Prediction Backbone"])


class PipelineQueryRequest(BaseModel):
    lat: Optional[float] = Field(None, description="Latitude in decimal degrees")
    lon: Optional[float] = Field(None, description="Longitude in decimal degrees")
    block_id: Optional[str] = Field(None, description="Block ID or name (e.g. 'WB_BIR_BOLPUR' or 'Bolpur')")
    panchayat_id: Optional[str] = Field(None, description="Panchayat ID or name")
    crop: str = Field("rice", description="Crop name (e.g. 'rice', 'cotton', 'soybean', 'wheat', 'jute')")
    stage: str = Field("vegetative", description="Crop growth stage (e.g. 'sowing', 'vegetative', 'flowering', 'harvesting')")
    bypass_cache: bool = Field(False, description="Set True to force fresh inference")


@router.get(
    "/predict/block/{block_id}",
    response_model=PredictionBackboneOutput,
    summary="Prediction Backbone for Block: Multi-hazard events, gridded fields & particle vectors"
)
def predict_block(
    block_id: str = Path(..., description="Block identifier or name"),
    crop: str = Query("rice", description="Crop name (e.g. 'rice', 'cotton', 'potato')"),
    stage: str = Query("vegetative", description="Growth stage (e.g. 'sowing', 'flowering')"),
    bypass_cache: bool = Query(False, description="Bypass cache for live run")
):
    try:
        output = prediction_backbone_service.predict(
            block_id=block_id,
            crop=crop,
            stage=stage,
            bypass_cache=bypass_cache
        )
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction backbone pipeline failed: {str(e)}")


@router.get(
    "/predict/panchayat/{panchayat_id}",
    response_model=PredictionBackboneOutput,
    summary="Prediction Backbone downscaled to Gram Panchayat boundary with confidence propagation"
)
def predict_panchayat(
    panchayat_id: str = Path(..., description="Gram Panchayat identifier"),
    block_id: Optional[str] = Query(None, description="Parent Block identifier"),
    crop: str = Query("rice", description="Crop name"),
    stage: str = Query("vegetative", description="Growth stage"),
    bypass_cache: bool = Query(False, description="Bypass cache for live run")
):
    try:
        output = prediction_backbone_service.predict(
            block_id=block_id,
            panchayat_id=panchayat_id,
            crop=crop,
            stage=stage,
            bypass_cache=bypass_cache
        )
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Panchayat downscaling pipeline failed: {str(e)}")


@router.post(
    "/predict/pipeline",
    response_model=PredictionBackboneOutput,
    summary="Flexible Prediction Backbone Query by Coordinates, Block, or Panchayat"
)
def predict_pipeline(req: PipelineQueryRequest):
    try:
        output = prediction_backbone_service.predict(
            lat=req.lat,
            lon=req.lon,
            block_id=req.block_id,
            panchayat_id=req.panchayat_id,
            crop=req.crop,
            stage=req.stage,
            bypass_cache=req.bypass_cache
        )
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction query failed: {str(e)}")


@router.get(
    "/predict/particles/grid",
    summary="2D Particle Vector Grid for MapLibre / Leaflet Streamline Animations"
)
def get_particle_grid(
    lat_min: float = Query(6.0, description="Minimum latitude"),
    lat_max: float = Query(36.0, description="Maximum latitude"),
    lon_min: float = Query(68.0, description="Minimum longitude"),
    lon_max: float = Query(98.0, description="Maximum longitude"),
    step_deg: float = Query(2.5, description="Grid step size in degrees")
):
    grid = prediction_backbone_service.get_particle_grid(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
        step_deg=step_deg
    )
    return {
        "status": "success",
        "count": len(grid),
        "model_version": prediction_backbone_service.version,
        "grid": grid
    }


@router.get(
    "/predict/benchmark/eval",
    summary="Meteorological Verification Benchmark: RMSE, MAE, Brier Score, CSI, Cyclone Track Error"
)
def get_benchmark_eval():
    report = MeteorologicalEvaluator.run_full_backbone_benchmark()
    return report
