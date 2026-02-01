import pandas as pd
import psycopg2
from psycopg2 import extras
import os
from dotenv import load_dotenv

# Load database credentials from .env file
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "ecopack_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def load_data():
    # 1. Load the processed CSV
    csv_path = 'materials_processed_milestone1.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run process_data.py first.")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} records from {csv_path}")

    # 2. Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected to PostgreSQL successfully.")

        # 3. Initialize Schema
        print("Initializing database schema...")
        with open('schema.sql', 'r') as f:
            cur.execute(f.read())
        print("Schema initialized.")

        # 4. Ingest Data
        print("Ingesting data into 'materials' table...")
        
        # Prepare the data for insertion
        # Mapping CSV columns to DB columns
        data_to_insert = [
            (
                row['Material_Type'],
                row['Tensile_Strength_MPa'],
                row['Weight_Capacity_kg'],
                row['Biodegradability_Score'],
                row['CO2_Emission_Score'],
                row['Recyclability_Percent'],
                row['Moisture_Barrier_Grade'],
                row['AI_Recommendation'],
                row['CO2_Impact_Index'],
                row['Cost_Efficiency_Index'],
                row['Material_Suitability_Score']
            )
            for _, row in df.iterrows()
        ]

        insert_query = """
            INSERT INTO materials (
                material_type, tensile_strength_mpa, weight_capacity_kg, 
                biodegradability_score, co2_emission_score, recyclability_percent, 
                moisture_barrier_grade, ai_recommendation, co2_impact_index, 
                cost_efficiency_index, material_suitability_score
            ) VALUES %s
        """

        extras.execute_values(cur, insert_query, data_to_insert)
        
        print(f"Successfully ingested {len(data_to_insert)} records.")

        cur.close()
        conn.close()
        print("Database connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_data()
