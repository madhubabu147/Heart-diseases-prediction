
import pytest
import json
import io
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"HeartGuard AI" in rv.data

def test_predict_api(client):
    # Test case: Typical case (Low risk)
    data = {
        "age": 45,
        "sex": 1,
        "cp": 0,
        "trestbps": 120,
        "chol": 200,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 0,
        "slope": 1,
        "ca": 0,
        "thal": 2
    }
    rv = client.post('/api/predict', json=data)
    assert rv.status_code == 200
    resp = rv.get_json()
    assert "prediction" in resp
    assert "probability" in resp
    assert "label" in resp

def test_predict_batch_api(client):
    # Create a dummy CSV
    csv_content = "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal\n45,1,0,120,200,0,0,150,0,0,1,0,2"
    data = {
        'file': (io.BytesIO(csv_content.encode('utf-8')), 'test.csv')
    }
    
    rv = client.post('/api/predict-batch', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200
    # Check if response is csv
    assert "text/csv" in rv.headers["Content-Type"]
    assert b"Prediction" in rv.data
