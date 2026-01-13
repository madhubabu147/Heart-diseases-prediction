# Heart Disease Prediction

> [!WARNING]
> **Not for Clinical Use.** This application is for research and demonstration purposes only.

This project predicts the likelihood of heart disease using machine learning.
The application includes a Flask backend, a modern responsive frontend, and a REST API.

## Features
- **Web Interface**: Interactive form with risk visualization.
- **Batch Processing**: Upload CSV files for bulk predictions.
- **API**: RESTful endpoints for integration.
- **Explainability**: Shows key influencing factors (generic).

## Setup

### Local generic
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Train model (if artifacts missing):
   ```bash
   python src/Heart/pipeline/Training_pipeline.py
   ```
3. Run application:
   ```bash
   python app.py
   ```
   Open [http://localhost:8080](http://localhost:8080).

### Docker
1. Build image:
   ```bash
   docker build -t heart-guard .
   ```
2. Run container:
   ```bash
   docker run -p 5000:5000 heart-guard
   ```

## API Usage

### Single Prediction
`POST /api/predict`
```json
{
  "age": 45, "sex": 1, "cp": 0, "trestbps": 120, "chol": 200, "fbs": 0,
  "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 0, "slope": 1,
  "ca": 0, "thal": 2
}
```

### Batch Prediction
`POST /api/predict-batch`
- Form-data key: `file` (CSV)
- Returns: CSV with predictions.

## Deployment
This app can be deployed to any container orchestration platform (Kubernetes, ECS) or PaaS (Heroku, Render).
Ensure to set up HTTPS and Authentication for production use.
