# VitalPlunder ☠️

> **Plunder Health Risks Before They Plunder You!**

A modular, scalable, AI-powered Personal Well-Being platform with a pirate theme. Built with Flask (Python) backend and React (Vite) frontend.

---

## 🏴‍☠️ Overview

VitalPlunder is a comprehensive health and wellness tracking platform featuring 7 specialized modules:

| Module | Pirate Name | Description |
|--------|-------------|-------------|
| Health Risk Scanner | **Storm Watch** | ML-based health risk prediction using vitals |
| Mental Health Monitor | **Mind Compass** | NLP sentiment analysis for mood tracking |
| Lifestyle Coaching | **Captain's Orders** | Lifestyle clustering and recommendations |
| Medication Tracker | **Supply Check** | Medication adherence monitoring |
| Sleep Quality | **Night Watch** | Sleep pattern analysis and scoring |
| Diet & Nutrition | **Galley Log** | Food image recognition and nutrition mapping |
| Medical Documents | **Ship Doctor** | AI-powered medical document analysis |

---

## 📁 Project Structure

```
vitalplunder/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── modules/
│       ├── storm_watch/      # Health Risk Module
│       │   ├── train_model.py
│       │   ├── predict.py
│       │   └── routes.py
│       ├── mind_compass/     # Mental Health Module
│       │   ├── sentiment_model.py
│       │   ├── stress_predictor.py
│       │   └── routes.py
│       ├── captains_orders/  # Lifestyle Module
│       │   ├── lifestyle_model.py
│       │   ├── lifestyle_rules.py
│       │   └── routes.py
│       ├── supply_check/     # Medication Module
│       │   ├── medication_model.py
│       │   ├── adherence_predictor.py
│       │   └── routes.py
│       ├── night_watch/      # Sleep Module
│       │   ├── sleep_model.py
│       │   ├── sleep_analyzer.py
│       │   └── routes.py
│       ├── galley_log/       # Diet Module
│       │   ├── food_classifier.py
│       │   ├── nutrition_mapper.py
│       │   └── routes.py
│       └── ship_doctor/      # Medical Docs Module
│           ├── document_parser.py
│           ├── gemini_analyzer.py
│           └── routes.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── services/
│       │   └── api.js        # Axios API service
│       ├── components/
│       │   └── Layout.jsx    # Main layout with sidebar
│       └── pages/
│           ├── Dashboard.jsx
│           ├── StormWatch.jsx
│           ├── MindCompass.jsx
│           ├── CaptainsOrders.jsx
│           ├── SupplyCheck.jsx
│           ├── NightWatch.jsx
│           ├── GalleyLog.jsx
│           └── ShipDoctor.jsx
└── datasets/
    ├── health_risk_sample.csv
    ├── stress_mood_sample.csv
    └── nutrition_data.json
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd vitalplunder/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys (optional for Ship Doctor module)
# GEMINI_API_KEY=your_key_here

# Run the server
python app.py
```

Backend runs at: `http://localhost:5000`

### Frontend Setup

```bash
cd vitalplunder/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🔌 API Endpoints

### Storm Watch (Health Risk)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/storm-watch/predict` | Predict health risk |
| POST | `/api/storm-watch/train` | Train model with data |
| GET | `/api/storm-watch/health` | Module health check |

### Mind Compass (Mental Health)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mind-compass/analyze` | Analyze mood/sentiment |
| POST | `/api/mind-compass/log` | Log mood entry |
| GET | `/api/mind-compass/history` | Get mood history |

### Captain's Orders (Lifestyle)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/captains-orders/analyze` | Analyze lifestyle |
| POST | `/api/captains-orders/goals` | Set lifestyle goals |
| GET | `/api/captains-orders/recommendations` | Get recommendations |

### Supply Check (Medication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/supply-check/medications` | List medications |
| POST | `/api/supply-check/medications` | Add medication |
| POST | `/api/supply-check/log` | Log dose taken |
| GET | `/api/supply-check/adherence` | Get adherence stats |

### Night Watch (Sleep)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/night-watch/log` | Log sleep entry |
| POST | `/api/night-watch/analyze` | Analyze sleep quality |
| GET | `/api/night-watch/history` | Get sleep history |

### Galley Log (Diet)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/galley-log/analyze` | Analyze food image |
| POST | `/api/galley-log/log` | Log meal manually |
| GET | `/api/galley-log/nutrition/{food}` | Get nutrition info |
| GET | `/api/galley-log/daily-summary` | Daily nutrition summary |

### Ship Doctor (Medical Docs)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ship-doctor/analyze` | Analyze medical document |
| POST | `/api/ship-doctor/extract-text` | Extract text from document |
| GET | `/api/ship-doctor/documents` | List uploaded documents |

---

## 🤖 ML Models

| Module | Algorithm | Purpose |
|--------|-----------|---------|
| Storm Watch | Random Forest Classifier | Health risk prediction |
| Mind Compass | TextBlob + NLTK | Sentiment analysis |
| Captain's Orders | KMeans Clustering | Lifestyle profiling |
| Supply Check | Gradient Boosting | Adherence prediction |
| Night Watch | Random Forest Regressor | Sleep quality scoring |
| Galley Log | CNN (placeholder) | Food image classification |
| Ship Doctor | Google Gemini API | Document understanding |

---

## 🎨 Tech Stack

### Backend
- **Framework:** Flask 3.0
- **ML:** scikit-learn, TextBlob, NLTK
- **OCR:** pytesseract, PyPDF2
- **AI:** Google Generative AI (Gemini)
- **Image:** Pillow

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **Routing:** React Router DOM
- **HTTP Client:** Axios
- **Charts:** Recharts
- **Icons:** Lucide React

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend folder:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key  # Optional, for Ship Doctor
```

### Training Models

Models can be trained using the sample datasets:

```bash
cd backend

# Train health risk model
python -c "from modules.storm_watch.train_model import HealthRiskModelTrainer; t = HealthRiskModelTrainer(); t.train('../datasets/health_risk_sample.csv')"

# Train lifestyle model
python -c "from modules.captains_orders.lifestyle_model import LifestyleModelTrainer; t = LifestyleModelTrainer(); t.train('../datasets/health_risk_sample.csv')"
```

---

## 📋 TODO / Future Enhancements

- [ ] User authentication (JWT)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Real food image classification model
- [ ] Wearable device integration
- [ ] Push notifications for medication reminders
- [ ] Data export (PDF reports)
- [ ] Multi-language support
- [ ] Dark/Light theme toggle
- [ ] Mobile app (React Native)

---

## ⚠️ Medical Disclaimer

**IMPORTANT:** VitalPlunder is designed for **informational and educational purposes only**. It is NOT intended to be a substitute for professional medical advice, diagnosis, or treatment.

- Always seek the advice of your physician or qualified health provider
- Never disregard professional medical advice because of something from this application
- If you think you may have a medical emergency, call your doctor or emergency services immediately

The health predictions, risk assessments, and recommendations provided by this platform are based on machine learning algorithms and should not be considered as medical diagnoses.

---

## 👥 Team

VitalPlunder is designed for development by a team of 3:
- **Developer 1:** Backend & ML (Storm Watch, Mind Compass, Captain's Orders)
- **Developer 2:** Backend & ML (Supply Check, Night Watch, Galley Log, Ship Doctor)
- **Developer 3:** Frontend & Integration

---

## 📄 License

MIT License - See LICENSE file for details.

---

<p align="center">
  <strong>⚓ Sail towards better health with VitalPlunder! ☠️</strong>
</p>
