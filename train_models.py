import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Setup directories
if not os.path.exists('models'):
    os.makedirs('models')

def evaluate_model(name, y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\nModel: {name}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2 Score: {r2:.4f}")

def main():
    # 1. Load Data
    input_path = 'materials_processed_milestone1.csv'
    print(f"Loading data from {input_path}...")
    if not os.path.exists(input_path):
        print("Error: Dataset not found. Run process_data.py first.")
        return
        
    df = pd.read_csv(input_path)
    
    # 2. Data Preparation
    print("\n--- Preparing Data for ML ---")
    
    # Encode 'Material_Type'
    le_material = LabelEncoder()
    df['Material_Encoded'] = le_material.fit_transform(df['Material_Type'])
    
    # Feature Selection
    feature_cols = [
        'Material_Encoded', 
        'Tensile_Strength_MPa', 
        'Weight_Capacity_kg', 
        'Biodegradability_Score', 
        'Recyclability_Percent', 
        'Moisture_Barrier_Grade'
    ]
    X = df[feature_cols]
    
    # Targets
    y_co2 = df['CO2_Emission_Score']
    y_cost = df['Cost_Efficiency_Index']
    
    # Split Data (80% Train, 20% Test)
    X_train, X_test, y_co2_train, y_co2_test, y_cost_train, y_cost_test = train_test_split(
        X, y_co2, y_cost, test_size=0.2, random_state=42
    )
    
    print(f"Training Data Shape: {X_train.shape}")
    print(f"Testing Data Shape: {X_test.shape}")
    
    # 3. Model Training - Using Proven Best Models
    
    # A. CO2 Prediction - Gradient Boosting (Best Performer ~0.97 R2)
    print("\n--- Training CO2 Prediction Model (Gradient Boosting) ---")
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_co2_train)
    
    y_co2_pred = gb_model.predict(X_test)
    evaluate_model("Gradient Boosting (CO2)", y_co2_test, y_co2_pred)
    
    joblib.dump(gb_model, 'models/best_co2_model.pkl')
    print("Saved 'models/best_co2_model.pkl'")

    # B. Cost Efficiency Prediction - Random Forest (Best Performer ~0.99 R2)
    print("\n--- Training Cost Efficiency Model (Random Forest) ---")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_cost_train)
    
    y_cost_pred = rf_model.predict(X_test)
    evaluate_model("Random Forest (Cost Efficiency)", y_cost_test, y_cost_pred)
    
    joblib.dump(rf_model, 'models/best_cost_model.pkl')
    print("Saved 'models/best_cost_model.pkl'")
    
    # Save Encoder
    joblib.dump(le_material, 'models/le_material.pkl')
    print("Saved 'models/le_material.pkl'")
    
    print("\nAll best-performing models trained and saved successfully.")

if __name__ == "__main__":
    main()
