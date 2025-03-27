-- Create the predictions table if it doesn't exist
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    predicted_demand DECIMAL(10,2),
    refund_amount DECIMAL(10,2),
    actual_revenue DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO predictions (predicted_demand, refund_amount, actual_revenue) VALUES
    (1000.00, 50.00, 950.00),
    (1500.00, 75.00, 1425.00),
    (2000.00, 100.00, 1900.00),
    (2500.00, 125.00, 2375.00),
    (3000.00, 150.00, 2850.00),
    (3500.00, 175.00, 3325.00),
    (4000.00, 200.00, 3800.00),
    (4500.00, 225.00, 4275.00),
    (5000.00, 250.00, 4750.00),
    (5500.00, 275.00, 5225.00);

-- Create an index on the id column for better query performance
CREATE INDEX IF NOT EXISTS idx_predictions_id ON predictions(id);

-- Create a view for revenue analysis
CREATE OR REPLACE VIEW revenue_analysis AS
SELECT 
    id,
    predicted_demand,
    refund_amount,
    actual_revenue,
    (predicted_demand - actual_revenue) as revenue_difference,
    (refund_amount / predicted_demand * 100) as refund_percentage,
    created_at
FROM predictions;

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE ON predictions TO adminuser;
GRANT SELECT ON revenue_analysis TO adminuser; 