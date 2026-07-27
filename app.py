import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template_string

# Initialize Flask Application for AWS WSGI / Gunicorn compatibility
app = Flask(__name__)
application = app

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Resolution logic to automatically load the model pkl file
MODEL_PATH = None
for filename in os.listdir(CURRENT_DIR):
    if filename.endswith("rfamodel.pkl"):
        MODEL_PATH = os.path.join(CURRENT_DIR, filename)
        break

model = None
if MODEL_PATH:
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print(f"Model loaded successfully from: {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")

# Global Multi-Currency Conversion Matrix (Assuming Base Model trains on USD values)
CURRENCY_MAP = {
    "USD": {"symbol": "$", "rate": 1.0},
    "EUR": {"symbol": "€", "rate": 0.92},
    "GBP": {"symbol": "£", "rate": 0.78},
    "INR": {"symbol": "₹", "rate": 83.50}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="emerald">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insurance Charges Estimator | AI Decision Engine</title>
    <!-- Google Fonts, FontAwesome, jsPDF, and Chart.js -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        [data-theme="emerald"] {
            --bg-dark: #02120a;
            --card-glass: rgba(6, 30, 18, 0.75);
            --card-border: rgba(16, 185, 129, 0.25);
            --primary-glow: #10b981;
            --primary-bright: #34d399;
            --primary-dim: rgba(16, 185, 129, 0.15);
        }

        [data-theme="cyberpunk"] {
            --bg-dark: #030712;
            --card-glass: rgba(15, 23, 42, 0.75);
            --card-border: rgba(0, 242, 254, 0.25);
            --primary-glow: #00f2fe;
            --primary-bright: #38bdf8;
            --primary-dim: rgba(0, 242, 254, 0.15);
        }

        [data-theme="amber"] {
            --bg-dark: #0a0d14;
            --card-glass: rgba(18, 24, 38, 0.75);
            --card-border: rgba(245, 158, 11, 0.25);
            --primary-glow: #f59e0b;
            --primary-bright: #fbbf24;
            --primary-dim: rgba(245, 158, 11, 0.15);
        }

        [data-theme="frost"] {
            --bg-dark: #0f172a;
            --card-glass: rgba(30, 41, 59, 0.75);
            --card-border: rgba(129, 140, 248, 0.25);
            --primary-glow: #818cf8;
            --primary-bright: #a5b4fc;
            --primary-dim: rgba(129, 140, 248, 0.15);
        }

        [data-theme="crimson"] {
            --bg-dark: #120307;
            --card-glass: rgba(30, 8, 15, 0.75);
            --card-border: rgba(244, 63, 94, 0.25);
            --primary-glow: #f43f5e;
            --primary-bright: #fb7185;
            --primary-dim: rgba(244, 63, 94, 0.15);
        }

        :root {
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --input-bg: rgba(10, 13, 20, 0.65);
            --input-border: rgba(255, 255, 255, 0.1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        .ambient-orb {
            position: fixed;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            filter: blur(140px);
            z-index: -1;
            opacity: 0.25;
            pointer-events: none;
            animation: pulseOrb 8s infinite alternate ease-in-out;
        }
        .orb-1 { top: -200px; right: -100px; background: var(--primary-glow); }
        .orb-2 { bottom: -200px; left: -100px; background: var(--primary-glow); animation-delay: -4s; }

        @keyframes pulseOrb {
            0% { transform: scale(1) translate(0, 0); opacity: 0.2; }
            100% { transform: scale(1.15) translate(-30px, 30px); opacity: 0.3; }
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 6%;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(10, 13, 20, 0.8);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .brand-logo {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--primary-glow), var(--primary-bright));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0a0d14;
            font-size: 1.2rem;
            box-shadow: 0 0 20px var(--primary-dim);
        }

        .theme-switcher {
            display: flex;
            gap: 8px;
            background: rgba(255, 255, 255, 0.04);
            padding: 6px 10px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .theme-btn {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .theme-btn.active {
            border-color: #ffffff;
            transform: scale(1.2);
        }

        .theme-matrix { background: #10b981; }
        .theme-cyber { background: #00f2fe; }
        .theme-amber { background: #f59e0b; }
        .theme-frost { background: #818cf8; }
        .theme-crimson { background: #f43f5e; }

        .workspace-container {
            max-width: 1400px;
            margin: 35px auto;
            padding: 0 4%;
            width: 100%;
            flex-grow: 1;
        }

        .header-section {
            text-align: center;
            margin-bottom: 38px;
        }

        .title-badge {
            display: inline-block;
            padding: 6px 18px;
            background: var(--primary-dim);
            border: 1px solid var(--primary-glow);
            border-radius: 30px;
            color: var(--primary-bright);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
        }

        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #ffffff 0%, var(--primary-bright) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .main-subtitle {
            color: var(--text-sub);
            font-size: 1.02rem;
            max-width: 650px;
            margin: 0 auto;
        }

        .grid-layout {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 32px;
            align-items: start;
        }

        .sticky-sidebar {
            position: sticky;
            top: 110px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .glass-card {
            background: var(--card-glass);
            border-radius: 28px;
            border: 1px solid var(--card-border);
            padding: 34px;
            backdrop-filter: blur(24px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        }

        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-title i {
            color: var(--primary-glow);
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .span-2 { grid-column: span 2; }

        label {
            font-size: 0.82rem;
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        .live-val {
            font-family: 'JetBrains Mono', monospace;
            color: var(--primary-bright);
            font-weight: 700;
        }

        input, select {
            width: 100%;
            padding: 13px 15px;
            background-color: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            color: var(--text-main);
            font-size: 0.92rem;
            font-weight: 500;
            transition: all 0.25s ease;
        }

        select {
            appearance: none;
            cursor: pointer;
            padding-right: 36px;
        }

        .select-wrapper {
            position: relative;
        }

        .select-wrapper::after {
            content: '\\f107';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-sub);
            pointer-events: none;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--primary-glow);
            box-shadow: 0 0 0 4px var(--primary-dim);
            background-color: rgba(10, 13, 20, 0.9);
        }

        .btn-predict {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, var(--primary-glow) 0%, var(--primary-bright) 100%);
            color: #0a0d14;
            font-weight: 800;
            font-size: 1.05rem;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-top: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            box-shadow: 0 10px 30px var(--primary-dim);
        }

        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px var(--primary-dim);
            color: #ffffff;
        }

        .valuation-card {
            background: linear-gradient(180deg, var(--primary-dim) 0%, rgba(10, 13, 20, 0.05) 100%);
            border: 1px solid var(--primary-glow);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
        }

        .val-tag {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-sub);
            font-weight: 700;
            margin-bottom: 6px;
        }

        .val-price {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 8px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .chart-box {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            height: 200px;
        }

        /* Person History Stream (Chat Presentation) */
        .chat-stream {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 250px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .chat-stream::-webkit-scrollbar { width: 4px; }
        .chat-stream::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

        .chat-msg {
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 16px;
            font-size: 0.88rem;
            line-height: 1.4;
            display: flex;
            flex-direction: column;
            gap: 4px;
            animation: messageFade 0.4s ease;
        }

        @keyframes messageFade {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .chat-msg.user {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .chat-msg.ai {
            background: var(--primary-dim);
            border: 1px solid var(--card-border);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .msg-meta {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-sub);
            font-weight: 700;
        }

        .msg-badges {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-top: 2px;
        }

        .badge-pill {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 0.75rem;
            color: var(--text-main);
            font-weight: 600;
        }

        .btn-report {
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.88rem;
            cursor: pointer;
            margin-top: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.25s ease;
        }

        .btn-report:hover {
            background: var(--primary-dim);
            border-color: var(--primary-glow);
            color: var(--primary-bright);
        }

        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(10, 13, 20, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        footer {
            text-align: center;
            padding: 24px;
            color: var(--text-sub);
            font-size: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            margin-top: auto;
        }

        @media (max-width: 1024px) {
            .grid-layout { grid-template-columns: 1fr; }
            .form-grid { grid-template-columns: 1fr; }
            .sticky-sidebar { position: static; }
        }
    </style>
</head>
<body>

<div class="ambient-orb orb-1"></div>
<div class="ambient-orb orb-2"></div>

<nav class="navbar">
    <div class="brand">
        <div class="brand-logo"><i class="fa-solid fa-notes-medical"></i></div>
        <span>MedicalCharges<span style="color: var(--primary-glow);">.ai</span></span>
    </div>
   
    <div style="display: flex; align-items: center; gap: 14px;">
        <div class="theme-switcher">
            <button class="theme-btn theme-matrix active" onclick="switchTheme('emerald')"></button>
            <button class="theme-btn theme-cyber" onclick="switchTheme('cyberpunk')"></button>
            <button class="theme-btn theme-amber" onclick="switchTheme('amber')"></button>
            <button class="theme-btn theme-frost" onclick="switchTheme('frost')"></button>
            <button class="theme-btn theme-crimson" onclick="switchTheme('crimson')"></button>
        </div>
    </div>
</nav>

<div class="workspace-container">
    <div class="header-section">
        <span class="title-badge">Decision Tree Regressor</span>
        <h1 class="main-title">Insurance Charges Estimator</h1>
        <p class="main-subtitle">Predict medical insurance costs in real-time based on individual health parameters.</p>
    </div>

    <div class="grid-layout">
        <!-- Input Form -->
        <div class="glass-card">
            <div class="section-header">
                <span class="section-title"><i class="fa-solid fa-sliders"></i> Medical Attributes</span>
                <span style="font-size: 0.8rem; color: var(--text-sub);">Insurance Dataset</span>
            </div>
           
            <form id="predictionForm">
                <div class="form-grid">
                   
                    <div class="form-group">
                        <label>Age <span class="live-val" id="ageVal">30</span></label>
                        <input type="number" name="age" value="30" min="18" max="100" required oninput="document.getElementById('ageVal').textContent = this.value">
                    </div>

                    <div class="form-group">
                        <label>Sex</label>
                        <div class="select-wrapper">
                            <select name="sex" required>
                                <option value="female" selected>Female</option>
                                <option value="male">Male</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>BMI (Body Mass Index) <span class="live-val" id="bmiVal">25.0</span></label>
                        <input type="number" name="bmi" value="25.0" step="0.1" min="10" max="60" required oninput="document.getElementById('bmiVal').textContent = parseFloat(this.value).toFixed(1)">
                    </div>

                    <div class="form-group">
                        <label>Children Count <span class="live-val" id="childVal">0</span></label>
                        <input type="number" name="children" value="0" min="0" max="10" required oninput="document.getElementById('childVal').textContent = this.value">
                    </div>

                    <div class="form-group">
                        <label>Smoker Status</label>
                        <div class="select-wrapper">
                            <select name="smoker" required>
                                <option value="no" selected>No</option>
                                <option value="yes">Yes</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Geographic Region</label>
                        <div class="select-wrapper">
                            <select name="region" required>
                                <option value="northwest" selected>Northwest</option>
                                <option value="northeast">Northeast</option>
                                <option value="southeast">Southeast</option>
                                <option value="southwest">Southwest</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group span-2">
                        <label>Output Base Currency</label>
                        <div class="select-wrapper">
                            <select id="currency" name="currency" onchange="updateCurrencyUI()">
                                <option value="USD" selected>USD ($) - United States Dollar</option>
                                <option value="EUR">EUR (€) - Eurozone</option>
                                <option value="GBP">GBP (£) - United Kingdom</option>
                                <option value="INR">INR (₹) - Indian Rupee</option>
                            </select>
                        </div>
                    </div>

                </div>

                <button type="submit" class="btn-predict" id="submitBtn">
                    <span class="btn-text">Estimate Medical Charges</span>
                    <div class="spinner" id="btnSpinner"></div>
                </button>
            </form>
        </div>

        <!-- Telemetry Sidebar -->
        <div class="sticky-sidebar" id="outputSection">
            <div class="glass-card">
                <div class="section-header">
                    <span class="section-title"><i class="fa-solid fa-calculator"></i> Estimated Telemetry</span>
                </div>
               
                <div class="valuation-card" id="resultCard">
                    <div class="val-tag">Predicted Insurance Cost</div>
                    <div class="val-price">
                        <i class="fa-solid fa-file-invoice-dollar" id="resultIcon" style="color: var(--primary-glow);"></i>
                        <span id="resultOutput">$0.00</span>
                    </div>
                </div>

                <!-- Pie Chart Target Canvas Area -->
                <div class="chart-box">
                    <canvas id="riskAllocationChart"></canvas>
                </div>
            </div>

            <!-- Person History Stack (Chat Presentation Block) -->
            <div class="glass-card">
                <div class="section-header">
                    <span class="section-title"><i class="fa-solid fa-clock-rotate-left"></i> Person Audit Logs</span>
                    <button class="btn-reset" style="background:none; border:none; text-decoration:underline; color:var(--text-sub); font-size:0.8rem; cursor:pointer;" onclick="flushChatMemory()">Clear</button>
                </div>
                
                <div class="chat-stream" id="chatFeed">
                    <div style="text-align: center; color: var(--text-sub); font-size: 0.85rem; margin: auto; padding: 1rem 0;" id="emptyFeedText">
                        No previous runs parsed in current stack session.
                    </div>
                </div>

                <button type="button" class="btn-report" onclick="downloadPDFReport()">
                    <i class="fa-solid fa-file-pdf"></i> Download Brief
                </button>
            </div>
        </div>

    </div>
</div>

<footer>&copy; 2026 Insurance Cost Predictor &bull; DecisionTree Core Engine</footer>

<script>
    let rawUSDValue = 0.00;
    let currencySymbol = "$";
    let currencyRate = 1.0;
    let telemetryChart = null;

    // Multi-Currency Mapping Definitions
    const currencyMatrix = {
        "USD": { symbol: "$", rate: 1.0 },
        "EUR": { symbol: "€", rate: 0.92 },
        "GBP": { symbol: "£", rate: 0.78 },
        "INR": { symbol: "₹", rate: 83.50 }
    };

    function switchTheme(themeName) {
        document.documentElement.setAttribute('data-theme', themeName);
        document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
        let themeMap = { 'emerald': 'matrix', 'cyberpunk': 'cyber', 'amber': 'amber', 'frost': 'frost', 'crimson': 'crimson' };
        document.querySelector(`.theme-${themeMap[themeName]}`).classList.add('active');
        if(telemetryChart) {
            updateChartColors();
        }
    }

    function updateCurrencyUI() {
        const select = document.getElementById('currency');
        const activeConfig = currencyMatrix[select.value];
        currencySymbol = activeConfig.symbol;
        currencyRate = activeConfig.rate;
        
        const scaledVal = rawUSDValue * currencyRate;
        document.getElementById('resultOutput').textContent = currencySymbol + scaledVal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
    }

    // ChartJS Dynamic Color Engine matching framework configuration themes
    function getThemeColors() {
        const theme = document.documentElement.getAttribute('data-theme') || 'emerald';
        if (theme === 'cyberpunk') return ['#00f2fe', '#38bdf8', '#6366f1', '#1f2937'];
        if (theme === 'amber') return ['#f59e0b', '#fbbf24', '#4b5563', '#1f2937'];
        if (theme === 'frost') return ['#818cf8', '#a5b4fc', '#475569', '#1e293b'];
        if (theme === 'crimson') return ['#f43f5e', '#fb7185', '#3f111a', '#1c050c'];
        return ['#10b981', '#34d399', '#064e3b', '#0c2214']; // emerald / default
    }

    function renderTelemetryChart(age, bmi, smoker) {
        const ctx = document.getElementById('riskAllocationChart').getContext('2d');
        const colors = getThemeColors();

        const baseTier = 1500;
        const ageWeight = Math.max(500, parseInt(age) * 65);
        const bmiWeight = Math.max(400, parseFloat(bmi) * 55);
        const lifestylePremium = smoker === 'yes' ? 12000 : 200;

        if (telemetryChart) {
            telemetryChart.destroy();
        }

        telemetryChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Base Risk Tier', 'Age Progression Weight', 'Volumetric BMI Weight', 'Lifestyle Penalty Adjust'],
                datasets: [{
                    data: [baseTier, ageWeight, bmiWeight, lifestylePremium],
                    backgroundColor: colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8', boxWidth: 10, font: { family: 'Plus Jakarta Sans', size: 9 } }
                    }
                }
            }
        });
    }

    function updateChartColors() {
        const colors = getThemeColors();
        telemetryChart.data.datasets[0].backgroundColor = colors;
        telemetryChart.update();
    }

    document.getElementById('predictionForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const form = e.target;
        const submitBtn = document.getElementById('submitBtn');
        const spinner = document.getElementById('btnSpinner');
        const btnText = submitBtn.querySelector('.btn-text');
        const resultOutput = document.getElementById('resultOutput');
       
        submitBtn.disabled = true;
        spinner.style.display = 'block';
        btnText.textContent = 'Traversing Decision Tree...';
       
        try {
            const response = await fetch('/predict', { method: 'POST', body: new FormData(form) });
            const data = await response.json();
            
            if (data.status === 'success') {
                rawUSDValue = data.raw_value;
                updateCurrencyUI();
                
                // Hide default empty context state indicator text label
                const emptyTxt = document.getElementById('emptyFeedText');
                if(emptyTxt) emptyTxt.style.display = 'none';

                const ageInput = form.elements['age'].value;
                const bmiInput = parseFloat(form.elements['bmi'].value).toFixed(1);
                const smokerInput = form.elements['smoker'].value;

                // Push dynamic frame allocation vectors to chart renderer
                renderTelemetryChart(ageInput, bmiInput, smokerInput);
                
                // Push chat blocks directly to presentation history logs container element view
                appendChatMessagePair(ageInput, bmiInput, smokerInput, currencySymbol + (rawUSDValue * currencyRate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}));

            } else {
                resultOutput.textContent = 'Error: ' + data.message;
            }
        } catch (error) {
            resultOutput.textContent = error.message;
        } finally {
            submitBtn.disabled = false;
            spinner.style.display = 'none';
            btnText.textContent = 'Estimate Medical Charges';
        }
    });

    function appendChatMessagePair(age, bmi, smoker, parsedOutputPrice) {
        const feed = document.getElementById('chatFeed');
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        // Build User Message Prompt Bubble block structure dynamically
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-msg user';
        userBubble.innerHTML = `
            <span class="msg-meta">Parameters Requested &bull; ${timestamp}</span>
            <div class="msg-badges">
                <span class="badge-pill">Age: ${age}</span>
                <span class="badge-pill">BMI: ${bmi}</span>
                <span class="badge-pill">Smoker: ${smoker.toUpperCase()}</span>
            </div>
        `;

        // Build AI System Prediction response framing bubble node framework block matching topology
        const aiBubble = document.createElement('div');
        aiBubble.className = 'chat-msg ai';
        aiBubble.innerHTML = `
            <span class="msg-meta" style="color:var(--primary-bright);">Engine Inference Response</span>
            <div style="font-weight:600;">Prediction resolves evaluation to <span class="tag-price">${parsedOutputPrice}</span></div>
        `;

        feed.insertBefore(aiBubble, feed.firstChild);
        feed.insertBefore(userBubble, feed.firstChild);
    }

    function flushChatMemory() {
        const feed = document.getElementById('chatFeed');
        feed.innerHTML = `<div style="text-align: center; color: var(--text-sub); font-size: 0.85rem; margin: auto; padding: 1rem 0;" id="emptyFeedText">No previous runs parsed in current stack session.</div>`;
        rawUSDValue = 0.0;
        document.getElementById('resultOutput').textContent = currencySymbol + "0.00";
        if(telemetryChart) telemetryChart.destroy();
    }

    function downloadPDFReport() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const select = document.getElementById('currency');
        
        doc.setFont("helvetica", "bold");
        doc.setFontSize(20);
        doc.text("Insurance Cost Estimation Report", 20, 22);
        doc.setFontSize(10);
        doc.text("Runtime Date Boundary Frame: " + new Date().toLocaleString(), 20, 30);
        doc.line(20, 35, 190, 35);
        
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Active Frame Parameter Logs Considered:", 20, 48);
        doc.setFont("helvetica", "normal");
        doc.text("- Demographics Evaluation Age Group: " + document.getElementById('predictionForm').elements['age'].value + " Years Old", 25, 58);
        doc.text("- Body Mass Index Volumetric Weight: " + document.getElementById('predictionForm').elements['bmi'].value + " BMI", 25, 66);
        doc.text("- Selected Base Output Localized Unit: " + select.value, 25, 74);
        
        doc.line(20, 84, 190, 84);
        doc.setFontSize(15);
        doc.setFont("helvetica", "bold");
        doc.text("Calculated Premium Cost: " + document.getElementById('resultOutput').textContent, 20, 98);
        doc.save("Insurance_Telemetry_Audit_Brief.pdf");
    }
</script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'status': 'error', 'message': 'Decision Tree Regressor model not loaded.'}), 500
        
    try:
        # Standard alphabetical LabelEncoder mappings matching scikit-learn
        sex_map = {'female': 0, 'male': 1}
        smoker_map = {'no': 0, 'yes': 1}
        region_map = {'northeast': 0, 'northwest': 1, 'southeast': 2, 'southwest': 3}

        age = float(request.form['age'])
        sex = sex_map.get(str(request.form['sex']).strip().lower(), 0)
        bmi = float(request.form['bmi'])
        children = float(request.form['children'])
        smoker = smoker_map.get(str(request.form['smoker']).strip().lower(), 0)
        region = region_map.get(str(request.form['region']).strip().lower(), 0)

        # Match exact feature array order expected by the model
        features_df = pd.DataFrame({
            'age': [age],
            'sex': [sex],
            'bmi': [bmi],
            'children': [children],
            'smoker': [smoker],
            'region': [region]
        })

        raw_pred = float(model.predict(features_df)[0])

        return jsonify({
            'status': 'success',
            'raw_value': raw_pred
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# AWS Execution Listener listening on port 5000
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
