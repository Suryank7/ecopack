import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 1. Loading Data
file_path = 'Ecopack-dataset_Ecopack-dataset.csv'
print(f"Loading dataset from {file_path}...")
df = pd.read_csv(file_path)

print("Original Data Info:")
print(df.info())
print(df.head())

# 2. Data Cleaning 
print("\n--- Starting Data Cleaning ---")
# Check for missing values
missing_data = df.isnull().sum()
print("Missing Values:\n", missing_data)

# Impute numerical columns with median if needed (simulation)
# In our clean csv they might be full, but good practice to include
numerical_cols = df.select_dtypes(include=[np.number]).columns
for col in numerical_cols:
    if df[col].isnull().sum() > 0:
        print(f"Imputing missing values for {col}")
        df[col] = df[col].fillna(df[col].median())

# 3. Feature Engineering
print("\n--- Starting Feature Engineering ---")

# A. CO2 Impact Index
# Inverse of CO2 Emission Score. We want a Score where HIGHER is BETTER (Greener).
# Formula: 1 / (CO2_Emission_Score + epsilon) -> Normalized
scaler = MinMaxScaler()
# Invert: Small CO2 emission = High score
df['CO2_Impact_Index_Raw'] = 1 / (df['CO2_Emission_Score'] + 0.1) 
df['CO2_Impact_Index'] = scaler.fit_transform(df[['CO2_Impact_Index_Raw']]) * 100

# B. Cost Efficiency Index
# Since we don't have cost data, we'll use a proxy based on material properties
# Higher Recyclability and Biodegradability per unit weight = Better Efficiency
df['Cost_Efficiency_Raw'] = (df['Recyclability_Percent'] + df['Biodegradability_Score']) / (df['Weight_Capacity_kg'] + 0.01)
df['Cost_Efficiency_Index'] = scaler.fit_transform(df[['Cost_Efficiency_Raw']]) * 100

# C. Material Suitability Score (MSS) - The Final Ranking Metric
# Weights: 40% CO2 Impact, 30% Cost Efficiency, 30% Biodegradability
df['Material_Suitability_Score'] = (
    0.4 * df['CO2_Impact_Index'] + 
    0.3 * df['Cost_Efficiency_Index'] + 
    0.3 * df['Biodegradability_Score']
)

# 4. Validation & Statistics
print("\n--- Summary Statistics of New Features ---")
print(df[['CO2_Impact_Index', 'Cost_Efficiency_Index', 'Material_Suitability_Score']].describe())

# Ranking
print("\n--- Top 5 Recommended Materials ---")
top_materials = df.sort_values(by='Material_Suitability_Score', ascending=False).head(5)
print(top_materials[['Material_Type', 'Material_Suitability_Score', 'CO2_Emission_Score', 'Biodegradability_Score']])

# 5. Output
output_path = 'materials_processed_milestone1.csv'
df.to_csv(output_path, index=False)
print(f"\nProcessed data saved to {output_path}")
