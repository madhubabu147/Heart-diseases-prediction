
const presets = {
    'typical': {
        age: 45, sex: 1, cp: 0, trestbps: 120, chol: 200, fbs: 0,
        restecg: 0, thalach: 150, exang: 0, oldpeak: 0, slope: 1, ca: 0, thal: 2
    },
    'risk': {
        age: 63, sex: 1, cp: 3, trestbps: 145, chol: 233, fbs: 1,
        restecg: 0, thalach: 150, exang: 0, oldpeak: 2.3, slope: 0, ca: 0, thal: 1
    }
};

function fillPreset(type) {
    const data = presets[type];
    for (const key in data) {
        const input = document.getElementsByName(key)[0];
        if (input) input.value = data[key];
    }
}

document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const btn = document.getElementById('predictBtn');
    const loader = btn.querySelector('.loader');
    const resultCard = document.getElementById('resultCard');

    // UI Loading state
    btn.disabled = true;
    loader.classList.remove('hidden');
    resultCard.classList.add('hidden');

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            displayResult(result);
        } else {
            alert('Error: ' + (result.error || 'Unknown error occurred'));
        }
    } catch (err) {
        console.error(err);
        alert('Network error occurred.');
    } finally {
        btn.disabled = false;
        loader.classList.add('hidden');
    }
});

function displayResult(data) {
    const resultCard = document.getElementById('resultCard');
    const ring = document.getElementById('progressRing');
    const probValue = document.getElementById('probValue');
    const riskLabel = document.getElementById('riskLabel');
    const analysisText = document.getElementById('analysisText');

    resultCard.classList.remove('hidden');

    // Animate Ring
    const probability = data.probability;
    const circumference = 440; // 2 * pi * 70
    const offset = circumference - (probability / 100) * circumference;

    // Reset for animation
    ring.style.strokeDashoffset = circumference;
    setTimeout(() => {
        ring.style.strokeDashoffset = offset;
    }, 100);

    // Update Color and Text
    let colorClass, textClass, labelText;
    if (probability < 30) {
        colorClass = 'text-green-500';
        textClass = 'bg-green-100 text-green-800';
        labelText = 'Low Risk';
    } else if (probability < 70) {
        colorClass = 'text-yellow-500';
        textClass = 'bg-yellow-100 text-yellow-800';
        labelText = 'Moderate Risk';
    } else {
        colorClass = 'text-red-500';
        textClass = 'bg-red-100 text-red-800';
        labelText = 'High Risk';
    }

    ring.className = `${colorClass} transition-all duration-1000 ease-out`;
    riskLabel.className = `inline-flex items-center px-4 py-1.5 rounded-full text-sm font-medium ${textClass}`;
    riskLabel.textContent = labelText;
    probValue.textContent = `${Math.round(probability)}%`;

    analysisText.innerHTML = `This patient shows a <strong>${probability}% probability</strong> of heart disease based on the provided clinical indicators. <br><br> Recommendation: ${probability > 50 ? 'Please consult a cardiologist for further evaluation.' : 'Maintain a healthy lifestyle and regular checkups.'}`;
}

// Batch Upload
document.getElementById('csvFile').addEventListener('change', async function (e) {
    if (!this.files[0]) return;

    const formData = new FormData();
    formData.append('file', this.files[0]);

    try {
        const response = await fetch('/api/predict-batch', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'prediction_results.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            alert('Error processing file.');
        }
    } catch (err) {
        alert('Upload failed.');
    }
});
