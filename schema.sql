-- Database Schema for EcoPackAI (Updated for 5000-row dataset)

-- Check if table exists and drop it (for development iteration)
DROP TABLE IF EXISTS material_suitability;
DROP TABLE IF EXISTS materials;
DROP TABLE IF EXISTS products;

-- Table to store material properties
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(255) NOT NULL,
    tensile_strength_mpa FLOAT,
    weight_capacity_kg FLOAT,
    biodegradability_score FLOAT,
    co2_emission_score FLOAT,
    recyclability_percent FLOAT,
    moisture_barrier_grade INT,
    ai_recommendation VARCHAR(255),
    co2_impact_index FLOAT,
    cost_efficiency_index FLOAT,
    material_suitability_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store product categories (for future mapping)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_category VARCHAR(255) NOT NULL, 
    packaging_requirement VARCHAR(500),
    typical_weight_kg FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Junction table for material suitability per product (for future use)
CREATE TABLE material_suitability (
    material_id INT REFERENCES materials(id),
    product_id INT REFERENCES products(id),
    suitability_override FLOAT,
    reason TEXT,
    PRIMARY KEY (material_id, product_id)
);
