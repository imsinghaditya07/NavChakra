"""
Database layer for Hyperlocal Monsoon & Disaster Management.
Uses SQLite with structured JSON and spatial attributes.
Ready for drop-in migration to PostgreSQL / PostGIS in high-scale production.
"""

import os
import sqlite3
import json
import time
from typing import List, Dict, Any

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "hyperlocal.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Blocks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        block_id TEXT PRIMARY KEY,
        block_name TEXT NOT NULL,
        district TEXT NOT NULL,
        state TEXT NOT NULL,
        subdivision TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        elevation_m REAL,
        major_crops TEXT,
        soil_type TEXT,
        normal_onset_doy INTEGER,
        normal_monsoon_rain_mm REAL,
        latest_risk_tier TEXT DEFAULT 'GREEN',
        latest_risk_score REAL DEFAULT 0.20,
        latest_prob_break REAL DEFAULT 0.15,
        latest_prob_storm REAL DEFAULT 0.10,
        latest_xai_reason TEXT,
        last_updated REAL
    );
    """)

    # Crowd Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crowd_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_id TEXT NOT NULL,
        report_type TEXT NOT NULL,
        intensity TEXT,
        notes TEXT,
        reporter_lat REAL,
        reporter_lon REAL,
        verified INTEGER DEFAULT 1,
        created_at REAL NOT NULL
    );
    """)

    # Advisories audit log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS advisories_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_id TEXT NOT NULL,
        crop TEXT NOT NULL,
        stage TEXT NOT NULL,
        risk_tier TEXT NOT NULL,
        rule_id TEXT NOT NULL,
        advisory_en TEXT NOT NULL,
        advisory_hi TEXT NOT NULL,
        advisory_mr TEXT NOT NULL,
        created_at REAL NOT NULL
    );
    """)

    # Farmer subscribers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        phone_number TEXT PRIMARY KEY,
        block_id TEXT NOT NULL,
        preferred_crop TEXT DEFAULT 'cotton',
        preferred_language TEXT DEFAULT 'hi',
        channel TEXT DEFAULT 'whatsapp',
        consent_notice_accepted INTEGER DEFAULT 1,
        registered_at REAL NOT NULL
    );
    """)

    conn.commit()
    conn.close()


def seed_blocks_if_empty(blocks_geojson_path: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM blocks;")
    count = cursor.fetchone()[0]

    if count == 0 and os.path.exists(blocks_geojson_path):
        with open(blocks_geojson_path, "r") as f:
            data = json.load(f)
        for feat in data.get("features", []):
            props = feat["properties"]
            cursor.execute("""
            INSERT OR REPLACE INTO blocks (
                block_id, block_name, district, state, subdivision,
                lat, lon, elevation_m, major_crops, soil_type,
                normal_onset_doy, normal_monsoon_rain_mm, latest_risk_tier,
                latest_risk_score, latest_prob_break, latest_prob_storm,
                latest_xai_reason, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                props["block_id"],
                props["block_name"],
                props["district"],
                props["state"],
                props["subdivision"],
                props["lat"],
                props["lon"],
                props["elevation_m"],
                json.dumps(props["major_crops"]),
                props["soil_type"],
                props["normal_onset_doy"],
                props["normal_monsoon_rain_mm"],
                "GREEN",
                0.22,
                0.18,
                0.12,
                "Normal pre-monsoon convective patterns; no imminent break detected.",
                time.time()
            ))
        conn.commit()
    conn.close()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "admin_boundaries", "blocks_sample.geojson")

init_db()
seed_blocks_if_empty(GEOJSON_PATH)

