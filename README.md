# EcoPackAI - Sustainable Packaging Recommendation System

EcoPackAI is an AI-powered platform designed to recommend optimal eco-friendly packaging materials based on product attributes, sustainability parameters, and cost efficiency.

## Project Structure
*   `app.py`: Main Flask application (Backend API & Routing).
*   `templates/`: HTML files (`home.html`, `index.html`) for the frontend.
*   `static/`: CSS styling, JavaScript logic, and assets.
*   `utils/model.py`: Core logic including Physics Simulation and ML Predictions.
*   `models/`: Directory where trained ML models are saved.
*   `train_models.py`: Script for training the AI models.
*   `process_data.py`: Script for data cleaning and feature engineering.

## Prerequisites
Ensure have Python installed. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

### Step 1: Start the Server
Launch the Flask application:

```bash
python app.py
```

### Step 2: Use the Application
1.  Open your browser and go to `http://127.0.0.1:5000/`.
2.  Click **"Get Started"** on the landing page.
3.  Open the **Sidebar Menu (☰)** in the top-left.
4.  Enter product details (Weight, Fragility, Shelf Life).
5.  Click **"Find Best Material"** to see AI recommendations.

---

## Key Features (Week 6 Update)

### 🧠 Physics-Based Expert System
The AI now understands physics. It creates dynamic material recommendations based on:
*   **Weight vs. Strength:** Heavy items get strong materials (Aluminum, Wood). Light items get sustainable ones (Mushroom, Bio).
*   **Shelf Life:** Perishable goods get moisture-resistant packaging.
*   **Eco-Bonus:** Sustainable materials like Cardboard get a boost for standard use cases.

### 🎨 Premium UI/UX (Overhaul)
*   **Light Mode Theme:** Fresh Mint & Emerald color palette.
*   **Animated Landing Page:** with floating leaf effects.
*   **Visualizations:** Radar Charts, Cost/CO2 Bar Charts, and Suitability Pie Charts.

## Project Status
*   ✅ **Milestone 1:** Data Foundation.
*   ✅ **Milestone 2:** AI Models (Cost & CO2).
*   ✅ **Milestone 3:** Flask API (Backend).
*   ✅ **Milestone 4 & 5:** Frontend Dashboard (UI).
*   ✅ **Milestone 6:** Physics Logic & Expert System (Final Polish).
