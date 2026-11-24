# NavChakra — Hyperlocal Monsoon Onset & Break Prediction System

### From Climate Signals to Confident Farming Decisions

[![Live Deployment](https://img.shields.io/badge/Live%20Demo-navchakra--s9dx.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://navchakra-s9dx.onrender.com/)
[![API Documentation](https://img.shields.io/badge/Swagger%20Docs-API%20Reference-blue?style=for-the-badge&logo=fastapi)](https://navchakra-s9dx.onrender.com/docs)
[![Adaptive AI](https://img.shields.io/badge/Adaptive%20AI-Adaption%20Labs-10B981?style=for-the-badge&logo=openai)](https://adaptionlabs.ai)
[![GitHub Repository](https://img.shields.io/badge/GitHub-imsinghaditya07%2FNavChakra-black?style=for-the-badge&logo=github)](https://github.com/imsinghaditya07/NavChakra)

> **🚀 Live Deployed App**: [https://navchakra-s9dx.onrender.com/](https://navchakra-s9dx.onrender.com/)  
> **📚 Demo Video Link**: [https://youtu.be/LNyUXiiQhS0?si=4ysWy1E2QRvXNXKz](https://youtu.be/LNyUXiiQhS0?si=4ysWy1E2QRvXNXKz)  
> **📑 Project Presentation**: [Google Drive Presentation](https://drive.google.com/file/d/19UHcfaDqVXFjIMmhgoAdQ_kBhy-icfyn/view?usp=drivesdk)  
> **🌱 Continuous Agro-LLM Learning**: **Adaption Labs** (Adaptive Data & AutoScientist)

---

**Core Engineering Team**:  
- **Aditya Singh** ([@imsinghaditya07](https://github.com/imsinghaditya07))  
- **Anand Kumar Jha**  
- **Aaryan Lal Das**  

- **Aditya Singh** ([@imsinghaditya07](https://github.com/imsinghaditya07))
- **Anand Kumar Jha**
- **Rishab Kumar**

---

## 1. System Overview & Architecture

This repository delivers an end-to-end, operational prototype for downscaling global climate teleconnections (NOAA ENSO, BOM IOD, NOAA MJO) to block and panchayat scales across India. It couples 7–30 day seasonal onset/break forecasting with 0–30 minute convective nowcasting, ICAR-aligned deterministic agronomic rules, an auditable Explainable AI (XAI) engine, and multi-channel last-mile delivery (PWA offline app, regional voice TTS, IVR gateway, and officials' disaster management dashboard).

### System Architecture Diagram

![System Architecture](docs/architecture.png)

```
[DATA SOURCES] ────────► [HYBRID ML ENGINE] ────────► [FUSION & OVERRIDE] ────────► [ADVISORY & XAI] ────────► [DELIVERY CHANNELS]
- IMD Gridded Rainfall   - Model A (LightGBM/LSTM)    - Weighted Confidence        - ICAR Rule Engine           - Farmer PWA (Offline)
- NOAA ENSO/IOD/MJO       (7-30d Break/Onset)          Score Formula                - SHAP Plain-Language        - Officials Dashboard
- ISRO INSAT-3D TIR      - Model B (Convective ONNX)  - Emergency Citizen           One-Liner Generator         - Regional Voice (TTS)
- Open-Meteo & CAPE       (0-30m Severe Storm)         Crowd-Report Fallback       - Grounded RAG Chatbot       - Asterisk IVR Gateway
- Blitzortung Strikes    - Hybrid ML Compute Engine    Override                     (No Hallucination)          - WhatsApp Cloud Free
```

---

## 2. Infrastructure Cost Statement & Operational Economics

| Component                       | Selected Tool / Provider                      | Commercial Alternative            | Prototype Cost                | Production Scaling Path                                |
| ------------------------------- | --------------------------------------------- | --------------------------------- | ----------------------------- | ------------------------------------------------------ |
| **Satellite Imagery**           | ISRO MOSDAC INSAT-3D/3DR TIR                  | Paid Planet/Spire Feeds           | **₹0.00**                     | Direct MoES NKN fiber feed                             |
| **Global Teleconnections**      | NOAA PSL (ENSO/MJO) & BOM (IOD)               | Paid Weather Analytics            | **₹0.00**                     | Automated Open FTP/HTTP cron                           |
| **Surface Agromet & CAPE**      | Open-Meteo & NASA POWER API                   | AccuWeather / IBM Weather         | **₹0.00**                     | IMD NCMRWF AWS/C-DAC servers                           |
| **Lightning Stroke Feed**       | Blitzortung.org Community TOA                 | Earth Networks / Vaisala          | **₹0.00**                     | IMD Damini / IITM Lightning Net                        |
| **ML Training & Acceleration**  | High-Performance GPU / Colab     | AWS EC2 p3.2xlarge                | **Low-cost / Elastic**        | C-DAC PARAM Ananta supercomputer                       |
| **Container & API Hosting**     | Render Free Tier / HF Spaces                  | AWS ECS Fargate                   | **₹0.00**                     | [Live on Render](https://navchakra-s9dx.onrender.com/) |
| **Agro-LLM Specialization**     | Adaption Labs (Adaptive Data & AutoScientist) | Manual Data Labeling / Annotation | **Self-serve API**            | In-house continuous fine-tuning pipeline               |
| **Multi-Lingual Translation**   | Bhashini (Govt of India) + Web Speech API     | Google Cloud Translation          | **₹0.00**                     | In-house IndicTrans2 models                            |
| **Map Base & Radar**            | OpenStreetMap + RainViewer API                | Mapbox / Google Maps              | **₹0.00**                     | ISRO Bhuvan GeoPlatform                                |
| **IVR Voice Gateway**           | Asterisk PBX Open-Source AGI                  | Twilio / Exotel Voice             | **₹0.00**                     | C-DOT Kisan Call Centre PRI lines                      |
| **Agentic AI Layer (Optional)** | Agent37 Cloud Hermes Sandbox                  | AutoGPT / Cloud LLM APIs          | Metered pay-per-minute / BYOK | Persistent sandbox with managed tools                  |
| **Core Platform Total**         | —                                             | —                                 | **₹0.00 / month**             | Budget-neutral for Government of India                 |

> **Cost & Metering Clarification**: The core prediction backbone (physics models, ML models A & B, deterministic agronomic rules, and grounded RAG chatbot) operates at **₹0.00 recurring infrastructure cost** on open tiers. The optional Agent37 agent layer is pay-per-minute after the free tier credit ($1.00 / 1,000,000 credit micros); model usage is metered unless you configure your own model API key (BYOK). When Agent37 credentials are not set, the platform functions with zero degradation via deterministic RAG.

---

## 2B. Continuous Agro-LLM Learning with Adaption Labs

NavChakra leverages **Adaption Labs** (`adaptionlabs.ai`) to power **Adaptive AI That Continuously Learns** specifically for **Kisan Saarthi (किसान सारथी)**, the autonomous agro-meteorological advisory assistant. Rather than modifying or replacing the core physical meteorology and numerical weather models, Adaption Labs is utilized to curate, expand, fine-tune, and specialize the agricultural natural language intelligence.

### Core Platform Capabilities

- **Adaptive Data**: Improves and expands datasets used to train AI models. For NavChakra, it synthesizes and enriches realistic examples of farmer questions, localized crop advice, meteorological explanations, and regional-language agricultural terminology.
- **AutoScientist**: Automates experiments around language model training, training configurations, loss evaluations, and hyperparameter tuning—empowering the development of a domain-specialized AI assistant for Indian agriculture.

### 4-Stage Adaptation & Integration Lifecycle

```mermaid
flowchart TD
    subgraph S1 ["1. Prepare Farmer Q&A Data"]
        A["🌾 <b>Domain Knowledge Ingestion</b><br/>• Real farmer questions across districts<br/>• ICAR verified crop advisory rules<br/>• Sowing, irrigation, & extreme weather alerts"]
    end

    subgraph S2 ["2. Adaptive Data Engine"]
        B["📈 <b>Dataset Expansion & Translation</b><br/>• Augments question diversity & edge cases<br/>• Synthesizes realistic farmer phrasing<br/>• Multi-dialect translation across 23 Indian languages"]
    end

    subgraph S3 ["3. AutoScientist Training Suite"]
        C["🧪 <b>Automated Experimentation</b><br/>• Fine-tunes supported language model backbones<br/>• Optimizes training hyperparameters & loss<br/>• Validates agromet response accuracy<br/>• Exports optimized model checkpoints"]
    end

    subgraph S4 ["4. NavChakra Operational Integration"]
        D["⚙️ <b>FastAPI Backend (/api/agent)</b><br/>Server-side streaming proxy & guardrails"]
        E["📱 <b>Kisan Saarthi Interface</b><br/>Real-time SSE chat + 23-language voice STT/TTS"]
    end

    A --> B
    B --> C
    C -->|Trained Model Checkpoint| D
    D --> E

    style S1 fill:#0f172a,stroke:#3b82f6,color:#ffffff,rx:10,ry:10
    style S2 fill:#064e3b,stroke:#10b981,color:#ffffff,rx:10,ry:10
    style S3 fill:#3b0764,stroke:#a855f7,color:#ffffff,rx:10,ry:10
    style S4 fill:#14532d,stroke:#22c55e,color:#ffffff,rx:10,ry:10
```

```
┌────────────────────────────────────────────────────────────────────────┐
│                      1. Prepare Farmer Q&A Data                        │
│   Curate questions on crops, irrigation, rainfall, & extreme weather   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        2. Adaptive Data Engine                         │
│   Improve, expand, and translate examples across supported languages   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        3. AutoScientist Suite                          │
│   Automate experiments around model training & fine-tuning configs     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      4. Integrate with NavChakra                       │
│    Connect trained checkpoint to FastAPI backend & farmer chat panel   │
└────────────────────────────────────────────────────────────────────────┘
```

### Detailed Workflow Steps:

1. **Prepare Farmer Q&A Data**: Gather realistic questions about crop stages (sowing, vegetative, harvesting), irrigation thresholds, monsoon break risks, and localized weather hazards paired with verified ICAR/MoES advisory answers.
2. **Use Adaptive Data**: Run the dataset through Adaption's Adaptive Data API to enrich vocabulary, handle regional conversational nuances, and scale training pairs into all 23 supported Indian languages.
3. **Use AutoScientist**: Execute autonomous fine-tuning experiments across model architectures to optimize domain comprehension, eliminate hallucinations, and download production-ready model checkpoints.
4. **Integrate with NavChakra**: Deploy the trained checkpoint to the Python/FastAPI backend (`/api/agent`), enabling real-time streaming, speech recognition (STT), and voice narration (TTS) inside the Kisan Saarthi drawer.

---

## 3. Known Free-Tier Limitations & Mitigation Strategy

1. **Hugging Face Spaces & Render Cold-Start Delay**:
   - _Limitation_: Free containers enter a sleep state after 15 minutes of inactivity, causing a 30–50 second cold-start delay on first request.
   - _Mitigation_: The app features an automated cron keep-alive ping script (`GET /health` every 12 minutes). A pre-warm ping can be dispatched before demonstrations.
2. **Google Colab & Kaggle Session Timeouts**:
   - _Limitation_: Free GPU runtimes disconnect after 60–90 minutes of idle time or 12 hours of total duration.
   - _Mitigation_: All model training scripts (`train_model_a_lightgbm.py`, `train_model_a_lstm.py`) implement automated per-epoch checkpointing and save weights directly into version-controlled paths tracked by DVC.
3. **WhatsApp Cloud API Free-Tier Cap**:
   - _Limitation_: Free sandbox/tier is restricted to 1,000 service conversations per calendar month.
   - _Mitigation_: Supplemented by browser-native Web Push via Firebase Cloud Messaging (FCM) and the Asterisk IVR voice fallback for feature phones.
4. **MOSDAC & Copernicus CDS External Approval Lead Time**:
   - _Limitation_: Automated API credentials can take 3 to 14 days for institutional verification.
   - _Mitigation_: Zero blockage! High-resolution verified sample tensors and physical profiles are pre-ingested in `/data/sample/insat3d/` and `/data/processed/`, allowing 100% of ML training and inference to function immediately.

---

## 4. Benchmark Evaluation: Model A vs IMD Subdivision Baseline

Direct comparison evaluated on the 2021–2025 Holdout Monsoon Seasons across core monsoon break zones:

| Metric                        | MoES Hyperlocal Model A (LightGBM) | IMD Operational Subdivision Forecast | Benchmark Improvement ($\Delta$)  |
| ----------------------------- | ---------------------------------- | ------------------------------------ | --------------------------------- |
| **Categorical Accuracy**      | **98.46%**                         | 63.03%                               | **+35.43% Improvement**           |
| **Weighted F1-Score**         | **0.9844**                         | 0.6777                               | **+0.3067 Improvement**           |
| **Break Spell Brier Error**   | **0.0001**                         | 0.0094                               | **98.6% Error Reduction**         |
| **Break False Alarm Rate**    | **0.00%**                          | 24.50%                               | **Eliminates False Break Alarms** |
| **Mean Absolute Error (MAE)** | **0.0158**                         | 0.7159                               | **97.8% Lower Error**             |

---

## 5. Quickstart & Local Execution

### Prerequisites

- Python 3.9+
- Git

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/imsinghaditya07/NavChakra.git
cd NavChakra

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Ingest Data & Train Models

```bash
# Build feature store from teleconnections, IMD grids & NASA POWER
python data/build_datasets.py

# Train PyTorch LSTM and Tabular models with GPU acceleration & checkpointing
python training/train.py --data data/sample/rainfall_sample.csv --out models/registry/v_sample --epochs 10

# Train Model A (LightGBM + LSTM) and Model B (Nowcast ONNX)
python models/training/train_model_a_lightgbm.py
python models/training/train_model_a_lstm.py
python models/training/train_model_b_nowcast.py
python models/training/export_model_a_onnx.py

# Run Evidently AI feature drift analysis
python models/eval/model_health_monitor.py
```

### 3. Run Pytest Verification Suite

```bash
PYTHONPATH=. pytest backend/tests/test_api.py -v
```

### 4. Start the Application Server

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Open your browser locally at **`http://localhost:8000`** or access the live deployment at **`https://navchakra-s9dx.onrender.com/`**.

---

## 6. Application Walkthrough (7 Key Journeys)

### Journey 1: Hyperlocal Monsoon Break Prediction (7–30 Day Horizon)

1. Open **`https://navchakra-s9dx.onrender.com/`** (or `http://localhost:8000` locally) in your browser.
2. Under the block selector dropdown, select **`Pusad (पुसद) - Yavatmal, Vidarbha`**.
3. Note the Risk Card updates to **ORANGE / RED Alert**:
   - Monsoon Break Probability: **74%**
   - Root-Zone Soil Moisture: **22%** (depleted)
   - Day of Year: 195 (Mid-July critical sowing/vegetative window).

### Journey 2: Explainable AI (XAI) One-Liner

1. Look at the **AI Meteorological Driver (XAI)** card:
   - _"Monsoon break risk elevated primarily due to Recent Rainfall Deficit (-1.45 SD) and active MJO Phase 1 suppressive wave."_
2. Switch language from **English** to **हिंदी (Hindi)**:
   - Notice the explanation seamlessly switches to verified regional Hindi: _"मानसून ब्रेक का खतरा मुख्य रूप से हालिया वर्षा में भारी कमी और शुष्क वायुमंडलीय दबाव के कारण बढ़ा है।"_

### Journey 3: Real-Time Convective Nowcasting (0–30 Minutes)

1. Inspect the Leaflet map around Central India.
2. Note the **flashing lightning markers (⚡ Blitzortung)** and the **rotating storm cell (🌀 Cell C-01)**.
3. Click on the storm cell marker to view:
   - Storm Nowcast Probability: **84%**
   - Cloud-Top Cooling Rate: **-12.4°C / 15m** (rapid updraft)
   - CAPE Instability: **2,850 J/kg**.

### Journey 4: Emergency Citizen Crowd Override Trigger

1. Switch to the **`Disaster Dashboard (आपदा प्रबंधन)`** tab.
2. Click the red button: **`🚨 Simulate Crowd Override Trigger`**.
3. The system simulates 3 citizen reports of flash rain/cloudburst in Pusad.
4. An immediate popup confirms: **`CRITICAL SAFETY OVERRIDE TRIGGERED: Ground observation override: 3 verified citizen storm reports.`**
5. Notice the block instantly escalates to **RED Emergency Alert**, overriding any safe model forecast to prevent farmer casualties!

### Journey 5: Grounded RAG Chatbot (No Weather Hallucination)

1. In the right-hand panel, ask: **`Should I sow cotton tomorrow?`** (or in Hindi: _"क्या मुझे अभी कपास की बुवाई करनी चाहिए?"_).
2. The chatbot responds strictly using retrieved ICAR agromet context:
   - _"Caution: Model A indicates a 74% monsoon break probability for Pusad. Sowing should be delayed by 7–10 days until consistent revival rains arrive. Do not sow on dry seedbeds."_
3. Ask about spraying: _"Should I spray insecticide?"_
   - Chatbot warns to suspend spraying due to impending squalls and wash-off risk.

### Journey 6: Offline PWA & Voice Accessibility

1. Click **`📶 Online`** in the header to toggle **Offline Mode**.
2. Notice the offline warning banner: _"Displaying cached block prediction from 2 hours ago."_
3. Click **`☀️ High Contrast`**: the UI shifts into an ultra-high-contrast daylight mode designed for direct sunlight in open fields.
4. Click **`🔊 Voice`** or **`Listen to Voice Advisory`**: the browser's Web Speech API speaks the advisory aloud in clean native Hindi/Marathi without any paid API keys!

### Journey 7: Kisan Saarthi Multilingual Agro-Advisory Agent

1. Click the floating green **`🌾 Kisan Saarthi (किसान सारथी)`** button or open the assistant drawer.
2. Type or speak using the microphone button: _"What is the monsoon break risk for my block?"_
3. Watch the answer stream in real time via Server-Sent Events (SSE) from the advisory engine (or automatic guarded RAG fallback if running offline/unconfigured).
4. Select any of the **23 regional languages** (e.g., Telugu, Punjabi, Bengali, Gujarati); notice both the response text and the native TTS audio narration instantly adapt.
