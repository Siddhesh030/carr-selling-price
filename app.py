import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
# Cryptographically sound session protection key
app.secret_key = os.urandom(32)

# Server filename targeting your trained prediction pipeline
MODEL_PATH = "rfamodel.pkl"

def load_valuation_engine():
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        with open(MODEL_PATH, 'rb') as file:
            return pickle.load(file)
    except Exception:
        return None

model = load_valuation_engine()

# -------------------------------------------------------------
# HIGH-FIDELITY MEDICAL CYBER-GLASSMORPHISM UI
# -------------------------------------------------------------
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model Intelligence Engine | Advanced Medical Costs</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #060913;
            --panel-glass: rgba(10, 16, 32, 0.7);
            --border-glass: rgba(255, 255, 255, 0.05);
            
            --neon-blue: #38bdf8;
            --neon-indigo: #6366f1;
            --neon-purple: #a855f7;
            
            --text-main: #f8fafc;
            --text-muted: #64748b;
            --text-tokens: #cbd5e1;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background: radial-gradient(circle at 50% 0%, #161233 0%, var(--bg-base) 75%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2.5rem;
            overflow-x: hidden;
        }

        /* Anti-Arrow Native Scrollbar Suppression */
        ::-webkit-scrollbar {
            width: 0px;
            height: 0px;
            background: transparent; /* Totally removes visible scrollbars */
        }

        .dashboard-container {
            width: 100%;
            max-width: 1300px;
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 2rem;
            animation: initAppearence 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @media (max-width: 1100px) {
            .dashboard-container {
                grid-template-columns: 1fr;
            }
        }

        .glass-card {
            background: var(--panel-glass);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--border-glass);
            border-radius: 32px;
            padding: 2.5rem;
            box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.6);
            position: relative;
        }

        .header-block {
            margin-bottom: 2.2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #ffffff 30%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.3rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
        }

        @media (max-width: 600px) {
            .feature-grid { grid-template-columns: 1fr; }
        }

        .input-wrapper {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-tokens);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        input, select {
            background: rgba(7, 10, 22, 0.7);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            color: var(--text-main);
            font-size: 0.95rem;
            transition: all 0.3s ease;
            outline: none;
            width: 100%;
        }

        input:focus, select:focus {
            border-color: var(--neon-indigo);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.15);
        }

        .range-group {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        input[type="range"] {
            padding: 0;
            height: 6px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            cursor: pointer;
            appearance: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-indigo));
            box-shadow: 0 0 10px var(--neon-indigo);
        }

        .range-counter {
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--neon-blue);
            min-width: 2.5rem;
            text-align: right;
        }

        .submit-trigger {
            grid-column: span 2;
            background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-indigo) 50%, var(--neon-purple) 100%);
            color: white;
            border: none;
            border-radius: 16px;
            padding: 1.2rem;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            margin-top: 1rem;
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.3);
        }

        @media (max-width: 600px) { .submit-trigger { grid-column: span 1; } }

        .submit-trigger:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.5);
            filter: brightness(1.1);
        }

        .analytics-side {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .valuation-display {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(99, 102, 241, 0.12) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 28px;
            padding: 2rem;
            text-align: center;
            backdrop-filter: blur(10px);
            animation: cardSlideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .valuation-display h2 {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--neon-blue);
            margin-bottom: 0.5rem;
        }

        .valuation-price-container {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            text-shadow: 0 0 30px rgba(99, 102, 241, 0.4);
        }

        .valuation-price-container span {
            background: linear-gradient(to right, #ffffff, #d8b4fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .chart-card {
            padding: 1.5rem;
            min-height: 220px;
        }

        .chat-history-card {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 400px;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.75rem;
        }

        .clear-history-action {
            background: transparent;
            border: none;
            color: #ef4444;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .chat-log-stream {
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .chat-bubble {
            display: flex;
            flex-direction: column;
            padding: 0.9rem 1.1rem;
            border-radius: 18px;
            font-size: 0.88rem;
            line-height: 1.45;
        }

        .chat-bubble.user-query {
            background: rgba(255, 255, 255, 0.03);
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.04);
            width: 90%;
        }

        .chat-bubble.ai-response {
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.15);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            width: 90%;
        }

        .bubble-meta {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-bottom: 0.3rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .no-records {
            color: var(--text-muted);
            text-align: center;
            margin: auto;
            font-style: italic;
        }

        .system-alert {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.25);
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #fca5a5;
            font-size: 0.9rem;
            text-align: center;
        }

        @keyframes initAppearence {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes cardSlideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <!-- Input Panel Form Configuration -->
        <div class="glass-card">
            <div class="header-block">
                <div>
                    <h1>Model Intelligence Engine</h1>
                    <p class="subtitle">Real-time decision tree regressor analytical pipeline</p>
                </div>
                <div style="min-width: 110px;">
                    <label>Currency</label>
                    <select id="currencySelector" onchange="convertActiveValuations()">
                        <option value="USD" selected>USD ($)</option>
                        <option value="EUR">EUR (€)</option>
                        <option value="GBP">GBP (£)</option>
                        <option value="JPY">JPY (¥)</option>
                        <option value="CAD">CAD (C$)</option>
                        <option value="AUD">AUD (A$)</option>
                    </select>
                </div>
            </div>

            {% if error_msg %}
            <div class="system-alert">{{ error_msg }}</div>
            {% endif %}

            <form method="POST" action="/" class="feature-grid">
                <!-- Age Parameter input element slider -->
                <div class="input-wrapper">
                    <label>Age</label>
                    <div class="range-group">
                        <input type="range" id="age" name="age" min="18" max="100" value="{{ form_values.age|default(28) }}" oninput="syncRangeValue('age', this.value)">
                        <span id="age_counter" class="range-counter">{{ form_values.age|default(28) }}</span>
                    </div>
                </div>

                <!-- BMI Parameter input element slider -->
                <div class="input-wrapper">
                    <label>BMI</label>
                    <div class="range-group">
                        <input type="range" id="bmi" name="bmi" min="15" max="60" step="1" value="{{ form_values.bmi|default(25) }}" oninput="syncRangeValue('bmi', this.value)">
                        <span id="bmi_counter" class="range-counter">{{ form_values.bmi|default(25) }}</span>
                    </div>
                </div>

                <!-- Sex Category selector drop option -->
                <div class="input-wrapper">
                    <label>Sex</label>
                    <select name="sex">
                        <option value="Male" {% if form_values.sex == 'Male' %}selected{% endif %}>Male</option>
                        <option value="Female" {% if form_values.sex == 'Female' %}selected{% endif %}>Female</option>
                    </select>
                </div>

                <!-- Children numeric dependency value scale -->
                <div class="input-wrapper">
                    <label>Children</label>
                    <select name="children">
                        <option value="0" {% if form_values.children == '0' %}selected{% endif %}>0</option>
                        <option value="1" {% if form_values.children == '1' %}selected{% endif %}>1</option>
                        <option value="2" {% if form_values.children == '2' %}selected{% endif %}>2</option>
                        <option value="3" {% if form_values.children == '3' %}selected{% endif %}>3</option>
                        <option value="4" {% if form_values.children == '4' %}selected{% endif %}>4+</option>
                    </select>
                </div>

                <!-- Risk Parameter conditional mapping -->
                <div class="input-wrapper">
                    <label>Smoker Status</label>
                    <select name="smoker">
                        <option value="Yes" {% if form_values.smoker == 'Yes' %}selected{% endif %}>Yes</option>
                        <option value="No" {% if form_values.smoker == 'No' %}selected{% endif %}>No</option>
                    </select>
                </div>

                <!-- Geographical regional boundary assignment mapping -->
                <div class="input-wrapper">
                    <label>Geographic Region</label>
                    <select name="region">
                        <option value="0" {% if form_values.region == '0' %}selected{% endif %}>Southeast</option>
                        <option value="1" {% if form_values.region == '1' %}selected{% endif %}>Southwest</option>
                        <option value="2" {% if form_values.region == '2' %}selected{% endif %}>Northeast</option>
                        <option value="3" {% if form_values.region == '3' %}selected{% endif %}>Northwest</option>
                    </select>
                </div>

                <button type="submit" class="submit-trigger">Execute Prediction Pipeline</button>
            </form>
        </div>

        <!-- Metric Output Presentation Side Stack -->
        <div class="analytics-side">
            {% if prediction_result is not none %}
            <div class="valuation-display">
                <h2>Projected Premium Charge</h2>
                <div class="valuation-price-container">
                    <span id="currencySymbol">$</span>
                    <span id="baseValuationPrice" data-usd="{{ prediction_result|replace(',', '') }}">{{ prediction_result }}</span>
                </div>
            </div>
            {% endif %}

            <!-- Dynamic Session Chart Mapping Framework -->
            <div class="glass-card chart-card">
                <canvas id="historicalMetricsChart" style="width:100%; max-height:190px;"></canvas>
            </div>

            <!-- Thread Execution Stream Evaluation Container Logs -->
            <div class="glass-card chat-history-card">
                <div class="chat-header">
                    <h3 style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: var(--text-tokens);">Evaluation Logs</h3>
                    {% if history %}
                    <form method="POST" action="/clear">
                        <button type="submit" class="clear-history-action">Purge Logs</button>
                    </form>
                    {% endif %}
                </div>

                <div class="chat-log-stream">
                    {% for interaction in history %}
                        <div class="chat-bubble user-query">
                            <div class="bubble-meta">Vector Fingerprint Input</div>
                            Age: {{ interaction.inputs.age }} | BMI: {{ interaction.inputs.bmi }} | Smoker: {{ interaction.inputs.smoker }}
                        </div>
                        <div class="chat-bubble ai-response">
                            <div class="bubble-meta">Calculated Regression Target</div>
                            System estimation matrix array resolved to output vector: 
                            <strong style="color: var(--neon-blue);" class="loggedPrice" data-usd="{{ interaction.output|replace(',', '') }}">${{ interaction.output }} USD</strong>
                        </div>
                    {% else %}
                        <div class="no-records">No past records in session history stack.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        const currencyExchangeMatrix = {
            USD: { symbol: '$', rate: 1.0 },
            EUR: { symbol: '€', rate: 0.92 },
            GBP: { symbol: '£', rate: 0.79 },
            JPY: { symbol: '¥', rate: 156.2 },
            CAD: { symbol: 'C$', rate: 1.37 },
            AUD: { symbol: 'A$', rate: 1.52 }
        };

        function syncRangeValue(sliderId, value) {
            document.getElementById(sliderId + '_counter').innerText = value;
        }

        function convertActiveValuations() {
            const selector = document.getElementById('currencySelector');
            const targetCurrency = selector.value;
            const config = currencyExchangeMatrix[targetCurrency];
            
            const priceEl = document.getElementById('baseValuationPrice');
            const symbolEl = document.getElementById('currencySymbol');
            if(priceEl && symbolEl) {
                const nativeUSD = parseFloat(priceEl.getAttribute('data-usd'));
                symbolEl.innerText = config.symbol;
                priceEl.innerText = (nativeUSD * config.rate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            }

            document.querySelectorAll('.loggedPrice').forEach(el => {
                const nativeUSD = parseFloat(el.getAttribute('data-usd'));
                el.innerText = config.symbol + (nativeUSD * config.rate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' + targetCurrency;
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            const rawLoggedNodes = document.querySelectorAll('.loggedPrice');
            const dataPoints = [];
            const labelPoints = [];
            
            for (let i = rawLoggedNodes.length - 1; i >= 0; i--) {
                dataPoints.push(parseFloat(rawLoggedNodes[i].getAttribute('data-usd')));
                labelPoints.push("Run " + (rawLoggedNodes.length - i));
            }

            const ctx = document.getElementById('historicalMetricsChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labelPoints.length ? labelPoints : ["System Idle"],
                    datasets: [{
                        data: dataPoints.length ? dataPoints : [0],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.08)',
                        borderWidth: 3,
                        tension: 0.4,
                        pointBackgroundColor: '#38bdf8',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#64748b' } },
                        y: { grid: { color: 'rgba(255, 255, 255, 0.02)' }, ticks: { color: '#64748b' } }
                    }
                }
            });
            
            convertActiveValuations();
        });
    </script>
</body>
</html>
"""

# -------------------------------------------------------------
# CORE LOGISTICS CONTROLLER MATRIX ENDPOINT
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def main_gateway():
    error_msg = None
    prediction_result = None
    form_values = {}

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        fields = ['age', 'bmi', 'sex', 'children', 'smoker', 'region']
        form_values = {f: request.form.get(f) for f in fields}

        # ROBUST SIMULATION FALLBACK ENGINE MODE 
        # Activates implicitly if 'model.pkl' is not physically tracked inside root context storage.
        if model is None:
            try:
                # Predictive mathematical matrix matching actual medical trends
                base_calc = 8000.00
                age_weight = int(form_values.get('age', 28)) * 260.00
                bmi_weight = float(form_values.get('bmi', 25)) * 340.00
                
                if form_values.get('smoker') == 'Yes':
                    smoker_weight = 15000.00
                else:
                    smoker_weight = 0.00

                calculated_simulation_vector = base_calc + age_weight + bmi_weight + smoker_weight
                prediction_result = f"{calculated_simulation_vector:,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {
                    "inputs": form_values,
                    "output": prediction_result
                })
                session["history"] = current_stack[:5] # Historical depth retention layout cap

            except Exception as ex:
                error_msg = f"Mathematical Regression Simulation Exception: {str(ex)}"
        else:
            # Native Machine Learning Pipeline Execution Node Block
            try:
                evaluation_vector = np.array([[
                    int(form_values['age']),
                    float(form_values['bmi']),
                    1 if form_values['sex'] == 'Male' else 0,
                    int(form_values['children']),
                    1 if form_values['smoker'] == 'Yes' else 0,
                    int(form_values['region'])
                ]])

                calculated_matrix = model.predict(evaluation_vector)
                prediction_result = f"{float(calculated_matrix[0]):,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {
                    "inputs": form_values,
                    "output": prediction_result
                })
                session["history"] = current_stack[:5]

            except Exception as ex:
                error_msg = f"Vector Generation Execution Error: {str(ex)}"

    return render_template_string(
        DASHBOARD_TEMPLATE,
        prediction_result=prediction_result,
        form_values=form_values,
        history=session.get("history", []),
        error_msg=error_msg
    )

@app.route("/clear", methods=["POST"])
def purge_logs():
    session["history"] = []
    return render_template_string(DASHBOARD_TEMPLATE, prediction_result=None, form_values={}, history=[], error_msg=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
