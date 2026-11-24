#!/usr/bin/env python3
"""
Complete State/UT Monthly Climatological Database.
Built from PDF data (1991-2021 IMD normals) for all 28 States + 8 UTs of India.

Data fields per month:
- avg_temp_c: Average temperature (°C)
- min_temp_c: Minimum temperature (°C)
- max_temp_c: Maximum temperature (°C)
- rainfall_mm: Precipitation / Rainfall (mm)
- humidity_pct: Humidity (%)
- rainy_days: Number of rainy days
- sun_hours: Average sun hours

Sources: State PDF screenshots (1991-2021 IMD climatological normals),
         cross-verified with IMD published subdivision normals.
"""

import json
import os

# ============================================================================
# COMPLETE MONTHLY CLIMATOLOGY FOR ALL 36 STATES & UTs
# Data extracted from PDF screenshots + IMD 1991-2021 normals
# ============================================================================

CLIMATOLOGY_DB = {
    # ======================================================================
    # 28 STATES
    # ======================================================================
    "Andhra Pradesh": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 912,
        "months": {
            "Jan": {"avg_temp_c": 24.2, "min_temp_c": 17.5, "max_temp_c": 30.9, "rainfall_mm": 7, "humidity_pct": 64, "rainy_days": 1, "sun_hours": 9.2},
            "Feb": {"avg_temp_c": 26.4, "min_temp_c": 19.3, "max_temp_c": 33.5, "rainfall_mm": 11, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 9.8},
            "Mar": {"avg_temp_c": 29.6, "min_temp_c": 22.4, "max_temp_c": 36.8, "rainfall_mm": 13, "humidity_pct": 52, "rainy_days": 1, "sun_hours": 10.2},
            "Apr": {"avg_temp_c": 32.1, "min_temp_c": 25.3, "max_temp_c": 38.9, "rainfall_mm": 24, "humidity_pct": 51, "rainy_days": 2, "sun_hours": 10.5},
            "May": {"avg_temp_c": 33.8, "min_temp_c": 27.0, "max_temp_c": 40.6, "rainfall_mm": 42, "humidity_pct": 54, "rainy_days": 3, "sun_hours": 10.8},
            "Jun": {"avg_temp_c": 31.4, "min_temp_c": 25.8, "max_temp_c": 37.0, "rainfall_mm": 107, "humidity_pct": 67, "rainy_days": 8, "sun_hours": 8.2},
            "Jul": {"avg_temp_c": 29.5, "min_temp_c": 24.6, "max_temp_c": 34.4, "rainfall_mm": 165, "humidity_pct": 75, "rainy_days": 12, "sun_hours": 6.5},
            "Aug": {"avg_temp_c": 29.1, "min_temp_c": 24.3, "max_temp_c": 33.9, "rainfall_mm": 181, "humidity_pct": 77, "rainy_days": 13, "sun_hours": 6.3},
            "Sep": {"avg_temp_c": 28.8, "min_temp_c": 23.8, "max_temp_c": 33.8, "rainfall_mm": 185, "humidity_pct": 78, "rainy_days": 11, "sun_hours": 7.0},
            "Oct": {"avg_temp_c": 27.4, "min_temp_c": 22.0, "max_temp_c": 32.8, "rainfall_mm": 122, "humidity_pct": 73, "rainy_days": 7, "sun_hours": 7.8},
            "Nov": {"avg_temp_c": 25.1, "min_temp_c": 19.3, "max_temp_c": 30.9, "rainfall_mm": 43, "humidity_pct": 67, "rainy_days": 3, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 23.5, "min_temp_c": 17.2, "max_temp_c": 29.8, "rainfall_mm": 12, "humidity_pct": 64, "rainy_days": 1, "sun_hours": 9.0}
        }
    },
    "Arunachal Pradesh": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 2782,
        "months": {
            "Jan": {"avg_temp_c": 11.2, "min_temp_c": 4.5, "max_temp_c": 17.9, "rainfall_mm": 42, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 6.8},
            "Feb": {"avg_temp_c": 13.5, "min_temp_c": 6.8, "max_temp_c": 20.2, "rainfall_mm": 68, "humidity_pct": 68, "rainy_days": 5, "sun_hours": 7.2},
            "Mar": {"avg_temp_c": 17.2, "min_temp_c": 10.5, "max_temp_c": 23.9, "rainfall_mm": 112, "humidity_pct": 64, "rainy_days": 8, "sun_hours": 7.8},
            "Apr": {"avg_temp_c": 20.8, "min_temp_c": 14.0, "max_temp_c": 27.6, "rainfall_mm": 225, "humidity_pct": 72, "rainy_days": 14, "sun_hours": 7.5},
            "May": {"avg_temp_c": 22.4, "min_temp_c": 16.2, "max_temp_c": 28.6, "rainfall_mm": 365, "humidity_pct": 80, "rainy_days": 18, "sun_hours": 6.5},
            "Jun": {"avg_temp_c": 23.5, "min_temp_c": 18.6, "max_temp_c": 28.4, "rainfall_mm": 495, "humidity_pct": 86, "rainy_days": 22, "sun_hours": 4.8},
            "Jul": {"avg_temp_c": 24.0, "min_temp_c": 19.8, "max_temp_c": 28.2, "rainfall_mm": 530, "humidity_pct": 88, "rainy_days": 24, "sun_hours": 4.2},
            "Aug": {"avg_temp_c": 24.1, "min_temp_c": 19.9, "max_temp_c": 28.3, "rainfall_mm": 445, "humidity_pct": 87, "rainy_days": 22, "sun_hours": 4.5},
            "Sep": {"avg_temp_c": 23.0, "min_temp_c": 18.2, "max_temp_c": 27.8, "rainfall_mm": 310, "humidity_pct": 84, "rainy_days": 16, "sun_hours": 5.8},
            "Oct": {"avg_temp_c": 19.8, "min_temp_c": 14.0, "max_temp_c": 25.6, "rainfall_mm": 120, "humidity_pct": 78, "rainy_days": 8, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 15.5, "min_temp_c": 9.2, "max_temp_c": 21.8, "rainfall_mm": 38, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 12.0, "min_temp_c": 5.5, "max_temp_c": 18.5, "rainfall_mm": 32, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 7.2}
        }
    },
    "Assam": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 2818,
        "months": {
            "Jan": {"avg_temp_c": 16.0, "min_temp_c": 9.8, "max_temp_c": 22.2, "rainfall_mm": 18, "humidity_pct": 78, "rainy_days": 2, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 18.5, "min_temp_c": 12.0, "max_temp_c": 25.0, "rainfall_mm": 32, "humidity_pct": 72, "rainy_days": 4, "sun_hours": 7.5},
            "Mar": {"avg_temp_c": 22.0, "min_temp_c": 15.5, "max_temp_c": 28.5, "rainfall_mm": 78, "humidity_pct": 68, "rainy_days": 8, "sun_hours": 7.8},
            "Apr": {"avg_temp_c": 25.0, "min_temp_c": 19.0, "max_temp_c": 31.0, "rainfall_mm": 195, "humidity_pct": 76, "rainy_days": 14, "sun_hours": 7.2},
            "May": {"avg_temp_c": 26.5, "min_temp_c": 21.5, "max_temp_c": 31.5, "rainfall_mm": 310, "humidity_pct": 82, "rainy_days": 17, "sun_hours": 6.5},
            "Jun": {"avg_temp_c": 27.8, "min_temp_c": 23.5, "max_temp_c": 32.1, "rainfall_mm": 428, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 5.2},
            "Jul": {"avg_temp_c": 28.2, "min_temp_c": 24.5, "max_temp_c": 31.9, "rainfall_mm": 465, "humidity_pct": 88, "rainy_days": 23, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 28.5, "min_temp_c": 24.5, "max_temp_c": 32.5, "rainfall_mm": 385, "humidity_pct": 87, "rainy_days": 20, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 23.0, "max_temp_c": 32.0, "rainfall_mm": 270, "humidity_pct": 84, "rainy_days": 14, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 25.0, "min_temp_c": 19.5, "max_temp_c": 30.5, "rainfall_mm": 135, "humidity_pct": 80, "rainy_days": 7, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 20.5, "min_temp_c": 14.0, "max_temp_c": 27.0, "rainfall_mm": 25, "humidity_pct": 76, "rainy_days": 2, "sun_hours": 8.2},
            "Dec": {"avg_temp_c": 17.0, "min_temp_c": 10.5, "max_temp_c": 23.5, "rainfall_mm": 12, "humidity_pct": 78, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Bihar": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1130,
        "months": {
            "Jan": {"avg_temp_c": 16.2, "min_temp_c": 10.6, "max_temp_c": 22.1, "rainfall_mm": 17, "humidity_pct": 69, "rainy_days": 2, "sun_hours": 8.6},
            "Feb": {"avg_temp_c": 19.9, "min_temp_c": 13.6, "max_temp_c": 26.2, "rainfall_mm": 17, "humidity_pct": 60, "rainy_days": 2, "sun_hours": 9.7},
            "Mar": {"avg_temp_c": 25.6, "min_temp_c": 18.4, "max_temp_c": 32.5, "rainfall_mm": 10, "humidity_pct": 43, "rainy_days": 2, "sun_hours": 10.7},
            "Apr": {"avg_temp_c": 30.6, "min_temp_c": 23.4, "max_temp_c": 37.6, "rainfall_mm": 12, "humidity_pct": 36, "rainy_days": 2, "sun_hours": 11.2},
            "May": {"avg_temp_c": 31.9, "min_temp_c": 25.9, "max_temp_c": 37.7, "rainfall_mm": 32, "humidity_pct": 50, "rainy_days": 4, "sun_hours": 11.0},
            "Jun": {"avg_temp_c": 31.2, "min_temp_c": 27.0, "max_temp_c": 35.7, "rainfall_mm": 175, "humidity_pct": 65, "rainy_days": 12, "sun_hours": 10.0},
            "Jul": {"avg_temp_c": 28.8, "min_temp_c": 26.3, "max_temp_c": 32.0, "rainfall_mm": 323, "humidity_pct": 81, "rainy_days": 19, "sun_hours": 8.2},
            "Aug": {"avg_temp_c": 28.6, "min_temp_c": 26.1, "max_temp_c": 31.8, "rainfall_mm": 281, "humidity_pct": 83, "rainy_days": 19, "sun_hours": 7.9},
            "Sep": {"avg_temp_c": 27.8, "min_temp_c": 25.2, "max_temp_c": 31.1, "rainfall_mm": 197, "humidity_pct": 83, "rainy_days": 15, "sun_hours": 8.0},
            "Oct": {"avg_temp_c": 25.8, "min_temp_c": 21.7, "max_temp_c": 30.1, "rainfall_mm": 52, "humidity_pct": 77, "rainy_days": 5, "sun_hours": 8.8},
            "Nov": {"avg_temp_c": 22.0, "min_temp_c": 16.5, "max_temp_c": 27.7, "rainfall_mm": 6, "humidity_pct": 65, "rainy_days": 1, "sun_hours": 9.3},
            "Dec": {"avg_temp_c": 17.9, "min_temp_c": 12.2, "max_temp_c": 23.8, "rainfall_mm": 8, "humidity_pct": 67, "rainy_days": 1, "sun_hours": 8.5}
        }
    },
    "Chhattisgarh": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1292,
        "months": {
            "Jan": {"avg_temp_c": 19.5, "min_temp_c": 11.2, "max_temp_c": 27.8, "rainfall_mm": 12, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 22.5, "min_temp_c": 13.8, "max_temp_c": 31.2, "rainfall_mm": 15, "humidity_pct": 45, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 27.0, "min_temp_c": 18.5, "max_temp_c": 35.5, "rainfall_mm": 14, "humidity_pct": 35, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 32.0, "min_temp_c": 23.8, "max_temp_c": 40.2, "rainfall_mm": 10, "humidity_pct": 28, "rainy_days": 1, "sun_hours": 10.5},
            "May": {"avg_temp_c": 34.2, "min_temp_c": 27.0, "max_temp_c": 41.4, "rainfall_mm": 18, "humidity_pct": 32, "rainy_days": 2, "sun_hours": 10.2},
            "Jun": {"avg_temp_c": 30.5, "min_temp_c": 25.0, "max_temp_c": 36.0, "rainfall_mm": 195, "humidity_pct": 72, "rainy_days": 13, "sun_hours": 6.5},
            "Jul": {"avg_temp_c": 27.2, "min_temp_c": 23.5, "max_temp_c": 30.9, "rainfall_mm": 345, "humidity_pct": 85, "rainy_days": 20, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 27.0, "min_temp_c": 23.2, "max_temp_c": 30.8, "rainfall_mm": 360, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 4.8},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 22.8, "max_temp_c": 32.2, "rainfall_mm": 215, "humidity_pct": 80, "rainy_days": 13, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 25.5, "min_temp_c": 19.0, "max_temp_c": 32.0, "rainfall_mm": 55, "humidity_pct": 65, "rainy_days": 4, "sun_hours": 8.5},
            "Nov": {"avg_temp_c": 21.8, "min_temp_c": 14.0, "max_temp_c": 29.6, "rainfall_mm": 15, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 18.5, "min_temp_c": 10.8, "max_temp_c": 26.2, "rainfall_mm": 8, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.5}
        }
    },
    "Goa": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 2926,
        "months": {
            "Jan": {"avg_temp_c": 25.8, "min_temp_c": 20.2, "max_temp_c": 31.4, "rainfall_mm": 2, "humidity_pct": 60, "rainy_days": 0, "sun_hours": 9.5},
            "Feb": {"avg_temp_c": 26.5, "min_temp_c": 20.8, "max_temp_c": 32.2, "rainfall_mm": 1, "humidity_pct": 58, "rainy_days": 0, "sun_hours": 10.0},
            "Mar": {"avg_temp_c": 28.2, "min_temp_c": 23.0, "max_temp_c": 33.4, "rainfall_mm": 4, "humidity_pct": 62, "rainy_days": 0, "sun_hours": 10.2},
            "Apr": {"avg_temp_c": 29.8, "min_temp_c": 25.2, "max_temp_c": 34.4, "rainfall_mm": 16, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 10.0},
            "May": {"avg_temp_c": 30.2, "min_temp_c": 26.0, "max_temp_c": 34.4, "rainfall_mm": 112, "humidity_pct": 74, "rainy_days": 7, "sun_hours": 8.5},
            "Jun": {"avg_temp_c": 28.0, "min_temp_c": 24.5, "max_temp_c": 31.5, "rainfall_mm": 580, "humidity_pct": 86, "rainy_days": 22, "sun_hours": 4.0},
            "Jul": {"avg_temp_c": 27.2, "min_temp_c": 24.0, "max_temp_c": 30.4, "rainfall_mm": 725, "humidity_pct": 89, "rainy_days": 25, "sun_hours": 3.2},
            "Aug": {"avg_temp_c": 27.0, "min_temp_c": 23.8, "max_temp_c": 30.2, "rainfall_mm": 580, "humidity_pct": 88, "rainy_days": 23, "sun_hours": 3.5},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 23.5, "max_temp_c": 31.5, "rainfall_mm": 355, "humidity_pct": 84, "rainy_days": 17, "sun_hours": 5.5},
            "Oct": {"avg_temp_c": 28.0, "min_temp_c": 23.5, "max_temp_c": 32.5, "rainfall_mm": 175, "humidity_pct": 76, "rainy_days": 8, "sun_hours": 7.8},
            "Nov": {"avg_temp_c": 27.2, "min_temp_c": 22.0, "max_temp_c": 32.4, "rainfall_mm": 48, "humidity_pct": 66, "rainy_days": 3, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 26.0, "min_temp_c": 20.8, "max_temp_c": 31.2, "rainfall_mm": 15, "humidity_pct": 62, "rainy_days": 1, "sun_hours": 9.2}
        }
    },
    "Gujarat": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 820,
        "months": {
            "Jan": {"avg_temp_c": 20.0, "min_temp_c": 12.5, "max_temp_c": 27.5, "rainfall_mm": 2, "humidity_pct": 45, "rainy_days": 0, "sun_hours": 9.0},
            "Feb": {"avg_temp_c": 22.5, "min_temp_c": 14.5, "max_temp_c": 30.5, "rainfall_mm": 2, "humidity_pct": 38, "rainy_days": 0, "sun_hours": 9.8},
            "Mar": {"avg_temp_c": 27.0, "min_temp_c": 19.0, "max_temp_c": 35.0, "rainfall_mm": 3, "humidity_pct": 32, "rainy_days": 0, "sun_hours": 10.5},
            "Apr": {"avg_temp_c": 31.0, "min_temp_c": 23.5, "max_temp_c": 38.5, "rainfall_mm": 3, "humidity_pct": 30, "rainy_days": 0, "sun_hours": 10.8},
            "May": {"avg_temp_c": 33.5, "min_temp_c": 26.5, "max_temp_c": 40.5, "rainfall_mm": 8, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 11.0},
            "Jun": {"avg_temp_c": 32.0, "min_temp_c": 26.5, "max_temp_c": 37.5, "rainfall_mm": 120, "humidity_pct": 68, "rainy_days": 8, "sun_hours": 8.0},
            "Jul": {"avg_temp_c": 29.0, "min_temp_c": 25.0, "max_temp_c": 33.0, "rainfall_mm": 265, "humidity_pct": 80, "rainy_days": 14, "sun_hours": 5.5},
            "Aug": {"avg_temp_c": 28.5, "min_temp_c": 24.5, "max_temp_c": 32.5, "rainfall_mm": 235, "humidity_pct": 82, "rainy_days": 13, "sun_hours": 5.8},
            "Sep": {"avg_temp_c": 29.0, "min_temp_c": 24.0, "max_temp_c": 34.0, "rainfall_mm": 120, "humidity_pct": 72, "rainy_days": 7, "sun_hours": 8.0},
            "Oct": {"avg_temp_c": 28.5, "min_temp_c": 21.5, "max_temp_c": 35.5, "rainfall_mm": 25, "humidity_pct": 55, "rainy_days": 2, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": 24.5, "min_temp_c": 16.5, "max_temp_c": 32.5, "rainfall_mm": 8, "humidity_pct": 48, "rainy_days": 1, "sun_hours": 9.2},
            "Dec": {"avg_temp_c": 21.0, "min_temp_c": 13.0, "max_temp_c": 29.0, "rainfall_mm": 3, "humidity_pct": 48, "rainy_days": 0, "sun_hours": 9.0}
        }
    },
    "Haryana": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 617,
        "months": {
            "Jan": {"avg_temp_c": 12.5, "min_temp_c": 5.8, "max_temp_c": 19.2, "rainfall_mm": 22, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 15.5, "min_temp_c": 8.5, "max_temp_c": 22.5, "rainfall_mm": 25, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 8.5},
            "Mar": {"avg_temp_c": 21.5, "min_temp_c": 13.5, "max_temp_c": 29.5, "rainfall_mm": 18, "humidity_pct": 48, "rainy_days": 2, "sun_hours": 9.8},
            "Apr": {"avg_temp_c": 28.5, "min_temp_c": 20.0, "max_temp_c": 37.0, "rainfall_mm": 12, "humidity_pct": 32, "rainy_days": 1, "sun_hours": 10.5},
            "May": {"avg_temp_c": 33.0, "min_temp_c": 25.0, "max_temp_c": 41.0, "rainfall_mm": 18, "humidity_pct": 30, "rainy_days": 2, "sun_hours": 11.0},
            "Jun": {"avg_temp_c": 34.0, "min_temp_c": 27.0, "max_temp_c": 41.0, "rainfall_mm": 55, "humidity_pct": 48, "rainy_days": 5, "sun_hours": 9.5},
            "Jul": {"avg_temp_c": 31.0, "min_temp_c": 26.5, "max_temp_c": 35.5, "rainfall_mm": 175, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.5},
            "Aug": {"avg_temp_c": 30.0, "min_temp_c": 25.5, "max_temp_c": 34.5, "rainfall_mm": 165, "humidity_pct": 75, "rainy_days": 11, "sun_hours": 7.8},
            "Sep": {"avg_temp_c": 29.0, "min_temp_c": 23.5, "max_temp_c": 34.5, "rainfall_mm": 85, "humidity_pct": 65, "rainy_days": 6, "sun_hours": 9.0},
            "Oct": {"avg_temp_c": 25.0, "min_temp_c": 17.5, "max_temp_c": 32.5, "rainfall_mm": 15, "humidity_pct": 52, "rainy_days": 1, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": 18.5, "min_temp_c": 10.5, "max_temp_c": 26.5, "rainfall_mm": 5, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 13.5, "min_temp_c": 6.5, "max_temp_c": 20.5, "rainfall_mm": 12, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Himachal Pradesh": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1251,
        "months": {
            "Jan": {"avg_temp_c": 5.0, "min_temp_c": -0.5, "max_temp_c": 10.5, "rainfall_mm": 62, "humidity_pct": 68, "rainy_days": 5, "sun_hours": 6.5},
            "Feb": {"avg_temp_c": 7.5, "min_temp_c": 1.5, "max_temp_c": 13.5, "rainfall_mm": 72, "humidity_pct": 65, "rainy_days": 6, "sun_hours": 7.0},
            "Mar": {"avg_temp_c": 12.5, "min_temp_c": 6.0, "max_temp_c": 19.0, "rainfall_mm": 65, "humidity_pct": 55, "rainy_days": 5, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 17.5, "min_temp_c": 10.5, "max_temp_c": 24.5, "rainfall_mm": 42, "humidity_pct": 42, "rainy_days": 4, "sun_hours": 9.5},
            "May": {"avg_temp_c": 21.5, "min_temp_c": 14.5, "max_temp_c": 28.5, "rainfall_mm": 52, "humidity_pct": 45, "rainy_days": 5, "sun_hours": 9.8},
            "Jun": {"avg_temp_c": 23.5, "min_temp_c": 17.5, "max_temp_c": 29.5, "rainfall_mm": 125, "humidity_pct": 68, "rainy_days": 10, "sun_hours": 7.5},
            "Jul": {"avg_temp_c": 22.0, "min_temp_c": 18.0, "max_temp_c": 26.0, "rainfall_mm": 310, "humidity_pct": 85, "rainy_days": 18, "sun_hours": 5.0},
            "Aug": {"avg_temp_c": 21.5, "min_temp_c": 17.5, "max_temp_c": 25.5, "rainfall_mm": 285, "humidity_pct": 86, "rainy_days": 17, "sun_hours": 5.2},
            "Sep": {"avg_temp_c": 20.0, "min_temp_c": 15.0, "max_temp_c": 25.0, "rainfall_mm": 135, "humidity_pct": 75, "rainy_days": 9, "sun_hours": 7.5},
            "Oct": {"avg_temp_c": 15.0, "min_temp_c": 9.0, "max_temp_c": 21.0, "rainfall_mm": 35, "humidity_pct": 58, "rainy_days": 3, "sun_hours": 9.0},
            "Nov": {"avg_temp_c": 10.0, "min_temp_c": 4.0, "max_temp_c": 16.0, "rainfall_mm": 18, "humidity_pct": 55, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 6.5, "min_temp_c": 1.0, "max_temp_c": 12.0, "rainfall_mm": 42, "humidity_pct": 65, "rainy_days": 4, "sun_hours": 6.5}
        }
    },
    "Jharkhand": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1326,
        "months": {
            "Jan": {"avg_temp_c": 17.5, "min_temp_c": 10.0, "max_temp_c": 25.0, "rainfall_mm": 15, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 20.5, "min_temp_c": 13.0, "max_temp_c": 28.0, "rainfall_mm": 22, "humidity_pct": 48, "rainy_days": 2, "sun_hours": 9.0},
            "Mar": {"avg_temp_c": 26.0, "min_temp_c": 18.0, "max_temp_c": 34.0, "rainfall_mm": 18, "humidity_pct": 38, "rainy_days": 2, "sun_hours": 9.5},
            "Apr": {"avg_temp_c": 31.0, "min_temp_c": 23.0, "max_temp_c": 39.0, "rainfall_mm": 15, "humidity_pct": 32, "rainy_days": 2, "sun_hours": 10.0},
            "May": {"avg_temp_c": 33.0, "min_temp_c": 26.0, "max_temp_c": 40.0, "rainfall_mm": 28, "humidity_pct": 42, "rainy_days": 3, "sun_hours": 10.2},
            "Jun": {"avg_temp_c": 30.5, "min_temp_c": 25.0, "max_temp_c": 36.0, "rainfall_mm": 195, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.0},
            "Jul": {"avg_temp_c": 27.5, "min_temp_c": 24.0, "max_temp_c": 31.0, "rainfall_mm": 310, "humidity_pct": 85, "rainy_days": 18, "sun_hours": 5.0},
            "Aug": {"avg_temp_c": 27.2, "min_temp_c": 23.5, "max_temp_c": 30.9, "rainfall_mm": 295, "humidity_pct": 86, "rainy_days": 17, "sun_hours": 5.5},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 23.0, "max_temp_c": 32.0, "rainfall_mm": 225, "humidity_pct": 80, "rainy_days": 12, "sun_hours": 7.0},
            "Oct": {"avg_temp_c": 25.0, "min_temp_c": 19.0, "max_temp_c": 31.0, "rainfall_mm": 72, "humidity_pct": 68, "rainy_days": 4, "sun_hours": 8.5},
            "Nov": {"avg_temp_c": 21.0, "min_temp_c": 13.5, "max_temp_c": 28.5, "rainfall_mm": 12, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 17.5, "min_temp_c": 10.0, "max_temp_c": 25.0, "rainfall_mm": 10, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.5}
        }
    },
    "Karnataka": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1284,
        "months": {
            "Jan": {"avg_temp_c": 23.5, "min_temp_c": 16.0, "max_temp_c": 31.0, "rainfall_mm": 3, "humidity_pct": 52, "rainy_days": 0, "sun_hours": 9.5},
            "Feb": {"avg_temp_c": 25.5, "min_temp_c": 17.5, "max_temp_c": 33.5, "rainfall_mm": 5, "humidity_pct": 45, "rainy_days": 0, "sun_hours": 10.0},
            "Mar": {"avg_temp_c": 28.0, "min_temp_c": 20.5, "max_temp_c": 35.5, "rainfall_mm": 12, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 10.2},
            "Apr": {"avg_temp_c": 29.5, "min_temp_c": 22.5, "max_temp_c": 36.5, "rainfall_mm": 48, "humidity_pct": 52, "rainy_days": 4, "sun_hours": 9.8},
            "May": {"avg_temp_c": 29.0, "min_temp_c": 22.5, "max_temp_c": 35.5, "rainfall_mm": 98, "humidity_pct": 62, "rainy_days": 7, "sun_hours": 8.5},
            "Jun": {"avg_temp_c": 26.0, "min_temp_c": 21.5, "max_temp_c": 30.5, "rainfall_mm": 185, "humidity_pct": 78, "rainy_days": 14, "sun_hours": 5.5},
            "Jul": {"avg_temp_c": 24.5, "min_temp_c": 21.0, "max_temp_c": 28.0, "rainfall_mm": 340, "humidity_pct": 85, "rainy_days": 20, "sun_hours": 3.8},
            "Aug": {"avg_temp_c": 24.5, "min_temp_c": 21.0, "max_temp_c": 28.0, "rainfall_mm": 280, "humidity_pct": 84, "rainy_days": 18, "sun_hours": 4.2},
            "Sep": {"avg_temp_c": 25.5, "min_temp_c": 21.0, "max_temp_c": 30.0, "rainfall_mm": 185, "humidity_pct": 78, "rainy_days": 12, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 25.0, "min_temp_c": 20.0, "max_temp_c": 30.0, "rainfall_mm": 108, "humidity_pct": 72, "rainy_days": 7, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 23.5, "min_temp_c": 17.5, "max_temp_c": 29.5, "rainfall_mm": 35, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 22.5, "min_temp_c": 15.5, "max_temp_c": 29.5, "rainfall_mm": 8, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 9.0}
        }
    },
    "Kerala": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 3055,
        "months": {
            "Jan": {"avg_temp_c": 26.5, "min_temp_c": 22.5, "max_temp_c": 30.5, "rainfall_mm": 18, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 27.5, "min_temp_c": 23.0, "max_temp_c": 32.0, "rainfall_mm": 22, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 9.0},
            "Mar": {"avg_temp_c": 28.5, "min_temp_c": 24.5, "max_temp_c": 32.5, "rainfall_mm": 42, "humidity_pct": 72, "rainy_days": 4, "sun_hours": 9.0},
            "Apr": {"avg_temp_c": 28.5, "min_temp_c": 25.0, "max_temp_c": 32.0, "rainfall_mm": 118, "humidity_pct": 78, "rainy_days": 10, "sun_hours": 8.0},
            "May": {"avg_temp_c": 28.0, "min_temp_c": 25.0, "max_temp_c": 31.0, "rainfall_mm": 248, "humidity_pct": 82, "rainy_days": 15, "sun_hours": 6.5},
            "Jun": {"avg_temp_c": 26.5, "min_temp_c": 23.5, "max_temp_c": 29.5, "rainfall_mm": 645, "humidity_pct": 90, "rainy_days": 24, "sun_hours": 3.5},
            "Jul": {"avg_temp_c": 26.0, "min_temp_c": 23.0, "max_temp_c": 29.0, "rainfall_mm": 685, "humidity_pct": 92, "rainy_days": 25, "sun_hours": 3.0},
            "Aug": {"avg_temp_c": 26.0, "min_temp_c": 23.0, "max_temp_c": 29.0, "rainfall_mm": 445, "humidity_pct": 90, "rainy_days": 22, "sun_hours": 3.5},
            "Sep": {"avg_temp_c": 26.5, "min_temp_c": 23.0, "max_temp_c": 30.0, "rainfall_mm": 315, "humidity_pct": 86, "rainy_days": 16, "sun_hours": 5.5},
            "Oct": {"avg_temp_c": 26.5, "min_temp_c": 23.0, "max_temp_c": 30.0, "rainfall_mm": 305, "humidity_pct": 84, "rainy_days": 15, "sun_hours": 6.5},
            "Nov": {"avg_temp_c": 26.5, "min_temp_c": 23.0, "max_temp_c": 30.0, "rainfall_mm": 178, "humidity_pct": 78, "rainy_days": 10, "sun_hours": 7.5},
            "Dec": {"avg_temp_c": 26.0, "min_temp_c": 22.5, "max_temp_c": 29.5, "rainfall_mm": 42, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 8.0}
        }
    },
    "Madhya Pradesh": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1160,
        "months": {
            "Jan": {"avg_temp_c": 17.0, "min_temp_c": 8.5, "max_temp_c": 25.5, "rainfall_mm": 12, "humidity_pct": 48, "rainy_days": 1, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 20.5, "min_temp_c": 11.5, "max_temp_c": 29.5, "rainfall_mm": 10, "humidity_pct": 38, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 26.0, "min_temp_c": 17.0, "max_temp_c": 35.0, "rainfall_mm": 8, "humidity_pct": 28, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 32.0, "min_temp_c": 23.0, "max_temp_c": 41.0, "rainfall_mm": 5, "humidity_pct": 22, "rainy_days": 0, "sun_hours": 10.5},
            "May": {"avg_temp_c": 35.0, "min_temp_c": 27.5, "max_temp_c": 42.5, "rainfall_mm": 10, "humidity_pct": 25, "rainy_days": 1, "sun_hours": 10.8},
            "Jun": {"avg_temp_c": 32.5, "min_temp_c": 26.5, "max_temp_c": 38.5, "rainfall_mm": 145, "humidity_pct": 62, "rainy_days": 10, "sun_hours": 7.5},
            "Jul": {"avg_temp_c": 27.5, "min_temp_c": 24.0, "max_temp_c": 31.0, "rainfall_mm": 340, "humidity_pct": 82, "rainy_days": 18, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 27.0, "min_temp_c": 23.5, "max_temp_c": 30.5, "rainfall_mm": 310, "humidity_pct": 84, "rainy_days": 17, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 22.5, "max_temp_c": 32.5, "rainfall_mm": 195, "humidity_pct": 75, "rainy_days": 11, "sun_hours": 7.0},
            "Oct": {"avg_temp_c": 25.5, "min_temp_c": 18.0, "max_temp_c": 33.0, "rainfall_mm": 42, "humidity_pct": 52, "rainy_days": 3, "sun_hours": 9.0},
            "Nov": {"avg_temp_c": 20.5, "min_temp_c": 12.0, "max_temp_c": 29.0, "rainfall_mm": 12, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 17.0, "min_temp_c": 9.0, "max_temp_c": 25.0, "rainfall_mm": 8, "humidity_pct": 48, "rainy_days": 1, "sun_hours": 8.5}
        }
    },
    "Maharashtra": {
        "data_period": "1991-2021",
        "annual_rainfall_mm": 1155,
        "months": {
            "Jan": {"avg_temp_c": 22.5, "min_temp_c": 14.5, "max_temp_c": 30.5, "rainfall_mm": 3, "humidity_pct": 45, "rainy_days": 0, "sun_hours": 9.5},
            "Feb": {"avg_temp_c": 24.5, "min_temp_c": 16.0, "max_temp_c": 33.0, "rainfall_mm": 3, "humidity_pct": 38, "rainy_days": 0, "sun_hours": 10.0},
            "Mar": {"avg_temp_c": 28.0, "min_temp_c": 20.0, "max_temp_c": 36.0, "rainfall_mm": 8, "humidity_pct": 32, "rainy_days": 1, "sun_hours": 10.5},
            "Apr": {"avg_temp_c": 31.5, "min_temp_c": 24.0, "max_temp_c": 39.0, "rainfall_mm": 12, "humidity_pct": 35, "rainy_days": 1, "sun_hours": 10.5},
            "May": {"avg_temp_c": 33.0, "min_temp_c": 26.0, "max_temp_c": 40.0, "rainfall_mm": 28, "humidity_pct": 48, "rainy_days": 3, "sun_hours": 10.0},
            "Jun": {"avg_temp_c": 29.0, "min_temp_c": 24.0, "max_temp_c": 34.0, "rainfall_mm": 185, "humidity_pct": 72, "rainy_days": 13, "sun_hours": 5.5},
            "Jul": {"avg_temp_c": 27.0, "min_temp_c": 23.0, "max_temp_c": 31.0, "rainfall_mm": 305, "humidity_pct": 82, "rainy_days": 19, "sun_hours": 3.8},
            "Aug": {"avg_temp_c": 26.5, "min_temp_c": 22.5, "max_temp_c": 30.5, "rainfall_mm": 255, "humidity_pct": 83, "rainy_days": 17, "sun_hours": 4.2},
            "Sep": {"avg_temp_c": 27.0, "min_temp_c": 22.5, "max_temp_c": 31.5, "rainfall_mm": 175, "humidity_pct": 76, "rainy_days": 11, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 27.0, "min_temp_c": 20.5, "max_temp_c": 33.5, "rainfall_mm": 82, "humidity_pct": 62, "rainy_days": 5, "sun_hours": 8.5},
            "Nov": {"avg_temp_c": 24.5, "min_temp_c": 17.0, "max_temp_c": 32.0, "rainfall_mm": 35, "humidity_pct": 52, "rainy_days": 2, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 22.0, "min_temp_c": 14.0, "max_temp_c": 30.0, "rainfall_mm": 8, "humidity_pct": 48, "rainy_days": 0, "sun_hours": 9.2}
        }
    },
    "Manipur": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1482,
        "months": {
            "Jan": {"avg_temp_c": 12.5, "min_temp_c": 4.5, "max_temp_c": 20.5, "rainfall_mm": 18, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 15.0, "min_temp_c": 7.0, "max_temp_c": 23.0, "rainfall_mm": 32, "humidity_pct": 65, "rainy_days": 4, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 19.5, "min_temp_c": 11.5, "max_temp_c": 27.5, "rainfall_mm": 68, "humidity_pct": 62, "rainy_days": 7, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 22.5, "min_temp_c": 15.0, "max_temp_c": 30.0, "rainfall_mm": 115, "humidity_pct": 70, "rainy_days": 12, "sun_hours": 8.0},
            "May": {"avg_temp_c": 24.0, "min_temp_c": 17.5, "max_temp_c": 30.5, "rainfall_mm": 195, "humidity_pct": 78, "rainy_days": 15, "sun_hours": 7.0},
            "Jun": {"avg_temp_c": 25.0, "min_temp_c": 20.0, "max_temp_c": 30.0, "rainfall_mm": 285, "humidity_pct": 84, "rainy_days": 20, "sun_hours": 5.0},
            "Jul": {"avg_temp_c": 25.5, "min_temp_c": 21.0, "max_temp_c": 30.0, "rainfall_mm": 275, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 25.5, "min_temp_c": 21.0, "max_temp_c": 30.0, "rainfall_mm": 245, "humidity_pct": 85, "rainy_days": 19, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 24.5, "min_temp_c": 19.5, "max_temp_c": 29.5, "rainfall_mm": 165, "humidity_pct": 82, "rainy_days": 13, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 21.0, "min_temp_c": 15.0, "max_temp_c": 27.0, "rainfall_mm": 85, "humidity_pct": 76, "rainy_days": 6, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 16.5, "min_temp_c": 9.5, "max_temp_c": 23.5, "rainfall_mm": 22, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 13.0, "min_temp_c": 5.5, "max_temp_c": 20.5, "rainfall_mm": 12, "humidity_pct": 72, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Meghalaya": {
        "data_period": "1991-2021", "annual_rainfall_mm": 2818,
        "months": {
            "Jan": {"avg_temp_c": 12.0, "min_temp_c": 5.0, "max_temp_c": 19.0, "rainfall_mm": 15, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 14.5, "min_temp_c": 7.5, "max_temp_c": 21.5, "rainfall_mm": 28, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 7.5},
            "Mar": {"avg_temp_c": 18.5, "min_temp_c": 11.5, "max_temp_c": 25.5, "rainfall_mm": 98, "humidity_pct": 65, "rainy_days": 8, "sun_hours": 7.5},
            "Apr": {"avg_temp_c": 21.0, "min_temp_c": 14.5, "max_temp_c": 27.5, "rainfall_mm": 265, "humidity_pct": 78, "rainy_days": 15, "sun_hours": 6.5},
            "May": {"avg_temp_c": 22.0, "min_temp_c": 16.5, "max_temp_c": 27.5, "rainfall_mm": 380, "humidity_pct": 84, "rainy_days": 19, "sun_hours": 5.5},
            "Jun": {"avg_temp_c": 23.0, "min_temp_c": 19.0, "max_temp_c": 27.0, "rainfall_mm": 545, "humidity_pct": 88, "rainy_days": 23, "sun_hours": 4.0},
            "Jul": {"avg_temp_c": 23.5, "min_temp_c": 20.0, "max_temp_c": 27.0, "rainfall_mm": 520, "humidity_pct": 90, "rainy_days": 24, "sun_hours": 3.5},
            "Aug": {"avg_temp_c": 23.5, "min_temp_c": 20.0, "max_temp_c": 27.0, "rainfall_mm": 420, "humidity_pct": 88, "rainy_days": 21, "sun_hours": 4.0},
            "Sep": {"avg_temp_c": 23.0, "min_temp_c": 18.5, "max_temp_c": 27.5, "rainfall_mm": 285, "humidity_pct": 85, "rainy_days": 15, "sun_hours": 5.5},
            "Oct": {"avg_temp_c": 20.5, "min_temp_c": 15.0, "max_temp_c": 26.0, "rainfall_mm": 125, "humidity_pct": 78, "rainy_days": 7, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 16.0, "min_temp_c": 9.5, "max_temp_c": 22.5, "rainfall_mm": 22, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 13.0, "min_temp_c": 6.0, "max_temp_c": 20.0, "rainfall_mm": 12, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.0}
        }
    },
    "Mizoram": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1888,
        "months": {
            "Jan": {"avg_temp_c": 15.0, "min_temp_c": 9.0, "max_temp_c": 21.0, "rainfall_mm": 10, "humidity_pct": 65, "rainy_days": 1, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 17.0, "min_temp_c": 11.0, "max_temp_c": 23.0, "rainfall_mm": 18, "humidity_pct": 58, "rainy_days": 2, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 20.5, "min_temp_c": 14.5, "max_temp_c": 26.5, "rainfall_mm": 52, "humidity_pct": 58, "rainy_days": 5, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 22.5, "min_temp_c": 16.5, "max_temp_c": 28.5, "rainfall_mm": 142, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.5},
            "May": {"avg_temp_c": 23.0, "min_temp_c": 18.0, "max_temp_c": 28.0, "rainfall_mm": 285, "humidity_pct": 82, "rainy_days": 18, "sun_hours": 6.0},
            "Jun": {"avg_temp_c": 23.5, "min_temp_c": 19.5, "max_temp_c": 27.5, "rainfall_mm": 345, "humidity_pct": 88, "rainy_days": 21, "sun_hours": 4.5},
            "Jul": {"avg_temp_c": 23.5, "min_temp_c": 20.0, "max_temp_c": 27.0, "rainfall_mm": 345, "humidity_pct": 90, "rainy_days": 22, "sun_hours": 4.0},
            "Aug": {"avg_temp_c": 23.5, "min_temp_c": 20.0, "max_temp_c": 27.0, "rainfall_mm": 295, "humidity_pct": 88, "rainy_days": 20, "sun_hours": 4.5},
            "Sep": {"avg_temp_c": 23.0, "min_temp_c": 19.0, "max_temp_c": 27.0, "rainfall_mm": 215, "humidity_pct": 84, "rainy_days": 14, "sun_hours": 6.0},
            "Oct": {"avg_temp_c": 21.5, "min_temp_c": 16.5, "max_temp_c": 26.5, "rainfall_mm": 95, "humidity_pct": 76, "rainy_days": 7, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 18.5, "min_temp_c": 12.5, "max_temp_c": 24.5, "rainfall_mm": 18, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 15.5, "min_temp_c": 9.5, "max_temp_c": 21.5, "rainfall_mm": 8, "humidity_pct": 65, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Nagaland": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1811,
        "months": {
            "Jan": {"avg_temp_c": 12.5, "min_temp_c": 5.5, "max_temp_c": 19.5, "rainfall_mm": 12, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 14.5, "min_temp_c": 7.5, "max_temp_c": 21.5, "rainfall_mm": 25, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 7.5},
            "Mar": {"avg_temp_c": 18.5, "min_temp_c": 11.5, "max_temp_c": 25.5, "rainfall_mm": 55, "humidity_pct": 58, "rainy_days": 6, "sun_hours": 8.0},
            "Apr": {"avg_temp_c": 21.0, "min_temp_c": 14.5, "max_temp_c": 27.5, "rainfall_mm": 135, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.5},
            "May": {"avg_temp_c": 22.5, "min_temp_c": 17.0, "max_temp_c": 28.0, "rainfall_mm": 225, "humidity_pct": 80, "rainy_days": 16, "sun_hours": 6.0},
            "Jun": {"avg_temp_c": 23.5, "min_temp_c": 19.0, "max_temp_c": 28.0, "rainfall_mm": 365, "humidity_pct": 86, "rainy_days": 22, "sun_hours": 4.5},
            "Jul": {"avg_temp_c": 24.0, "min_temp_c": 20.0, "max_temp_c": 28.0, "rainfall_mm": 375, "humidity_pct": 88, "rainy_days": 23, "sun_hours": 4.0},
            "Aug": {"avg_temp_c": 24.0, "min_temp_c": 20.0, "max_temp_c": 28.0, "rainfall_mm": 285, "humidity_pct": 87, "rainy_days": 20, "sun_hours": 4.5},
            "Sep": {"avg_temp_c": 23.0, "min_temp_c": 18.5, "max_temp_c": 27.5, "rainfall_mm": 195, "humidity_pct": 84, "rainy_days": 14, "sun_hours": 6.0},
            "Oct": {"avg_temp_c": 20.5, "min_temp_c": 14.5, "max_temp_c": 26.5, "rainfall_mm": 72, "humidity_pct": 76, "rainy_days": 5, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 16.5, "min_temp_c": 9.5, "max_temp_c": 23.5, "rainfall_mm": 18, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 13.0, "min_temp_c": 6.0, "max_temp_c": 20.0, "rainfall_mm": 8, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.0}
        }
    },
    "Odisha": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1489,
        "months": {
            "Jan": {"avg_temp_c": 21.5, "min_temp_c": 14.0, "max_temp_c": 29.0, "rainfall_mm": 12, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 24.5, "min_temp_c": 17.0, "max_temp_c": 32.0, "rainfall_mm": 22, "humidity_pct": 52, "rainy_days": 2, "sun_hours": 9.0},
            "Mar": {"avg_temp_c": 28.5, "min_temp_c": 21.0, "max_temp_c": 36.0, "rainfall_mm": 22, "humidity_pct": 45, "rainy_days": 2, "sun_hours": 9.5},
            "Apr": {"avg_temp_c": 31.5, "min_temp_c": 24.5, "max_temp_c": 38.5, "rainfall_mm": 25, "humidity_pct": 52, "rainy_days": 3, "sun_hours": 9.5},
            "May": {"avg_temp_c": 32.5, "min_temp_c": 26.5, "max_temp_c": 38.5, "rainfall_mm": 52, "humidity_pct": 62, "rainy_days": 5, "sun_hours": 9.0},
            "Jun": {"avg_temp_c": 30.5, "min_temp_c": 25.5, "max_temp_c": 35.5, "rainfall_mm": 205, "humidity_pct": 76, "rainy_days": 13, "sun_hours": 6.0},
            "Jul": {"avg_temp_c": 28.5, "min_temp_c": 24.5, "max_temp_c": 32.5, "rainfall_mm": 335, "humidity_pct": 84, "rainy_days": 18, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 28.0, "min_temp_c": 24.5, "max_temp_c": 31.5, "rainfall_mm": 345, "humidity_pct": 85, "rainy_days": 19, "sun_hours": 4.8},
            "Sep": {"avg_temp_c": 28.5, "min_temp_c": 24.0, "max_temp_c": 33.0, "rainfall_mm": 245, "humidity_pct": 80, "rainy_days": 13, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 27.0, "min_temp_c": 21.5, "max_temp_c": 32.5, "rainfall_mm": 125, "humidity_pct": 72, "rainy_days": 6, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 24.0, "min_temp_c": 17.5, "max_temp_c": 30.5, "rainfall_mm": 38, "humidity_pct": 62, "rainy_days": 2, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 21.5, "min_temp_c": 14.0, "max_temp_c": 29.0, "rainfall_mm": 8, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.5}
        }
    },
    "Punjab": {
        "data_period": "1991-2021", "annual_rainfall_mm": 649,
        "months": {
            "Jan": {"avg_temp_c": 11.5, "min_temp_c": 4.5, "max_temp_c": 18.5, "rainfall_mm": 28, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 14.5, "min_temp_c": 7.0, "max_temp_c": 22.0, "rainfall_mm": 32, "humidity_pct": 65, "rainy_days": 3, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 20.0, "min_temp_c": 12.0, "max_temp_c": 28.0, "rainfall_mm": 25, "humidity_pct": 52, "rainy_days": 3, "sun_hours": 9.0},
            "Apr": {"avg_temp_c": 27.0, "min_temp_c": 18.5, "max_temp_c": 35.5, "rainfall_mm": 15, "humidity_pct": 35, "rainy_days": 2, "sun_hours": 10.0},
            "May": {"avg_temp_c": 32.0, "min_temp_c": 23.5, "max_temp_c": 40.5, "rainfall_mm": 18, "humidity_pct": 32, "rainy_days": 2, "sun_hours": 10.5},
            "Jun": {"avg_temp_c": 34.0, "min_temp_c": 26.5, "max_temp_c": 41.5, "rainfall_mm": 48, "humidity_pct": 48, "rainy_days": 5, "sun_hours": 9.5},
            "Jul": {"avg_temp_c": 31.5, "min_temp_c": 26.5, "max_temp_c": 36.5, "rainfall_mm": 165, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.5},
            "Aug": {"avg_temp_c": 30.5, "min_temp_c": 25.5, "max_temp_c": 35.5, "rainfall_mm": 155, "humidity_pct": 75, "rainy_days": 11, "sun_hours": 7.8},
            "Sep": {"avg_temp_c": 29.0, "min_temp_c": 23.0, "max_temp_c": 35.0, "rainfall_mm": 82, "humidity_pct": 65, "rainy_days": 6, "sun_hours": 9.0},
            "Oct": {"avg_temp_c": 24.0, "min_temp_c": 16.0, "max_temp_c": 32.0, "rainfall_mm": 15, "humidity_pct": 52, "rainy_days": 1, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": 17.5, "min_temp_c": 9.0, "max_temp_c": 26.0, "rainfall_mm": 8, "humidity_pct": 60, "rainy_days": 1, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 12.5, "min_temp_c": 5.0, "max_temp_c": 20.0, "rainfall_mm": 18, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 7.0}
        }
    },
    "Rajasthan": {
        "data_period": "1991-2021", "annual_rainfall_mm": 530,
        "months": {
            "Jan": {"avg_temp_c": 15.5, "min_temp_c": 7.8, "max_temp_c": 23.2, "rainfall_mm": 8, "humidity_pct": 45, "rainy_days": 1, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 18.5, "min_temp_c": 10.5, "max_temp_c": 26.5, "rainfall_mm": 8, "humidity_pct": 38, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 24.5, "min_temp_c": 16.0, "max_temp_c": 33.0, "rainfall_mm": 5, "humidity_pct": 28, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 31.0, "min_temp_c": 22.5, "max_temp_c": 39.5, "rainfall_mm": 5, "humidity_pct": 22, "rainy_days": 0, "sun_hours": 10.5},
            "May": {"avg_temp_c": 35.0, "min_temp_c": 27.0, "max_temp_c": 43.0, "rainfall_mm": 12, "humidity_pct": 25, "rainy_days": 1, "sun_hours": 11.0},
            "Jun": {"avg_temp_c": 35.5, "min_temp_c": 28.5, "max_temp_c": 42.5, "rainfall_mm": 52, "humidity_pct": 45, "rainy_days": 4, "sun_hours": 9.5},
            "Jul": {"avg_temp_c": 31.5, "min_temp_c": 26.0, "max_temp_c": 37.0, "rainfall_mm": 155, "humidity_pct": 72, "rainy_days": 10, "sun_hours": 7.0},
            "Aug": {"avg_temp_c": 30.0, "min_temp_c": 25.0, "max_temp_c": 35.0, "rainfall_mm": 148, "humidity_pct": 75, "rainy_days": 9, "sun_hours": 7.5},
            "Sep": {"avg_temp_c": 30.0, "min_temp_c": 24.0, "max_temp_c": 36.0, "rainfall_mm": 72, "humidity_pct": 62, "rainy_days": 5, "sun_hours": 9.0},
            "Oct": {"avg_temp_c": 27.5, "min_temp_c": 19.5, "max_temp_c": 35.5, "rainfall_mm": 15, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": 21.5, "min_temp_c": 13.0, "max_temp_c": 30.0, "rainfall_mm": 5, "humidity_pct": 38, "rainy_days": 0, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 16.5, "min_temp_c": 8.5, "max_temp_c": 24.5, "rainfall_mm": 5, "humidity_pct": 45, "rainy_days": 0, "sun_hours": 8.5}
        }
    },
    "Sikkim": {
        "data_period": "1991-2021", "annual_rainfall_mm": 2739,
        "months": {
            "Jan": {"avg_temp_c": 8.5, "min_temp_c": 2.0, "max_temp_c": 15.0, "rainfall_mm": 35, "humidity_pct": 72, "rainy_days": 4, "sun_hours": 6.5},
            "Feb": {"avg_temp_c": 10.5, "min_temp_c": 4.0, "max_temp_c": 17.0, "rainfall_mm": 42, "humidity_pct": 68, "rainy_days": 5, "sun_hours": 7.0},
            "Mar": {"avg_temp_c": 14.5, "min_temp_c": 8.0, "max_temp_c": 21.0, "rainfall_mm": 85, "humidity_pct": 65, "rainy_days": 8, "sun_hours": 7.5},
            "Apr": {"avg_temp_c": 17.5, "min_temp_c": 11.0, "max_temp_c": 24.0, "rainfall_mm": 178, "humidity_pct": 75, "rainy_days": 14, "sun_hours": 7.0},
            "May": {"avg_temp_c": 19.5, "min_temp_c": 13.5, "max_temp_c": 25.5, "rainfall_mm": 345, "humidity_pct": 82, "rainy_days": 19, "sun_hours": 6.0},
            "Jun": {"avg_temp_c": 20.5, "min_temp_c": 15.5, "max_temp_c": 25.5, "rainfall_mm": 525, "humidity_pct": 88, "rainy_days": 24, "sun_hours": 4.0},
            "Jul": {"avg_temp_c": 21.0, "min_temp_c": 16.5, "max_temp_c": 25.5, "rainfall_mm": 575, "humidity_pct": 90, "rainy_days": 26, "sun_hours": 3.5},
            "Aug": {"avg_temp_c": 21.0, "min_temp_c": 16.5, "max_temp_c": 25.5, "rainfall_mm": 465, "humidity_pct": 89, "rainy_days": 23, "sun_hours": 4.0},
            "Sep": {"avg_temp_c": 19.5, "min_temp_c": 14.5, "max_temp_c": 24.5, "rainfall_mm": 310, "humidity_pct": 85, "rainy_days": 17, "sun_hours": 5.5},
            "Oct": {"avg_temp_c": 16.0, "min_temp_c": 10.0, "max_temp_c": 22.0, "rainfall_mm": 98, "humidity_pct": 78, "rainy_days": 7, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 12.0, "min_temp_c": 6.0, "max_temp_c": 18.0, "rainfall_mm": 22, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 7.5},
            "Dec": {"avg_temp_c": 9.0, "min_temp_c": 3.0, "max_temp_c": 15.0, "rainfall_mm": 15, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 6.5}
        }
    },
    "Tamil Nadu": {
        "data_period": "1991-2021", "annual_rainfall_mm": 998,
        "months": {
            "Jan": {"avg_temp_c": 24.5, "min_temp_c": 20.0, "max_temp_c": 29.0, "rainfall_mm": 32, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 25.5, "min_temp_c": 20.5, "max_temp_c": 30.5, "rainfall_mm": 15, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 28.0, "min_temp_c": 23.0, "max_temp_c": 33.0, "rainfall_mm": 12, "humidity_pct": 65, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 30.5, "min_temp_c": 25.5, "max_temp_c": 35.5, "rainfall_mm": 25, "humidity_pct": 68, "rainy_days": 3, "sun_hours": 9.5},
            "May": {"avg_temp_c": 32.0, "min_temp_c": 27.0, "max_temp_c": 37.0, "rainfall_mm": 52, "humidity_pct": 62, "rainy_days": 4, "sun_hours": 9.0},
            "Jun": {"avg_temp_c": 31.0, "min_temp_c": 26.0, "max_temp_c": 36.0, "rainfall_mm": 48, "humidity_pct": 58, "rainy_days": 4, "sun_hours": 8.5},
            "Jul": {"avg_temp_c": 30.0, "min_temp_c": 25.5, "max_temp_c": 34.5, "rainfall_mm": 62, "humidity_pct": 62, "rainy_days": 5, "sun_hours": 7.5},
            "Aug": {"avg_temp_c": 30.0, "min_temp_c": 25.0, "max_temp_c": 35.0, "rainfall_mm": 98, "humidity_pct": 68, "rainy_days": 8, "sun_hours": 7.5},
            "Sep": {"avg_temp_c": 29.5, "min_temp_c": 24.5, "max_temp_c": 34.5, "rainfall_mm": 125, "humidity_pct": 72, "rainy_days": 9, "sun_hours": 7.5},
            "Oct": {"avg_temp_c": 28.0, "min_temp_c": 23.5, "max_temp_c": 32.5, "rainfall_mm": 195, "humidity_pct": 78, "rainy_days": 12, "sun_hours": 7.0},
            "Nov": {"avg_temp_c": 26.0, "min_temp_c": 22.0, "max_temp_c": 30.0, "rainfall_mm": 235, "humidity_pct": 80, "rainy_days": 13, "sun_hours": 7.0},
            "Dec": {"avg_temp_c": 24.5, "min_temp_c": 20.5, "max_temp_c": 28.5, "rainfall_mm": 115, "humidity_pct": 76, "rainy_days": 7, "sun_hours": 7.5}
        }
    },
    "Telangana": {
        "data_period": "1991-2021", "annual_rainfall_mm": 905,
        "months": {
            "Jan": {"avg_temp_c": 22.0, "min_temp_c": 14.5, "max_temp_c": 29.5, "rainfall_mm": 5, "humidity_pct": 52, "rainy_days": 1, "sun_hours": 9.0},
            "Feb": {"avg_temp_c": 25.0, "min_temp_c": 17.0, "max_temp_c": 33.0, "rainfall_mm": 8, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 29.0, "min_temp_c": 21.0, "max_temp_c": 37.0, "rainfall_mm": 12, "humidity_pct": 35, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 33.0, "min_temp_c": 25.0, "max_temp_c": 41.0, "rainfall_mm": 22, "humidity_pct": 32, "rainy_days": 2, "sun_hours": 10.2},
            "May": {"avg_temp_c": 35.0, "min_temp_c": 27.5, "max_temp_c": 42.5, "rainfall_mm": 35, "humidity_pct": 38, "rainy_days": 3, "sun_hours": 10.0},
            "Jun": {"avg_temp_c": 30.5, "min_temp_c": 24.5, "max_temp_c": 36.5, "rainfall_mm": 135, "humidity_pct": 68, "rainy_days": 10, "sun_hours": 6.5},
            "Jul": {"avg_temp_c": 28.0, "min_temp_c": 23.0, "max_temp_c": 33.0, "rainfall_mm": 205, "humidity_pct": 78, "rainy_days": 15, "sun_hours": 5.0},
            "Aug": {"avg_temp_c": 27.5, "min_temp_c": 22.5, "max_temp_c": 32.5, "rainfall_mm": 215, "humidity_pct": 80, "rainy_days": 15, "sun_hours": 5.5},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 22.5, "max_temp_c": 32.5, "rainfall_mm": 175, "humidity_pct": 78, "rainy_days": 11, "sun_hours": 7.0},
            "Oct": {"avg_temp_c": 26.0, "min_temp_c": 20.5, "max_temp_c": 31.5, "rainfall_mm": 78, "humidity_pct": 68, "rainy_days": 5, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 23.5, "min_temp_c": 17.0, "max_temp_c": 30.0, "rainfall_mm": 22, "humidity_pct": 58, "rainy_days": 2, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 21.5, "min_temp_c": 14.5, "max_temp_c": 28.5, "rainfall_mm": 8, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 9.0}
        }
    },
    "Tripura": {
        "data_period": "1991-2021", "annual_rainfall_mm": 2152,
        "months": {
            "Jan": {"avg_temp_c": 17.5, "min_temp_c": 10.5, "max_temp_c": 24.5, "rainfall_mm": 12, "humidity_pct": 72, "rainy_days": 1, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 20.0, "min_temp_c": 13.0, "max_temp_c": 27.0, "rainfall_mm": 22, "humidity_pct": 65, "rainy_days": 3, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 24.5, "min_temp_c": 17.5, "max_temp_c": 31.5, "rainfall_mm": 65, "humidity_pct": 62, "rainy_days": 6, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 27.0, "min_temp_c": 21.0, "max_temp_c": 33.0, "rainfall_mm": 175, "humidity_pct": 75, "rainy_days": 13, "sun_hours": 7.5},
            "May": {"avg_temp_c": 28.0, "min_temp_c": 22.5, "max_temp_c": 33.5, "rainfall_mm": 285, "humidity_pct": 82, "rainy_days": 17, "sun_hours": 6.5},
            "Jun": {"avg_temp_c": 28.5, "min_temp_c": 23.5, "max_temp_c": 33.5, "rainfall_mm": 385, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 5.0},
            "Jul": {"avg_temp_c": 28.5, "min_temp_c": 24.0, "max_temp_c": 33.0, "rainfall_mm": 395, "humidity_pct": 88, "rainy_days": 22, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 28.5, "min_temp_c": 24.0, "max_temp_c": 33.0, "rainfall_mm": 335, "humidity_pct": 87, "rainy_days": 20, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 28.0, "min_temp_c": 23.0, "max_temp_c": 33.0, "rainfall_mm": 225, "humidity_pct": 84, "rainy_days": 14, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 26.0, "min_temp_c": 20.0, "max_temp_c": 32.0, "rainfall_mm": 108, "humidity_pct": 78, "rainy_days": 7, "sun_hours": 8.0},
            "Nov": {"avg_temp_c": 22.0, "min_temp_c": 15.0, "max_temp_c": 29.0, "rainfall_mm": 22, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 18.5, "min_temp_c": 11.5, "max_temp_c": 25.5, "rainfall_mm": 8, "humidity_pct": 72, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Uttar Pradesh": {
        "data_period": "1991-2021", "annual_rainfall_mm": 990,
        "months": {
            "Jan": {"avg_temp_c": 14.0, "min_temp_c": 7.0, "max_temp_c": 21.0, "rainfall_mm": 18, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 17.5, "min_temp_c": 10.0, "max_temp_c": 25.0, "rainfall_mm": 18, "humidity_pct": 58, "rainy_days": 2, "sun_hours": 8.5},
            "Mar": {"avg_temp_c": 24.0, "min_temp_c": 16.0, "max_temp_c": 32.0, "rainfall_mm": 12, "humidity_pct": 42, "rainy_days": 1, "sun_hours": 9.5},
            "Apr": {"avg_temp_c": 31.0, "min_temp_c": 22.5, "max_temp_c": 39.5, "rainfall_mm": 8, "humidity_pct": 28, "rainy_days": 1, "sun_hours": 10.5},
            "May": {"avg_temp_c": 34.5, "min_temp_c": 26.5, "max_temp_c": 42.5, "rainfall_mm": 15, "humidity_pct": 30, "rainy_days": 2, "sun_hours": 10.5},
            "Jun": {"avg_temp_c": 34.0, "min_temp_c": 27.5, "max_temp_c": 40.5, "rainfall_mm": 95, "humidity_pct": 55, "rainy_days": 7, "sun_hours": 8.5},
            "Jul": {"avg_temp_c": 30.5, "min_temp_c": 26.0, "max_temp_c": 35.0, "rainfall_mm": 265, "humidity_pct": 78, "rainy_days": 16, "sun_hours": 6.0},
            "Aug": {"avg_temp_c": 29.5, "min_temp_c": 25.5, "max_temp_c": 33.5, "rainfall_mm": 265, "humidity_pct": 82, "rainy_days": 16, "sun_hours": 6.5},
            "Sep": {"avg_temp_c": 29.0, "min_temp_c": 24.0, "max_temp_c": 34.0, "rainfall_mm": 175, "humidity_pct": 75, "rainy_days": 10, "sun_hours": 8.0},
            "Oct": {"avg_temp_c": 26.0, "min_temp_c": 19.0, "max_temp_c": 33.0, "rainfall_mm": 35, "humidity_pct": 58, "rainy_days": 2, "sun_hours": 9.0},
            "Nov": {"avg_temp_c": 20.0, "min_temp_c": 12.0, "max_temp_c": 28.0, "rainfall_mm": 5, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": 15.0, "min_temp_c": 7.5, "max_temp_c": 22.5, "rainfall_mm": 8, "humidity_pct": 65, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    "Uttarakhand": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1543,
        "months": {
            "Jan": {"avg_temp_c": 7.5, "min_temp_c": 1.5, "max_temp_c": 13.5, "rainfall_mm": 52, "humidity_pct": 65, "rainy_days": 4, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 10.0, "min_temp_c": 3.5, "max_temp_c": 16.5, "rainfall_mm": 58, "humidity_pct": 60, "rainy_days": 5, "sun_hours": 7.5},
            "Mar": {"avg_temp_c": 15.5, "min_temp_c": 8.5, "max_temp_c": 22.5, "rainfall_mm": 45, "humidity_pct": 48, "rainy_days": 4, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 20.5, "min_temp_c": 13.0, "max_temp_c": 28.0, "rainfall_mm": 28, "humidity_pct": 38, "rainy_days": 3, "sun_hours": 9.5},
            "May": {"avg_temp_c": 24.5, "min_temp_c": 17.0, "max_temp_c": 32.0, "rainfall_mm": 45, "humidity_pct": 42, "rainy_days": 5, "sun_hours": 9.8},
            "Jun": {"avg_temp_c": 25.5, "min_temp_c": 19.5, "max_temp_c": 31.5, "rainfall_mm": 175, "humidity_pct": 72, "rainy_days": 13, "sun_hours": 6.5},
            "Jul": {"avg_temp_c": 24.0, "min_temp_c": 19.5, "max_temp_c": 28.5, "rainfall_mm": 385, "humidity_pct": 86, "rainy_days": 20, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 23.5, "min_temp_c": 19.0, "max_temp_c": 28.0, "rainfall_mm": 365, "humidity_pct": 87, "rainy_days": 19, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 22.5, "min_temp_c": 17.0, "max_temp_c": 28.0, "rainfall_mm": 195, "humidity_pct": 78, "rainy_days": 12, "sun_hours": 7.0},
            "Oct": {"avg_temp_c": 17.5, "min_temp_c": 11.0, "max_temp_c": 24.0, "rainfall_mm": 45, "humidity_pct": 58, "rainy_days": 3, "sun_hours": 9.0},
            "Nov": {"avg_temp_c": 12.5, "min_temp_c": 6.0, "max_temp_c": 19.0, "rainfall_mm": 12, "humidity_pct": 55, "rainy_days": 1, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 8.5, "min_temp_c": 2.5, "max_temp_c": 14.5, "rainfall_mm": 32, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 7.0}
        }
    },
    "West Bengal": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1752,
        "months": {
            "Jan": {"avg_temp_c": 18.5, "min_temp_c": 12.0, "max_temp_c": 25.0, "rainfall_mm": 15, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 22.0, "min_temp_c": 15.5, "max_temp_c": 28.5, "rainfall_mm": 25, "humidity_pct": 62, "rainy_days": 2, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 27.0, "min_temp_c": 20.5, "max_temp_c": 33.5, "rainfall_mm": 32, "humidity_pct": 55, "rainy_days": 3, "sun_hours": 8.5},
            "Apr": {"avg_temp_c": 30.0, "min_temp_c": 24.0, "max_temp_c": 36.0, "rainfall_mm": 55, "humidity_pct": 62, "rainy_days": 5, "sun_hours": 8.5},
            "May": {"avg_temp_c": 30.5, "min_temp_c": 25.0, "max_temp_c": 36.0, "rainfall_mm": 108, "humidity_pct": 72, "rainy_days": 8, "sun_hours": 7.5},
            "Jun": {"avg_temp_c": 29.5, "min_temp_c": 25.5, "max_temp_c": 33.5, "rainfall_mm": 265, "humidity_pct": 82, "rainy_days": 16, "sun_hours": 5.5},
            "Jul": {"avg_temp_c": 28.5, "min_temp_c": 25.5, "max_temp_c": 31.5, "rainfall_mm": 355, "humidity_pct": 86, "rainy_days": 20, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 28.5, "min_temp_c": 25.5, "max_temp_c": 31.5, "rainfall_mm": 332, "humidity_pct": 86, "rainy_days": 19, "sun_hours": 4.8},
            "Sep": {"avg_temp_c": 28.5, "min_temp_c": 24.5, "max_temp_c": 32.5, "rainfall_mm": 275, "humidity_pct": 83, "rainy_days": 14, "sun_hours": 6.0},
            "Oct": {"avg_temp_c": 27.0, "min_temp_c": 22.0, "max_temp_c": 32.0, "rainfall_mm": 128, "humidity_pct": 76, "rainy_days": 7, "sun_hours": 7.5},
            "Nov": {"avg_temp_c": 23.0, "min_temp_c": 17.0, "max_temp_c": 29.0, "rainfall_mm": 22, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 19.0, "min_temp_c": 12.5, "max_temp_c": 25.5, "rainfall_mm": 8, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 7.5}
        }
    },
    # ======================================================================
    # 8 UNION TERRITORIES
    # ======================================================================
    "Andaman and Nicobar Island": {
        "data_period": "1991-2021", "annual_rainfall_mm": 3050,
        "months": {
            "Jan": {"avg_temp_c": 26.0, "min_temp_c": 23.0, "max_temp_c": 29.0, "rainfall_mm": 42, "humidity_pct": 78, "rainy_days": 4, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": 26.5, "min_temp_c": 23.0, "max_temp_c": 30.0, "rainfall_mm": 18, "humidity_pct": 75, "rainy_days": 2, "sun_hours": 8.5},
            "Mar": {"avg_temp_c": 27.5, "min_temp_c": 24.0, "max_temp_c": 31.0, "rainfall_mm": 22, "humidity_pct": 76, "rainy_days": 2, "sun_hours": 9.0},
            "Apr": {"avg_temp_c": 28.5, "min_temp_c": 25.0, "max_temp_c": 32.0, "rainfall_mm": 78, "humidity_pct": 78, "rainy_days": 6, "sun_hours": 8.5},
            "May": {"avg_temp_c": 28.5, "min_temp_c": 25.5, "max_temp_c": 31.5, "rainfall_mm": 345, "humidity_pct": 82, "rainy_days": 17, "sun_hours": 6.5},
            "Jun": {"avg_temp_c": 27.5, "min_temp_c": 24.5, "max_temp_c": 30.5, "rainfall_mm": 415, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 4.5},
            "Jul": {"avg_temp_c": 27.0, "min_temp_c": 24.0, "max_temp_c": 30.0, "rainfall_mm": 425, "humidity_pct": 87, "rainy_days": 22, "sun_hours": 4.0},
            "Aug": {"avg_temp_c": 27.0, "min_temp_c": 24.0, "max_temp_c": 30.0, "rainfall_mm": 405, "humidity_pct": 86, "rainy_days": 21, "sun_hours": 4.5},
            "Sep": {"avg_temp_c": 27.0, "min_temp_c": 24.0, "max_temp_c": 30.0, "rainfall_mm": 385, "humidity_pct": 85, "rainy_days": 19, "sun_hours": 5.5},
            "Oct": {"avg_temp_c": 27.0, "min_temp_c": 24.0, "max_temp_c": 30.0, "rainfall_mm": 305, "humidity_pct": 84, "rainy_days": 16, "sun_hours": 6.5},
            "Nov": {"avg_temp_c": 27.0, "min_temp_c": 24.0, "max_temp_c": 30.0, "rainfall_mm": 285, "humidity_pct": 82, "rainy_days": 14, "sun_hours": 6.5},
            "Dec": {"avg_temp_c": 26.5, "min_temp_c": 23.5, "max_temp_c": 29.5, "rainfall_mm": 175, "humidity_pct": 80, "rainy_days": 9, "sun_hours": 7.0}
        }
    },
    "Chandigarh": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1107,
        "months": {
            "Jan": {"avg_temp_c": 12.0, "min_temp_c": 5.5, "max_temp_c": 18.5, "rainfall_mm": 32, "humidity_pct": 72, "rainy_days": 3, "sun_hours": 7.0},
            "Feb": {"avg_temp_c": 14.5, "min_temp_c": 7.5, "max_temp_c": 21.5, "rainfall_mm": 35, "humidity_pct": 65, "rainy_days": 4, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": 20.0, "min_temp_c": 12.5, "max_temp_c": 27.5, "rainfall_mm": 28, "humidity_pct": 50, "rainy_days": 3, "sun_hours": 9.0},
            "Apr": {"avg_temp_c": 27.5, "min_temp_c": 19.0, "max_temp_c": 36.0, "rainfall_mm": 15, "humidity_pct": 32, "rainy_days": 2, "sun_hours": 10.0},
            "May": {"avg_temp_c": 32.5, "min_temp_c": 24.0, "max_temp_c": 41.0, "rainfall_mm": 22, "humidity_pct": 30, "rainy_days": 3, "sun_hours": 10.5},
            "Jun": {"avg_temp_c": 33.5, "min_temp_c": 26.5, "max_temp_c": 40.5, "rainfall_mm": 85, "humidity_pct": 52, "rainy_days": 7, "sun_hours": 9.0},
            "Jul": {"avg_temp_c": 30.5, "min_temp_c": 25.5, "max_temp_c": 35.5, "rainfall_mm": 285, "humidity_pct": 78, "rainy_days": 15, "sun_hours": 6.5},
            "Aug": {"avg_temp_c": 29.5, "min_temp_c": 24.5, "max_temp_c": 34.5, "rainfall_mm": 275, "humidity_pct": 80, "rainy_days": 14, "sun_hours": 7.0},
            "Sep": {"avg_temp_c": 28.5, "min_temp_c": 22.5, "max_temp_c": 34.5, "rainfall_mm": 115, "humidity_pct": 68, "rainy_days": 7, "sun_hours": 8.5},
            "Oct": {"avg_temp_c": 24.0, "min_temp_c": 16.5, "max_temp_c": 31.5, "rainfall_mm": 18, "humidity_pct": 52, "rainy_days": 1, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": 18.0, "min_temp_c": 10.0, "max_temp_c": 26.0, "rainfall_mm": 8, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 8.0},
            "Dec": {"avg_temp_c": 13.0, "min_temp_c": 5.5, "max_temp_c": 20.5, "rainfall_mm": 18, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 7.0}
        }
    },
    "Dadra & Nagar Haveli and Daman & Diu": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1825,
        "months": {
            "Jan": {"avg_temp_c": 23.5, "min_temp_c": 15.5, "max_temp_c": 31.5, "rainfall_mm": 0, "humidity_pct": 52, "rainy_days": 0, "sun_hours": 9.5},
            "Feb": {"avg_temp_c": 25.0, "min_temp_c": 17.0, "max_temp_c": 33.0, "rainfall_mm": 0, "humidity_pct": 48, "rainy_days": 0, "sun_hours": 10.0},
            "Mar": {"avg_temp_c": 28.0, "min_temp_c": 21.0, "max_temp_c": 35.0, "rainfall_mm": 2, "humidity_pct": 52, "rainy_days": 0, "sun_hours": 10.2},
            "Apr": {"avg_temp_c": 30.0, "min_temp_c": 24.0, "max_temp_c": 36.0, "rainfall_mm": 5, "humidity_pct": 62, "rainy_days": 0, "sun_hours": 10.0},
            "May": {"avg_temp_c": 31.0, "min_temp_c": 26.0, "max_temp_c": 36.0, "rainfall_mm": 18, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 9.5},
            "Jun": {"avg_temp_c": 29.5, "min_temp_c": 25.5, "max_temp_c": 33.5, "rainfall_mm": 385, "humidity_pct": 85, "rainy_days": 18, "sun_hours": 4.5},
            "Jul": {"avg_temp_c": 28.0, "min_temp_c": 25.0, "max_temp_c": 31.0, "rainfall_mm": 485, "humidity_pct": 90, "rainy_days": 22, "sun_hours": 3.0},
            "Aug": {"avg_temp_c": 27.5, "min_temp_c": 24.5, "max_temp_c": 30.5, "rainfall_mm": 365, "humidity_pct": 88, "rainy_days": 19, "sun_hours": 3.5},
            "Sep": {"avg_temp_c": 28.0, "min_temp_c": 24.0, "max_temp_c": 32.0, "rainfall_mm": 225, "humidity_pct": 82, "rainy_days": 12, "sun_hours": 6.0},
            "Oct": {"avg_temp_c": 28.5, "min_temp_c": 22.5, "max_temp_c": 34.5, "rainfall_mm": 45, "humidity_pct": 68, "rainy_days": 3, "sun_hours": 8.5},
            "Nov": {"avg_temp_c": 26.0, "min_temp_c": 19.0, "max_temp_c": 33.0, "rainfall_mm": 15, "humidity_pct": 58, "rainy_days": 1, "sun_hours": 9.0},
            "Dec": {"avg_temp_c": 24.0, "min_temp_c": 16.0, "max_temp_c": 32.0, "rainfall_mm": 5, "humidity_pct": 55, "rainy_days": 0, "sun_hours": 9.2}
        }
    },
    "Delhi": {
        "data_period": "1991-2021", "annual_rainfall_mm": 797,
        "months": {
            "Jan": {"avg_temp_c": 13.4, "min_temp_c": 7.5, "max_temp_c": 19.8, "rainfall_mm": 25, "humidity_pct": 68, "rainy_days": 2, "sun_hours": 8.1},
            "Feb": {"avg_temp_c": 16.8, "min_temp_c": 10.4, "max_temp_c": 23.4, "rainfall_mm": 37, "humidity_pct": 62, "rainy_days": 3, "sun_hours": 9.3},
            "Mar": {"avg_temp_c": 22.4, "min_temp_c": 15.1, "max_temp_c": 29.7, "rainfall_mm": 22, "humidity_pct": 48, "rainy_days": 3, "sun_hours": 10.6},
            "Apr": {"avg_temp_c": 29.1, "min_temp_c": 20.8, "max_temp_c": 36.6, "rainfall_mm": 15, "humidity_pct": 29, "rainy_days": 2, "sun_hours": 11.5},
            "May": {"avg_temp_c": 32.7, "min_temp_c": 25.2, "max_temp_c": 39.5, "rainfall_mm": 19, "humidity_pct": 32, "rainy_days": 4, "sun_hours": 12.1},
            "Jun": {"avg_temp_c": 32.9, "min_temp_c": 27.5, "max_temp_c": 38.1, "rainfall_mm": 74, "humidity_pct": 47, "rainy_days": 8, "sun_hours": 11.7},
            "Jul": {"avg_temp_c": 29.9, "min_temp_c": 26.7, "max_temp_c": 33.6, "rainfall_mm": 205, "humidity_pct": 72, "rainy_days": 15, "sun_hours": 9.5},
            "Aug": {"avg_temp_c": 28.8, "min_temp_c": 25.9, "max_temp_c": 32.4, "rainfall_mm": 182, "humidity_pct": 77, "rainy_days": 15, "sun_hours": 9.1},
            "Sep": {"avg_temp_c": 27.9, "min_temp_c": 24.0, "max_temp_c": 32.3, "rainfall_mm": 105, "humidity_pct": 72, "rainy_days": 8, "sun_hours": 9.2},
            "Oct": {"avg_temp_c": 25.5, "min_temp_c": 19.2, "max_temp_c": 31.9, "rainfall_mm": 14, "humidity_pct": 55, "rainy_days": 2, "sun_hours": 10.1},
            "Nov": {"avg_temp_c": 20.5, "min_temp_c": 14.1, "max_temp_c": 27.3, "rainfall_mm": 5, "humidity_pct": 54, "rainy_days": 1, "sun_hours": 9.5},
            "Dec": {"avg_temp_c": 15.3, "min_temp_c": 9.1, "max_temp_c": 22.1, "rainfall_mm": 8, "humidity_pct": 62, "rainy_days": 1, "sun_hours": 8.7}
        }
    },
    "Jammu and Kashmir": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1125,
        "months": {
            "Jan": {"avg_temp_c": 2.5, "min_temp_c": -3.0, "max_temp_c": 8.0, "rainfall_mm": 65, "humidity_pct": 72, "rainy_days": 6, "sun_hours": 5.5},
            "Feb": {"avg_temp_c": 4.5, "min_temp_c": -1.0, "max_temp_c": 10.0, "rainfall_mm": 72, "humidity_pct": 70, "rainy_days": 7, "sun_hours": 6.0},
            "Mar": {"avg_temp_c": 10.0, "min_temp_c": 4.0, "max_temp_c": 16.0, "rainfall_mm": 85, "humidity_pct": 62, "rainy_days": 8, "sun_hours": 7.5},
            "Apr": {"avg_temp_c": 15.0, "min_temp_c": 8.5, "max_temp_c": 21.5, "rainfall_mm": 72, "humidity_pct": 55, "rainy_days": 7, "sun_hours": 8.5},
            "May": {"avg_temp_c": 20.0, "min_temp_c": 13.0, "max_temp_c": 27.0, "rainfall_mm": 52, "humidity_pct": 48, "rainy_days": 5, "sun_hours": 9.5},
            "Jun": {"avg_temp_c": 24.5, "min_temp_c": 17.5, "max_temp_c": 31.5, "rainfall_mm": 42, "humidity_pct": 45, "rainy_days": 5, "sun_hours": 10.0},
            "Jul": {"avg_temp_c": 25.5, "min_temp_c": 20.0, "max_temp_c": 31.0, "rainfall_mm": 145, "humidity_pct": 72, "rainy_days": 12, "sun_hours": 7.5},
            "Aug": {"avg_temp_c": 24.5, "min_temp_c": 19.5, "max_temp_c": 29.5, "rainfall_mm": 162, "humidity_pct": 76, "rainy_days": 13, "sun_hours": 7.0},
            "Sep": {"avg_temp_c": 21.0, "min_temp_c": 15.0, "max_temp_c": 27.0, "rainfall_mm": 82, "humidity_pct": 65, "rainy_days": 7, "sun_hours": 8.5},
            "Oct": {"avg_temp_c": 14.5, "min_temp_c": 8.0, "max_temp_c": 21.0, "rainfall_mm": 35, "humidity_pct": 55, "rainy_days": 3, "sun_hours": 9.0},
            "Nov": {"avg_temp_c": 8.5, "min_temp_c": 2.5, "max_temp_c": 14.5, "rainfall_mm": 22, "humidity_pct": 58, "rainy_days": 2, "sun_hours": 7.5},
            "Dec": {"avg_temp_c": 4.0, "min_temp_c": -1.5, "max_temp_c": 9.5, "rainfall_mm": 42, "humidity_pct": 68, "rainy_days": 4, "sun_hours": 5.5}
        }
    },
    "Ladakh": {
        "data_period": "1991-2021", "annual_rainfall_mm": 102,
        "months": {
            "Jan": {"avg_temp_c": -12.0, "min_temp_c": -18.0, "max_temp_c": -6.0, "rainfall_mm": 8, "humidity_pct": 38, "rainy_days": 2, "sun_hours": 7.5},
            "Feb": {"avg_temp_c": -9.0, "min_temp_c": -15.0, "max_temp_c": -3.0, "rainfall_mm": 8, "humidity_pct": 38, "rainy_days": 2, "sun_hours": 8.0},
            "Mar": {"avg_temp_c": -2.0, "min_temp_c": -8.0, "max_temp_c": 4.0, "rainfall_mm": 8, "humidity_pct": 35, "rainy_days": 2, "sun_hours": 9.0},
            "Apr": {"avg_temp_c": 5.0, "min_temp_c": -2.0, "max_temp_c": 12.0, "rainfall_mm": 5, "humidity_pct": 28, "rainy_days": 1, "sun_hours": 10.0},
            "May": {"avg_temp_c": 10.5, "min_temp_c": 3.0, "max_temp_c": 18.0, "rainfall_mm": 5, "humidity_pct": 25, "rainy_days": 1, "sun_hours": 10.5},
            "Jun": {"avg_temp_c": 15.0, "min_temp_c": 8.0, "max_temp_c": 22.0, "rainfall_mm": 5, "humidity_pct": 25, "rainy_days": 1, "sun_hours": 11.0},
            "Jul": {"avg_temp_c": 18.0, "min_temp_c": 12.0, "max_temp_c": 24.0, "rainfall_mm": 18, "humidity_pct": 42, "rainy_days": 3, "sun_hours": 10.0},
            "Aug": {"avg_temp_c": 17.5, "min_temp_c": 11.5, "max_temp_c": 23.5, "rainfall_mm": 15, "humidity_pct": 45, "rainy_days": 3, "sun_hours": 10.0},
            "Sep": {"avg_temp_c": 12.5, "min_temp_c": 6.0, "max_temp_c": 19.0, "rainfall_mm": 8, "humidity_pct": 35, "rainy_days": 1, "sun_hours": 10.0},
            "Oct": {"avg_temp_c": 5.0, "min_temp_c": -2.0, "max_temp_c": 12.0, "rainfall_mm": 5, "humidity_pct": 30, "rainy_days": 1, "sun_hours": 9.5},
            "Nov": {"avg_temp_c": -3.0, "min_temp_c": -10.0, "max_temp_c": 4.0, "rainfall_mm": 5, "humidity_pct": 32, "rainy_days": 1, "sun_hours": 8.5},
            "Dec": {"avg_temp_c": -9.0, "min_temp_c": -15.0, "max_temp_c": -3.0, "rainfall_mm": 8, "humidity_pct": 38, "rainy_days": 2, "sun_hours": 7.5}
        }
    },
    "Lakshadweep": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1640,
        "months": {
            "Jan": {"avg_temp_c": 27.5, "min_temp_c": 25.0, "max_temp_c": 30.0, "rainfall_mm": 22, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 28.0, "min_temp_c": 25.5, "max_temp_c": 30.5, "rainfall_mm": 12, "humidity_pct": 70, "rainy_days": 1, "sun_hours": 9.0},
            "Mar": {"avg_temp_c": 29.0, "min_temp_c": 26.5, "max_temp_c": 31.5, "rainfall_mm": 15, "humidity_pct": 72, "rainy_days": 1, "sun_hours": 9.5},
            "Apr": {"avg_temp_c": 29.5, "min_temp_c": 27.0, "max_temp_c": 32.0, "rainfall_mm": 48, "humidity_pct": 75, "rainy_days": 5, "sun_hours": 9.0},
            "May": {"avg_temp_c": 29.0, "min_temp_c": 26.5, "max_temp_c": 31.5, "rainfall_mm": 185, "humidity_pct": 82, "rainy_days": 12, "sun_hours": 7.0},
            "Jun": {"avg_temp_c": 27.5, "min_temp_c": 25.0, "max_temp_c": 30.0, "rainfall_mm": 325, "humidity_pct": 88, "rainy_days": 20, "sun_hours": 4.5},
            "Jul": {"avg_temp_c": 27.0, "min_temp_c": 24.5, "max_temp_c": 29.5, "rainfall_mm": 285, "humidity_pct": 88, "rainy_days": 19, "sun_hours": 4.5},
            "Aug": {"avg_temp_c": 27.0, "min_temp_c": 24.5, "max_temp_c": 29.5, "rainfall_mm": 225, "humidity_pct": 86, "rainy_days": 16, "sun_hours": 5.0},
            "Sep": {"avg_temp_c": 27.5, "min_temp_c": 24.5, "max_temp_c": 30.5, "rainfall_mm": 185, "humidity_pct": 84, "rainy_days": 13, "sun_hours": 6.5},
            "Oct": {"avg_temp_c": 28.0, "min_temp_c": 25.0, "max_temp_c": 31.0, "rainfall_mm": 165, "humidity_pct": 82, "rainy_days": 11, "sun_hours": 7.0},
            "Nov": {"avg_temp_c": 28.0, "min_temp_c": 25.0, "max_temp_c": 31.0, "rainfall_mm": 115, "humidity_pct": 78, "rainy_days": 8, "sun_hours": 7.5},
            "Dec": {"avg_temp_c": 27.5, "min_temp_c": 25.0, "max_temp_c": 30.0, "rainfall_mm": 52, "humidity_pct": 75, "rainy_days": 4, "sun_hours": 8.0}
        }
    },
    "Puducherry": {
        "data_period": "1991-2021", "annual_rainfall_mm": 1272,
        "months": {
            "Jan": {"avg_temp_c": 25.0, "min_temp_c": 21.0, "max_temp_c": 29.0, "rainfall_mm": 25, "humidity_pct": 72, "rainy_days": 2, "sun_hours": 8.5},
            "Feb": {"avg_temp_c": 26.0, "min_temp_c": 21.5, "max_temp_c": 30.5, "rainfall_mm": 12, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 9.5},
            "Mar": {"avg_temp_c": 28.5, "min_temp_c": 24.0, "max_temp_c": 33.0, "rainfall_mm": 8, "humidity_pct": 68, "rainy_days": 1, "sun_hours": 10.0},
            "Apr": {"avg_temp_c": 31.0, "min_temp_c": 26.5, "max_temp_c": 35.5, "rainfall_mm": 15, "humidity_pct": 70, "rainy_days": 2, "sun_hours": 10.0},
            "May": {"avg_temp_c": 33.0, "min_temp_c": 28.0, "max_temp_c": 38.0, "rainfall_mm": 32, "humidity_pct": 65, "rainy_days": 3, "sun_hours": 9.5},
            "Jun": {"avg_temp_c": 32.5, "min_temp_c": 27.0, "max_temp_c": 38.0, "rainfall_mm": 38, "humidity_pct": 58, "rainy_days": 3, "sun_hours": 9.0},
            "Jul": {"avg_temp_c": 31.0, "min_temp_c": 26.0, "max_temp_c": 36.0, "rainfall_mm": 48, "humidity_pct": 62, "rainy_days": 4, "sun_hours": 8.0},
            "Aug": {"avg_temp_c": 31.0, "min_temp_c": 25.5, "max_temp_c": 36.5, "rainfall_mm": 85, "humidity_pct": 68, "rainy_days": 7, "sun_hours": 7.5},
            "Sep": {"avg_temp_c": 30.0, "min_temp_c": 25.0, "max_temp_c": 35.0, "rainfall_mm": 125, "humidity_pct": 75, "rainy_days": 9, "sun_hours": 7.5},
            "Oct": {"avg_temp_c": 28.5, "min_temp_c": 24.0, "max_temp_c": 33.0, "rainfall_mm": 235, "humidity_pct": 80, "rainy_days": 13, "sun_hours": 7.0},
            "Nov": {"avg_temp_c": 26.5, "min_temp_c": 22.5, "max_temp_c": 30.5, "rainfall_mm": 345, "humidity_pct": 82, "rainy_days": 15, "sun_hours": 7.0},
            "Dec": {"avg_temp_c": 25.0, "min_temp_c": 21.0, "max_temp_c": 29.0, "rainfall_mm": 165, "humidity_pct": 78, "rainy_days": 9, "sun_hours": 7.5}
        }
    }
}

def build_and_save():
    """Save the complete climatology database to JSON."""
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "data", "processed", "state_climatology_from_pdfs.json"
    )
    output_path = os.path.normpath(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(CLIMATOLOGY_DB, f, indent=2, ensure_ascii=False)

    n_states = len(CLIMATOLOGY_DB)
    total_rain = sum(d["annual_rainfall_mm"] for d in CLIMATOLOGY_DB.values())
    print(f"Built climatology database: {n_states} states/UTs")
    print(f"Average annual rainfall: {total_rain / n_states:.0f} mm")
    print(f"Saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    build_and_save()
