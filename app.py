import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session state encryption key

# -------------------------------------------------------------
# AUTOMOTIVE PREDICTION PIPELINE CONFIGURATION
# -------------------------------------------------------------
MODEL_PATH = "rfamodel.pkl"

# Feature structure extracted from model metadata:
# ['Make', 'Model', 'Year', 'Fuel_Type', 'Transmission', 'Engine_Size', 
#  'Service_History', 'Mileage', 'Horsepower', 'Torque', 'Owners', 
#  'Accident_History', 'Color', 'Body_Type', 'Drivetrain', 'Fuel_Efficiency', 'Location']

def load_valuation_engine():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as file:
        return pickle.load(file)

model = load_valuation_engine()

# -------------------------------------------------------------
# HIGH-FIDELITY GLASSMORPHISM UI WITH CHAT STREAM LOGS
# -------------------------------------------------------------
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoValuate AI | Predictive Market Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --panel-glass: rgba(17, 24, 39, 0.7);
            --border-glass: rgba(255, 255, 255, 0.06);
            --neon-accent: #3b82f6;
            --neon-secondary: #6366f1;
            --neon-glow: rgba(99, 102, 241, 0.35);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background: radial-gradient(circle at 50% 0%, #1e1e38 0%, var(--bg-dark) 70%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            overflow-x: hidden;
        }

        .dashboard-container {
            width: 100%;
            max-width: 1300px;
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 2rem;
            animation: containerAppearing 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @media (max-width: 1100px) {
            .dashboard-container {
                grid-template-columns: 1fr;
            }
        }

        .glass-card {
            background: var(--panel-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 28px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            position: relative;
        }

        .header-block {
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 1.25rem;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #ffffff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-top: 0.25rem;
        }

        /* 17 Feature Entry Form Layout Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
        }

        @media (max-width: 780px) {
            .feature-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 520px) {
            .feature-grid {
                grid-template-columns: 1fr;
            }
        }

        .input-wrapper {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .span-2 {
            grid-column: span 2;
        }
        @media (max-width: 780px) {
            .span-2 { grid-column: span 1; }
        }

        label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        input, select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            transition: all 0.25s ease;
            outline: none;
            width: 100%;
        }

        input:focus, select:focus {
            border-color: var(--neon-accent);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
            background: rgba(15, 23, 42, 0.8);
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
        }

        .range-counter {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--neon-accent);
            min-width: 3.5rem;
            text-align: right;
        }

        .submit-trigger {
            grid-column: span 3;
            background: linear-gradient(135deg, var(--neon-accent) 0%, var(--neon-secondary) 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 1.1rem;
            font-size: 1.05rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
            box-shadow: 0 4px 20px var(--neon-glow);
        }

        @media (max-width: 780px) { .submit-trigger { grid-column: span 2; } }
        @media (max-width: 520px) { .submit-trigger { grid-column: span 1; } }

        .submit-trigger:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--neon-glow);
            filter: brightness(1.1);
        }

        /* Sidebar & Live Metrics Output styling */
        .analytics-side {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .valuation-display {
            background: var(--success-gradient);
            border-radius: 24px;
            padding: 2.2rem;
            text-align: center;
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.25);
            animation: cardSlidingUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .valuation-display h2 {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            opacity: 0.85;
            margin-bottom: 0.4rem;
        }

        .valuation-price {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            text-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }

        /* Conversational Execution History Stream */
        .chat-history-card {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 540px;
            min-height: 400px;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }

        .clear-history-action {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.8rem;
            transition: color 0.2s;
        }

        .clear-history-action:hover {
            color: #ef4444;
        }

        .chat-log-stream {
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            padding-right: 0.4rem;
            flex-grow: 1;
        }

        .chat-log-stream::-webkit-scrollbar { width: 5px; }
        .chat-log Stream::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
        }

        .chat-bubble {
            display: flex;
            flex-direction: column;
            max-width: 88%;
            padding: 0.85rem 1.1rem;
            border-radius: 18px;
            font-size: 0.88rem;
            line-height: 1.45;
            animation: bubblePop 0.4s ease-out;
        }

        .chat-bubble.user-query {
            background: rgba(255, 255, 255, 0.04);
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            border: 1px solid rgba(255,255,255,0.03);
        }

        .chat-bubble.ai-response {
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(99, 102, 241, 0.18);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .bubble-meta {
            font-size: 0.72rem;
            color: var(--text-secondary);
            margin-bottom: 0.3rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .no-records {
            color: var(--text-secondary);
            text-align: center;
            margin: auto;
            font-style: italic;
            font-size: 0.9rem;
        }

        .system-alert {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #fca5a5;
            font-size: 0.9rem;
            text-align: center;
        }

        /* Fluid Animation Framework */
        @keyframes containerAppearing {
            from { opacity: 0; transform: scale(0.98) translateY(15px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        @keyframes cardSlidingUp {
            from { opacity: 0; transform: translateY(25px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bubblePop {
            from { opacity: 0; transform: scale(0.95) translateY(5px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <!-- Input Parameters Core -->
        <div class="glass-card">
            <div class="header-block">
                <h1>Valuation Intelligence Console</h1>
                <p class="subtitle">17-Factor RandomForest Vehicle Analysis Execution Node</p>
            </div>

            {% if error_msg %}
            <div class="system-alert">{{ error_msg }}</div>
            {% endif %}

            <form method="POST" action="/" class="feature-grid">
                <!-- Row 1: Brand Spec Base -->
                <div class="input-wrapper">
                    <label>Make</label>
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
                        <option value="0" {% if form_values.Model == '0' %}selected{% endif %}>Sedan Base</option>
                        <option value="1" {% if form_values.Model == '1' %}selected{% endif %}>SUV Sport</option>
                        <option value="2" {% if form_values.Model == '2' %}selected{% endif %}>Eco Hatch</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Year of Manufacture</label>
                    <div class="range-group">
                        <input type="range" id="Year" name="Year" min="2010" max="2026" value="{{ form_values.Year|default(2020) }}" oninput="syncRangeValue('Year', this.value)">
                        <span id="Year_counter" class="range-counter">{{ form_values.Year|default(2020) }}</span>
                    </div>
                </div>

                <!-- Row 2: Mechanicals -->
                <div class="input-wrapper">
                    <label>Fuel Type</label>
                    <select name="Fuel_Type">
                        <option value="0" {% if form_values.Fuel_Type == '0' %}selected{% endif %}>Petrol</option>
                        <option value="1" {% if form_values.Fuel_Type == '1' %}selected{% endif %}>Diesel</option>
                        <option value="2" {% if form_values.Fuel_Type == '2' %}selected{% endif %}>Electric</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Transmission</label>
                    <select name="Transmission">
                        <option value="0" {% if form_values.Transmission == '0' %}selected{% endif %}>Manual</option>
                        <option value="1" {% if form_values.Transmission == '1' %}selected{% endif %}>Automatic</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Engine Size (L)</label>
                    <div class="range-group">
                        <input type="range" id="Engine_Size" name="Engine_Size" min="0.8" max="6.0" step="0.1" value="{{ form_values.Engine_Size|default(2.0) }}" oninput="syncRangeValue('Engine_Size', this.value)">
                        <span id="Engine_Size_counter" class="range-counter">{{ form_values.Engine_Size|default(2.0) }}</span>
                    </div>
                </div>

                <!-- Row 3: Use Dynamics -->
                <div class="input-wrapper span-2">
                    <label>Mileage Tracking (kms)</label>
                    <div class="range-group">
                        <input type="range" id="Mileage" name="Mileage" min="0" max="200000" step="500" value="{{ form_values.Mileage|default(45000) }}" oninput="syncRangeValue('Mileage', this.value)">
                        <span id="Mileage_counter" class="range-counter">{{ form_values.Mileage|default(45000) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Service History</label>
                    <select name="Service_History">
                        <option value="0" {% if form_values.Service_History == '0' %}selected{% endif %}>Full Documented</option>
                        <option value="1" {% if form_values.Service_History == '1' %}selected{% endif %}>Partial / Missing</option>
                    </select>
                </div>

                <!-- Row 4: Power metrics -->
                <div class="input-wrapper">
                    <label>Horsepower</label>
                    <div class="range-group">
                        <input type="range" id="Horsepower" name="Horsepower" min="60" max="600" value="{{ form_values.Horsepower|default(150) }}" oninput="syncRangeValue('Horsepower', this.value)">
                        <span id="Horsepower_counter" class="range-counter">{{ form_values.Horsepower|default(150) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Torque (Nm)</label>
                    <div class="range-group">
                        <input type="range" id="Torque" name="Torque" min="100" max="700" value="{{ form_values.Torque|default(250) }}" oninput="syncRangeValue('Torque', this.value)">
                        <span id="Torque_counter" class="range-counter">{{ form_values.Torque|default(250) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Previous Owners</label>
                    <select name="Owners">
                        <option value="1" {% if form_values.Owners == '1' %}selected{% endif %}>1 Owner</option>
                        <option value="2" {% if form_values.Owners == '2' %}selected{% endif %}>2 Owners</option>
                        <option value="3" {% if form_values.Owners == '3' %}selected{% endif %}>3+</option>
                    </select>
                </div>

                <!-- Row 5: Safety & Cosmetics -->
                <div class="input-wrapper">
                    <label>Accident History</label>
                    <select name="Accident_History">
                        <option value="0" {% if form_values.Accident_History == '0' %}selected{% endif %}>No Incidents</option>
                        <option value="1" {% if form_values.Accident_History == '1' %}selected{% endif %}>Major / Repaired</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Color Class</label>
                    <select name="Color">
                        <option value="0" {% if form_values.Color == '0' %}selected{% endif %}>Metallic Black</option>
                        <option value="1" {% if form_values.Color == '1' %}selected{% endif %}>Pure White</option>
                        <option value="2" {% if form_values.Color == '2' %}selected{% endif %}>Silver Accent</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Body Architecture</label>
                    <select name="Body_Type">
                        <option value="0" {% if form_values.Body_Type == '0' %}selected{% endif %}>Coupe</option>
                        <option value="1" {% if form_values.Body_Type == '1' %}selected{% endif %}>Sedan</option>
                        <option value="2" {% if form_values.Body_Type == '2' %}selected{% endif %}>SUV</option>
                    </select>
                </div>

                <!-- Row 6: Structural and Geography -->
                <div class="input-wrapper">
                    <label>Drivetrain Config</label>
                    <select name="Drivetrain">
                        <option value="0" {% if form_values.Drivetrain == '0' %}selected{% endif %}>FWD</option>
                        <option value="1" {% if form_values.Drivetrain == '1' %}selected{% endif %}>RWD</option>
                        <option value="2" {% if form_values.Drivetrain == '2' %}selected{% endif %}>AWD</option>
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
                    <label>Regional Location</label>
                    <select name="Location">
                        <option value="0" {% if form_values.Location == '0' %}selected{% endif %}>Metro Hub</option>
                        <option value="1" {% if form_values.Location == '1' %}selected{% endif %}>Regional District</option>
                    </select>
                </div>

                <button type="submit" class="submit-trigger">Process Asset Value Vectors</button>
            </form>
        </div>

        <!-- Output Analytics Logs Side Column -->
        <div class="analytics-side">
            {% if prediction_result is not none %}
            <div class="valuation-display">
                <h2>Evaluated Market Value</h2>
                <div class="valuation-price">${{ prediction_result }}</div>
                <p style="font-size: 0.82rem; opacity: 0.8; margin-top: 0.25rem;">RandomForest Ensemble Consensus</p>
            </div>
            {% endif %}

            <!-- Chat Message Streams Format -->
            <div class="glass-card chat-history-card">
                <div class="chat-header">
                    <h3 style="font-size: 1.05rem; font-weight:600;">Prediction Stream Thread</h3>
                    {% if history %}
                    <form method="POST" action="/clear">
                        <button type="submit" class="clear-history-action">Purge Threads</button>
                    </form>
                    {% endif %}
                </div>

                <div class="chat-log-stream">
                    {% for interaction in history %}
                        <div class="chat-bubble user-query">
                            <div class="bubble-meta">User Input Payload</div>
                            Year: {{ interaction.inputs.Year }} | Mileage: {{ interaction.inputs.Mileage }} km | HP: {{ interaction.inputs.Horsepower }}
                        </div>
                        <div class="chat-bubble ai-response">
                            <div class="bubble-meta">Model Response System</div>
                            The estimated asset valuation model pipeline maps this index signature matrix to standard vector value: <strong>${{ interaction.output }}</strong>.
                        </div>
                    {% else %}
                        <div class="no-records">No session history tracked in active socket state.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        function syncRangeValue(sliderId, value) {
            document.getElementById(sliderId + '_counter').innerText = value;
        }
    </script>
</body>
</html>
"""

# -------------------------------------------------------------
# GATEWAY CONTROLLER ARCHITECTURE
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def main_gateway():
    error_msg = None
    prediction_result = None
    form_values = {}

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        # Capture raw form fields matching the 17 architectural features
        fields = [
            'Make', 'Model', 'Year', 'Fuel_Type', 'Transmission', 'Engine_Size', 
            'Service_History', 'Mileage', 'Horsepower', 'Torque', 'Owners', 
            'Accident_History', 'Color', 'Body_Type', 'Drivetrain', 'Fuel_Efficiency', 'Location'
        ]
        
        form_values = {f: request.form.get(f) for f in fields}

        if model is None:
            error_msg = "Critical Engine Alert: 'model.pkl' could not be safely initialized from target storage memory."
        else:
            try:
                # Structure input feature vector matching dataset alignment 
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

                # Compute value using target random forest regressor
                calculated_matrix = model.predict(evaluation_vector)
                prediction_result = f"{float(calculated_matrix[0]):,.2f}"

                # Update operational thread list trace metrics
                current_stack = session["history"]
                current_stack.insert(0, {
                    "inputs": form_values,
                    "output": prediction_result
                })
                session["history"] = current_stack[:5]  # Retention layer constraint limit

            except Exception as ex:
                error_msg = f"Vector Compilation Error: {str(ex)}"

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
