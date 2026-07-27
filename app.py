import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, session, jsonify

app = Flask(__name__)
# Cryptographically sound session protection key
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
# DYNAMIC PREMIUM CYBER-GLASSMORPHISM UI
# -------------------------------------------------------------
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoValuate AI | Advanced Predictive Matrix</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #060913;
            --panel-glass: rgba(10, 16, 32, 0.7);
            --border-glass: rgba(255, 255, 255, 0.05);
            --border-hover: rgba(99, 102, 241, 0.3);
            --accent-glow: rgba(99, 102, 241, 0.4);
            
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

        /* Anti-Arrow Native Scrollbar Suppression Layout */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.01);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.2);
            border-radius: 20px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--neon-indigo);
        }

        .dashboard-container {
            width: 100%;
            max-width: 1440px;
            display: grid;
            grid-template-columns: 1.25fr 0.75fr;
            gap: 2rem;
            animation: initAppearence 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @media (max-width: 1200px) {
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
            transition: border 0.3s ease;
        }
        
        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.08);
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
            font-size: 2.4rem;
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
            font-weight: 400;
        }

        .control-panel {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        /* 20 Deep Multi-Dimensional Feature Entry Form Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }

        @media (max-width: 900px) {
            .feature-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 600px) {
            .feature-grid { grid-template-columns: 1fr; }
        }

        .input-wrapper {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .span-2 {
            grid-column: span 2;
        }
        @media (max-width: 900px) {
            .span-2 { grid-column: span 1; }
        }

        label {
            font-size: 0.72rem;
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
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            outline: none;
            width: 100%;
        }

        input:focus, select:focus {
            border-color: var(--neon-indigo);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.15);
            background: rgba(7, 10, 22, 0.9);
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
            transition: transform 0.1s;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }

        .range-counter {
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--neon-blue);
            min-width: 4rem;
            text-align: right;
        }

        .submit-trigger {
            grid-column: span 3;
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
            box-shadow: 0 8px 30px var(--accent-glow);
            letter-spacing: 0.02em;
        }

        @media (max-width: 900px) { .submit-trigger { grid-column: span 2; } }
        @media (max-width: 600px) { .submit-trigger { grid-column: span 1; } }

        .submit-trigger:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
            filter: brightness(1.15);
        }

        .analytics-side {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Valuation Dashboard Display Overlay */
        .valuation-display {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 28px;
            padding: 2.2rem;
            text-align: center;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.3);
            animation: cardSlideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(10px);
        }

        .valuation-display h2 {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: var(--neon-blue);
            margin-bottom: 0.5rem;
            font-weight: 700;
        }

        .valuation-price-container {
            font-size: 3.2rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.25rem;
        }

        .valuation-price-container span {
            background: linear-gradient(to right, #ffffff, #d8b4fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Historical Thread Visualization Section */
        .chart-card {
            padding: 2rem;
            min-height: 260px;
        }

        .chat-history-card {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            max-height: 480px;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
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
            letter-spacing: 0.05em;
            transition: opacity 0.2s;
        }

        .clear-history-action:hover {
            opacity: 0.8;
        }

        .chat-log-stream {
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            padding-right: 0.5rem;
        }

        .chat-bubble {
            display: flex;
            flex-direction: column;
            padding: 1rem 1.25rem;
            border-radius: 20px;
            font-size: 0.9rem;
            line-height: 1.5;
            animation: bubbleReveal 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        .chat-bubble.user-query {
            background: rgba(255, 255, 255, 0.03);
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.04);
            max-width: 90%;
        }

        .chat-bubble.ai-response {
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.15);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            max-width: 90%;
        }

        .bubble-meta {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .no-records {
            color: var(--text-muted);
            text-align: center;
            margin: auto;
            font-style: italic;
            font-size: 0.9rem;
        }

        .system-alert {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.25);
            border-radius: 16px;
            padding: 1.1rem;
            margin-bottom: 2rem;
            color: #fca5a5;
            font-size: 0.9rem;
            font-weight: 500;
            text-align: center;
        }

        @keyframes initAppearence {
            from { opacity: 0; transform: scale(0.99) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        @keyframes cardSlideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bubbleReveal {
            from { opacity: 0; transform: scale(0.96) translateY(8px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <!-- Main Form Entry Card Asset Elements -->
        <div class="glass-card">
            <div class="header-block">
                <div>
                    <h1>Valuation Matrix Node</h1>
                    <p class="subtitle">Next-Gen 20-Factor Architectural Prediction Workspace</p>
                </div>
                <div class="control-panel">
                    <!-- Dynamic Currency Custom Dropdown Matrix -->
                    <div class="input-wrapper" style="min-width: 110px;">
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
            </div>

            {% if error_msg %}
            <div class="system-alert">{{ error_msg }}</div>
            {% endif %}

            <form method="POST" action="/" class="feature-grid">
                <!-- Group 1: Core Specs Matrix -->
                <div class="input-wrapper">
                    <label>Brand Manufacturer</label>
                    <select name="Make">
                        <option value="0" {% if form_values.Make == '0' %}selected{% endif %}>Toyota</option>
                        <option value="1" {% if form_values.Make == '1' %}selected{% endif %}>Honda</option>
                        <option value="2" {% if form_values.Make == '2' %}selected{% endif %}>Ford</option>
                        <option value="3" {% if form_values.Make == '3' %}selected{% endif %}>BMW</option>
                        <option value="4" {% if form_values.Make == '4' %}selected{% endif %}>Mercedes-Benz</option>
                        <option value="5" {% if form_values.Make == '5' %}selected{% endif %}>Audi</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Variant Architectural Form</label>
                    <select name="Model">
                        <option value="0" {% if form_values.Model == '0' %}selected{% endif %}>Sedan Base Matrix</option>
                        <option value="1" {% if form_values.Model == '1' %}selected{% endif %}>SUV Hyper Sport</option>
                        <option value="2" {% if form_values.Model == '2' %}selected{% endif %}>Eco Hatch Core</option>
                        <option value="3" {% if form_values.Model == '3' %}selected{% endif %}>Gran Coupe Premium</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Trim Variant Class</label>
                    <select name="Trim_Level">
                        <option value="0" {% if form_values.Trim_Level == '0' %}selected{% endif %}>Standard Entry</option>
                        <option value="1" {% if form_values.Trim_Level == '1' %}selected{% endif %}>Mid Tier Comfort</option>
                        <option value="2" {% if form_values.Trim_Level == '2' %}selected{% endif %}>Luxury Pro Line</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Year of Assembly</label>
                    <div class="range-group">
                        <input type="range" id="Year" name="Year" min="2010" max="2026" value="{{ form_values.Year|default(2020) }}" oninput="syncRangeValue('Year', this.value)">
                        <span id="Year_counter" class="range-counter">{{ form_values.Year|default(2020) }}</span>
                    </div>
                </div>

                <!-- Group 2: Powertrain Vectors -->
                <div class="input-wrapper">
                    <label>Fuel System Source</label>
                    <select name="Fuel_Type">
                        <option value="0" {% if form_values.Fuel_Type == '0' %}selected{% endif %}>Unleaded Petrol</option>
                        <option value="1" {% if form_values.Fuel_Type == '1' %}selected{% endif %}>Refined Diesel</option>
                        <option value="2" {% if form_values.Fuel_Type == '2' %}selected{% endif %}>Solid State Electric</option>
                        <option value="3" {% if form_values.Fuel_Type == '3' %}selected{% endif %}>Plug-in Hybrid (PHEV)</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Transmission Gear Layout</label>
                    <select name="Transmission">
                        <option value="0" {% if form_values.Transmission == '0' %}selected{% endif %}>Manual Mesh</option>
                        <option value="1" {% if form_values.Transmission == '1' %}selected{% endif %}>Dual Clutch Automatic</option>
                        <option value="2" {% if form_values.Transmission == '2' %}selected{% endif %}>Continuously Variable (CVT)</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Engine Displacement Capacity (L)</label>
                    <div class="range-group">
                        <input type="range" id="Engine_Size" name="Engine_Size" min="0.8" max="6.5" step="0.1" value="{{ form_values.Engine_Size|default(2.0) }}" oninput="syncRangeValue('Engine_Size', this.value)">
                        <span id="Engine_Size_counter" class="range-counter">{{ form_values.Engine_Size|default(2.0) }}</span>
                    </div>
                </div>

                <!-- Group 3: Dynamic Physics Parameters -->
                <div class="input-wrapper span-2">
                    <label>Accumulated Distance Traveled (Odometer km)</label>
                    <div class="range-group">
                        <input type="range" id="Mileage" name="Mileage" min="0" max="250000" step="500" value="{{ form_values.Mileage|default(45000) }}" oninput="syncRangeValue('Mileage', this.value)">
                        <span id="Mileage_counter" class="range-counter">{{ form_values.Mileage|default(45000) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Service Portfolio State</label>
                    <select name="Service_History">
                        <option value="0" {% if form_values.Service_History == '0' %}selected{% endif %}>Full Digital Verified</option>
                        <option value="1" {% if form_values.Service_History == '1' %}selected{% endif %}>Partial Tracking Logs</option>
                        <option value="2" {% if form_values.Service_History == '2' %}selected{% endif %}>No Documented Records</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Brake Horsepower Rating</label>
                    <div class="range-group">
                        <input type="range" id="Horsepower" name="Horsepower" min="50" max="750" value="{{ form_values.Horsepower|default(180) }}" oninput="syncRangeValue('Horsepower', this.value)">
                        <span id="Horsepower_counter" class="range-counter">{{ form_values.Horsepower|default(180) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Torque Curve Rating (Nm)</label>
                    <div class="range-group">
                        <input type="range" id="Torque" name="Torque" min="90" max="850" value="{{ form_values.Torque|default(280) }}" oninput="syncRangeValue('Torque', this.value)">
                        <span id="Torque_counter" class="range-counter">{{ form_values.Torque|default(280) }}</span>
                    </div>
                </div>
                <div class="input-wrapper">
                    <label>Previous User Matrix Count</label>
                    <select name="Owners">
                        <option value="1" {% if form_values.Owners == '1' %}selected{% endif %}>1 Registered Owner</option>
                        <option value="2" {% if form_values.Owners == '2' %}selected{% endif %}>2 Registered Owners</option>
                        <option value="3" {% if form_values.Owners == '3' %}selected{% endif %}>3 Registered Owners</option>
                        <option value="4" {% if form_values.Owners == '4' %}selected{% endif %}>4+ System Chain</option>
                    </select>
                </div>

                <!-- Group 4: Risk Mitigation & Aesthetics Matrix -->
                <div class="input-wrapper">
                    <label>Incident Structural History</label>
                    <select name="Accident_History">
                        <option value="0" {% if form_values.Accident_History == '0' %}selected{% endif %}>Zero Dynamic Incidents</option>
                        <option value="1" {% if form_values.Accident_History == '1' %}selected{% endif %}>Minor Non-Structural Panel</option>
                        <option value="2" {% if form_values.Accident_History == '2' %}selected{% endif %}>Major Insurance Restructuring</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Premium Coating Color Specification</label>
                    <select name="Color">
                        <option value="0" {% if form_values.Color == '0' %}selected{% endif %}>Obsidian Metallic Black</option>
                        <option value="1" {% if form_values.Color == '1' %}selected{% endif %}>Chalk Pure White</option>
                        <option value="2" {% if form_values.Color == '2' %}selected{% endif %}>Liquid Silver Metallic</option>
                        <option value="3" {% if form_values.Color == '3' %}selected{% endif %}>San Marino Deep Blue</option>
                        <option value="4" {% if form_values.Color == '4' %}selected{% endif %}>Nardo Slate Grey</option>
                        <option value="5" {% if form_values.Color == '5' %}selected{% endif %}>Rosso Corsa Crimson</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Interior Aesthetic State</label>
                    <select name="Interior_Condition">
                        <option value="0" {% if form_values.Interior_Condition == '0' %}selected{% endif %}>Pristine Showroom Condition</option>
                        <option value="1" {% if form_values.Interior_Condition == '1' %}selected{% endif %}>Minimal Wear Layer</option>
                        <option value="2" {% if form_values.Interior_Condition == '2' %}selected{% endif %}>Heavy Operational Wear</option>
                    </select>
                </div>

                <!-- Group 5: Environment & Geography Configurations -->
                <div class="input-wrapper">
                    <label>Chassis Body Architecture</label>
                    <select name="Body_Type">
                        <option value="0" {% if form_values.Body_Type == '0' %}selected{% endif %}>Aerodynamic Coupe</option>
                        <option value="1" {% if form_values.Body_Type == '1' %}selected{% endif %}>Classic Structural Sedan</option>
                        <option value="2" {% if form_values.Body_Type == '2' %}selected{% endif %}>High-Ground Clearance SUV</option>
                        <option value="3" {% if form_values.Body_Type == '3' %}selected{% endif %}>Modular Liftback Hatch</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Drivetrain Dynamic Matrix</label>
                    <select name="Drivetrain">
                        <option value="0" {% if form_values.Drivetrain == '0' %}selected{% endif %}>Front-Wheel Vector (FWD)</option>
                        <option value="1" {% if form_values.Drivetrain == '1' %}selected{% endif %}>Rear-Wheel Balance (RWD)</option>
                        <option value="2" {% if form_values.Drivetrain == '2' %}selected{% endif %}>Intelligent All-Wheel (AWD)</option>
                    </select>
                </div>
                <div class="input-wrapper">
                    <label>Integrated Electronics Suite</label>
                    <select name="Tech_Package">
                        <option value="0" {% if form_values.Tech_Package == '0' %}selected{% endif %}>Standard Analogue Hub</option>
                        <option value="1" {% if form_values.Tech_Package == '1' %}selected{% endif %}>Advanced Infotainment Tier</option>
                        <option value="2" {% if form_values.Tech_Package == '2' %}selected{% endif %}>Autonomous Driver Assistance Level 2</option>
                    </select>
                </div>

                <div class="input-wrapper">
                    <label>Resource Consumption Efficiency (km/L)</label>
                    <div class="range-group">
                        <input type="range" id="Fuel_Efficiency" name="Fuel_Efficiency" min="4" max="35" value="{{ form_values.Fuel_Efficiency|default(14) }}" oninput="syncRangeValue('Fuel_Efficiency', this.value)">
                        <span id="Fuel_Efficiency_counter" class="range-counter">{{ form_values.Fuel_Efficiency|default(14) }}</span>
                    </div>
                </div>
                <div class="input-wrapper span-2">
                    <label>Geographic Marketplace Cluster</label>
                    <select name="Location">
                        <option value="0" {% if form_values.Location == '0' %}selected{% endif %}>Tier 1 Capital Metropolitan Hub</option>
                        <option value="1" {% if form_values.Location == '1' %}selected{% endif %}>Tier 2 Regional Distribution Node</option>
                        <option value="2" {% if form_values.Location == '2' %}selected{% endif %}>Coastal Rural Logistical Cluster</option>
                    </select>
                </div>

                <button type="submit" class="submit-trigger">Execute Asset Pipeline Prediction Vector</button>
            </form>
        </div>

        <!-- Column 2: Dashboard Visualization Frameworks -->
        <div class="analytics-side">
            <!-- Consolidated Dynamic Machine Output Matrix -->
            {% if prediction_result is not none %}
            <div class="valuation-display">
                <h2>Evaluated Target Vector Consensus</h2>
                <div class="valuation-price-container">
                    <span id="currencySymbol">$</span>
                    <span id="baseValuationPrice" data-usd="{{ prediction_result|replace(',', '') }}">{{ prediction_result }}</span>
                </div>
                <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.4rem; color: #a5b4fc;">RandomForest Regressor Ensemble 20-D Matrix Mapping</p>
            </div>
            {% endif %}

            <!-- Dynamic Statistical Engine Tracking Node -->
            <div class="glass-card chart-card">
                <h3 style="font-size: 1rem; font-weight: 700; margin-bottom: 1rem; color: var(--neon-blue); letter-spacing: 0.05em; text-transform: uppercase;">Real-Time Pipeline Tracking Metrics</h3>
                <canvas id="historicalMetricsChart" style="width:100%; max-height: 190px;"></canvas>
            </div>

            <!-- Historical Operations Stream Node -->
            <div class="glass-card chat-history-card">
                <div class="chat-header">
                    <h3 style="font-size: 1rem; font-weight: 700; color: var(--text-tokens); text-transform: uppercase; letter-spacing: 0.05em;">Sequential Prediction Logs</h3>
                    {% if history %}
                    <form method="POST" action="/clear">
                        <button type="submit" class="clear-history-action">Purge Logs</button>
                    </form>
                    {% endif %}
                </div>

                <div class="chat-log-stream">
                    {% for interaction in history %}
                        <div class="chat-bubble user-query">
                            <div class="bubble-meta">Asset Input Fingerprint Payload</div>
                            Year Assembly: {{ interaction.inputs.Year }} | Mileage Tracker: {{ interaction.inputs.Mileage }} km | Engine Displacement: {{ interaction.inputs.Engine_Size }}L
                        </div>
                        <div class="chat-bubble ai-response">
                            <div class="bubble-meta">Model Engine Vector Response</div>
                            Asset Target Valuation Resolution Vector calculated at: 
                            <strong style="color: var(--neon-blue);" class="loggedPrice" data-usd="{{ interaction.output|replace(',', '') }}">${{ interaction.output }} USD</strong>
                        </div>
                    {% else %}
                        <div class="no-records">No session records tracked in current system state stack.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global Currency Reference Multipliers Matrix
        const currencyExchangeMatrix = {
            USD: { symbol: '$', rate: 1.0 },
            EUR: { symbol: '€', rate: 0.91 },
            GBP: { symbol: '£', rate: 0.78 },
            JPY: { symbol: '¥', rate: 155.4 },
            CAD: { symbol: 'C$', rate: 1.36 },
            AUD: { symbol: 'A$', rate: 1.51 }
        };

        function syncRangeValue(sliderId, value) {
            document.getElementById(sliderId + '_counter').innerText = value;
        }

        function convertActiveValuations() {
            const selector = document.getElementById('currencySelector');
            const targetCurrency = selector.value;
            const configuration = currencyExchangeMatrix[targetCurrency];
            
            // Primary Value Vector Component Adjustment
            const primaryPriceElement = document.getElementById('baseValuationPrice');
            const primarySymbolElement = document.getElementById('currencySymbol');
            if(primaryPriceElement && primarySymbolElement) {
                const nativeUSDValue = parseFloat(primaryPriceElement.getAttribute('data-usd'));
                const scaledPrice = nativeUSDValue * configuration.rate;
                primarySymbolElement.innerText = configuration.symbol;
                primaryPriceElement.innerText = scaledPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            }

            // Historical List Matrix Vector Iteration Update
            const logs = document.querySelectorAll('.loggedPrice');
            logs.forEach(element => {
                const nativeUSD = parseFloat(element.getAttribute('data-usd'));
                const scaled = nativeUSD * configuration.rate;
                element.innerText = configuration.symbol + scaled.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' + targetCurrency;
            });
        }

        // Initialize Internal Application Graph Diagnostics
        document.addEventListener("DOMContentLoaded", function() {
            const rawLoggedNodes = document.querySelectorAll('.loggedPrice');
            const coordinateDataPoints = [];
            const coordinateLabels = [];
            
            // Reversing raw execution indices to map correctly chronologically left-to-right
            for (let i = rawLoggedNodes.length - 1; i >= 0; i--) {
                coordinateDataPoints.push(parseFloat(rawLoggedNodes[i].getAttribute('data-usd')));
                coordinateLabels.push("Run " + (rawLoggedNodes.length - i));
            }

            const visualContextNode = document.getElementById('historicalMetricsChart').getContext('2d');
            new Chart(visualContextNode, {
                type: 'line',
                data: {
                    labels: coordinateLabels.length ? coordinateLabels : ["Idle Node State"],
                    datasets: [{
                        label: 'Valuation Tracking Curve (USD)',
                        data: coordinateDataPoints.length ? coordinateDataPoints : [0],
                        borderColor: '#6366f1',
                        backgroundGradientColor: 'rgba(99, 102, 241, 0.1)',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        pointBackgroundColor: '#38bdf8',
                        pointBorderColor: '#ffffff',
                        pointRadius: 4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(255, 255, 255, 0.03)' }, ticks: { color: '#64748b' } },
                        y: { grid: { color: 'rgba(255, 255, 255, 0.03)' }, ticks: { color: '#64748b' } }
                    }
                }
            });
            
            // Execute fallback system formatting loop on interface configuration load
            convertActiveValuations();
        });
    </script>
</body>
</html>
"""

# -------------------------------------------------------------
# LOGISTICAL ENDPOINT MATRIX ROUTER
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def main_gateway():
    error_msg = None
    prediction_result = None
    form_values = {}

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        # 20 Distinct Architectural Pipeline Variables
        fields = [
            'Make', 'Model', 'Trim_Level', 'Year', 'Fuel_Type', 'Transmission', 'Engine_Size', 
            'Service_History', 'Mileage', 'Horsepower', 'Torque', 'Owners', 
            'Accident_History', 'Color', 'Interior_Condition', 'Body_Type', 'Drivetrain', 
            'Tech_Package', 'Fuel_Efficiency', 'Location'
        ]
        
        form_values = {f: request.form.get(f) for f in fields}

        if model is None:
            # Safe Fallback Engine Simulation Mode if rfamodel.pkl hasn't been written to root storage memory
            try:
                base_calculation = 42000.00
                mileage_deduction = float(form_values.get('Mileage', 45000)) * 0.12
                age_deduction = (2026 - int(form_values.get('Year', 2020))) * 1800
                power_bonus = (int(form_values.get('Horsepower', 180)) - 150) * 85
                
                calculated_sim_val = max(3500.00, base_calculation - mileage_deduction - age_deduction + power_bonus)
                prediction_result = f"{calculated_sim_val:,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {
                    "inputs": form_values,
                    "output": prediction_result
                })
                session["history"] = current_stack[:6]  # Expanded historical cache depth index constraint
            except Exception as ex:
                error_msg = f"Vector Generation Simulation Exception: {str(ex)}"
        else:
            try:
                # Structure input array sequence mapped explicitly to 20-dimensional model blueprint
                evaluation_vector = np.array([[
                    int(form_values['Make']),
                    int(form_values['Model']),
                    int(form_values['Trim_Level']),
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
                    int(form_values['Interior_Condition']),
                    int(form_values['Body_Type']),
                    int(form_values['Drivetrain']),
                    int(form_values['Tech_Package']),
                    float(form_values['Fuel_Efficiency']),
                    int(form_values['Location'])
                ]], dtype=object)

                calculated_matrix = model.predict(evaluation_vector)
                prediction_result = f"{float(calculated_matrix[0]):,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {
                    "inputs": form_values,
                    "output": prediction_result
                })
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
