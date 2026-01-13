from flask import Flask, request, render_template, jsonify, send_file
import pandas as pd
import io
import os
from src.Heart.services.predict_service import PredictService, CustomData

app = Flask(__name__)

# Initialize Service
try:
    predict_service = PredictService()
except Exception as e:
    print(f"Warning: Model artifacts not found. Please run training pipeline. Error: {e}")
    predict_service = None

@app.route("/", methods=["GET"])
def home():
    return render_template("index_modern.html")

@app.route("/api/predict", methods=["POST"])
def predict_api():
    if not predict_service:
        return jsonify({"error": "Model not active. Contact admin."}), 503

    try:
        req = request.get_json()
        
        data = CustomData(
            age=float(req.get("age")),
            sex=int(req.get("sex")),
            cp=int(req.get("cp")),
            trestbps=float(req.get("trestbps")),
            chol=float(req.get("chol")),
            fbs=int(req.get("fbs")),
            restecg=int(req.get("restecg")),
            thalach=float(req.get("thalach")),
            exang=int(req.get("exang")),
            oldpeak=float(req.get("oldpeak")),
            slope=int(req.get("slope")),
            ca=int(req.get("ca")),
            thal=int(req.get("thal"))
        )
        
        result = predict_service.predict(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/predict-batch", methods=["POST"])
def predict_batch_api():
    if not predict_service:
        return jsonify({"error": "Model not active. Contact admin."}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        df = pd.read_csv(file)
        
        # Verify columns if needed, but the service handles it
        result_df = predict_service.predict_batch(df)
        
        output = io.BytesIO()
        result_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="prediction_results.csv"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
