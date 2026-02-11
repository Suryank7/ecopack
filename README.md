# EcoPackAI - Sustainable Packaging Recommendation System

AI-powered platform to recommend eco-friendly packaging materials based on sustainability metrics.

## Features

- **Data Processing**: Cleans and engineers features from 5,000+ material records
- **ML Models**: Predicts CO2 emissions and cost efficiency (R² > 97%)
- **Database**: PostgreSQL integration for scalable data storage
- **Visualizations**: Performance charts and material comparisons

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline

```bash
# Process data
python process_data.py

# Train models
python train_models.py

# Load to database (optional)
python load_to_db.py

# Generate reports
python evaluate_models.py
```

### 3. Database Setup (Optional)

1. Install PostgreSQL
2. Create database: `CREATE DATABASE ecopack_db;`
3. Copy `.env.example` to `.env` and add credentials
4. Run `python load_to_db.py`

## Project Structure

```
EcoPackAI/
├── process_data.py          # Data processing and feature engineering
├── train_models.py          # Model training (RF, XGBoost, LightGBM, CatBoost)
├── load_to_db.py            # PostgreSQL data loading
├── evaluate_models.py       # Model evaluation and visualization
├── schema.sql               # Database schema
├── models/                  # Trained models
├── reports/                 # Generated charts
└── requirements.txt         # Python dependencies
```

## Model Performance

| Model | CO2 R² | Cost Efficiency R² |
|-------|--------|-------------------|
| Random Forest | 0.9693 | 0.9988 |
| XGBoost | 0.9703 | 0.9988 |
| **LightGBM** | **0.9703** | **0.9993** |
| CatBoost | 0.9693 | 0.9988 |

## Top Sustainable Materials

1. Mushroom Mycelium
2. Seaweed-Based Packaging
3. Bamboo Fiber
4. Recycled Paper
5. Bioplastic (PLA)

## Dataset--

Source: Ecopack Sustainable Packaging Dataset (5,000 materials)

**Features:**
- Material Type
- Tensile Strength
- Weight Capacity
- Biodegradability Score
- CO2 Emission Score
- Recyclability Percentage
- Moisture Barrier Grade

## License

MIT License

## Contributing

Pull requests welcome. For major changes, please open an issue first.
