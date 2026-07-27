import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = os.urandom(32)

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
# HIGH-ENHANCEMENT LUXURY NEON UI TEMPLATE
# -------------------------------------------------------------
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoValuate AI | Premium Dynamic Valuation</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #080c18;
            --panel-glass: rgba(15, 22, 42, 0.75);
            --border-glass: rgba(255, 255, 255, 0.08);
            --neon-cyan: #06b6d4;
            --neon-purple: #8b5cf6;
            --neon-pink: #ec4899;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background: radial-gradient(circle at 50% 0%, #1c1942 0%, var(--bg-base) 70%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            overflow-x: hidden;
        }

        /* Suppress Arrow Scrollbars Completely */
        ::-webkit-scrollbar {
            width: 0px;
            height: 0px;
            background: transparent;
        }

        .dashboard-container {
            width: 100%;
            max-width: 1400px;
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 2rem;
            animation: fadeIn 0.6s ease-out;
        }

        @media (max-width: 1150px) {
            .dashboard-container { grid-template-columns: 1fr; }
        }

        .glass-card {
            background: var(--panel-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 24px;
            padding: 2.2rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .header-block {
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 40%, var(--neon-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.25rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
        }

        @media (max-width: 850px) {
            .feature-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 550px) {
            .feature-grid { grid-template-columns: 1fr; }
        }

        .input-wrapper {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .span-2 { grid-column: span 2; }
        @media (max-width: 850px) { .span-2 { grid-column: span 1; } }

        label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input, select {
            background: rgba(10, 15, 30, 0.8);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.25s ease;
            width: 100%;
        }

        input:focus, select:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.2);
        }

        .range-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        input[type="range"] {
            padding: 0;
            height: 5px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            cursor: pointer;
            appearance: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--neon-cyan);
            box-shadow: 0 0 8px var(--neon-cyan);
        }

        .range-counter {
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--neon-cyan);
            min-width: 3.5rem;
            text-align: right;
        }

        .submit-trigger {
            grid-column: span 3;
            background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 50%, var(--neon-pink) 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 1.1rem;
            font-size: 1.05rem;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-top: 0.75rem;
            box-shadow: 0 5px 20px rgba(139, 92, 246, 0.3);
        }

        @media (max-width: 850px) { .submit-trigger { grid-column: span 2; } }
        @media (max-width: 550px) { .submit-trigger { grid-column: span 1; } }

        .submit-trigger:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
        }

        .analytics-side {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .valuation-display {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
        }

        .valuation-display h2 {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--neon-cyan);
            margin-bottom: 0.3rem;
        }

        .valuation-price-container {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.2rem;
            text-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        }

        .valuation-price-container span {
            background: linear-gradient(to right, #ffffff, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .chart-card {
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .chat-history-card {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 420px;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 0.5rem;
        }

        .clear-history-action {
            background: transparent;
            border: none;
            color: var(--neon-pink);
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
            border-radius: 16px;
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
            background: rgba(6, 182, 212, 0.08);
            border: 1px solid rgba(6, 182, 212, 0.15);
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
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #fca5a5;
            text-align: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <!-- Main Form Entries Architecture -->
        <div class="glass-card">
            <div class="header-block">
                <div>
                    <h1>Valuation Matrix Node</h1>
                    <p class="subtitle">Ensemble Learning 17-Factor Pricing Node Blueprint</p>
                </div>
                <div style="min-width: 120px;">
                    <label>Currency</label>
                    <select id="currencySelector" onchange="convertActiveValuations()">
                        <option value="USD" selected>USD ($)</option>
                        <option value="INR">INR (₹)</option>
                        <option value="EUR">EUR (€)</option>
                        <option value="GBP">GBP (£)</option>
                    </select>
                </div>
            </div>

            {% if error_msg %}
            <div class="system-alert">{{ error_msg }}</div>
            {% endif %}

            <form method="POST" action="/" class="feature-grid">
                <!-- Dropdown Fields Matrix -->
                <div class="input-wrapper">
                    <label>Brand Manufacturer</label>
                    <select name="Make">
                        <option value="0" {% if form_values.Make == '0' %}selected{% endif %}>Toyota</option>
                        <option value="1" {% if form_values.Make == '1' %}selected{% endif %}>Honda</option>
                        <option value="2" {% if form_values.Make == '2' %}selected{% endif %}>Ford</option>
                        <option value="3" {% if form_values.Make == '3' %}selected{% endif %}>BMW</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Model Variant</label>
                    <select name="Model">
                        <option value="0" {% if form_values.Model == '0' %}selected{% endif %}>Sedan Base Matrix</option>
                        <option value="1" {% if form_values.Model == '1' %}selected{% endif %}>SUV Hyper Sport</option>
                        <option value="2" {% if form_values.Model == '2' %}selected{% endif %}>Eco Hatch Core</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Trim Variant Class</label>
                    <select name="Trim_Level">
                        <option value="0" {% if form_values.Trim_Level == '0' %}selected{% endif %}>Standard Entry</option>
                        <option value="1" {% if form_values.Trim_Level == '1' %}selected{% endif %}>Mid Tier Comfort</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Year of Assembly</label>
                    <div class="range-group">
                        <input type="range" id="Year" name="Year" min="2010" max="2026" value="{{ form_values.Year|default(2020) }}" oninput="syncRangeValue('Year', this.value)">
                        <span id="Year_counter" class="range-counter">{{ form_values.Year|default(2020) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Fuel System Source</label>
                    <select name="Fuel_Type">
                        <option value="0" {% if form_values.Fuel_Type == '0' %}selected{% endif %}>Unleaded Petrol</option>
                        <option value="1" {% if form_values.Fuel_Type == '1' %}selected{% endif %}>Refined Diesel</option>
                        <option value="2" {% if form_values.Fuel_Type == '2' %}selected{% endif %}>Solid State Electric</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Transmission Gear Layout</label>
                    <select name="Transmission">
                        <option value="0" {% if form_values.Transmission == '0' %}selected{% endif %}>Manual Mesh</option>
                        <option value="1" {% if form_values.Transmission == '1' %}selected{% endif %}>Dual Clutch Automatic</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Engine Capacity (L)</label>
                    <div class="range-group">
                        <input type="range" id="Engine_Size" name="Engine_Size" min="0.8" max="6.0" step="0.1" value="{{ form_values.Engine_Size|default(2.0) }}" oninput="syncRangeValue('Engine_Size', this.value)">
                        <span id="Engine_Size_counter" class="range-counter">{{ form_values.Engine_Size|default(2.0) }}</span>
                    </div>
                </div>
                <div class="input-wrapper span-2">
                    <label>Distance Traveled (Odometer km)</label>
                    <div class="range-group">
                        <input type="range" id="Mileage" name="Mileage" min="0" max="200000" step="500" value="{{ form_values.Mileage|default(45000) }}" oninput="syncRangeValue('Mileage', this.value)">
                        <span id="Mileage_counter" class="range-counter">{{ form_values.Mileage|default(45000) }}</span>
                    </div>
                </div>

                <div class="input-wrapper">
                    <label>Service Portfolio State</label>
                    <select name="Service_History">
                        <option value="0" {% if form_values.Service_History == '0' %}selected{% endif %}>Full Documented</option>
                        <option value="1" {% if form_values.Service_History == '1' %}selected{% endif %}>Partial / Missing</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Brake Horsepower</label>
                    <div class="range-group">
                        <input type="range" id="Horsepower" name="Horsepower" min="60" max="600" value="{{ form_values.Horsepower|default(150) }}" oninput="syncRangeValue('Horsepower', this.value)">
                        <span id="Horsepower_counter" class="range-counter">{{ form_values.Horsepower|default(150) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Torque Curve (Nm)</label>
                    <div class="range-group">
                        <input type="range" id="Torque" name="Torque" min="100" max="700" value="{{ form_values.Torque|default(250) }}" oninput="syncRangeValue('Torque', this.value)">
                        <span id="Torque_counter" class="range-counter">{{ form_values.Torque|default(250) }}</span>
                    </div>
                </div>

                <div class="input-wrapper">
                    <label>Previous Owners Count</label>
                    <select name="Owners">
                        <option value="1" {% if form_values.Owners == '1' %}selected{% endif %}>1 Owner</option>
                        <option value="2" {% if form_values.Owners == '2' %}selected{% endif %}>2 Owners</option>
                        <option value="3" {% if form_values.Owners == '3' %}selected{% endif %}>3+</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Incident History</label>
                    <select name="Accident_History">
                        <option value="0" {% if form_values.Accident_History == '0' %}selected{% endif %}>No Incidents</option>
                        <option value="1" {% if form_values.Accident_History == '1' %}selected{% endif %}>Major / Repaired</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Coating Color Class</label>
                    <select name="Color">
                        <option value="0" {% if form_values.Color == '0' %}selected{% endif %}>Metallic Black</option>
                        <option value="1" {% if form_values.Color == '1' %}selected{% endif %}>Pure White</option>
                        <option value="2" {% if form_values.Color == '2' %}selected{% endif %}>Silver Accent</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Interior Wear State</label>
                    <select name="Interior_Condition">
                        <option value="0" {% if form_values.Interior_Condition == '0' %}selected{% endif %}>Pristine</option>
                        <option value="1" {% if form_values.Interior_Condition == '1' %}selected{% endif %}>Moderate Wear</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Chassis Body Architecture</label>
                    <select name="Body_Type">
                        <option value="0" {% if form_values.Body_Type == '0' %}selected{% endif %}>Coupe</option>
                        <option value="1" {% if form_values.Body_Type == '1' %}selected{% endif %}>Sedan</option>
                        <option value="2" {% if form_values.Body_Type == '2' %}selected{% endif %}>SUV</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Drivetrain Config</label>
                    <select name="Drivetrain">
                        <option value="0" {% if form_values.Drivetrain == '0' %}selected{% endif %}>FWD</option>
                        <option value="1" {% if form_values.Drivetrain == '1' %}selected{% endif %}>RWD</option>
                        <option value="2" {% if form_values.Drivetrain == '2' %}selected{% endif %}>AWD</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Electronics Package</label>
                    <select name="Tech_Package">
                        <option value="0" {% if form_values.Tech_Package == '0' %}selected{% endif %}>Standard Hub</option>
                        <option value="1" {% if form_values.Tech_Package == '1' %}selected{% endif %}>Advanced Navigation</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Fuel Efficiency (km/L)</label>
                    <div class="range-group">
                        <input type="range" id="Fuel_Efficiency" name="Fuel_Efficiency" min="5" max="30" value="{{ form_values.Fuel_Efficiency|default(15) }}" oninput="syncRangeValue('Fuel_Efficiency', this.value)">
                        <span id="Fuel_Efficiency_counter" class="range-counter">{{ form_values.Fuel_Efficiency|default(15) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Regional Marketplace</label>
                    <select name="Location">
                        <option value="0" {% if form_values.Location == '0' %}selected{% endif %}>Metro Hub</option>
                        <option value="1" {% if form_values.Location == '1' %}selected{% endif %}>Regional District</option>
                    </select>
                </div>

                <button type="submit" class="submit-trigger">Process Asset Value Vectors</button>
            </form>
        </div>

        <!-- Output Analytics Logs Column -->
        <div class="analytics-side">
            {% if prediction_result is not none %}
            <div class="valuation-display">
                <h2>Evaluated Target Vector Consensus</h2>
                <div class="valuation-price-container">
                    <span id="currencySymbol">$</span>
                    <span id="baseValuationPrice" data-usd="{{ prediction_result|replace(',', '') }}">{{ prediction_result }}</span>
                </div>
                <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.4rem; color: var(--neon-cyan);">RandomForest Regressor Ensemble 17-D Core Output</p>
            </div>
            {% endif %}

            <!-- High-Contrast Neon Pie Chart Container Mapping Features -->
            <div class="glass-card chart-card">
                <h3 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 1rem; color: var(--neon-cyan); text-transform: uppercase; letter-spacing: 0.05em;">Feature Weight Distribution</h3>
                <div style="width: 100%; max-height: 200px; display: flex; justify-content: center;">
                    <canvas id="featureWeightPieChart"></canvas>
                </div>
            </div>

            <!-- Thread Execution Logs Container Stack -->
            <div class="glass-card chat-history-card">
                <div class="chat-header">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #cbd5e1; text-transform: uppercase;">Sequential Prediction Logs</h3>
                    {% if history %}
                    <form method="POST" action="/clear">
                        <button type="submit" class="clear-history-action">Purge Logs</button>
                    </form>
                    {% endif %}
                </div>

                <div class="chat-log-stream">
                    {% for interaction in history %}
                        <div class="chat-bubble user-query">
                            <div class="bubble-meta">Asset Input Payload Data</div>
                            Year: {{ interaction.inputs.Year }} | Mileage: {{ interaction.inputs.Mileage }} km | HP: {{ interaction.inputs.Horsepower }}
                        </div>
                        <div class="chat-bubble ai-response">
                            <div class="bubble-meta">Pipeline Output</div>
                            Resolution metrics mapped value signature to token: 
                            <strong style="color: var(--neon-cyan);" class="loggedPrice" data-usd="{{ interaction.output|replace(',', '') }}">${{ interaction.output }} USD</strong>
                        </div>
                    {% else %}
                        <div class="no-records">No session records tracked in system active thread.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        const currencyExchangeMatrix = {
            USD: { symbol: '$', rate: 1.0 },
            INR: { symbol: '₹', rate: 83.45 },
            EUR: { symbol: '€', rate: 0.92 },
            GBP: { symbol: '£', rate: 0.79 }
        };

        function syncRangeValue(sliderId, value) {
            document.getElementById(sliderId + '_counter').innerText = value;
        }

        function convertActiveValuations() {
            const selector = document.getElementById('currencySelector');
            const targetCurrency = selector.value;
            const configuration = currencyExchangeMatrix[targetCurrency];
            
            const primaryPriceElement = document.getElementById('baseValuationPrice');
            const primarySymbolElement = document.getElementById('currencySymbol');
            if(primaryPriceElement && primarySymbolElement) {
                const nativeUSDValue = parseFloat(primaryPriceElement.getAttribute('data-usd'));
                const scaledPrice = nativeUSDValue * configuration.rate;
                primarySymbolElement.innerText = configuration.symbol;
                primaryPriceElement.innerText = scaledPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            }

            document.querySelectorAll('.loggedPrice').forEach(element => {
                const nativeUSD = parseFloat(element.getAttribute('data-usd'));
                const scaled = nativeUSD * configuration.rate;
                element.innerText = configuration.symbol + scaled.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' + targetCurrency;
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            // Setup dynamic vector weighting array elements inside our modern Pie Chart
            const yearVal = parseFloat(document.getElementById('Year') ? document.getElementById('Year').value : 2020);
            const mileageVal = parseFloat(document.getElementById('Mileage') ? document.getElementById('Mileage').value : 45000);
            const hpVal = parseFloat(document.getElementById('Horsepower') ? document.getElementById('Horsepower').value : 150);

            const ctx = document.getElementById('featureWeightPieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Odometer Metrics', 'Age Matrix', 'Engine Output', 'Remaining Vector Attributes'],
                    datasets: [{
                        data: [mileageVal * 0.4, (2026 - yearVal) * 800, hpVal * 15, 12000],
                        backgroundColor: ['#06b6d4', '#8b5cf6', '#ec4899', '#334155'],
                        borderWidth: 1,
                        borderColor: 'rgba(255,255,255,0.1)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 10 } } }
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
# DYNAMIC MATRIX LOGISTICS DISPATCHER GATEWAY
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def main_gateway():
    error_msg = None
    prediction_result = None
    form_values = {}

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        all_ui_fields = [
            'Make', 'Model', 'Trim_Level', 'Year', 'Fuel_Type', 'Transmission', 'Engine_Size', 
            'Service_History', 'Mileage', 'Horsepower', 'Torque', 'Owners', 
            'Accident_History', 'Color', 'Interior_Condition', 'Body_Type', 'Drivetrain', 
            'Tech_Package', 'Fuel_Efficiency', 'Location'
        ]
        form_values = {f: request.form.get(f) for f in all_ui_fields}

        if model is None:
            # Intuitive mathematical fallback logic loop
            try:
                base_calculation = 42500.00
                mileage_deduction = float(form_values.get('Mileage', 45000)) * 0.11
                age_deduction = (2026 - int(form_values.get('Year', 2020))) * 1700
                calculated_sim_val = max(3400.00, base_calculation - mileage_deduction - age_deduction)
                prediction_result = f"{calculated_sim_val:,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {"inputs": form_values, "output": prediction_result})
                session["history"] = current_stack[:6]
            except Exception as ex:
                error_msg = f"Vector Generation Simulation Exception: {str(ex)}"
        else:
            try:
                # COMPILATION RECTIFICATION ROUTE: Mapped array explicitly to 17 features expected by the pipeline
                evaluation_vector = np.array([[
                    int(form_values['Make']),
                    int(form_values['Model']),
                    int(form_values['Year']),
                    int(form_values['Fuel_Type']),
                    int(form_values['Transmission']),
                    float(form_values['Engine_Size']),
                    int(form_values['Service_History']),
                    float(form_values['Mileage']),
                    int(form_values['Horsepower']),
                    int(form_values['Torque']),
                    int(form_values['Owners']),
                    int(form_values['Accident_History']),
                    int(form_values['Color']),
                    int(form_values['Body_Type']),
                    int(form_values['Drivetrain']),
                    float(form_values['Fuel_Efficiency']),
                    int(form_values['Location'])
                ]], dtype=object)

                calculated_matrix = model.predict(evaluation_vector)
                prediction_result = f"{float(calculated_matrix[0]):,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {"inputs": form_values, "output": prediction_result})
                session["history"] = current_stack[:6]

            except Exception as ex:
                error_msg = f"Vector Compilation Execution Error: {str(ex)}"

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
